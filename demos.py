"""Demo definitions for the "See it work" coded demo, one entry per verified spoke.

SINGLE SOURCE OF TRUTH. The embed JS and the human review manifest are both
generated from this file (build.py). Nothing here is hand-transcribed into the
embed -- that mistake shipped a fabricated blurb once already.

CLAIMS RULE. Every on-screen string for a tool comes from that tool's OWN
claims doc section. `claims` lists the approved capabilities each beat leans on,
by the section's own wording, so the factchecker has something to check against.

READS ONLY, EVERYWHERE. No demo animates a write, even where the section
approves writes (Gmail can send, Todoist can add tasks, and so on). Two reasons:
a hero animation is exactly the "high-volume page copy" several sections want
eng sign-off for, and the brief says high-stakes verbs are never animated.
Variation therefore comes from panel type, beat count, which read leads, and
question phrasing -- not from escalating to writes.

PANEL TYPES are deliberately different per tool family so no two demos read
identical, while the surrounding product chrome stays byte-identical (the whole
point: it is one product).

REAL FOOTAGE WINS. Three spokes -- gmail, notion, todoist -- already have a real
self-hosted demo video, injected into the same hero slot by the VIDEOS map in the
template's head code. Shipping a coded recreation next to the real recording of
the same product would put two "see it work" visuals in one hero, and the
recording is the better asset (the coded demo exists BECAUSE most spokes have no
footage; these three are where the footage came from). Those three carry
`video=True` and the engine returns early on them. Their definitions are built
and gated like every other, so flipping the decision is deleting one flag.
"""

# Each demo:
#   slug      Webflow spoke slug (gates which page the demo builds on)
#   name      display name, as the product would show it
#   section   claims doc section, for the manifest
#   tier      provenance tier, for the manifest
#   panel     renderer key (see PANEL_TYPES)
#   logo      Webflow CDN asset for the app icon (filled in by build.py)
#   sub       METADATA ONLY since 2026-08-28. Was the static sub-line under a
#             "See it work" heading; the founder had both removed so the demo
#             renders with no wrapper text. Kept because it is the tightest
#             one-sentence statement of what each demo claims, which makes it
#             the right raw material for a meta description or an editor's
#             summary -- but it is neither rendered nor shipped in the embed
#             payload, so it is not published copy. gate.py still gates it for
#             exactly that reason: the day it is reused, it becomes published.
#   claims    approved capabilities leaned on, quoting the section
#   beats     the animated exchanges. beat = dict(q, card, steps, panel)
#               q      the user's question (varied phrasing style per tool)
#               card   the tool-card title once work starts
#               steps  [[icon, label], ...] 2 or 3 rows
#               panel  {title, meta?, rows: [...]}  rows shape is per panel type

DEMOS = [

# ---------------------------------------------------------------- Linear (shipped)
# Kept EXACTLY as shipped and signed off: one exchange, issue list. Listed here
# so the manifest covers the whole set, and so a future edit has its definition
# in the same place as the rest.
dict(
    slug="linear", name="Linear", section="9.9", tier="TELEMETRY-VERIFIED",
    panel="issues", style="direct question",
    sub="Ask in Chat. Kestrel can list issues across your Linear "
        "workspace and read the comments on any issue.",
    claims=["list_issues: 'can list issues across your Linear workspace'",
            "list_teams: 'can list the teams in your Linear workspace'",
            "list_comments: 'can read the comments on any issue'"],
    beats=[dict(
        q="What's still open on the Mobile team?",
        card="Reading Linear",
        steps=[["find", "Checking Linear connection"],
               ["doc", "Listing issues on the Mobile team"],
               ["note", "Reading comments on LB-241"]],
        panel=dict(title="Mobile", rows=[
            ["prog", "LB-241", "Offline sync drops queued edits", "Priya"],
            ["", "LB-238", "Push token refresh fails on reinstall", "Marco"],
            ["rev", "LB-233", "Crash on cold start, Android 14", "Priya"]]),
    )],
),

# ---------------------------------------------------------------- Gmail
# Differentiator vs Outlook: multi-account is verified here and NOT there.
dict(
    slug="gmail", video=True, name="Gmail", section="9.1", tier="PRODUCT-VERIFIED",
    panel="mail", style="colloquial, vague recall",
    sub="Ask in Chat. Kestrel reads across every connected Gmail account "
        "to surface the open loops.",
    claims=["'reads your email to surface open loops'",
            "'Ask what a client emailed this week and Kestrel pulls it "
            "from the right account'",
            "'Multiple Gmail accounts can be connected'"],
    beats=[
        dict(q="Anything from Northwind I still owe a reply to?",
             card="Reading Gmail",
             steps=[["find", "Checking Gmail connection"],
                    ["mail", "Searching both connected accounts"],
                    ["note", "Reading the Northwind thread"]],
             panel=dict(title="Northwind", meta="2 accounts searched", rows=[
                 ["Dana Whitfield", "Re: contract redlines, one open question", "Tue"],
                 ["Dana Whitfield", "Redlines attached for your review", "Mon"],
                 ["you", "Redlines coming back today", "Mon"]])),
        dict(q="And the open loop in it?",
             card="Reading Gmail",
             steps=[["note", "Reading the last message in the thread"],
                    ["find", "Surfacing what is unanswered"]],
             panel=dict(kind="kv", title="Open loop", meta="from Dana, Tue", rows=[
                 ["Dana asked", "which entity signs, Northwind US or EU", ""],
                 ["Unanswered since", "Tuesday", ""]])),
    ],
),

# ---------------------------------------------------------------- Google Calendar
# OUT OF SCOPE, and not for a claims reason: section 9.2 is PRODUCT-VERIFIED and
# would make a good demo, but THERE IS NO google-calendar SPOKE PAGE. The
# collection holds apple-calendar and google-drive; no Google Calendar item
# exists, so there is nothing to attach an embed to. Definition kept below,
# commented, so it is a copy-paste away if the page is ever created.
#
#   panel "events" (left time column + title + duration), 2 beats, imperative
#   Q1 "Walk me through tomorrow."     -> list Events
#   Q2 "Where could a 45-minute block go?" -> find free slots
#   claims: schema 1220584ccdcb list Events / find free slots / list calendars
#   NOTE the "events" panel renderer is built and unused; it is what this
#   demo would use, and costs nothing to leave in place.

# ---------------------------------------------------------------- Notion
dict(
    slug="notion", video=True, name="Notion", section="9.3", tier="PRODUCT-VERIFIED",
    panel="docs", style="vague recall, 'what did it say'",
    sub="Ask in Chat. Kestrel searches your Notion workspace and pulls the "
        "page into context.",
    claims=["notion-search: 'surfaces the page, database, or block you need'",
            "notion-fetch: 'can pull the full content of any Notion page'",
            "notion-query-database-view: 'can query a Notion database view "
            "and return filtered results'"],
    beats=[
        dict(q="What did we write down about the rate limit decision?",
             card="Reading Notion",
             steps=[["find", "Checking Notion connection"],
                    ["doc", "Searching your workspace"],
                    ["note", "Pulling the page"]],
             panel=dict(title="Search results", meta="3 matches", rows=[
                 ["API rate limits, decided", "Engineering / Decisions",
                  "the 600/min ceiling and why"],
                 ["Platform RFC 014", "Engineering / RFCs",
                  "original proposal, superseded"],
                 ["Q3 planning notes", "Product",
                  "one line on limits, no detail"]])),
        dict(q="Just the decision itself.",
             card="Reading Notion",
             steps=[["doc", "Pulling the full page content"]],
             panel=dict(kind="kv", title="API rate limits, decided",
                        meta="Engineering / Decisions", rows=[
                 ["Ceiling", "600 requests per minute per workspace", ""],
                 ["Rationale", "p99 burst was 540, headroom kept deliberate", ""],
                 ["Revisit", "when a single tenant passes 400 sustained", ""]])),
    ],
),

# ---------------------------------------------------------------- Todoist
# Uses "projects" -- Todoist's approved vocabulary.
dict(
    slug="todoist", video=True, name="Todoist", section="9.4", tier="PRODUCT-VERIFIED",
    panel="checks", style="terse, keyword",
    sub="Ask in Chat. Kestrel finds your tasks across Todoist and can "
        "read them back by due date.",
    claims=["find-tasks-by-date: 'can find your tasks by due date'",
            "find-projects: 'can find your Todoist projects'",
            "get-overview: 'can get an overview of your tasks and projects'"],
    beats=[
        dict(q="Due today?",
             card="Reading Todoist",
             steps=[["find", "Checking Todoist connection"],
                    ["check", "Finding tasks due today"]],
             panel=dict(title="Today", meta="4 tasks", rows=[
                 ["", "Revised SOW for Northwind", "Work"],
                 ["", "Review Priya's PR", "Work"],
                 ["due", "Renew domain", "Admin"],
                 ["", "Book the dentist", "Personal"]])),
        dict(q="Which project is the heaviest right now?",
             card="Reading Todoist",
             steps=[["doc", "Finding your projects"],
                    ["check", "Getting an overview"]],
             panel=dict(title="Projects", meta="by open tasks", rows=[
                 ["", "Work", "18 open"],
                 ["", "Admin", "6 open"],
                 ["", "Personal", "4 open"]])),
    ],
),

# ---------------------------------------------------------------- GitHub
dict(
    slug="github", name="GitHub", section="9.5", tier="TELEMETRY-VERIFIED",
    panel="repos", style="terse, keyword",
    sub="Ask in Chat. Kestrel lists your pull requests and can read the "
        "full details of any one of them.",
    claims=["list_pull_requests: 'can list open and closed pull requests'",
            "pull_request_read: 'can read the full details of any pull request'",
            "list_commits: 'can list and surface commits across your repositories'"],
    beats=[
        dict(q="Open PRs on the web repo?",
             card="Reading GitHub",
             steps=[["find", "Checking GitHub connection"],
                    ["repo", "Listing open pull requests"]],
             panel=dict(title="acme/web", meta="3 open", rows=[
                 ["open", "#812", "Cache the settings query", "priya/cache-settings"],
                 ["draft", "#809", "Extract the mailer into a job", "marco/mailer-job"],
                 ["open", "#804", "Bump the client to 4.2", "deps/client-4-2"]])),
        dict(q="What's actually in 812?",
             card="Reading GitHub",
             steps=[["repo", "Reading the pull request details"],
                    ["note", "Listing the commits on it"]],
             panel=dict(title="#812 Cache the settings query",
                        meta="priya/cache-settings", rows=[
                 ["commit", "a3f1c0", "Settings cache read path", ""],
                 ["commit", "77bd42", "Invalidation on workspace update", ""],
                 ["commit", "e10a95", "Test coverage for invalidation", ""]])),
        dict(q="Anything touching the auth module?",
             card="Reading GitHub",
             steps=[["find", "Searching code across your repositories"]],
             # a code-search hit is a path plus context, not a numbered PR, so
             # this beat drops the repos row template for the doc-style one --
             # the mono id column is 5.6cqw and a filepath does not fit in it.
             panel=dict(kind="docs", title="Code search", meta="auth module", rows=[
                 ["lib/auth/session.rb", "touched by #809", "3 matches"],
                 ["lib/auth/tokens.rb", "no open PR", "1 match"]])),
    ],
),

# ---------------------------------------------------------------- ClickUp
# Differentiator: workspace hierarchy is a ClickUp-specific read.
dict(
    slug="clickup", name="ClickUp", section="9.6", tier="TELEMETRY-VERIFIED",
    panel="checks", style="direct question",
    sub="Ask in Chat. Kestrel reads your ClickUp workspace structure and "
        "filters tasks inside it.",
    claims=["get_workspace_hierarchy: 'can read your ClickUp workspace structure'",
            "filter_tasks: 'can filter tasks across your ClickUp workspace'",
            "get_task_comments: 'can read the comments on any ClickUp task'"],
    beats=[
        dict(q="How is the Platform space laid out?",
             card="Reading ClickUp",
             steps=[["find", "Checking ClickUp connection"],
                    ["doc", "Reading the workspace structure"]],
             panel=dict(title="Platform", meta="space, 3 lists", rows=[
                 ["", "Ingest pipeline", "12 tasks"],
                 ["", "Query layer", "9 tasks"],
                 ["", "Runbooks", "4 tasks"]])),
        dict(q="What's blocked in the query layer?",
             card="Reading ClickUp",
             steps=[["check", "Filtering tasks by status"],
                    ["note", "Reading the comments on them"]],
             panel=dict(title="Query layer", meta="status: blocked", rows=[
                 ["due", "Partition the events table", "waiting on infra"],
                 ["due", "Backfill the Q2 range", "blocked by the above"]])),
    ],
),

# ---------------------------------------------------------------- Asana
dict(
    slug="asana", name="Asana", section="9.7", tier="TELEMETRY-VERIFIED",
    panel="checks", style="first person, 'my'",
    sub="Ask in Chat. Kestrel surfaces your own Asana tasks and reads the "
        "details of any of them.",
    claims=["get_my_tasks: 'can surface the tasks assigned to you in Asana'",
            "get_task: 'can read the full details of any task in Asana'",
            "get_projects: 'can surface your Asana projects'"],
    beats=[
        dict(q="What's on me this week?",
             card="Reading Asana",
             steps=[["find", "Checking Asana connection"],
                    ["check", "Surfacing your own tasks"]],
             panel=dict(title="My tasks", meta="this week", rows=[
                 ["due", "Write the migration runbook", "Thu"],
                 ["", "Review the vendor security questionnaire", "Fri"],
                 ["", "Sign off on the Q3 brief", "Fri"]])),
        dict(q="How does Platform look overall?",
             card="Reading Asana",
             steps=[["doc", "Surfacing your projects"],
                    ["note", "Reading the project details"]],
             panel=dict(kind="kv", title="Platform", meta="project", rows=[
                 ["Owner", "you"],
                 ["Open tasks", "14, three due this week"],
                 ["Status", "on track, cutover set for the 14th"]])),
    ],
),

# ---------------------------------------------------------------- Plaud
# READ-ONLY integration. No write tools exist in telemetry at all.
dict(
    slug="plaud", name="Plaud", section="9.8", tier="TELEMETRY-VERIFIED",
    panel="recordings", style="vague recall",
    sub="Ask in Chat. Kestrel lists your Plaud recordings and retrieves "
        "the note or the full transcript from any of them.",
    claims=["list_files: 'can list your Plaud recordings'",
            "get_note: 'can retrieve the AI-generated note for any Plaud recording'",
            "get_transcript: 'can retrieve the full transcript of any Plaud recording'"],
    beats=[
        dict(q="Find the recording where we argued about pricing.",
             card="Reading Plaud",
             steps=[["find", "Checking Plaud connection"],
                    ["rec", "Listing your recordings"]],
             panel=dict(title="Recordings", meta="3 matches", rows=[
                 ["", "Pricing working session", "48m, Tue"],
                 ["", "Weekly product sync", "31m, Mon"],
                 ["", "Northwind discovery call", "52m, last Thu"]])),
        dict(q="What did the note say?",
             card="Reading Plaud",
             steps=[["note", "Retrieving the note for that recording"]],
             panel=dict(kind="kv", title="Pricing working session",
                        meta="AI note, 48m", rows=[
                 ["Decision", "hold the entry price, add a usage tier", ""],
                 ["Open", "who owns the migration comms", ""],
                 ["Next", "revisit after the Northwind renewal", ""]])),
        dict(q="Read me the exact line about the usage tier.",
             card="Reading Plaud",
             steps=[["rec", "Retrieving the full transcript"]],
             panel=dict(kind="events", title="Transcript",
                        meta="Pricing working session", rows=[
                 ["18:42", "so the usage tier sits above Plus, not beside it", ""],
                 ["18:51", "and it does not touch the entry price at all", ""]])),
    ],
),

# ---------------------------------------------------------------- TickTick
# MUST say "lists", never "projects" -- section 9.11 vocabulary rule.
dict(
    slug="ticktick", name="TickTick", section="9.11", tier="PRODUCT-VERIFIED",
    panel="checks", style="imperative",
    sub="Ask in Chat. Kestrel finds your TickTick tasks and reads the full "
        "detail of any one of them.",
    claims=["find-tasks: 'can find your tasks across TickTick'",
            "find-lists: 'can find your TickTick lists'",
            "read full task details: 'can read the full details of any task in TickTick'"],
    beats=[
        dict(q="Show me what's overdue.",
             card="Reading TickTick",
             steps=[["find", "Checking TickTick connection"],
                    ["check", "Finding tasks by due date"]],
             panel=dict(title="Overdue", meta="2 tasks", rows=[
                 ["due", "Chase the insurance renewal", "Admin"],
                 ["due", "Tax docs for Marco", "Admin"]])),
        dict(q="Open the insurance one.",
             card="Reading TickTick",
             steps=[["doc", "Reading the full task details"]],
             panel=dict(kind="kv", title="Chase the insurance renewal",
                        meta="Admin, was due Monday", rows=[
                 ["Priority", "high", ""],
                 ["Notes", "policy number is on the Feb statement", ""],
                 ["List", "Admin", ""]])),
    ],
),

# ---------------------------------------------------------------- Outlook
# Cannot send. Attachment INFO is explicitly allowed and is the differentiator.
dict(
    slug="outlook", name="Outlook", section="9.12", tier="DOCS-VERIFIED",
    panel="mail", style="direct question",
    sub="Ask in Chat. Kestrel searches your Outlook inbox and reads a "
        "message even when Outlook is closed.",
    claims=["'search by keyword, sender, or date across all folders'",
            "'read full message content'",
            "'view attachment info (file names, sizes, and types)'"],
    beats=[
        dict(q="Did the signed order form ever come back from procurement?",
             card="Reading Outlook",
             steps=[["find", "Checking Outlook connection"],
                    ["mail", "Searching your inbox"],
                    ["note", "Checking the attachments on it"]],
             panel=dict(title="Procurement", meta="4 results", rows=[
                 ["Ines Vogel", "Signed order form attached", "Wed"],
                 ["Ines Vogel", "Re: order form, one correction", "Tue"],
                 ["noreply", "Approval routed to procurement", "Mon"]])),
        dict(q="What's attached to Wednesday's?",
             card="Reading Outlook",
             steps=[["mail", "Reading the message"],
                    ["doc", "Listing its attachments"]],
             panel=dict(kind="files", title="Signed order form attached",
                        meta="from Ines Vogel, Wed", rows=[
                 ["pdf", "order-form-signed.pdf", "", "412 KB"],
                 ["pdf", "w9-northwind.pdf", "", "88 KB"]])),
    ],
),

# ---------------------------------------------------------------- Google Drive
# SURFACE-VERIFIED, cross-check SILENT: plainest terms, reads only, and
# explicitly NOT usable as a composed-claim leg (so single tool only).
dict(
    slug="google-drive", name="Google Drive", section="9.15",
    tier="SURFACE-VERIFIED", panel="docs", style="vague recall",
    sub="Ask in Chat. Kestrel can find the file and read what's in it.",
    claims=["'Connect Google Drive and Kestrel can find the file and read "
            "what's in it'",
            "schema 1220584ccdcb: find file",
            "schema 1220584ccdcb: export Google Workspace file"],
    beats=[
        dict(q="Find the deck where we sized the market.",
             card="Reading Google Drive",
             steps=[["find", "Checking Google Drive connection"],
                    ["doc", "Finding the file"]],
             panel=dict(title="Results", meta="2 files", rows=[
                 ["Market sizing v4", "Slides, edited last Thu",
                  "the numbers we presented"],
                 ["Market sizing scratch", "Sheets, edited in March",
                  "working cells, superseded"]])),
        dict(q="What number did v4 actually land on?",
             card="Reading Google Drive",
             steps=[["doc", "Reading what's in it"]],
             panel=dict(title="Market sizing v4", meta="Slides", rows=[
                 ["Slide 6", "serviceable market, 1.8B",
                  "bottom-up, seats times price"],
                 ["Slide 7", "reachable in 3 years, 240M",
                  "assumes current channel mix"]])),
    ],
),

# ---------------------------------------------------------------- monday.com
# SURFACE-VERIFIED. The pass returned OBJECT TYPES, not verbs -> no write verb
# may be asserted. Reads phrased in the section's own words ("reads it back").
dict(
    slug="monday-com", name="monday.com", section="9.16",
    tier="SURFACE-VERIFIED", panel="board", style="colloquial",
    # 9.16 lists "can find the item you were just talking about" as approved
    # phrasing, and the factchecker FAILED it: "you were just talking about"
    # makes the conversation (a capture source) the precondition for the
    # monday.com action, which 9.14's ceiling forbids for a SURFACE-VERIFIED
    # section -- and 9.16 is explicitly "Not a composed-claim leg". That is an
    # inconsistency inside the claims doc, and 9.14 says resolve to the NARROWER
    # claim, always. So this uses 9.16's OTHER approved phrasing instead.
    sub="Ask in Chat. Kestrel reads the board back to you, items and "
        "columns included.",
    claims=["'Ask what's actually on the board this week and Kestrel "
            "reads it back'",
            "RECORD: board items, columns, groups",
            "NOT used: 9.16's 'the item you were just talking about' -- "
            "composed claim under the 9.14 ceiling, see comment"],
    beats=[
        dict(q="What's actually on the launch board this week?",
             card="Reading monday.com",
             steps=[["find", "Checking monday.com connection"],
                    ["board", "Finding the board"],
                    ["note", "Reading the items on it"]],
             panel=dict(title="Launch", meta="This week group", rows=[
                 ["working", "Press release copy", "Dana"],
                 ["stuck", "Pricing page update", "Marco"],
                 ["done", "Support macros", "Priya"]])),
        dict(q="Which one is stuck?",
             card="Reading monday.com",
             steps=[["board", "Reading the item's columns"]],
             panel=dict(kind="kv", title="Pricing page update", meta="Launch board", rows=[
                 ["Status", "stuck, owned by Marco"],
                 ["Blocked by", "legal review of the usage tier wording"],
                 ["Timeline", "was this week, now unset"]])),
    ],
),

# ---------------------------------------------------------------- Webflow
# SURFACE-VERIFIED, hardest constraint in the set: NO write verb may be named
# for any object, publishing and script management are HELD. So the demo is
# strictly "can look" -- which is the section's own approved phrasing.
dict(
    slug="webflow", name="Webflow", section="9.17",
    tier="SURFACE-VERIFIED", panel="cms", style="direct question",
    sub="Ask in Chat. Kestrel can work with your CMS content and pages.",
    claims=["'Connect Webflow and Kestrel can work with your CMS content "
            "and pages'",
            "'Ask which CMS items are missing a field and Kestrel can look'",
            "RECORD: CMS, pages, collections"],
    beats=[
        dict(q="Which blog posts are missing an SEO title?",
             card="Reading Webflow",
             steps=[["find", "Checking Webflow connection"],
                    ["cms", "Looking at the Blog Posts collection"],
                    ["note", "Checking which items are missing the field"]],
             panel=dict(title="Blog Posts", meta="3 of 48 missing SEO title", rows=[
                 ["missing", "How we think about context", "no SEO title"],
                 ["missing", "Changelog, July", "no SEO title"],
                 ["missing", "Hiring an ops lead", "no SEO title"]])),
        dict(q="Anything else thin on that collection?",
             card="Reading Webflow",
             steps=[["cms", "Looking at the rest of the fields"]],
             panel=dict(title="Blog Posts", meta="field coverage", rows=[
                 ["ok", "Slug, author, body", "48 of 48"],
                 ["missing", "Open graph image", "11 of 48 missing"],
                 ["ok", "Category", "48 of 48"]])),
    ],
),

# ---------------------------------------------------------------- Axiom
# SURFACE-VERIFIED. Notifiers are HELD (a notifier exists in order to send).
# No claims about query speed, data volume, retention, or completeness.
dict(
    slug="axiom", name="Axiom", section="9.18",
    tier="SURFACE-VERIFIED", panel="query", style="imperative",
    sub="Ask in Chat. Kestrel can query the dataset and bring the number "
        "back.",
    claims=["'Connect Axiom and Kestrel can query the dataset and bring "
            "the number back'",
            "'Ask what the error rate did overnight and Kestrel can look "
            "it up'",
            "RECORD: query datasets; metrics (query, list)"],
    beats=[
        dict(q="Pull the error rate overnight.",
             card="Reading Axiom",
             steps=[["find", "Checking Axiom connection"],
                    ["query", "Querying the dataset"]],
             panel=dict(title="0.42%", meta="error rate, 00:00 to 08:00", rows=[
                 ["Requests", "1,284,900", ""],
                 ["Errors", "5,397", ""],
                 ["Peak", "1.9% at 03:10", ""]])),
        dict(q="What was it the night before?",
             card="Reading Axiom",
             steps=[["query", "Querying the same window"]],
             panel=dict(title="0.11%", meta="error rate, previous night", rows=[
                 ["Requests", "1,190,440", ""],
                 ["Errors", "1,309", ""],
                 ["Change", "up 0.31 points overnight", ""]])),
    ],
),

# ---------------------------------------------------------------- Dropbox
# Differentiator: file revisions is a Dropbox-specific read in the schema.
dict(
    slug="dropbox", name="Dropbox", section="9.19", tier="PRODUCT-VERIFIED",
    panel="files", style="terse, keyword",
    sub="Ask in Chat. Kestrel can search your Dropbox and read what's in "
        "a file.",
    claims=["schema 1220584ccdcb: search files and folders",
            "schema 1220584ccdcb: read a file",
            "schema 1220584ccdcb: list file revisions"],
    beats=[
        dict(q="Where's the signed Northwind MSA?",
             card="Reading Dropbox",
             steps=[["find", "Checking Dropbox connection"],
                    ["file", "Searching files and folders"]],
             panel=dict(title="Results", meta="2 files", rows=[
                 ["pdf", "Northwind MSA signed.pdf", "/Contracts/2026", "1.2 MB"],
                 ["pdf", "Northwind MSA draft.pdf", "/Contracts/drafts", "1.1 MB"]])),
        dict(q="Has the signed one changed since February?",
             card="Reading Dropbox",
             steps=[["file", "Listing the file revisions"]],
             panel=dict(title="Northwind MSA signed.pdf",
                        meta="3 revisions", rows=[
                 ["rev", "Current", "12 Feb", "1.2 MB"],
                 ["rev", "Previous", "9 Feb", "1.2 MB"],
                 ["rev", "First", "9 Feb", "1.1 MB"]])),
    ],
),

# ---------------------------------------------------------------- PostHog
# PRE-STAGED 2026-08-25, NOT SHIPPED. Carries `pending`, so build.py leaves it
# out of the deployed bundle; it is still gated by gate.py on every run. Remove
# the `pending` key to ship, and nothing else.
#
# Stands on the DRAFT section 9.24 (output/posthog-section-DRAFT.md), which is
# SURFACE-VERIFIED off a committed eval-harness enumeration dated 2026-05-15 --
# 3.5 months stale. The mitigation for that staleness is visible here: all three
# beats use only DOUBLE-ATTESTED capabilities, i.e. tools returned by the
# registry pass AND named independently in the backend's own posthog-analytics
# skill reference (query-run, insight-query, experiment-results-get). Error
# tracking and logs are in the section but deliberately NOT demoed -- the skill
# guide names those categories without naming their tools.
#
# Panel is `query`, same renderer as Axiom: this is the analytics shape and the
# template stays as shipped. Varied against Axiom by exchange count (3, not 2)
# and by style. Every beat is a read. Feature-flag and experiment WRITES are
# HELD by 9.24 and appear nowhere.
dict(
    slug="posthog", name="PostHog", section="9.24",
    tier="SURFACE-VERIFIED", panel="query", style="conversational follow-up",
    # No replay label: the control was removed 2026-08-28 (nothing visible
    # around the demo). The word "replay" now appears nowhere on the page,
    # which satisfies claims doc 9.24's vocabulary ban by construction.
    sub="Ask in Chat. Kestrel can run the question against your product "
        "data and bring the answer back.",
    claims=["'Connect PostHog and ask what happened to signups last week'",
            "'Ask for the number and Kestrel queries PostHog for it'",
            "'Kestrel can pull up a saved insight and give you its "
            "current numbers'",
            "RECORD 9.24: query-run; insight-query; experiment-results-get "
            "(all three double-attested)"],
    beats=[
        dict(q="What happened to signups last week?",
             card="Reading PostHog",
             steps=[["find", "Checking PostHog connection"],
                    ["query", "Running the query"]],
             panel=dict(title="1,847", meta="signups, last 7 days", rows=[
                 ["Week before", "1,612", ""],
                 ["Change", "up 235", ""],
                 ["Best day", "Tuesday, 342", ""]])),
        # The query panel's title slot is an OVERSIZED FIGURE (6.6cqw), not a
        # heading -- Axiom's is "0.42%". A phrase there renders at display size
        # and pushes the rows off the stage. So every beat's headline is the
        # answer as a number, the meta names what it is, and the rows support it
        # without repeating it.
        dict(q="Which channel drove most of them?",
             card="Reading PostHog",
             steps=[["doc", "Opening the saved insight"]],
             panel=dict(title="742", meta="organic search, from the Signups "
                        "by source insight", rows=[
                 ["Direct", "531", ""],
                 ["Referral", "398", ""],
                 ["Paid", "176", ""]])),
        dict(q="And the pricing page experiment?",
             card="Reading PostHog",
             steps=[["query", "Reading the experiment results"]],
             panel=dict(title="5.3%", meta="variant B, pricing page test "
                        "over 14 days", rows=[
                 ["Control", "4.1% conversion", ""],
                 ["Lift", "up 1.2 points", ""],
                 ["Exposure", "18,402 users", ""]])),
    ],
),

# ---------------------------------------------------------------- Echo
# DROPPED 2026-08-20 on Nikhil's call: "a ping check isn't a demo." Section 9.23
# has exactly one tool, `ping`, and zero reads, so there is no result to put in a
# panel -- the honest version was a connection check, which is not a reason to
# buy anything. Nothing here is claims-blocked; the surface is just too thin to
# demo. If Echo ever gains read tools, write a real entry rather than reviving
# this one.
]

# Panel renderers, for the manifest's benefit.
PANEL_TYPES = {
    "issues":     "issue list, status ring + mono key + title + assignee",
    "checks":     "task list, checkbox circle + title + project/list chip",
    "mail":       "mail list, bold sender + subject + right-aligned day",
    "docs":       "document results, doc tile + title + grey snippet line",
    "events":     "event list, left time column + title + duration",
    "repos":      "pull request list, state glyph + mono number + title + branch",
    "query":      "query result, headline figure + supporting rows",
    "cms":        "CMS items, item name + field-coverage chip",
    "files":      "file list, type glyph + name + path + size",
    "recordings": "recording list, waveform glyph + title + duration",
    "board":      "board items, status pill + item name + owner",
    "ping":       "connection check, single status line, no result rows",
}
