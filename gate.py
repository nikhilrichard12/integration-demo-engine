"""Deterministic gates over every on-screen string in every demo.

    python3 gate.py            # exit 1 on any hard fail

In production this file imported the content pipeline's own claim-checking
library, so a demo was held by exactly the rule that would hold page copy
(section lookup, composed-claim detection, surface ceilings, held verbs, each
tool's do-not-claim list). That library is not part of this repo. What remains
here is the portable subset, plus a hook (`extra_checks`) where you wire in your
own claims source.

Checks, per demo:
  1. shape           every beat has q, card, 1-3 steps, a panel with rows
  2. reads only      no write verb in any card title or step label
  3. punctuation     no Unicode em/en dash, no smart quotes, ASCII only
  4. banned words    marketing filler never reaches a rendered string
  5. claims present  every demo names the capabilities it leans on
  6. lengths         questions, titles and rows fit the stage at mobile width
"""
import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from demos import DEMOS  # noqa: E402

WRITE_VERBS = re.compile(
    r"\b(creat(e|ing)|add(ing)?|updat(e|ing)|edit(ing)?|delet(e|ing)|remov(e|ing)|"
    r"send(ing)?|post(ing)?|publish(ing)?|assign(ing)?|clos(e|ing)|mark(ing)?|"
    r"schedul(e|ing)|book(ing)?|writ(e|ing)|sav(e|ing)|upload(ing)?|mov(e|ing))\b",
    re.I)
BANNED = re.compile(r"\b(seamless(ly)?|effortless(ly)?|streamline[sd]?|game.?changer|"
                    r"supercharge[sd]?|unlock(s|ed)?|revolutioni[sz]e[sd]?|magic(al)?)\b", re.I)
NON_ASCII = re.compile(r"[^\x00-\x7f]")
MAX_Q = 72       # one wrapped bubble at 390px
MAX_TITLE = 40
MAX_CELL = 48
MAX_ROWS = 5


def strings_of(d):
    """Every string that could reach a reader, in render order."""
    out = [d.get("sub", "")]
    for b in d["beats"]:
        out += [b["q"], b["card"]] + [s[1] for s in b["steps"]]
        p = b["panel"]
        out.append(p["title"])
        if p.get("meta"):
            out.append(p["meta"])
        for r in p["rows"]:
            out += [str(c) for c in r if str(c).strip()]
    return out


def extra_checks(d, blob):
    """Hook: return a list of failure strings from your own claims source.

    The production version looked each tool up in a versioned claims doc and
    failed the demo on any capability, verb or phrasing the section did not
    approve. Implement the same idea against whatever you maintain.
    """
    return []


def check(d):
    fails, notes = [], []
    if not d.get("claims"):
        fails.append("no claims listed")
    for i, b in enumerate(d["beats"], 1):
        if not (1 <= len(b["steps"]) <= 3):
            fails.append("beat %d: %d steps, want 1-3" % (i, len(b["steps"])))
        if len(b["q"]) > MAX_Q:
            fails.append("beat %d: question is %d chars, max %d" % (i, len(b["q"]), MAX_Q))
        for txt in [b["card"]] + [s[1] for s in b["steps"]]:
            m = WRITE_VERBS.search(txt)
            if m and not re.search(r"\b(read|list|find|search|check|pull|open|surfac|retriev|query|look)", txt, re.I):
                fails.append("beat %d: write verb '%s' in '%s'" % (i, m.group(0), txt))
        p = b["panel"]
        if len(p["title"]) > MAX_TITLE:
            fails.append("beat %d: panel title too long" % i)
        if len(p["rows"]) > MAX_ROWS:
            fails.append("beat %d: %d rows, max %d" % (i, len(p["rows"]), MAX_ROWS))
        for r in p["rows"]:
            for c in r:
                if len(str(c)) > MAX_CELL:
                    fails.append("beat %d: cell too long: %r" % (i, c))
    blob = "\n".join(strings_of(d))
    if NON_ASCII.search(blob):
        fails.append("non-ASCII character: %r" % NON_ASCII.search(blob).group(0))
    if "--" in blob:
        fails.append("double hyphen in rendered copy")
    m = BANNED.search(blob)
    if m:
        fails.append("banned word: %s" % m.group(0))
    fails += extra_checks(d, blob)
    return fails, notes


def run():
    bad = 0
    for d in DEMOS:
        fails, notes = check(d)
        tag = "FAIL" if fails else "PASS"
        bad += bool(fails)
        print("%-14s %s  %s" % (d["slug"], tag, "; ".join(fails) or ""))
    print("\n%d of %d demos pass" % (len(DEMOS) - bad, len(DEMOS)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run())
