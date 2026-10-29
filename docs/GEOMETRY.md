# The real Kestrel demo UI, measured from the shipped demo videos

Source: the three mp4s in the spoke template's `VIDEOS` map, downloaded from the CDN
and frame-extracted with ffmpeg (1fps for structure, 4fps for the animation).

    todoist-demo-v1.mp4   notion-demo-v1.mp4   gmail-demo-v1.mp4

All three: **1440x1080 (4:3), 30fps, 10.97s**. All three follow the SAME three-act
structure. Everything below is measured, not guessed. Pixel coordinates are in the
1440x1080 frame; the embed reproduces them proportionally with `cqw` units
(1cqw = 14.4px of the reference frame), so fidelity holds at any rendered size.

## What I got wrong the first time

There is **no window chrome**. No title bar, no traffic-light dots, no "Kestrel"
label, no integration chip in a header, no bot avatar, no bouncing "thinking" dots,
and the background is **pure white (#ffffff)**, not cream. The first build invented
all of that from generic chat-app convention.

**Do not hand-draw the app icon either.** The second build tried to draw Linear's
mark as inline SVG paths and it rendered as a purple square with a blob in it. The
reference videos use each app's real icon, so the rebuild uses the *site's own*
Linear asset (`linear.png`, the same file the spoke hero and the directory card
use), shrunk to 96px and inlined as a base64 data URI (~6.2KB) so the embed still
makes no external request. Note this asset is a periwinkle circle cut by diagonal
bands -- it is the site's Linear mark, not Linear's official logo. Separately worth
flagging: the *Integration Directory* item for Linear points at a
black-and-white `favicons.jpeg`, which is what `/all-integrations` currently shows.

## Act 1 -- the composer (0.0s to ~2.1s)

A single floating composer, horizontally centred, sitting slightly below the middle.
Nothing else on screen.

| thing | measured | cqw |
|---|---|---|
| composer box | x135 y375, 1172x255 | left 9.375, top 26.042, 81.389 x 17.708 |
| corner radius | 23px | 1.597 |
| fill / border | `#fafaf8` / warm hairline | |
| typed text | 34px, near-black `#141414`, x172 | font 2.361, pad-left 2.569 |
| "+" chip | 52x52 at x160, radius 12, hairline border | 3.611, radius 0.833 |
| mic glyph | ~30px outline, centre x1176 | 2.083 |
| send button | **black circle** 66px, white up-arrow, centre x1252 | 4.583 |

**Typing is real.** "Update my Todoist with tasks from this morning." (46 chars) types
between ~0.5s and ~2.0s -> **~33ms/char**. Frame 01 shows a single "U"; frame 02
shows the full sentence. So the typewriter stays, at that rate.

## Act 2 -- the conversation (~2.1s to ~7.0s)

The composer is gone. Three elements, top-down:

1. **User bubble**, right-aligned. Fill `#f5f3eb`, radius 24px, all corners equal
   (no tail, no asymmetric corner), padding ~28x24, text 34px `#1b1c15`, wrapping to
   2 lines at max-width ~660px. Right edge inset 200px from the frame edge.
2. **Tool card**, left-aligned at x203, 487x117, radius 16, fill `#fdfbf9`.
   Contains: the **source app's real icon** on a white rounded tile (44px), a title
   in **regular weight** (34px, `#2f2f2d`), and a chevron. Title changes over the
   act: "Gathering context" (chevron **right**) -> "Updating <App>" (chevron **down**).
   **The activity indicator is an indigo highlight that ORBITS the card's own 1px
   ring.** It is not a separate bar, and -- corrected after a second pass -- it is
   also **not a progress fill**. In frame 05 the bright arc sits on the
   top-right / right / bottom-right; one second later in frame 06 it has moved to
   the top-left / left. It simply goes round and round while the tool works.
   Sampled pixels, frame 05: brightest point (bottom-right corner) `174,181,225`,
   base ring away from the arc `240,235,228`, and the top-left of the ring is
   effectively invisible at `255,255,253`. Implemented as a rotating conic
   gradient on a square pseudo-element (side >= the card's diagonal) clipped by
   the wrapper's rounded overflow, with the opaque card face masking the middle.
3. **Step list, outdented BELOW the card** -- plain rows on the background, no card.
   Outline icon (31px, ~2px stroke: magnifier, document, checkbox-check) + label
   (34px). Icon at x240, label at x305, row pitch 72px.
   **Steps reveal one at a time**, and a not-yet-started step shows its icon
   **dimmed with no label** (clearly visible in gmail frame 05).

## Act 3 -- the app cutaway (~7.0s to end)

A hard **cut**, not a fade.

- **Pill tab**, top-left at x95 y82, 215x51, fully rounded, white with a soft
  shadow: an `x` glyph, the app icon, the app name.
- **Large panel** below it at x80 y170, width 1285, radius 24, white, hairline
  border, bleeding off the bottom of the frame.
- Inside: a faithful mock of the third-party app (Todoist "Inbox" list, Notion page
  with cover art, etc). Rows **populate one at a time** (frame 07 has one row,
  frame 09 has three).
- Panel internals, measured off frame 09 (all panel-relative unless stated):
  title top 4.51cqw, left 5.556cqw, ~48px/3.194cqw semibold. **There is no
  subtitle under the title** -- the list starts immediately. First row band
  starts 10.42cqw, row height 6.04cqw, row text 2.361cqw. Status circle
  2.361cqw across with a ~0.174cqw stroke (thin and large -- easy to draw far
  too small), gap to the text 1.18cqw. Separators inset ~4.9cqw left and
  ~5.7cqw right, i.e. ~88% of the panel width.
- The panel also carries a trailing `+ Add task` affordance. **Deliberately
  omitted from the Linear build**: the demo is claims-gated to reads, and a
  visible create affordance reads as a write capability.
- The **Kestrel hummingbird** silhouette is overlaid and **flies across the
  panel** as the rows fill -- bottom-left in frame 07, top-right in frame 09.
  Brand asset: `kestrel-hub-ink.svg`, viewBox `0 0 2820 2477`, fill `#1B1C15`.
  Inlined in the embed so it costs no request.
  Absolute frame coords: start (frame 07) left 6.60cqw / top 59.03cqw, end
  (frame 09) left 71.53cqw / top 17.71cqw, ~9.03cqw wide. The end point sits to
  the RIGHT OF THE TITLE and above the rows, not down among them.
  Two traps: the bird is **rotated**, so its visual box is ~1.1x its layout box
  and sits ~0.5cqw up and left of it -- the CSS values are pre-compensated so the
  silhouette, not the layout box, lands on the reference coords. And Linear's
  rows carry a right-aligned assignee column that Todoist's do not, so the end
  point has to be checked for collision with it (currently clears by 35px).

## Timeline used for the Linear rebuild (matches the reference's ~11s)

    0.00  composer, empty
    0.40  typing starts, 33ms/char
    1.62  typing complete
    2.10  CUT: composer out, bubble in
    2.50  tool card "Reading Linear", chevron right, top border starts filling
    3.10  step 1 label
    4.00  step 2 label
    4.90  step 3 label
    6.30  border fill complete, chevron flips down
    7.00  CUT to act 3: pill + panel, bird enters low-left
    7.40  row 1     8.00  row 2     8.60  row 3
    7.40 -> 9.60  bird flies to upper-right
    9.60  hold
    11.00 loop

The earlier build ran 16.2s with a structure that does not exist in the product.
The reference is 11s, so the rebuild is 11s.
