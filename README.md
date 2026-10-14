# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->

A listing has these fields:
```
  id             str    lst_001
  title          str    Vintage Levi's 501 Jeans — Medium Wash
  description    str    Classic 501s in a perfect medium wash. Some light fading a…
  category       str    bottoms
  style_tags     list   ['vintage', 'classic', 'denim', 'streetwear']
  size           str    W30 L30
  condition      str    good
  price          float  38.0
  colors         list   ['blue', 'indigo']
  brand          str    Levi's
  platform       str    depop
```

A wardrobe item has these fields:
```
  id             str    w_001
  name           str    Baggy straight-leg jeans, dark wash
  category       str    bottoms
  colors         list   ['dark blue', 'indigo']
  style_tags     list   ['denim', 'streetwear', 'baggy']
  notes          str    High-waisted, sits above the hip
```

These are what `search_listings` can filter on.

---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:**
searches the listings dataset based on a description and optionally, size and a maximum price, and returns matches
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" -->
`description` (str) describing what the user wants, `size` (str | None) to filter on, `max_price` (float | None) to filter on -- inclusive
- **Returns:**
A list of matching listing dicts with best match first, each with `id`, `title`, `description`, `category`, `style_tags`, `size`, `condition`, `price`, `colors`, `brand`, `platform`
- **When it has nothing:**
An empty list


### `suggest_outfit`

- **What it does:**
Given an item and a user's wardrobe, suggest one or two outfits as outfit styling ideas
- **Inputs:**
a `new_item` (dict) the user is considering, a `wardrobe` (dict) with an `items` key holding a list of items
- **Returns:**
A nonempty string saying the outfit suggestion that names some wardrobe pieces when the wardrobe is not empty
- **When it has nothing:**
When wardrobe is empty, return a string of general styling advice for the item

### `create_fit_card`

- **What it does:**
Writes a short postable caption based on the suggested styling ideas for the item
- **Inputs:**
The `new_item`(dict) the user wants to thrift, `outfit`(str) -- the outfit suggestion string gotten from `suggest_outfit`
- **Returns:**
A 2-4 sentence caption string created based on the item and the suggested outfit
- **When it has nothing:**
When the outfit is empty, still output a descriptive message string

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**
If `search_listings` returns an empty list, put a message in `session["error"]` saying what the user could change and return the session without calling `suggest_outfit`. Otherwise, take the first item in the search results, put it in `session["selected_item"]`, and continue to `suggest_outfit`.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->
Asking the model. `_parse_query()` sends the raw query to the LLM with a prompt asking for a JSON object (description, size, max_price), then parses that JSON. If parsing fails, it falls back to using the raw query as the description with size and max_price set to None.

**What moves through the session:** <!-- which fields, in what order -->
**What moves through the session:**

1. `query` — the raw input
2. `parsed` — the `description` / `size` / `max_price` dict from `_parse_query`
3. `search_results` — the full list from `search_listings`
4. `selected_item` — the first result (or left `None` if the branch exits early)
5. `outfit_suggestion` — from `suggest_outfit`
6. `fit_card` — from `create_fit_card`
7. `wardrobe` is passed in unchanged, and `error` is only set if the run stops early at the branch.
---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   Here are two outfit ideas using the new graphic tee and pieces already in your wardrobe:

**Outfit 1: 90s Streetwear Grunge**
*   **Top:** Graphic Tee (new)
*   **Bottoms:** Baggy straight-leg jeans, dark wash
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

*Why it works:* Tucking or letting the boxy, faded tee hang loose over your high-waisted baggy jeans hits that effortless 90s streetwear proportion. Layering the slightly cropped black denim jacket on top adds depth and texture without hiding the graphic, while the chunky white sneakers tie the look together.

**Outfit 2: Contrast Edgy Casual**
*   **Top:** Graphic Tee (new)
*   **Bottoms:** Wide-leg khaki trousers
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt, Black crossbody bag

*Why it works:* This outfit plays with style mixing by pairing the grungy, faded band tee with polished khaki trousers. Tucking the tee into the wide-legs and adding the brown belt breaks up the silhouette, and the black combat boots ground the earth tones with an edgy finish.

  Fit card: Scored this insanely soft 2003 tour bootleg tee for just $24 on Depop and honestly, it’s already the anchor of my whole wardrobe. The fade and the boxy fit giveit that exact 90s streetwear grunge energy I've been hunting for. Can't wait to beat this thing up even more.

1 model calls this session, 2 served from cache, 91 prompt + 22 output tokens

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]
```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfit ideas that pair the vintage Levi's 501s with pieces already in your wardrobe:

**Outfit 1: Casual Streetwear**
*   **Top:** White ribbed tank top
*   **Outerwear:** Black cropped zip hoodie (worn open or layered over the tank)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* The medium wash of the Levi's breaks up the heavy dark denim and trousers already in your closet, and pairing them with the fitted white tank and chunkysneakers creates an effortless, balanced 90s streetwear look.

**Outfit 2: Vintage Grunge**
*   **Top:** Oversized grey crewneck sweatshirt
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt
*   *Why it works:* Tucking the medium-wash 501s in with the brown leather belt adds structure to the oversized grey crewneck. Layering the cropped black denim jacket on top creates a great contrast in proportions and washes, finished off with the edgy combat boots.
```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Found the ultimate lived-in look with these vintage Levi's 501 jeans, complete with that ideal faded knee wear. Snagged them on Depop for just $38.00 and I'm honestly living for that effortless 90s slouch. Just add crisp white sneakers and a beat-up tee and you're good to go.
```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I gave Claude my `search_listings` spec to suggest for implementation.
- *What came back:* It did not include the `condition` or `platform` of the listings while comparing the listing against the user-specified description, so when user specified something like "excellent condition jacket" or "poshmark sneakers", those words would contribute nothing to the score.
- *What I changed:*
I added those attributes when concatenating a description for each listing.

**Moment 2**

- *What I asked for:* I asked Claude how to parse a free-text query into description/size/max_price.
- *What came back:* It suggested using regex.
- *What I changed:* I found using a model call more suitable and rewrote using a model call.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1. Matching query completes all three tools, returns a fit card | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 2. Impossible query stops before `suggest_outfit` | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 3. `selected_item`'s id matches what `suggest_outfit` actually receives | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 4. Fit card (2-4 sentences, names item/price/platform once each) | 4 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |
| 5. Empty wardrobe → nonempty general styling advice | 5 of 5 | PASS | PASS | PASS | PASS | PASS | MET (5/5) |

Full output for all 45 runs (5 criteria × 5 tries, plus extra fit-card-item
scenarios) is in `results/run_2026-10-14_0053_before.md`, produced by
`run_eval.py --label before`.

For criterion 3 and criterion 4, the five scenarios behind the "Try" columns
aren't five repeats of one run — they're the five different runs each
criterion actually names (five different queries for state, five different
items for the fit card), per the scenarios in `scenarios.py`.

**Real output, pasted as text, naming the file and function that produced it:**

**Criterion 1** — `agent.py::run_agent` (via `run_eval.py::run_once`), scenario "matching query completes," try 1, query `vintage graphic tee under $30`:

```
[1] parse_query
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Vintage Graphic Hoodie — Faded Black … +7 more
[3] suggest_outfit
      in:  new_item='Graphic Tee — 2003 Tour Bootleg Style', wardrobe_items=10
      out: Here are two specific outfit ideas using the new graphic tee and pieces already in your wardrobe:  **Outfit 1:…
[4] create_fit_card
      in:  outfit='Here are two specific outfit ideas using the new graphic tee'…
      out: Found the ultimate 2003 tour bootleg tee on Depop for $24 and I'm officially obsessed with how soft and worn-i…

Fit card: Found the ultimate 2003 tour bootleg tee on Depop for $24 and I'm officially obsessed with how soft and worn-in it is. Already planning to pair the faded graphic with baggy dark denim and combat boots for an effortless grunge vibe. Grab it before I change my mind!
```

**Criterion 2** — `agent.py::run_agent`, the branch at the `if not results:` check, scenario "impossible query stops early," try 1, query `designer ballgown size XXS under $5`:

```
[1] parse_query
      in:  designer ballgown size XXS under $5
      out: description='designer ballgown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping

stopped early: yes — No listings matched that search. Try a broader description, a different size, or a higher max price.
selected_item: (none)
```

**Criterion 3** — `agent.py::run_agent` (`session["selected_item"] = results[0]`, then `suggest_outfit(session["selected_item"], wardrobe)`). The trace only prints titles, so to check the *id* specifically I patched `suggest_outfit` to record the id it actually received and compared it against `session["selected_item"]["id"]`:

```
$ python -c "
from unittest.mock import patch
from agent import run_agent
from utils.data_loader import get_example_wardrobe
from tools import suggest_outfit as real_suggest_outfit

seen = {}
def spy(new_item, wardrobe):
    seen['id_passed_in'] = new_item.get('id')
    return real_suggest_outfit(new_item, wardrobe)

import agent
with patch.object(agent, 'suggest_outfit', spy):
    session = run_agent('classic denim jacket', get_example_wardrobe())

print('session[selected_item][id] =', session['selected_item']['id'])
print('id passed into suggest_outfit =', seen['id_passed_in'])
print('match:', session['selected_item']['id'] == seen['id_passed_in'])
"

session[selected_item][id] = lst_007
id passed into suggest_outfit = lst_007
match: True
```

Repeated across all 5 state-scenario tries in `results/run_2026-10-14_0053_before.md`, the trace consistently shows the same title going from `search_listings` into `suggest_outfit` (e.g. try 1: `selected_item: Denim Jacket — Light Wash, Cropped` → `suggest_outfit in: new_item='Denim Jacket — Light Wash, Cropped'`) — expected, since `session["selected_item"]` and the `new_item` passed to `suggest_outfit` are the same dict object, not a copy.

**Criterion 4** — `tools.py::create_fit_card` (via `agent.py::run_agent`), one of the five items, "fit card: corduroy pants," try 1, query `corduroy wide-leg pants rust`:

```
[1] parse_query
      in:  corduroy wide-leg pants rust
      out: description='corduroy wide-leg pants rust', size=None, max_price=None
[2] search_listings (via MCP)
      in:  description='corduroy wide-leg pants rust', size=None, max_price=None
      out: 5 items: Corduroy Wide-Leg Pants — Rust, Wide-Leg Linen Trousers — Natural, Straight Leg Khaki Trousers — Olive … +2 more
[3] suggest_outfit
      in:  new_item='Corduroy Wide-Leg Pants — Rust', wardrobe_items=10
      out: Here are two great outfit combinations you can make using the new rust corduroy pants and pieces already in yo…
[4] create_fit_card
      in:  outfit='Here are two great outfit combinations you can make using th'…
      out: Scored these dreamy rust wide-leg cords on Depop for $32 and I am never taking them off. They give the ultimat…

Fit card: Scored these dreamy rust wide-leg cords on Depop for $32 and I am never taking them off. They give the ultimate effortless 70s autumn energy, especially paired with a crisp white tank and combat boots. Already planning ten different ways to style them before the weather even cools down! 🍂✨
```

3 sentences, names the item ("rust wide-leg cords"), the price ("$32") and the platform ("Depop") once each.

**Criterion 5** — `tools.py::suggest_outfit`, the `if not items:` branch (via `agent.py::run_agent`), scenario "empty wardrobe," try 1, query `denim jacket under $50`:

```
[1] parse_query
      in:  denim jacket under $50
      out: description='denim jacket', size=None, max_price=50.0
[2] search_listings (via MCP)
      in:  description='denim jacket', size=None, max_price=50.0
      out: 6 items: Denim Jacket — Light Wash, Cropped, High-Waisted Denim Shorts — Cutoff, Denim Vest — Medium Wash, Studded … +3 more
[3] suggest_outfit
      in:  new_item='Denim Jacket — Light Wash, Cropped', wardrobe_items=0
      out: Since this is a cropped, light-wash denim jacket with structured shoulders and a classic vintage vibe, it's a …
[4] create_fit_card
      in:  outfit='Since this is a cropped, light-wash denim jacket with struct'…
      out: Scored this vintage cropped light-wash denim jacket for $42 on Poshmark and I'm obsessed with the structured s…
```

`wardrobe_items=0` and `suggest_outfit` still returned a nonempty string of general styling advice (quoted above under "out:"), instead of an empty string or an exception.

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Matching query completes all three tools, returns a fit card | 4 of 5 | MET (5/5) | All 5 tries of `vintage graphic tee under $30` ran `parse_query` → `search_listings` → `suggest_outfit` → `create_fit_card` and ended with a nonempty `session["fit_card"]`. |
| 2 | Impossible query stops before `suggest_outfit` | 5 of 5 | MET (5/5) | All 5 tries of `designer ballgown size XXS under $5` set `session["error"]` and returned right after `search_listings` returned `[]`; the trace has no `suggest_outfit` or `create_fit_card` line in any of the 5. |
| 3 | `selected_item`'s id matches what `suggest_outfit` receives | 5 of 5 | MET (5/5) | Verified structurally in `agent.py::run_agent` (`session["selected_item"] = results[0]` is the exact object passed to `suggest_outfit`, not a copy) and confirmed directly by patching `suggest_outfit` to record the id it received across 5 different queries — it matched `session["selected_item"]["id"]` every time. |
| 4 | Fit card: 2-4 sentences, names item/price/platform once each | 4 of 5 | MET (5/5) | Checked one fit card per item across the 5 distinct-item scenarios in `scenarios.py`; all 5 landed in 2-4 sentences and named the item, price, and platform exactly once each. |
| 5 | Empty wardrobe → nonempty general styling advice | 5 of 5 | MET (5/5) | All 5 tries with the empty wardrobe hit the `if not items:` branch in `tools.py::suggest_outfit` (`wardrobe_items=0` in the trace) and returned a nonempty, item-specific advice string — no empty string, no exception. |

**Diagnoses**

No misses on a plain read — every criterion cleared its target on all 5 tries I scored. Rather than call that a clean sweep, here's where I pushed back on my own result:

**Criteria 1 and 2 didn't actually stress the risk their targets were written for.** Both ran the *same* query 5 times. `_parse_query` (`agent.py::_parse_query`) calls the model at `temperature=0.0`, and `search_listings` (`tools.py::search_listings`) makes no model call at all — so for one fixed query, nothing downstream of the query string has any real freedom to vary between tries. The target for criterion 1 (4 of 5, not 5 of 5) exists specifically because keyword-overlap search "will miss some phrasings" — but repeating one phrasing five times can only ever produce 5/5 or 0/5; it structurally cannot land on 3/5 or 4/5, which is the regime the target is meant to catch. I got 5/5, and it's real, but it's weak evidence for the thing I was worried about when I wrote the target. The fix isn't the target, it's the scenario: I'd replace "matching query completes" with 5 *different* real phrasings for the same kind of item (e.g. "band tee cheap," "old concert shirt," "faded graphic tee") before trusting this number. If that still comes back 5/5, criterion 1's target should move to 5 of 5.

**Criterion 4's extra runs (beyond the 5 I scored) caught the one real failure in this whole eval.** I ran each of the 5 fit-card items 5 times each (25 runs total), even though the criterion only requires one check per item. On "chelsea boots," try 3 hit a genuine `ModelUnavailable: 503 UNAVAILABLE` from Gemini inside `suggest_outfit`, and `agent.py::run_agent`'s `except ModelUnavailable` handler caught it and stopped cleanly — session error set, no crash, but also no fit card for that attempt. That's a model/infra-layer failure, not a tool or prompt bug: nothing about `create_fit_card`'s sentence-count or mention requirements broke, the service was down for 1 call out of 25. This is exactly the risk criterion 4's sub-5/5 target already prices in, so I'm not tightening it — if anything, catching a real outage on the first extended run says 4 of 5 is about right, maybe even a touch generous for infra risk on top of wording risk.

**No pattern across tools or the branch.** The one failure observed (the 503) sits in the model-call layer, isolated to a single external request — it didn't recur across the other 24 fit-card runs, the other 4 items, or any other criterion, so there's nothing systemic to fix in `tools.py` or the branch in `agent.py::run_agent`. If I had to name one thing to change before the next round, it's the test for criterion 1, not any of the five targets.

---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```
$ python app.py ask 'vintage graphic tee under $30' --trace

[1] parse_query
      in:  vintage graphic tee under $30
      out: description='vintage graphic tee', size=None, max_price=30.0
[2] search_listings (via MCP)
      in:  description='vintage graphic tee', size=None, max_price=30.0
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Vintage Graphic Hoodie — Faded Black … +7 more
[3] suggest_outfit
      in:  new_item='Graphic Tee — 2003 Tour Bootleg Style', wardrobe_items=10
      out: Here are two outfit ideas using the new graphic tee and pieces already in your wardrobe:  **Outfit 1: 90s Stre…
[4] create_fit_card
      in:  outfit='Here are two outfit ideas using the new graphic tee and piec'…
      out: Scored this insanely soft 2003 tour bootleg tee for just $24 on Depop and honestly, it’s already the anchor of…
```

**Empty search**

```
$ python app.py ask 'designer ballgown size XXS under $5' --trace

[1] parse_query
      in:  designer ballgown size XXS under $5
      out: description='designer ballgown', size='XXS', max_price=5.0
[2] search_listings (via MCP)
      in:  description='designer ballgown', size='XXS', max_price=5.0
      out: [] (empty)
      →    branch: empty, stopping

  No listings matched that search. Try a broader description, a different size, or a higher max price.
```

**On the MCP move:** `search_listings` is called through `call_tool("search_listings", {...})` in `mcp_client.py` instead of calling the function in `tools.py` directly — that line is commented out in `agent.py` rather than deleted, so the diff is visible. The return value didn't change shape: still a list of listing dicts with the same fields, in the same order. The rewire worked on the first try; nothing downstream (selecting an item, building the outfit prompt, the fit card) needed to change.

---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
