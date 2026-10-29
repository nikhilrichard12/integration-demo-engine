"""Local harness: one page per slug, plus a contact-sheet page.

Mirrors the real spoke DOM just enough for the embed to mount (.int-hero >
.int-ctr > .int-demo-media) and puts the page at /integrations/<slug>/ so the
slug gate resolves exactly as it will in production.
"""
import json, os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from demos import DEMOS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "harness")
EMBED = open(os.path.join(HERE, "embed.html")).read()

SHELL = """<!doctype html><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<style>
 body{margin:0;background:#fffdf5;color:#1b1c15;
      font-family:"Sohne Buch",Arial,sans-serif}
 .section_hero.int-hero{overflow:hidden;padding:24px 0}
 .int-ctr{max-width:%(w)spx;margin:0 auto;padding:0 20px}
 .int-demo-media{display:none}
 .hnav{font:12px/1.4 ui-monospace,monospace;padding:8px 20px;color:#8a8b7e}
 .hnav a{color:#2D6CC0;margin-right:10px}
</style>
<script>
/* TEST-ONLY, harness shell, never shipped. ?rm=1 makes
   matchMedia('(prefers-reduced-motion: reduce)') report true BEFORE the embed
   script runs, which is the only way to exercise the reduced-motion path from
   a desktop browser -- and that path is the prime suspect for the iOS report
   (Low Power Mode and the Reduce Motion accessibility switch both set it). */
if (location.search.indexOf('rm=1') > -1) {
  var _mm = window.matchMedia.bind(window);
  window.matchMedia = function (qq) {
    if (/reduced-motion/.test(qq)) {
      return { matches: true, media: qq, addEventListener: function () {},
               removeEventListener: function () {}, addListener: function () {},
               removeListener: function () {} };
    }
    return _mm(qq);
  };
}
</script>
<div class="hnav">%(nav)s</div>
<section class="section_hero int-hero"><div class="int-ctr">
  <img class="int-demo-media w-dyn-bind-empty" alt="">
</div></section>
%(embed)s
"""

if os.path.isdir(OUT):
    shutil.rmtree(OUT)
nav = " ".join('<a href="/integrations/%s/">%s</a>' % (d["slug"], d["slug"])
               for d in DEMOS)

for d in DEMOS:
    p = os.path.join(OUT, "integrations", d["slug"])
    os.makedirs(p)
    open(os.path.join(p, "index.html"), "w").write(
        SHELL % dict(title=d["name"] + " demo", embed=EMBED, nav=nav, w=1080))
    # narrow variant for the mobile check, same slug path so the gate passes
    pm = os.path.join(OUT, "m", "integrations", d["slug"])
    os.makedirs(pm)
    open(os.path.join(pm, "index.html"), "w").write(
        SHELL % dict(title=d["name"] + " mobile", embed=EMBED, nav=nav, w=430))

# a generic page that must stay EMPTY -- the negative test
gp = os.path.join(OUT, "integrations", "happyscribe")
os.makedirs(gp)
open(os.path.join(gp, "index.html"), "w").write(
    SHELL % dict(title="generic page, must stay empty", embed=EMBED, nav=nav, w=1080))

print("harness: %d slugs + 1 generic negative test" % len(DEMOS))
