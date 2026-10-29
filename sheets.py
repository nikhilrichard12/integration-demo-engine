"""Rebuild the review sheets. Run AFTER harness.py, which clears harness/."""
import sys, os, re; sys.path.insert(0,'.')
from demos import DEMOS
H='harness/'
def write(name, cells, css):
    open(H+name,'w').write('<!doctype html><meta charset="utf-8"><title>%s</title>\n<style>%s</style>\n%s'
        % (name, css, "\n".join(cells)))

WIDE = ("body{margin:0;padding:16px;background:#f4f2ec;font:13px ui-monospace,monospace}"
        "figure{margin:0 0 10px}figcaption{padding:3px 0;color:#555}"
        "iframe{border:1px solid #ccc;background:#fff;width:1080px;height:880px;"
        "transform:scale(.42);transform-origin:top left;margin-bottom:-510px}")
MOB  = ("body{margin:0;padding:12px;background:#e9e7e1;font:12px ui-monospace,monospace}"
        ".grid{display:flex;flex-wrap:wrap;gap:10px}figure{margin:0}"
        "figcaption{padding:2px 0;color:#555}"
        "iframe{border:1px solid #bbb;background:#fff;width:390px;height:820px}")

# settled (last beat, via reduced motion)
write('settled.html',
      ['<figure><figcaption>%s &middot; %s &middot; %d beat(s)</figcaption>'
       '<iframe src="/integrations/%s/?rm=1" data-slug="%s"></iframe></figure>'
       % (d['name'], d['panel'], len(d['beats']), d['slug'], d['slug']) for d in DEMOS],
      WIDE)

# mobile, both modes, 390px true viewport
# Echo was dropped 2026-08-20; keep this list resilient to the set changing.
picks = [s for s in ['linear','gmail','axiom','github','dropbox','webflow',
                     'plaud','ticktick','notion','todoist','monday-com','outlook']
         if any(d['slug'] == s for d in DEMOS)]
cells = []
for slug in picks:
    d = next(x for x in DEMOS if x['slug']==slug)
    for mode,label in (('','autoplay'),('?rm=1','reduced-motion')):
        cells.append('<figure><figcaption>%s / %s</figcaption>'
            '<iframe src="/integrations/%s/%s" data-slug="%s" data-mode="%s" '
            'width="390" height="820"></iframe></figure>'
            % (d['name'],label,slug,mode,slug,label))
write('mobile.html', ['<div class="grid">'] + cells + ['</div>'], MOB)
print('sheets: settled(%d) mobile(%d)' % (len(DEMOS), len(cells)))
