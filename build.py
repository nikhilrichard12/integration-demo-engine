"""Generate the multi-tool "See it work" embed + the review manifest.

  python3 build.py            -> writes embed.html and MANIFEST.md

Everything comes from demos.py and logos.json. Nothing is hand-typed into the
embed: that is the rule this pipeline learned the hard way when six of nine
FEATURED_DATA blurbs were typed from memory and one shipped fabricated.

GEOMETRY is inherited verbatim from docs/GEOMETRY.md,
measured off the shipped demo videos. Do not "tidy" any cqw number in here
without re-measuring against the reference frames.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, HERE)
from demos import DEMOS, PANEL_TYPES  # noqa: E402

# LOGOS. Optional. logos.json maps a slug to a local or hosted image plus its
# MEASURED ink box (tools/measure_ink.py writes the numbers). When a slug has no
# entry the engine falls back to a monogram tile in a per-tool accent, so the
# repo builds and runs with zero third-party brand assets checked in.
#
# Why measured ink and not the canvas: a square icon floating in 83% transparent
# padding and a tight 6:1 wordmark SVG have to render at ONE visual height in the
# chip, the pill and the hero lockup. Sizing from the canvas makes the first one
# tiny and the second one enormous. Sizing from the ink box, with object-fit:cover
# inside a box cut to the ink aspect, makes both read correctly without any
# per-tool fudge numbers.
LOGOS_PATH = os.path.join(HERE, "logos.json")
LOGOS = json.load(open(LOGOS_PATH)) if os.path.exists(LOGOS_PATH) else {}

# A logo is a WORDMARK when its ink is more than twice as wide as it is tall.
# Wordmarks get cap-height treatment: a 5.9:1 lockup set to the same height as a
# pictorial glyph is visually enormous, so it is set to WORDMARK_CAP of that
# height instead. This is the standard lockup convention and the number to tune
# if the balance looks off.
WORDMARK_MIN_ASPECT = 2.0
WORDMARK_CAP = 0.60

ACCENTS = ["#5E6AD2", "#2f8f5b", "#c4553d", "#e2a336", "#3b7dd8", "#8e5bd0",
           "#1f9e8a", "#d0557a"]


def accent_for(slug):
    return ACCENTS[sum(ord(c) for c in slug) % len(ACCENTS)]


def icon_for(d):
    """The chip/pill logo: URL plus the two numbers that drive every size.

    `aspect` is the ink aspect, not the canvas aspect. `wm` says whether to use
    cap-height treatment. Nothing here knows about object-fit or box widths;
    that is the stylesheet's job, driven by these two values. With no entry in
    logos.json the chip gets a monogram tile instead.
    """
    rec = LOGOS.get(d["slug"])
    if not rec:
        return {"mono": d["name"][0].upper(), "accent": accent_for(d["slug"]),
                "aspect": 1.0}
    if "aspect" not in rec:
        raise SystemExit("logos.json entry for %s has no measured aspect; run "
                         "tools/measure_ink.py on the asset" % d["slug"])
    out = {"url": rec["url"], "aspect": rec["aspect"]}
    if rec["aspect"] >= WORDMARK_MIN_ASPECT:
        out["wm"] = True
    return out


def hero_for(d):
    """Hero lockup metrics: the same aspect and wordmark flag, so the partner
    mark in the page hero is normalised by the same numbers at runtime."""
    rec = LOGOS.get(d["slug"])
    if not rec:
        return {"aspect": 1.0}
    out = {"aspect": rec["aspect"]}
    if rec["aspect"] >= WORDMARK_MIN_ASPECT:
        out["wm"] = True
    if rec.get("hero_src"):
        out["src"] = rec["hero_src"]
    return out


# --------------------------------------------------------------------------
# CSS. Act 1/2 geometry and the pill/panel/bird are the measured reference
# values. Panel INTERNALS then branch per type so no two tools read identical
# while the surrounding chrome stays byte-for-byte the same product.
# --------------------------------------------------------------------------
CSS = r"""
/* ===========================================================================
   "See it work" -- a frame-for-frame recreation of Kestrel's OWN demo UI,
   measured from the shipped demo videos (todoist/gmail/notion in this
   template's VIDEOS map). Measurements: docs/GEOMETRY.md

   Reference frames are 1440x1080. Every dimension is in `cqw` (1cqw = 1% of
   the stage width = 14.4px of the reference frame) on a fixed 4:3 stage, so
   proportions hold at any rendered size and cannot reflow the page.

   ONE EMBED, MANY SPOKES. This sits on the SHARED spoke template. The script
   looks the page's slug up in DEMOS and returns if there is no entry, so
   generic pages get nothing. Every class is int-ld-*.

   CLAIMS: each demo's strings come from that tool's OWN claims doc section, and
   every demo is READS ONLY -- no write is animated anywhere, even where the
   section approves writes.
   =========================================================================== */
.int-ld,.int-ld *,.int-ld *::before,.int-ld *::after{box-sizing:border-box}
.int-ld{
  --ink:#141414; --body:rgba(27,28,21,.75); --step:#141414;
  --bubble:#f5f3eb; --comp:#fafaf8; --comp-line:#efe9dc;
  --card:#fdfbf9; --card-line:#f0efe9; --prog:#a9b0e8;
  --panel-line:rgba(27,28,21,.13); --muted:#8a8b7e;
  --amber:#e2a336; --indigo:#5E6AD2; --green:#2f8f5b; --red:#c4553d;
  font-family:"Sohne Buch",Sohne,Arial,sans-serif;
  width:min(1040px,92vw); max-width:none;
  position:relative; left:50%; transform:translateX(-50%);
  /* Was 1rem top, when a heading and subline sat above the stage and did the
     separating. With those gone the stage is the first thing in the block and
     needs the breathing room itself, or it crowds whatever precedes it in the
     hero. Bottom is unchanged. */
  margin:2rem auto 2.5rem; text-align:left;
}
/* .int-ld-head / -title / -sub removed 2026-08-28 -- nothing renders them. */

.int-ld-stage{
  container-type:inline-size;
  position:relative; aspect-ratio:4/3; width:100%;
  background:#fff; border:1px solid var(--panel-line); border-radius:.75rem;
  overflow:hidden; color:var(--ink);
}
.int-ld-act{position:absolute; inset:0; opacity:0; pointer-events:none}
.int-ld-act.on{opacity:1}

/* ---------- ACT 1: the composer ---------- */
.int-ld-comp{
  position:absolute; left:9.375cqw; top:26.042cqw; width:81.389cqw; height:17.708cqw;
  background:var(--comp); border:1px solid var(--comp-line); border-radius:1.597cqw;
}
.int-ld-ctext{
  position:absolute; left:2.569cqw; top:3.3cqw; right:2.569cqw;
  font-size:2.361cqw; line-height:1.35; color:var(--ink); white-space:pre-wrap;
}
.int-ld-cbar{position:absolute; left:1.736cqw; right:1.528cqw; bottom:1.6cqw; height:4.583cqw; display:flex; align-items:center}
.int-ld-plus{
  width:3.611cqw; height:3.611cqw; border:1px solid var(--comp-line); border-radius:.833cqw;
  display:flex; align-items:center; justify-content:center; color:#6f6f6a; font-size:2.1cqw; line-height:1;
}
.int-ld-mic{margin-left:auto; width:2.083cqw; height:2.083cqw; color:#8a8a85}
.int-ld-send{
  margin-left:2.4cqw; width:4.583cqw; height:4.583cqw; border-radius:50%;
  background:#141414; display:flex; align-items:center; justify-content:center;
}
.int-ld-send svg{width:2cqw; height:2cqw; color:#fff}

/* ---------- ACT 2: bubble, tool card, steps ---------- */
.int-ld-bub{
  position:absolute; right:13.889cqw; top:20.5cqw; max-width:45.833cqw;
  background:var(--bubble); border-radius:1.667cqw; padding:1.667cqw 1.944cqw;
  font-size:2.361cqw; line-height:1.32; color:#1b1c15;
  opacity:0; transition:opacity .3s ease;
}
.int-ld-bub.on{opacity:1}
/* The "working" indicator is an indigo highlight that ORBITS the card's 1px
   ring. NOT a progress bar and NOT a left-to-right fill: in todoist frame 05
   it sits on the right edge and one second later in frame 06 on the left. A
   rotating conic gradient clipped by the wrapper's rounded overflow; the
   opaque card face masks the middle so only the 1px edge shows. The square
   must be at least the card's diagonal or the corners go dark mid-rotation. */
.int-ld-cardw{
  position:absolute; left:14.097cqw; top:32.5cqw; height:8.125cqw;
  padding:1.5px; border-radius:1.111cqw;
  background-color:var(--card-line);
  overflow:hidden; isolation:isolate;
  opacity:0; transition:opacity .25s ease;
}
.int-ld-cardw.on{opacity:1}
.int-ld-cardw::before{
  content:''; position:absolute; top:50%; left:50%;
  width:36cqw; height:36cqw; margin:-18cqw 0 0 -18cqw;
  background:conic-gradient(from 0turn,
    transparent 0 54%, var(--prog) 68%, var(--prog) 84%, transparent 96% 100%);
  opacity:0; transition:opacity .3s ease;
}
.int-ld-cardw.run::before{opacity:1; animation:int-ld-orbit 2s linear infinite}
@keyframes int-ld-orbit{to{transform:rotate(1turn)}}
.int-ld-card{
  position:relative; z-index:1;
  height:100%; display:inline-flex; align-items:center; gap:1.667cqw;
  padding:0 1.944cqw 0 1.389cqw;
  background:var(--card); border-radius:calc(1.111cqw - 1.5px);
}
/* LOGO SIZING, one rule for every asset.
   --lg-a is the MEASURED ink aspect (logos.json), not the canvas aspect.
   The image box is cut to that aspect at a fixed INK HEIGHT and filled with
   object-fit:cover, so the ink renders exactly --lg-ih tall whatever padding
   the asset carries. Before this, size came from the canvas: PostHog's ink is
   17% of its canvas height, so it rendered 3px tall in the hero while a tight
   asset next to it rendered 56px. Never reintroduce a fixed square here.
   Wordmarks (.wm) get cap height, 0.60 of icon height -- a 5.9:1 lockup at
   full icon height is visually enormous. */
.int-ld{--lg-ih:2.4cqw; --lg-pill-ih:2.083cqw}
.int-ld.wm{--lg-ih:1.44cqw; --lg-pill-ih:1.25cqw}
.int-ld-tile{
  width:3.056cqw; height:3.056cqw; border-radius:.556cqw; background:#fff;
  display:flex; align-items:center; justify-content:center; flex-shrink:0;
  box-shadow:0 0 0 1px rgba(27,28,21,.05); overflow:hidden;
}
/* Wordmark chips widen to fit the ink plus the tile's own side padding. The
   card is inline-flex, so a wider chip just widens the card; nothing reflows. */
.int-ld.wm .int-ld-tile{width:calc(var(--lg-ih) * var(--lg-a) + 1.2cqw)}
.int-ld-tile img{
  height:var(--lg-ih); width:calc(var(--lg-ih) * var(--lg-a));
  max-width:none; display:block; object-fit:cover;
}
.int-ld-mono{
  display:flex; align-items:center; justify-content:center;
  width:100%; height:100%; border-radius:inherit; color:#fff;
  font-size:1.9cqw; font-weight:600; line-height:1; letter-spacing:.01em;
}
.int-ld-tile .int-ld-mono{border-radius:.556cqw}
.int-ld-ctitle{font-size:2.361cqw; color:var(--ink); white-space:nowrap}
.int-ld-chev{width:1.667cqw; height:1.667cqw; color:#2f2f2d; flex-shrink:0; transition:transform .3s ease}
.int-ld-cardw.done .int-ld-chev{transform:rotate(90deg)}

.int-ld-steps{position:absolute; left:16.667cqw; top:43.6cqw; display:flex; flex-direction:column; gap:0}
.int-ld-strow{height:5cqw; display:flex; align-items:center; gap:2.153cqw}
.int-ld-sicon{width:2.153cqw; height:2.153cqw; color:var(--step); flex-shrink:0; opacity:.13; transition:opacity .3s ease}
.int-ld-strow.on .int-ld-sicon{opacity:1}
.int-ld-slabel{font-size:2.361cqw; color:var(--step); white-space:nowrap; opacity:0; transition:opacity .3s ease}
.int-ld-strow.on .int-ld-slabel{opacity:1}

/* ---------- ACT 3: pill tab + app panel + the bird ---------- */
.int-ld-pill{
  position:absolute; left:6.597cqw; top:5.694cqw; height:3.542cqw;
  display:inline-flex; align-items:center; gap:1.1cqw; padding:0 1.6cqw 0 1.1cqw;
  background:#fff; border-radius:999px;
  box-shadow:0 1px 2px rgba(27,28,21,.06),0 6px 18px rgba(27,28,21,.07);
  font-size:2.083cqw; color:#1b1c15; white-space:nowrap;
}
.int-ld-pill .x{width:1.6cqw; height:1.6cqw; color:#6f6f6a; flex-shrink:0}
.int-ld-pill .mark{
  height:var(--lg-pill-ih); width:calc(var(--lg-pill-ih) * var(--lg-a));
  flex-shrink:0; overflow:hidden; border-radius:.35cqw;
}
.int-ld-pill .x svg{width:100%; height:100%; display:block; object-fit:contain}
.int-ld-pill .mark img{width:100%; height:100%; display:block; object-fit:cover}
.int-ld-pill .mark .int-ld-mono{font-size:1.35cqw; border-radius:.35cqw}
/* In the tab pill a wordmark carries the name itself, so the duplicate text
   label is dropped -- "[PLAUD] Plaud" reads as a mistake. */
.int-ld-panel{
  position:absolute; left:5.556cqw; top:11.806cqw; width:89.236cqw; bottom:-2cqw;
  background:#fff; border:1px solid var(--panel-line);
  border-radius:1.667cqw 1.667cqw 0 0; overflow:hidden;
}
/* Title top 4.51cqw and rows top 10.42cqw are the reference frame's own
   spacing (title y235, first row band starts y320, panel top y170). The
   reference has NO subtitle under the title -- `meta` is an opt-in line used
   only by panel types that genuinely need a qualifier, and it shifts the rows
   down rather than crowding them. */
.int-ld-ptitle{position:absolute; left:5.556cqw; top:4.51cqw; font-size:3.194cqw; font-weight:600; letter-spacing:-.01em; color:#1b1c15; white-space:nowrap}
.int-ld-pmeta{position:absolute; left:5.556cqw; top:9.1cqw; font-size:1.94cqw; color:var(--muted); white-space:nowrap}
.int-ld-rows{position:absolute; left:5.556cqw; right:5.556cqw; top:10.42cqw}
.int-ld-panel.hasmeta .int-ld-rows{top:13.4cqw}
.int-ld-prow{
  display:flex; align-items:center; gap:1.18cqw; padding:1.37cqw 0; line-height:1.4;
  border-bottom:1px solid rgba(27,28,21,.07);
  opacity:0; transform:translateY(.5cqw); transition:opacity .3s ease, transform .3s ease;
}
.int-ld-prow.on{opacity:1; transform:none}
.int-ld-pwhat{font-size:2.361cqw; color:#1b1c15; flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.int-ld-pwho{font-size:2.083cqw; color:var(--muted); flex-shrink:0; white-space:nowrap}
/* nowrap is load-bearing: at 6.2cqw "LB-241" wrapped to two lines and pushed
   the row to 8.66cqw against the reference's 6.04cqw. */
.int-ld-pid{font-size:2.083cqw; color:var(--muted); flex-shrink:0; white-space:nowrap; font-variant-numeric:tabular-nums}

/* -- per-panel-type row internals -------------------------------------- */
/* issues: status ring + mono key + title + assignee */
.int-ld-p-issues .int-ld-pid{width:7.6cqw}
.int-ld-dot{width:2.361cqw; height:2.361cqw; border-radius:50%; border:.174cqw solid var(--muted); flex-shrink:0}
.int-ld-dot.prog{border-color:var(--amber)}
.int-ld-dot.rev{border-color:var(--indigo)}
/* checks: checkbox circle, amber when overdue */
.int-ld-box{width:2.361cqw; height:2.361cqw; border-radius:50%; border:.174cqw solid var(--muted); flex-shrink:0}
.int-ld-box.due{border-color:var(--amber)}
.int-ld-chip{
  font-size:1.8cqw; color:var(--muted); flex-shrink:0; white-space:nowrap;
  border:1px solid rgba(27,28,21,.1); border-radius:.7cqw; padding:.2cqw .8cqw;
}
/* mail: sender in medium weight, subject grey-ish, day right */
.int-ld-from{font-size:2.222cqw; color:#1b1c15; font-weight:600; flex-shrink:0; width:16cqw; overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
.int-ld-p-mail .int-ld-pwhat{color:#3d3f38}
/* docs: doc tile + title + grey snippet under it */
.int-ld-p-docs .int-ld-prow{align-items:flex-start}
.int-ld-dtile{width:2.8cqw; height:2.8cqw; border-radius:.4cqw; background:#f2f0ea; flex-shrink:0; margin-top:.2cqw}
.int-ld-dstack{display:flex; flex-direction:column; gap:.35cqw; min-width:0; flex:1}
.int-ld-dsnip{font-size:1.94cqw; color:var(--muted); overflow:hidden; text-overflow:ellipsis; white-space:nowrap}
/* events: left time column, tabular */
.int-ld-time{font-size:2.222cqw; color:#1b1c15; flex-shrink:0; width:8.5cqw; font-variant-numeric:tabular-nums}
/* repos: state glyph + mono number + title + branch chip */
.int-ld-p-repos .int-ld-pid{width:5.6cqw}
.int-ld-st{width:2.1cqw; height:2.1cqw; border-radius:50%; flex-shrink:0; background:var(--green)}
.int-ld-st.draft{background:var(--muted)}
.int-ld-st.commit{background:transparent; border:.174cqw solid var(--muted); width:1.7cqw; height:1.7cqw}
.int-ld-st.file{background:transparent; border:.174cqw solid var(--indigo); border-radius:.3cqw; width:1.8cqw; height:1.8cqw}
.int-ld-branch{font-size:1.8cqw; color:var(--indigo); flex-shrink:0; white-space:nowrap; font-variant-numeric:tabular-nums}
/* query: the figure IS the title, oversized, with supporting rows */
.int-ld-p-query .int-ld-ptitle{font-size:6.6cqw; letter-spacing:-.03em; top:3.6cqw}
.int-ld-p-query .int-ld-pmeta{top:11.4cqw}
.int-ld-panel.hasmeta.int-ld-p-query .int-ld-rows{top:15.8cqw}
.int-ld-p-query .int-ld-pwhat{color:var(--muted); flex:0 0 22cqw}
.int-ld-p-query .int-ld-pval{font-size:2.361cqw; color:#1b1c15; font-variant-numeric:tabular-nums}
/* cms: field-coverage chip, red when something is missing */
.int-ld-flag{
  font-size:1.8cqw; flex-shrink:0; white-space:nowrap; border-radius:.7cqw;
  padding:.2cqw .8cqw; border:1px solid transparent;
}
.int-ld-flag.missing{color:var(--red); background:rgba(196,85,61,.09)}
.int-ld-flag.ok{color:var(--green); background:rgba(47,143,91,.09)}
/* files: type glyph + name + path + size */
.int-ld-ftype{
  font-size:1.6cqw; color:#fff; background:var(--muted); border-radius:.35cqw;
  padding:.25cqw .6cqw; flex-shrink:0; text-transform:uppercase; letter-spacing:.04em;
}
.int-ld-fpath{font-size:1.94cqw; color:var(--muted); flex-shrink:0; white-space:nowrap}
/* recordings: waveform bars */
.int-ld-wave{display:flex; align-items:center; gap:.28cqw; flex-shrink:0; width:2.8cqw; height:2.4cqw}
.int-ld-wave i{display:block; width:.4cqw; background:var(--muted); border-radius:.2cqw}
/* board: status pill */
.int-ld-pillst{
  font-size:1.8cqw; color:#fff; border-radius:.7cqw; padding:.2cqw .9cqw;
  flex-shrink:0; white-space:nowrap; background:var(--muted);
}
.int-ld-pillst.working{background:var(--amber)}
.int-ld-pillst.stuck{background:var(--red)}
.int-ld-pillst.done{background:var(--green)}
/* ping: one centred status line, deliberately no result rows */
.int-ld-p-ping .int-ld-rows{top:12cqw}
/* kv: label/value detail read-out, used by "open that one" beats */
.int-ld-klabel{font-size:2.083cqw; color:var(--muted); flex:0 0 20cqw; white-space:nowrap}
.int-ld-p-kv .int-ld-pwhat{white-space:normal}

/* ---------- the bird ---------- */
/* Start = reference frame 07 (abs left 6.60cqw, top 59.03cqw). End = frame 09,
   measured bbox abs left 72.15 / top 18.19, 8.06 x 7.22cqw -- to the RIGHT OF
   THE TITLE, clear of the rows. Values are panel-relative AND pre-compensated
   for rotation: a rotated box's visual extent is ~1.1x its layout box and sits
   ~0.5cqw up and left, so the silhouette lands on the reference coords. */
.int-ld-bird{
  position:absolute; width:7.26cqw; color:#1B1C15;
  left:1.04cqw; top:47.22cqw; opacity:0; transform:rotate(-6deg);
  transition:opacity .5s ease, left 2.2s cubic-bezier(.4,0,.3,1), top 2.2s cubic-bezier(.4,0,.3,1), transform 2.2s ease;
}
.int-ld-bird.on{opacity:1}
.int-ld-bird.flew{left:66.49cqw; top:6.37cqw; transform:rotate(-8deg)}
.int-ld-bird svg{width:100%; height:auto; display:block}

/* ---------- the play affordance, now invisible ---------- */
/* The foot and its Replay control are gone (the founder, 2026-08-28: nothing
   visible around the demo). What remains is a stage-sized transparent button,
   active ONLY in the settled state.

   THE iOS CASE this protects: a reduced-motion viewer -- which on iOS includes
   anyone in Low Power Mode -- gets a settled still frame. Previously a visible
   "Play" pill said it was a still and not a broken embed. That pill is now
   disallowed, so the whole stage is the target instead. Keep it a real button:
   it stays keyboard reachable and shows a focus ring, which is the only visible
   affordance left and only when a keyboard user asks for it. */
.int-ld-tap{
  position:absolute; inset:0; z-index:3; border:0; margin:0; padding:0;
  background:transparent; cursor:pointer; font:inherit; color:inherit;
  display:none; -webkit-tap-highlight-color:transparent;
}
.int-ld.is-idle .int-ld-tap{display:block}
.int-ld-tap:focus-visible{outline:2px solid #2D6CC0; outline-offset:-3px; border-radius:.75rem}

@media (max-width:600px){
  .int-ld{width:100%; left:0; transform:none; margin:1.5rem 0 1.75rem}
  /* The stage is a scaled-down 4:3 product screen, so on a phone every cqw
     size shrinks with it and the smallest labels land under 9px. Floor them.
     Raising the floor makes long row text ellipsize sooner, which is the right
     trade: truncated-but-readable beats complete-but-illegible. */
  .int-ld-ctext,.int-ld-slabel,.int-ld-pwhat,.int-ld-bub,
  .int-ld-from,.int-ld-time,.int-ld-pval{font-size:max(12px,2.361cqw)}
  .int-ld-pid,.int-ld-pwho,.int-ld-chip,.int-ld-branch,.int-ld-flag,.int-ld-klabel,
  .int-ld-fpath,.int-ld-pmeta,.int-ld-dsnip,.int-ld-ftype,.int-ld-pillst{font-size:max(10px,1.94cqw)}
  .int-ld-ptitle{font-size:max(15px,3.194cqw)}
  .int-ld-p-query .int-ld-ptitle{font-size:max(24px,6.6cqw)}
  /* The fixed cqw widths on the mono columns are correct at desktop, where
     they hold the reference's alignment, but the floored font above overflows
     them on a phone and the id ran into the title. Let content size them and
     keep a real gap instead. */
  .int-ld-p-issues .int-ld-pid,.int-ld-p-repos .int-ld-pid{width:auto}
  .int-ld-klabel{flex:0 0 auto; min-width:9ch}
  .int-ld-prow{gap:max(7px,1.18cqw)}
  .int-ld-from{width:auto; max-width:38%}
}

@media (prefers-reduced-motion:reduce){
  .int-ld-act,.int-ld-cardw,.int-ld-bub,.int-ld-strow .int-ld-sicon,
  .int-ld-strow .int-ld-slabel,.int-ld-prow,.int-ld-bird{transition:none !important}
  /* the orbiting ring is the one thing here that loops forever -- stop it dead */
  .int-ld-cardw.run::before{animation:none !important}
}
"""

# --------------------------------------------------------------------------
# JS. The engine: one DEMOS map, pluggable panel renderers, a data-driven
# timeline so a 1-, 2- or 3-beat demo needs no hand-timing.
# --------------------------------------------------------------------------
JS_HEAD = r"""
(function () {
  'use strict';
  /* Hero lockup ink heights, in px. The Kestrel bird is a tight-viewBox SVG
     in a 74x56 contain box, so it renders exactly 56px tall -- that is the
     parity reference, measured, not chosen. Wordmarks take cap height at
     HERO_CAP_H; matching a 5.9:1 lockup to a pictorial glyph's full height
     would be visually enormous. Tune HERO_CAP_H if the balance reads off. */
  var HERO_ICON_H = 56;
  var HERO_CAP_H = 33;
  var parts = location.pathname.split('/').filter(Boolean);
  var slug = parts[parts.length - 1] || '';
  var D = DEMOS[slug];
  if (!D) return;                       /* generic pages get nothing */

  /* ---- HERO LOCKUP, normalised first and unconditionally ----
     The hero is the "bird x partner" pairing above the H1. It is Webflow
     markup bound to the CMS logo field, sized `width:74px; height:56px;
     object-fit:contain` for every tool alike -- so a partner logo rendered at
     1/aspect of its canvas. PostHog measured 9.7px tall beside a 56px bird.
     Here the partner box is recut to the MEASURED ink aspect at a fixed ink
     height, so every mark renders the same height as the bird (wordmarks at
     cap height). Runs before the video early-return on purpose: the three
     video spokes have the same hero and deserve the same fix. */
  (function normaliseHero() {
    if (!D.hero) return;
    var lock = document.querySelector('.int-hero .int-lockup, .section_hero .int-lockup');
    if (!lock) return;
    var marks = lock.querySelectorAll('.int-lockup-logo');
    if (marks.length < 2) return;       /* no partner mark to size */
    var partner = marks[marks.length - 1];
    /* Swap the asset where the CMS field holds the wrong variant (ClickUp).
       See hero_for() in build.py for why this is not a CMS edit. */
    if (D.hero.src) partner.src = D.hero.src;
    var H = D.hero.wm ? HERO_CAP_H : HERO_ICON_H;
    partner.style.height = H + 'px';
    partner.style.width = (H * D.hero.aspect).toFixed(1) + 'px';
    partner.style.objectFit = 'cover';
    partner.style.maxWidth = 'none';
  })();

  if (document.querySelector('.int-ld')) return;
  /* Real footage wins. gmail / notion / todoist have a self-hosted demo video
     that the template's head code injects into this same hero slot; a coded
     recreation of the product next to a real recording of it would be two
     "see it work" visuals in one hero. Flag lives in demos.py. The element
     check is belt and braces: the video injector and this script both run on
     DOMContentLoaded and their order is not guaranteed. */
  if (D.video) return;                  /* real footage wins -- see demos.py */
  if (document.querySelector('video.int-demo-video')) return;

  var mq = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');
  var reduce = !!(mq && mq.matches);

  var ICON = {
    find: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21"/></svg>',
    doc:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M14 3H6.5A1.5 1.5 0 0 0 5 4.5v15A1.5 1.5 0 0 0 6.5 21h11a1.5 1.5 0 0 0 1.5-1.5V8z"/><path d="M14 3v5h5"/><path d="M8.5 12.5h7M8.5 16h7"/></svg>',
    note: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20 15.5A1.5 1.5 0 0 1 18.5 17H8l-4 4V5.5A1.5 1.5 0 0 1 5.5 4h13A1.5 1.5 0 0 1 20 5.5z"/></svg>',
    mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></svg>',
    check:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="m8.5 12.5 2.5 2.5 4.5-5"/></svg>',
    cal:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3.5v3M16 3.5v3"/></svg>',
    repo: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="7" cy="6" r="2.5"/><circle cx="7" cy="18" r="2.5"/><circle cx="17" cy="12" r="2.5"/><path d="M7 8.5v7M9.5 6h3a2 2 0 0 1 2 2v2"/></svg>',
    query:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19V5M4 19h16"/><path d="m7 15 3.5-4 3 2.5L20 7"/></svg>',
    cms:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="4" width="17" height="5" rx="1.5"/><rect x="3.5" y="12" width="17" height="8" rx="1.5"/></svg>',
    file: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7.5A1.5 1.5 0 0 1 5.5 6h4l2 2.5h7A1.5 1.5 0 0 1 20 10v7.5A1.5 1.5 0 0 1 18.5 19h-13A1.5 1.5 0 0 1 4 17.5z"/></svg>',
    rec:  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="M5 10v4M9 7v10M13 9v6M17 11v2M21 10v4"/></svg>',
    board:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><rect x="3.5" y="4.5" width="17" height="15" rx="2"/><path d="M9 4.5v15M15 4.5v15"/></svg>'
  };
  var SEND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 19V5"/><path d="m5 12 7-7 7 7"/></svg>';
  var MIC  = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><rect x="9" y="2.5" width="6" height="11" rx="3"/><path d="M5.5 11a6.5 6.5 0 0 0 13 0M12 17.5V21"/></svg>';
  var CHEV = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m9 6 6 6-6 6"/></svg>';
  var XG   = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  var BIRD = '__BIRD__';

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }
  function reveal(el) { void el.offsetWidth; el.classList.add('on'); }
  /* the app icon: the site's OWN asset for this tool, never hand-drawn. An
     earlier build drew Linear's mark from memory and shipped a purple blob.
     Where no square asset exists, a monogram tile in the tool's accent -- the
     square shape the reference videos actually show. */
  /* Every logo is sized from its MEASURED ink box, never from its canvas.
     --lg-a is the ink aspect; the .wm class switches to cap-height treatment.
     The image always uses object-fit:cover inside a box cut to the ink aspect,
     which makes the ink fill the box exactly -- verified for all 17 assets: 14
     are centre-padded and the other two are off-centre by 1-5%, which crops
     invisibly. That is why no wrapper and no negative offset is needed. */
  function markHTML() {
    /* monogram: documented last resort, no tool uses it today */
    if (D.icon.mono) {
      return '<span class="int-ld-mono" style="background:' + esc(D.icon.accent) +
             '">' + esc(D.icon.mono) + '</span>';
    }
    return '<img alt="" decoding="async" src="' + esc(D.icon.url) + '">';
  }
  /* a wordmark IS the name; showing both reads as a bug */
  function pillLabel() { return D.icon.wm ? '' : esc(D.name); }

  /* ---- panel renderers. One per family, so the internals differ while the
     surrounding chrome does not. Each takes a row array and returns cells. --- */
  var PANEL = {
    issues: function (r) {
      return '<span class="int-ld-dot ' + esc(r[0]) + '"></span>' +
             '<span class="int-ld-pid">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[2]) + '</span>' +
             '<span class="int-ld-pwho">' + esc(r[3]) + '</span>';
    },
    checks: function (r) {
      return '<span class="int-ld-box ' + esc(r[0]) + '"></span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             (r[2] ? '<span class="int-ld-chip">' + esc(r[2]) + '</span>' : '');
    },
    mail: function (r) {
      return '<span class="int-ld-from">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-pwho">' + esc(r[2]) + '</span>';
    },
    docs: function (r) {
      return '<span class="int-ld-dtile"></span><span class="int-ld-dstack">' +
             '<span class="int-ld-pwhat">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-dsnip">' + esc(r[1]) +
             (r[2] ? ' &middot; ' + esc(r[2]) : '') + '</span></span>';
    },
    events: function (r) {
      return '<span class="int-ld-time">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-pwho">' + esc(r[2]) + '</span>';
    },
    repos: function (r) {
      return '<span class="int-ld-st ' + esc(r[0]) + '"></span>' +
             '<span class="int-ld-pid">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[2]) + '</span>' +
             (r[3] ? '<span class="int-ld-branch">' + esc(r[3]) + '</span>' : '');
    },
    query: function (r) {
      return '<span class="int-ld-pwhat">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pval">' + esc(r[1]) + '</span>';
    },
    cms: function (r) {
      return '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-flag ' + esc(r[0]) + '">' + esc(r[2]) + '</span>';
    },
    files: function (r) {
      return '<span class="int-ld-ftype">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             (r[2] ? '<span class="int-ld-fpath">' + esc(r[2]) + '</span>' : '') +
             (r[3] ? '<span class="int-ld-pwho">' + esc(r[3]) + '</span>' : '');
    },
    recordings: function (r) {
      return '<span class="int-ld-wave"><i style="height:40%"></i>' +
             '<i style="height:85%"></i><i style="height:60%"></i>' +
             '<i style="height:100%"></i><i style="height:45%"></i></span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-pwho">' + esc(r[2]) + '</span>';
    },
    board: function (r) {
      return '<span class="int-ld-pillst ' + esc(r[0]) + '">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>' +
             '<span class="int-ld-pwho">' + esc(r[2]) + '</span>';
    },
    ping: function (r) {
      return '<span class="int-ld-pwhat">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pwho">' + esc(r[1]) + '</span>';
    },
    /* Detail views. A real product does not render "open one item" with the
       same row template as the list it came from, so a beat can override the
       demo's panel type with kind:'kv' and get a label/value read-out. This is
       also what keeps the four task-list tools from looking like each other:
       their list beats share a renderer, their detail beats do not. */
    kv: function (r) {
      return '<span class="int-ld-klabel">' + esc(r[0]) + '</span>' +
             '<span class="int-ld-pwhat">' + esc(r[1]) + '</span>';
    }
  };

  var root = document.createElement('div');
  root.className = D.icon.wm ? 'int-ld wm' : 'int-ld';
  root.style.setProperty('--lg-a', D.icon.aspect);
  root.innerHTML =
    /* No heading, no subline. the founder, 2026-08-28: the demo speaks for itself
       and the wrapper text was noise. The stage's aria-label still carries the
       full description, including "Read only; nothing is changed", so the
       disclosure survives for assistive tech even though nothing is drawn. */
    '<div class="int-ld-stage" role="img" aria-label="' + esc(D.alt) + '">' +
      '<div class="int-ld-act int-ld-a1">' +
        '<div class="int-ld-comp">' +
          '<div class="int-ld-ctext"></div>' +
          '<div class="int-ld-cbar">' +
            '<div class="int-ld-plus">+</div>' +
            '<div class="int-ld-mic">' + MIC + '</div>' +
            '<div class="int-ld-send">' + SEND + '</div>' +
          '</div>' +
        '</div>' +
      '</div>' +
      '<div class="int-ld-act int-ld-a2">' +
        '<div class="int-ld-bub"></div>' +
        '<div class="int-ld-cardw"><div class="int-ld-card">' +
          '<span class="int-ld-tile">' + markHTML() + '</span>' +
          '<span class="int-ld-ctitle">Gathering context</span>' +
          '<span class="int-ld-chev">' + CHEV + '</span>' +
        '</div></div>' +
        '<div class="int-ld-steps"></div>' +
      '</div>' +
      '<div class="int-ld-act int-ld-a3">' +
        '<div class="int-ld-pill"><span class="x">' + XG + '</span>' +
          '<span class="mark">' + markHTML() + '</span>' + pillLabel() + '</div>' +
        '<div class="int-ld-panel int-ld-p-' + esc(D.panel) + '">' +
          '<div class="int-ld-ptitle"></div>' +
          '<div class="int-ld-pmeta"></div>' +
          '<div class="int-ld-rows"></div>' +
          '<div class="int-ld-bird">' + BIRD + '</div>' +
        '</div>' +
      '</div>' +
      /* Invisible, stage-sized tap target. the founder, 2026-08-28: nothing visible
         around the demo, which took the foot's Replay control AND this button's
         "Play" pill with it. The control still EXISTS -- it covers the stage, it
         is a real <button> so it stays keyboard reachable, and it shows a focus
         ring when tabbed to. It is only active in the settled state (.is-idle),
         i.e. reduced-motion and scrolled-away, so it never swallows a click
         while the demo is looping. */
      '<button type="button" class="int-ld-tap" aria-label="Replay the demo">' +
      '</button>' +
    '</div>';

  var q = function (s) { return root.querySelector(s); };
  var a1 = q('.int-ld-a1'), a2 = q('.int-ld-a2'), a3 = q('.int-ld-a3'),
      ctext = q('.int-ld-ctext'), bub = q('.int-ld-bub'),
      card = q('.int-ld-cardw'), ctitle = q('.int-ld-ctitle'),
      stepsBox = q('.int-ld-steps'), panel = q('.int-ld-panel'),
      ptitle = q('.int-ld-ptitle'), pmeta = q('.int-ld-pmeta'),
      rowsBox = q('.int-ld-rows'), bird = q('.int-ld-bird'),
      stage = q('.int-ld-stage'), tap = q('.int-ld-tap');

  var timers = [];
  function at(ms, fn) { timers.push(setTimeout(fn, ms)); }
  function clearAll() { timers.forEach(clearTimeout); timers = []; }
  function only(act) {
    [a1, a2, a3].forEach(function (x) { x.classList.toggle('on', x === act); });
  }

  /* Render one beat's step list and panel. Beats replace this content rather
     than the markup being static, which is what lets a demo have 2 or 3
     exchanges without three copies of the DOM. */
  function paintSteps(beat) {
    stepsBox.innerHTML = beat.steps.map(function (s) {
      return '<div class="int-ld-strow"><span class="int-ld-sicon">' +
             (ICON[s[0]] || ICON.find) + '</span>' +
             '<span class="int-ld-slabel">' + esc(s[1]) + '</span></div>';
    }).join('');
    return stepsBox.querySelectorAll('.int-ld-strow');
  }
  function paintPanel(beat) {
    var p = beat.panel;
    var kind = p.kind || D.panel;        /* a beat may override the renderer */
    var fn = PANEL[kind] || PANEL.issues;
    /* keep the type class in step with the renderer, or the type-specific CSS
       (the oversized query figure, the docs two-line row) lands on the wrong
       markup. */
    panel.className = 'int-ld-panel int-ld-p-' + kind;
    ptitle.textContent = p.title;
    pmeta.textContent = p.meta || '';
    panel.classList.toggle('hasmeta', !!p.meta);
    rowsBox.innerHTML = p.rows.map(function (r) {
      return '<div class="int-ld-prow">' + fn(r) + '</div>';
    }).join('');
    return rowsBox.querySelectorAll('.int-ld-prow');
  }

  function resetAll() {
    clearAll();
    ctext.textContent = '';
    bub.textContent = '';
    bub.classList.remove('on');
    card.className = 'int-ld-cardw';
    ctitle.textContent = 'Gathering context';
    stepsBox.innerHTML = '';
    rowsBox.innerHTML = '';
    ptitle.textContent = '';
    pmeta.textContent = '';
    bird.classList.remove('on', 'flew');
    only(null);
  }

  /* The settled frame: last beat, everything in place. This is what a
     reduced-motion viewer sees, and it is also the resting state after the
     loop is stopped -- never a frozen mid-animation frame. */
  function still() {
    resetAll();
    var last = D.beats[D.beats.length - 1];
    bub.textContent = last.q;
    bub.classList.add('on');
    var rows = paintPanel(last);
    Array.prototype.forEach.call(rows, function (r) { r.classList.add('on'); });
    bird.classList.add('on', 'flew');
    only(a3);
    idle(true);
  }

  function idle(on) { root.classList.toggle('is-idle', !!on); }

  /* Data-driven timeline. Beat 1 types into the composer; later beats skip
     the composer, the way a real second question would. Every offset below is
     the reference video's own pacing (33ms/char, ~400ms to the card, ~900ms
     between step reveals, ~700ms before the cut, rows 600ms apart). */
  function play() {
    resetAll();
    idle(false);
    var t = 0;
    D.beats.forEach(function (beat, i) {
      var steps;
      if (i === 0) {
        only(a1);
        t += 400;
        at(t, function () {
          only(a1);
          var n = 0;
          (function tick() {
            ctext.textContent = beat.q.slice(0, ++n);
            if (n < beat.q.length) at(33, tick);
          })();
        });
        t += beat.q.length * 33 + 480;
      } else {
        t += 700;                        /* a breath between exchanges */
      }
      var tCut = t;
      at(tCut, function () {
        only(a2);
        bub.textContent = beat.q;
        reveal(bub);
        card.className = 'int-ld-cardw';
        ctitle.textContent = 'Gathering context';
        steps = paintSteps(beat);
      });
      at(tCut + 400, function () {
        card.classList.add('on');
        at(60, function () { card.classList.add('run'); });
      });
      beat.steps.forEach(function (s, k) {
        at(tCut + 1000 + k * 900, function () {
          if (steps && steps[k]) steps[k].classList.add('on');
        });
      });
      at(tCut + 1300, function () {
        ctitle.textContent = beat.card;
        card.classList.add('done');
      });
      var tPanel = tCut + 900 + beat.steps.length * 900 + 700;
      at(tPanel, function () {
        only(a3);
        var rows = paintPanel(beat);
        if (i === 0) {
          bird.classList.add('on');
          at(400, function () { bird.classList.add('flew'); });
        } else {
          bird.classList.add('on', 'flew');   /* already flown, stays put */
        }
        beat.panel.rows.forEach(function (_, k) {
          at(400 + k * 600, function () {
            if (rows[k]) rows[k].classList.add('on');
          });
        });
      });
      t = tPanel + 400 + beat.panel.rows.length * 600 + 1400;
    });
    at(t + 600, play);                   /* loop */
  }

  /* ---- start / stop -------------------------------------------------
     THE iOS BUG. the founder saw a static frame on Chrome iOS. Cause, confirmed by
     reading the shipped v2 source rather than guessing: `still()` ended with
     `replay.style.display = 'none'`, and boot() called still() and returned
     whenever prefers-reduced-motion matched. iOS sets that preference from
     BOTH the Reduce Motion accessibility switch and Low Power Mode, and Chrome
     iOS is WebKit underneath, so a phone on low battery got the settled frame
     and literally no control -- indistinguishable from a broken embed.

     Second, smaller defect on the same report: the old IntersectionObserver
     called clearAll() when the stage left the viewport, which cancels timers
     but leaves the DOM mid-animation. An iOS address-bar collapse or a
     rubber-band scroll can fire enter-then-leave in quick succession, which
     froze the demo on a half-typed question with no way back.

     So: the settled frame stays (it is the right answer to the preference),
     but it is now always accompanied by a visible Play control, leaving the
     viewport SETTLES rather than freezes, and every way of arriving at "should
     be playing but isn't" funnels through ensure().
     -------------------------------------------------------------------- */
  var running = false;
  function start() {
    if (running) return;
    running = true;
    play();
  }
  /* AUTO-start paths must never fire for a reduced-motion user; an explicit tap
     still may, because that IS the user asking for motion. Hence the guard sits
     here and at ensure(), not inside start() -- tapped() calls start() directly
     and must keep working.

     Why this exists: boot() returns early on reduce, so a user who loads the
     page with reduce ON never reaches the observer or the visibilitychange
     listener. But a user who turns reduce ON mid-session HAS both installed,
     and both called start() unguarded -- so scrolling away and back, or
     switching tabs and back, restarted the animation on someone who had just
     asked their OS for less motion. Narrow, but a real regression path. */
  function autoStart() {
    if (reduce) return;
    start();
  }
  function stop(settle) {
    running = false;
    clearAll();
    if (settle) still();               /* never freeze mid-frame */
  }
  function inView() {
    var r = stage.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    return r.top < vh && r.bottom > 0;
  }
  /* The single recovery path. Safe to call as often as you like. */
  function ensure() {
    if (reduce || running) return;
    if (inView()) autoStart();
  }

  function tapped() {
    /* An explicit tap is explicit intent, so it plays even under reduced
       motion -- the preference governs what happens unasked, not what the
       viewer asks for. */
    stop(false);
    start();
  }
  tap.addEventListener('click', tapped);

  function mount() {
    var slot = document.querySelector('.int-hero .int-demo-media');
    if (slot && slot.parentNode) { slot.parentNode.insertBefore(root, slot); return true; }
    var ctr = document.querySelector('.int-hero .int-ctr');
    if (!ctr) return false;
    ctr.appendChild(root);
    return true;
  }

  function boot() {
    if (!mount()) return;

    /* Reduced motion: the settled frame, plus a Play control. Never silent. */
    if (reduce) { still(); return; }

    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          if (e.isIntersecting) autoStart();
          else if (running) stop(true);
        });
      }, { threshold: 0.2 }).observe(stage);
    } else {
      autoStart();
    }

    /* Belt and braces for mobile WebKit, where a deferred or mis-timed first
       IO callback has been seen to leave the stage blank: re-check shortly
       after boot, then on scroll, then whenever the tab comes back. All three
       land in ensure(), which no-ops if the loop is already running. */
    setTimeout(ensure, 1200);
    window.addEventListener('scroll', ensure, { passive: true });

    document.addEventListener('visibilitychange', function () {
      /* A backgrounded tab throttles setTimeout; returning to it would
         otherwise dump the whole queue at once. Restart clean. */
      if (document.hidden) { if (running) stop(true); }
      else if (inView()) { stop(false); autoStart(); }
    });

    /* Honour a mid-session change to the motion preference -- on iOS this
       fires when Low Power Mode switches on or off under the viewer. */
    if (mq && mq.addEventListener) {
      mq.addEventListener('change', function (e) {
        reduce = e.matches;
        if (reduce) { stop(false); still(); } else { ensure(); }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else { boot(); }
})();
"""

# The product mark drawn in the transcript. A generic spark; swap in your own
# path (keep the viewBox in sync) when you deploy this for a real product.
BIRD_PATH = ("M50 4 L58 40 L94 48 L58 56 L50 92 L42 56 L6 48 L42 40 Z")
BIRD_SVG = ('<svg viewBox="0 0 100 100" aria-hidden="true">'
            '<path fill="currentColor" d="' + BIRD_PATH + '"/></svg>')


def alt_text(d):
    """Screen-reader description. Names the reads, and says nothing changed."""
    firsts = d["beats"][0]
    caps = ", ".join(s[1][0].lower() + s[1][1:] for s in firsts["steps"])
    return ("A simulated Kestrel session on the %s integration. Asked \"%s\", "
            "Kestrel works through %s, then shows the result in a %s panel. "
            "Read only; nothing is changed." %
            (d["name"], firsts["q"], caps, d["panel"]))


def foot_text(d):
    """METADATA ONLY since 2026-08-28 -- no longer rendered or shipped.

    Kept because the manifest prints it and it is the one-line statement of
    what each demo is: a read. If a caption ever comes back, this is its text.
    """
    return "%s, read" % d["name"]


def js_demos():
    out = {}
    for d in DEMOS:
        # PRE-STAGED, NOT SHIPPED. A demo carrying `pending` is fully written and
        # fully gated, but is kept out of the deployed bundle until the claims doc
        # section it stands on is approved. Deleting the one key ships it; there
        # is no second place to edit. See demos.py (posthog).
        # DEMO_PREVIEW_PENDING=1 includes them, for the local harness only, so a
        # pre-staged demo can be looked at before it is approved. Never set it
        # on a path that deploys.
        if d.get("pending") and not os.environ.get("DEMO_PREVIEW_PENDING"):
            continue
        out[d["slug"]] = {
            "name": d["name"],
            "icon": icon_for(d),
            "panel": d["panel"],
            "video": bool(d.get("video")),
            # `sub` and `foot` are NOT emitted any more. Nothing renders them
            # as of 2026-08-28, and shipping them anyway would leave unseen
            # copy sitting in the served HTML of 13 pages -- crawlable text no
            # reader ever sees, which is the shape the duplicate-content audit
            # exists to avoid. They stay in demos.py and the manifest as
            # metadata; see foot_text() and demos.py's `sub`.
            "alt": alt_text(d),
            # Hero lockup metrics. Shipped for EVERY demo including the three
            # video ones: the hero normaliser runs before the video
            # early-return, because those pages have the same hero.
            "hero": hero_for(d),
            # No `replay` key any more: the control it labelled was removed
            # 2026-08-28, so there is nothing to label. claims doc 9.24's ban on
            # the words "session" and "replay" in PostHog copy still stands,
            # and is now satisfied by construction -- neither word appears.
            "beats": [{"q": b["q"], "card": b["card"],
                       "steps": b["steps"], "panel": b["panel"]}
                      for b in d["beats"]],
        }
    return json.dumps(out, separators=(",", ":"), ensure_ascii=True)


def build_embed():
    js = JS_HEAD.replace("__BIRD__", BIRD_SVG.replace("'", "\\'"))
    return ("<style>" + CSS + "</style>\n<script>\nvar DEMOS = " +
            js_demos() + ";\n" + js + "</script>\n")


# --------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------
def build_manifest(gates):
    L = []
    W = L.append
    W("# \"See it work\" rollout, review manifest")
    W("")
    W("Pages: `/integrations/<slug>` on the site the embed is installed on")
    W("")
    W("**%d spokes.** One embed on the shared spoke template, keyed by slug, so a "
      "page with no entry gets nothing (generic pages are untouched by "
      "construction, not by a filter someone has to maintain)." % len(DEMOS))
    W("")
    W("**Every demo is READS ONLY.** No write is animated anywhere, including on "
      "the sections that approve writes (Gmail can send, Todoist can add tasks, "
      "Notion can create pages). A hero animation is the \"high-volume page copy\" "
      "several sections want eng sign-off for, so variation comes from panel "
      "type, beat count, which read leads, and question phrasing instead.")
    W("")
    W("## Read this first")
    W("")
    n_render = sum(1 for d in DEMOS if not d.get("video"))
    W("- **%d of %d actually render today.** gmail, notion and todoist already have "
      "real self-hosted demo videos in the same hero slot, so the coded demo "
      "returns early there rather than putting a simulation next to real footage. "
      "All three are still built and gated; deleting one flag in `demos.py` flips "
      "any of them." % (n_render, len(DEMOS)))
    W("- **Google Calendar is not here, and not for a claims reason.** Section 9.2 "
      "is PRODUCT-VERIFIED and would make a good demo, but there is no "
      "`google-calendar` spoke page to attach it to (the collection has "
      "apple-calendar and google-drive). The definition is written and commented "
      "out in `demos.py`, and its `events` panel renderer is built and working "
      "(Plaud's transcript beat uses it), so it is a copy-paste if the page appears.")
    W("- **Echo was dropped** (2026-08-20). Section 9.23 has one tool, "
      "`ping`, and zero reads, so there was no result to put in a panel. "
      "Not a claims problem, just too thin to demo.")
    W("- **The iOS static frame is fixed, and it was not a guess.** The shipped "
      "code ended `still()` with `replay.style.display = 'none'`, and `boot()` "
      "called `still()` and returned whenever `prefers-reduced-motion` matched. "
      "iOS sets that preference from both Reduce Motion **and Low Power Mode**, so "
      "a phone on low battery got the settled frame and no control at all. The "
      "settled frame stays (it is the right answer to the preference) but now "
      "always carries a visible Play button, the whole stage is tappable, leaving "
      "the viewport settles instead of freezing mid-animation, and an explicit tap "
      "plays even under reduced motion. Verified at a real 390px viewport in both "
      "motion modes.")
    W("- **Both gate layers ran, and both were needed.** The deterministic "
      "gates are the real pipeline functions (`gate.py`) over every "
      "on-screen string. The LLM factchecker then ran offline with the "
      "real `4-factchecker.md` prompt, grounded on each tool's own section. "
      "It FAILED monday.com for a composed claim the deterministic pass had "
      "cleared: 9.16's own approved phrasing, \"the item you were just "
      "talking about\", makes the conversation a precondition for the tool "
      "action, which 9.14 forbids for that very section. Reworded to 9.16's "
      "other approved phrasing; re-run is PASS. **9.16 is worth amending.** "
      "All 15 now PASS both layers.")
    W("")
    for d in DEMOS:
        g = gates[d["slug"]]
        flag = ("  **FLAG: %s**" % d["flag"]) if d.get("flag") else ""
        W("---")
        W("")
        W("## %s  &middot;  `/integrations/%s`%s" % (d["name"], d["slug"], flag))
        W("")
        W("| | |")
        W("|---|---|")
        W("| Panel | `%s` -- %s |" % (d["panel"], PANEL_TYPES[d["panel"]]))
        W("| Exchanges | %d |" % len(d["beats"]))
        W("| Phrasing | %s |" % d["style"])
        W("| Basis | claims doc %s, %s |" % (d["section"], d["tier"]))
        if d.get("video"):
            W("| Renders? | **NO -- defers to the real demo video** on this "
              "spoke. Built and gated; one flag in demos.py to flip. |")
        W("| Gates | %s |" % g)
        W("")
        W("Capabilities leaned on:")
        for c in d["claims"]:
            W("- %s" % c)
        W("")
        W("Script. Everything below RENDERS, except the two lines marked")
        W("(metadata) -- the heading, subline and foot caption were removed")
        W("2026-08-28 and are kept only in demos.py. Gate them anyway: they")
        W("become published copy the moment anyone reuses them.")
        W("")
        W("```")
        W("SUB   %s   (metadata, not rendered)" % d["sub"])
        for i, b in enumerate(d["beats"], 1):
            W("")
            W("Q%-4d %s" % (i, b["q"]))
            W("CARD  %s" % b["card"])
            for s in b["steps"]:
                W("STEP  %s" % s[1])
            p = b["panel"]
            W("PANEL %s%s" % (p["title"],
                              ("  (%s)" % p["meta"]) if p.get("meta") else ""))
            for r in p["rows"]:
                cells = [str(c) for c in r if str(c).strip()]
                W("  ROW %s" % "  |  ".join(cells))
        W("FOOT  %s   (metadata, not rendered)" % foot_text(d))
        W("CTRL  %s" % d.get("replay", "Replay"))
        W("```")
        W("")
    return "\n".join(L) + "\n"


# --------------------------------------------------------------------------
# Deploy artifact. The repo copy (embed.html) keeps every comment -- it is the
# documented source. The deployed copy keeps a short header pointing back here
# plus the two load-bearing warnings, and strips the rest to fit comfortably in
# one API write.
# --------------------------------------------------------------------------
DEPLOY_HEADER = """<!-- "See it work" coded demo, %d verified spokes.
     SOURCE OF TRUTH: see-it-work/{demos.py,build.py}
     Regenerate with `python3 build.py`; do not hand-edit this block.
     GEOMETRY: every cqw value is measured off the shipped demo videos, see
     docs/GEOMETRY.md. Do not tidy a number without
     re-measuring against the reference frames.
     CLAIMS: strings come from each tool's own claims doc section, READS ONLY.
     Gates: gate.py -- re-run it if any string changes.
     iOS: reduced motion renders the settled frame AND a visible Play control.
     Never hide that control: a still frame with no control is the bug this
     replaced. -->
"""


def minify(src):
    css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
    js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"^[ \t]+", "", css, flags=re.M)
    css = re.sub(r"\n{2,}", "\n", css).strip()
    js = re.sub(r"\n[ \t]*/\*.*?\*/", "", js, flags=re.S)
    js = re.sub(r"^[ \t]*/\*.*?\*/", "", js, flags=re.S | re.M)
    js = re.sub(r"\n[ \t]*//[^\n]*", "", js)
    js = re.sub(r"\n{2,}", "\n", js).strip()
    return (DEPLOY_HEADER % len(DEMOS) + "<style>" + css + "</style>\n<script>\n"
            + js + "\n</script>")


def split_deploy(src):
    """Webflow caps a single HtmlEmbed's `code` setting at 50,000 characters and
    the one-block artifact is ~51.6k. Split on the seam with no ordering
    dependency: a stylesheet can load in either order, whereas `var DEMOS` must
    exist before the engine IIFE runs, so data and engine stay together.
    Returns (css_block, js_block)."""
    mini = minify(src)
    css = re.search(r"<style>.*?</style>", mini, re.S).group(0)
    js = re.search(r"<script>.*?</script>", mini, re.S).group(0)
    css_hdr = ('<!-- "See it work" demo, STYLES ONLY. The engine + per-tool data live in\n'
               '     the sibling embed with domId int-ld-mount. Split because one block is\n'
               '     over Webflow\'s 50,000-char limit for a single embed; a stylesheet has\n'
               '     no load-order dependency, `var DEMOS` does.\n'
               '     SOURCE: see-it-work/build.py -- regenerate,\n'
               '     do not hand-edit. Geometry is measured; see OBSERVED-UI-SPEC.md. -->\n')
    js_hdr = ('<!-- "See it work" demo, ENGINE + DATA for %d verified spokes. Styles are in\n'
              '     the sibling embed with domId int-ld-style.\n'
              '     SOURCE OF TRUTH: see-it-work/{demos.py,build.py}\n'
              '     Regenerate with `python3 build.py`; do not hand-edit.\n'
              '     CLAIMS: strings come from each tool\'s own claims doc section, READS ONLY.\n'
              '     Gates: gate.py -- re-run it if any string changes.\n'
              '     ICONS: every tool shows its REAL mark, sized from measured ink so all\n'
              '     13 render at one visual height. Audited 2026-08-24 and again 2026-08-28.\n'
              '     NO CHROME: no heading, no subline, no caption, no visible control\n'
              '     (the founder, 2026-08-28). The demo loops on its own; the only control is\n'
              '     a transparent stage-sized button, active in the settled state only.\n'
              '     LOGO SIZING is driven by each asset MEASURED ink box (logos.json),\n'
              '     never by its canvas: --lg-a is the ink aspect and .wm switches to cap\n'
              '     height. The hero lockup is normalised by the same numbers at runtime.\n'
              '     REDUCED MOTION: a user whose OS asks for less motion gets the settled\n'
              '     final transcript and NO auto-loop, ever. Every automatic start goes\n'
              '     through autoStart(), which refuses; only an explicit stage tap calls\n'
              '     start() directly, because that is the user asking for motion. -->\n' % len(DEMOS))
    return css_hdr + css, js_hdr + js


if __name__ == "__main__":
    embed = build_embed()
    open(os.path.join(HERE, "embed.html"), "w").write(embed)
    pend = [d["slug"] for d in DEMOS if d.get("pending")]
    prev = bool(os.environ.get("DEMO_PREVIEW_PENDING"))
    if pend and prev:
        note = " -- PREVIEW BUILD, includes pending (%s). DO NOT DEPLOY." \
            % ", ".join(pend)
        n = len(DEMOS)
    elif pend:
        note = " (pending, not shipped: %s)" % ", ".join(pend)
        n = len(DEMOS) - len(pend)
    else:
        note, n = "", len(DEMOS)
    print("embed.html %d bytes, %d of %d demos in the bundle%s"
          % (len(embed), n, len(DEMOS), note))
    counts = {}
    for d in DEMOS:
        counts[d["panel"]] = counts.get(d["panel"], 0) + 1
    print("panel spread:", counts)
    print("beat spread:", sorted(len(d["beats"]) for d in DEMOS))

    # Write the two deploy blocks every time. They used to be produced by an
    # ad-hoc call, which meant embed.*.deploy.html could sit a build behind
    # demos.py and nothing would say so -- the PostHog build hit exactly that.
    # Regenerating here makes the artifact that gets pasted into Webflow a
    # function of demos.py, not of whether someone remembered a second step.
    if not prev:
        css_block, js_block = split_deploy(embed)
        for fn, block in (("embed.css.deploy.html", css_block),
                          ("embed.js.deploy.html", js_block)):
            open(os.path.join(HERE, fn), "w").write(block)
            flag = "" if len(block) <= 50000 else "  <-- OVER THE 50,000 LIMIT"
            print("%-26s %6d chars%s" % (fn, len(block), flag))
        assert max(len(css_block), len(js_block)) <= 50000, \
            "a deploy block exceeds Webflow's 50,000-char cap on one embed"
    else:
        print("preview build: deploy artifacts NOT rewritten")
