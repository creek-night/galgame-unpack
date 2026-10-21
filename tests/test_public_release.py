"""Publication smoke tests using generated data; no game assets or game execution."""
import hashlib
import io
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile
import unittest
from PIL import Image, PngImagePlugin

SCRIPTS=Path(__file__).resolve().parents[1]/'skills'/'galgame-unpack'/'scripts'

class PublicReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='gal-unpack-')
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.source=self.root/'source game'
        self.source.mkdir()
        (self.source/'sentinel.txt').write_text('read only',encoding='utf-8')
        self.env=os.environ.copy()
        self.env.pop('GALGAME_UNPACK_OUTPUT_ROOT',None)
        self.env.pop('GALGAME_HXV4_TOOL_MANIFEST',None)
        self.env.update(PYTHONIOENCODING='utf-8',PYTHONDONTWRITEBYTECODE='1')

    def run_script(self,script,*args,env=None,ok=True):
        cp=subprocess.run([sys.executable,'-X','utf8','-B',str(SCRIPTS/script),*map(str,args)],
                          capture_output=True,text=True,encoding='utf-8',env=env or self.env,cwd=self.root,timeout=30)
        if ok:self.assertEqual(cp.returncode,0,cp.stderr)
        else:self.assertNotEqual(cp.returncode,0)
        return cp

    def new_run(self,*extra,env=None,ok=True):
        return self.run_script('new_run.py','--game','测试 game','--source',self.source,'--compose','no','--scope','sample',*extra,env=env,ok=ok)

    def test_default_root_uses_user_home(self):
        home=self.root/'fake home';home.mkdir()
        env=dict(self.env,HOME=str(home),USERPROFILE=str(home))
        cp=self.new_run(env=env)
        manifest=json.loads((Path(cp.stdout.strip())/'manifest.json').read_text(encoding='utf-8'))
        self.assertEqual(Path(manifest['output_root']),home/'galgame-unpack-output')
        self.assertEqual(manifest['requested_categories'],['cg','sprites'])
        self.assertFalse(manifest['compose'])

    def test_environment_root(self):
        target=self.root/'env output'
        cp=self.new_run(env=dict(self.env,GALGAME_UNPACK_OUTPUT_ROOT=str(target)))
        self.assertTrue(Path(cp.stdout.strip()).is_relative_to(target))

    def test_explicit_root_overrides_environment(self):
        target=self.root/'explicit output';unused=self.root/'unused'
        cp=self.new_run('--root',target,env=dict(self.env,GALGAME_UNPACK_OUTPUT_ROOT=str(unused)))
        self.assertTrue(Path(cp.stdout.strip()).is_relative_to(target))
        self.assertFalse(unused.exists())

    def test_output_cannot_be_inside_game(self):
        self.new_run('--root',self.source/'output',ok=False)
        self.assertEqual([p.name for p in self.source.iterdir()],['sentinel.txt'])

    def test_runs_do_not_overwrite(self):
        out=self.root/'runs'
        first=Path(self.new_run('--root',out).stdout.strip())
        before=(first/'manifest.json').read_bytes()
        second=Path(self.new_run('--root',out).stdout.strip())
        self.assertNotEqual(first,second)
        self.assertEqual((first/'manifest.json').read_bytes(),before)

    def make_pf8(self,invalid=False):
        stream=io.BytesIO();info=PngImagePlugin.PngInfo();info.add_text('Comment','offset=1,2')
        Image.new('RGBA',(2,3),(20,40,60,128)).save(stream,format='PNG',pnginfo=info)
        payload=stream.getvalue();name=b'cg/sample.png'
        length=4+4+len(name)+12
        offset=7+length+(100000 if invalid else 0)
        index=struct.pack('<II',1,len(name))+name+struct.pack('<III',0,offset,len(payload))
        key=hashlib.sha1(index).digest()
        encrypted=bytes(b^key[i%20] for i,b in enumerate(payload))
        archive=self.source/'sample.pfs'
        archive.write_bytes(b'pf8'+struct.pack('<I',length)+index+encrypted)
        return archive,payload

    def test_pf8_preserves_exact_png_and_refuses_overwrite(self):
        archive,payload=self.make_pf8();before=archive.read_bytes()
        out=self.root/'out'/'sample.png'
        self.run_script('pfs_extract.py','extract',archive,'--entry','cg/sample.png','--image','--out',out)
        self.assertEqual(out.read_bytes(),payload)
        with Image.open(out) as im:self.assertEqual(im.info['Comment'],'offset=1,2')
        self.run_script('pfs_extract.py','extract',archive,'--entry','cg/sample.png','--out',out,ok=False)
        self.assertEqual(out.read_bytes(),payload)
        self.assertEqual(archive.read_bytes(),before)

    def test_pf8_rejects_out_of_bounds_payload(self):
        archive,_=self.make_pf8(invalid=True);out=self.root/'out'/'bad.png'
        self.run_script('pfs_extract.py','extract',archive,'--entry','cg/sample.png','--out',out,ok=False)
        self.assertFalse(out.exists())

    def test_alpha_over_preserves_opaque_canvas(self):
        layers=self.root/'layers';layers.mkdir()
        Image.new('RGBA',(3,3),(0,0,255,255)).save(layers/'base.png')
        Image.new('RGBA',(1,1),(255,0,0,128)).save(layers/'face.png')
        recipe=layers/'recipe.json'
        recipe.write_text(json.dumps({'evidence':'Generated arithmetic fixture','canvas':[3,3],'layers':[
            {'file':'base.png','position':[0,0]},{'file':'face.png','position':[1,1]}]}),encoding='utf-8')
        out=self.root/'composite.png'
        self.run_script('compose_layers.py',recipe,'--out',out)
        with Image.open(out) as im:
            self.assertEqual(im.getpixel((1,1)),(128,0,127,255))
            self.assertEqual(im.getpixel((0,0)),(0,0,255,255))
        before=out.read_bytes()
        self.run_script('compose_layers.py',recipe,'--out',out,ok=False)
        self.assertEqual(out.read_bytes(),before)

    def test_hxv4_missing_tool_has_actionable_error(self):
        cp=self.run_script('hxv4.py','index',ok=False)
        self.assertIn('GALGAME_HXV4_TOOL_MANIFEST',cp.stderr)
        self.assertIn('not bundled',cp.stderr)

    def test_hxv4_find_does_not_require_external_decoder(self):
        name='sample.png';digest=hashlib.blake2s((name+'xp3hnp').encode('utf-16le')).digest()
        index=self.root/'index.tsv'
        index.write_text('index\tname\tunpacked_size\tadler32\thx_info\n0\thashed\t4\t00000001\tfile_hash: '+str(list(digest))+'\n',encoding='utf-8')
        Path(str(index)+'.json').write_text(json.dumps({'kind':'index','status':'verified','entry_count':1,
            'sha256':hashlib.sha256(index.read_bytes()).hexdigest()}),encoding='utf-8')
        cp=self.run_script('hxv4.py','find','--index-file',index,'--name',name)
        self.assertEqual(json.loads(cp.stdout)['index'],0)

if __name__=='__main__':unittest.main()
