"""Lossless restoration of axis-aligned translated SpriteDicing quads."""
from PIL import Image
from UnityPy.helpers.MeshHelper import MeshHandler
from UnityPy.export.SpriteHelper import get_image

def restore(sprite):
    mesh=MeshHandler(sprite.m_RD,sprite.object_reader.version)
    mesh.process()
    if not mesh.m_Vertices or not mesh.m_UV0:
        raise ValueError("Missing Sprite mesh/UV metadata")
    w,h=round(sprite.m_Rect.width),round(sprite.m_Rect.height)
    if not (0<w<=32768 and 0<h<=32768 and w*h<=100_000_000):
        raise ValueError("Invalid or excessive Sprite canvas")
    texture=get_image(sprite,sprite.m_RD.texture,sprite.m_RD.alphaTexture).convert("RGBA")
    tw,th=texture.size
    ppu=sprite.m_PixelsToUnits
    positions=[(v[0]*ppu+w*sprite.m_Pivot.x,v[1]*ppu+h*sprite.m_Pivot.y) for v in mesh.m_Vertices]
    uvs=[(u*tw,v*th) for u,v in mesh.m_UV0]
    rounding=max(abs(c-round(c)) for xy in positions+uvs for c in xy)
    if rounding>0.002: raise ValueError("Non-integral pixels require a different rasterizer")
    pos=[tuple(round(c) for c in xy) for xy in positions]
    uv=[tuple(round(c) for c in xy) for xy in uvs]
    canvas=Image.new("RGBA",(w,h))
    boxes=[]
    for triangles in mesh.get_triangles():
        if len(triangles)%2: raise ValueError("Expected paired quad triangles")
        for k in range(0,len(triangles),2):
            ids=set(triangles[k])|set(triangles[k+1])
            if len(ids)!=4: raise ValueError("Non-quad Sprite mesh")
            a=[pos[i] for i in ids]; b=[uv[i] for i in ids]
            ax,ay=min(x for x,y in a),min(y for x,y in a)
            bx,by=max(x for x,y in a),max(y for x,y in a)
            sx,sy=min(x for x,y in b),min(y for x,y in b)
            ex,ey=max(x for x,y in b),max(y for x,y in b)
            if set(a)!={(ax,ay),(bx,ay),(ax,by),(bx,by)}:
                raise ValueError("Non-rectangular quad")
            if len({(pos[i][0]-uv[i][0],pos[i][1]-uv[i][1]) for i in ids})!=1:
                raise ValueError("Rotated/scaled tile is outside this adapter")
            if not (0<=ax<bx<=w and 0<=ay<by<=h and 0<=sx<ex<=tw and 0<=sy<ey<=th):
                raise ValueError("Tile exceeds texture/canvas bounds")
            # Keep source RGBA values verbatim; no repeated alpha blending at tile edges.
            canvas.paste(texture.crop((sx,sy,ex,ey)),(ax,ay))
            boxes.append(dict(source=[sx,sy,ex,ey],destination=[ax,ay,bx,by]))
    if not boxes: raise ValueError("Empty Sprite mesh")
    return canvas.transpose(Image.Transpose.FLIP_TOP_BOTTOM),dict(
        algorithm="sprite-dicing-translated-quads-v1",canvas=[w,h],atlas=[tw,th],
        vertices=len(pos),tiles=len(boxes),max_rounding_error=rounding,
        coordinate_system="bottom-left before final vertical flip",tile_map=boxes)
