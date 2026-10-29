"""Measure each logo asset's ink box and emit logos.json entries.

    python3 tools/measure_ink.py logos/*.png logos/*.svg > logos.json

Each argument is a file named <slug>.<ext>; the slug must match demos.py.
Output maps slug -> {url, aspect, centred, ...}. `url` defaults to the
relative path; edit it to wherever the asset is hosted.

Ink offsets, to test whether padding is symmetric.

Why it matters: if the ink is centred in its canvas, then a box cut to the ink's
aspect ratio with object-fit:cover renders the ink exactly filling the box -- no
wrapper element, no negative offsets, one CSS rule per logo. If the padding is
lopsided, cover would crop the ink and a wrapper would be required instead.
"""
import glob, json, os, re, sys
from PIL import Image

def ink_bbox(im):
    im = im.convert("RGBA"); w,h = im.size; px = im.load()
    minx,miny,maxx,maxy = w,h,-1,-1
    for y in range(h):
        for x in range(w):
            r,g,b,a = px[x,y]
            if a <= 24: continue
            if r>242 and g>240 and b>232: continue
            minx=min(minx,x); maxx=max(maxx,x); miny=min(miny,y); maxy=max(maxy,y)
    return None if maxx<0 else (minx,miny,maxx,maxy)

rows={}
print("%-14s %-11s %-11s %-7s %-22s %s" % ("slug","canvas","ink","aspect","padding L/R T/B","centred?"), file=sys.stderr)
print("-"*92, file=sys.stderr)
for path in (sys.argv[1:] or sorted(glob.glob("logos/*"))):
    slug=os.path.splitext(os.path.basename(path))[0]
    if path.endswith(".svg"):
        s=open(path,encoding="utf-8",errors="replace").read()
        m=re.search(r'viewBox\s*=\s*"([\d.\-\s]+)"', s)
        p=[float(v) for v in m.group(1).split()] if m else [0,0,1,1]
        nw,nh=p[2],p[3]
        rows[slug]=dict(url=path,nw=nw,nh=nh,x0=0,y0=0,iw=nw,ih=nh,aspect=round(nw/nh,3),svg=True)
        print("%-14s %-11s %-11s %-7s %-22s %s" % (slug,"%gx%g"%(nw,nh),"viewBox",
              round(nw/nh,2),"0/0 0/0","yes (vector, tight)"), file=sys.stderr)
        continue
    im=Image.open(path); nw,nh=im.size
    bb=ink_bbox(im)
    if not bb: continue
    x0,y0,x1,y1=bb; iw,ih=x1-x0+1,y1-y0+1
    padL,padR = x0, nw-1-x1
    padT,padB = y0, nh-1-y1
    cx = abs(padL-padR) <= max(2, 0.02*nw)
    cy = abs(padT-padB) <= max(2, 0.02*nh)
    rows[slug]=dict(url=path,nw=nw,nh=nh,x0=x0,y0=y0,iw=iw,ih=ih,aspect=round(iw/ih,3),svg=False,
                    centred=bool(cx and cy))
    print("%-14s %-11s %-11s %-7s %-22s %s" % (slug,"%dx%d"%(nw,nh),"%dx%d"%(iw,ih),
          round(iw/ih,2), "%d/%d %d/%d"%(padL,padR,padT,padB),
          ("yes" if (cx and cy) else "NO -> needs offset (x %s, y %s)"%(cx,cy))), file=sys.stderr)
print(json.dumps(rows, indent=1), file=sys.stdout)
print("\n(table above is on stderr; JSON on stdout)", file=sys.stderr)
