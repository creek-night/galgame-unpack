"""Read bounded plain PSB v3 metadata and extract one exact resource; no script execution."""
from pathlib import Path
import argparse,hashlib,json,struct,zlib
from adapter_io import output_path,save_json,save_bytes

class PSB:
    def __init__(self,path):
        self.path=Path(path).resolve(strict=True)
        if not 44<=self.path.stat().st_size<=64*1024*1024:raise ValueError("PSB size outside 44 bytes..64 MiB")
        self.data=self.path.read_bytes();self.visits=0
        if self.data[:8]!=b'PSB\0\x03\0\0\0':raise ValueError("Only plain PSB v3 is supported; identify shells/encryption separately")
        self.header=dict(zip(['header_length','names','strings','string_data','chunk_offsets','chunk_lengths','chunk_data','entries','checksum'],struct.unpack_from('<9I',self.data,8)))
        h=self.header
        if h['header_length']!=44 or h['names']!=44:raise ValueError("Unsupported PSB header layout")
        if h['checksum']!=zlib.adler32(self.data[8:40])&0xffffffff:raise ValueError("PSB header checksum mismatch")
        if any(not 0<=value<=len(self.data) for key,value in h.items() if key!='checksum'):raise ValueError("PSB offset outside file")
        charset,pos=self.array(h['names']);tree,pos=self.array(pos);indices,pos=self.array(pos)
        self.names=[]
        for index in indices:
            current=self.item(tree,index);letters=[];seen=set()
            while current:
                if current in seen or len(letters)>4096:raise ValueError("Cyclic or oversized PSB name")
                seen.add(current);parent=self.item(tree,current);value=current-self.item(charset,parent)
                if not 0<=value<=255:raise ValueError("Invalid PSB name trie")
                letters.append(value);current=parent
            self.names.append(bytes(reversed(letters)).decode('utf-8'))
        offsets,_=self.array(h['strings']);self.strings=[]
        for offset in offsets:
            pos=h['string_data']+offset;self.read(pos,1)
            end=self.data.find(b'\0',pos,min(len(self.data),pos+1024*1024))
            if end<0:raise ValueError("Unterminated/oversized PSB string")
            self.strings.append(self.data[pos:end].decode('utf-8'))
        self.offsets,_=self.array(h['chunk_offsets']);self.lengths,_=self.array(h['chunk_lengths'])
        if len(self.offsets)!=len(self.lengths):raise ValueError("PSB resource tables disagree")
        for offset,size in zip(self.offsets,self.lengths):self.read(h['chunk_data']+offset,size)
        self.root=self.node(h['entries'])
    @staticmethod
    def item(values,index):
        if not 0<=index<len(values):raise ValueError("PSB table index outside bounds")
        return values[index]
    def read(self,position,size):
        if not 0<=size or not 0<=position<=len(self.data)-size:raise ValueError("PSB read outside file")
        return self.data[position:position+size]
    def number(self,position,size):return int.from_bytes(self.read(position,size),'little')
    def array(self,position):
        width=self.number(position,1)-12
        if not 1<=width<=8:raise ValueError("Invalid PSB array count type")
        count=self.number(position+1,width);position+=width+1
        item_width=self.number(position,1)-12;position+=1
        if not 0<=item_width<=4 or count>1000000 or (count and not item_width):raise ValueError("Unsupported PSB array size")
        self.read(position,count*item_width)
        return [self.number(position+i*item_width,item_width) for i in range(count)],position+count*item_width
    def node(self,position,depth=0):
        self.visits+=1
        if depth>=100 or self.visits>1000000:raise ValueError("PSB object traversal limit")
        kind=self.number(position,1);position+=1
        if kind in [0,1]:return None
        if kind in [2,3]:return kind==3
        if kind==4:return 0
        if 5<=kind<=12:return int.from_bytes(self.read(position,kind-4),'little',signed=True)
        if 13<=kind<=20:return self.array(position-1)[0]
        if 21<=kind<=24:return self.item(self.strings,self.number(position,kind-20))
        if 25<=kind<=28:
            index=self.number(position,kind-24);self.item(self.offsets,index)
            return {'resource_index':index}
        if kind==29:return 0.0
        if kind in [30,31]:return struct.unpack('<f' if kind==30 else '<d',self.read(position,4 if kind==30 else 8))[0]
        if kind==32:
            offsets,base=self.array(position)
            return [self.node(base+offset,depth+1) for offset in offsets]
        if kind==33:
            keys,position=self.array(position);offsets,base=self.array(position)
            if len(keys)!=len(offsets):raise ValueError("PSB dictionary table mismatch")
            names=[self.item(self.names,key) for key in keys]
            if len(set(names))!=len(names):raise ValueError("Duplicate PSB dictionary name")
            return {name:self.node(base+offset,depth+1) for name,offset in zip(names,offsets)}
        raise ValueError('Unsupported PSB node '+str(kind))
    def resource(self,name):
        if not isinstance(self.root,dict) or name not in self.root:raise ValueError("Exact resource name not found")
        value=self.root[name]
        if not isinstance(value,dict) or set(value)!={'resource_index'}:raise ValueError("Selected entry is not a direct PSB resource")
        index=value['resource_index'];offset=self.header['chunk_data']+self.item(self.offsets,index)
        return self.read(offset,self.item(self.lengths,index)),index
    def metadata(self):
        return {'source':str(self.path),'sha256':hashlib.sha256(self.data).hexdigest(),'header':self.header,
                'names':self.names,'strings':self.strings,'root':self.root,'resource_count':len(self.offsets),
                'boundary':'Plain PSB v3 metadata/direct resources only; not arbitrary PSB image or animation rendering'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['index','extract']);p.add_argument('source')
    p.add_argument('--entry');p.add_argument('--out',required=True);a=p.parse_args()
    source=Path(a.source).resolve(strict=True);out=output_path(a.out,[source.parent]);psb=PSB(source)
    if a.mode=='index':result=psb.metadata();save_json(out,result)
    else:
        if not a.entry:p.error('extract requires an exact --entry')
        data,index=psb.resource(a.entry)
        result=save_bytes(out,data,{'source':str(source),'source_sha256':hashlib.sha256(psb.data).hexdigest(),'entry':a.entry,'resource_index':index,'decoder':'plain-psb-v3'})
    print(json.dumps({k:v for k,v in result.items() if k not in ['names','strings','root']},ensure_ascii=False))
if __name__=='__main__':main()
