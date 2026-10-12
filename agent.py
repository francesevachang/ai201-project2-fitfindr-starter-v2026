"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import json
import re

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import generate, ModelUnavailable
from mcp_client import call_tool


# ── query parsing ────────────────────────────────────────────────────────────

_FENCE_RE = re.compile(r"^```(?:json)?\s*|\s*```$")


def _parse_query(query: str) -> tuple[str, str | None, float | None]:
    """
    Ask the model to pull a description, a size, and a max_price out of a
    plain-language query.
    """
    prompt = (
        "Extract a search description, a size, and a maximum price from this "
        "thrifting query. Respond with ONLY a JSON object — no other text, no "
        "markdown fences — in exactly this shape:\n"
        '{"description": "<keywords describing the item, with any size or '
        'price removed>", "size": "<size string, or null if none>", '
        '"max_price": <number, or null if none>}\n\n'
        f"Query: {query}"
    )
    response = generate(prompt, temperature=0.0)

    try:
        parsed = json.loads(_FENCE_RE.sub("", response.strip()))
    except json.JSONDecodeError:
        return query, None, None

    description = parsed.get("description") or query
    size = parsed.get("size") or None

    max_price = parsed.get("max_price")
    try:
        max_price = float(max_price) if max_price is not None else None
    except (TypeError, ValueError):
        max_price = None

    return description, size, max_price


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)

    count = 1
    trace.check_iterations(count)

    description, size, max_price = _parse_query(query)
    session["parsed"] = {
        "description": description,
        "size": size,
        "max_price": max_price,
    }

    # results = search_listings(description, size=size, max_price=max_price)
    results = call_tool("search_listings", {
        "description": description,
        "size": size,
        "max_price": max_price,
    })
    session["search_results"] = results

    if not results:
        session["error"] = (
            "No listings matched that search. Try a broader description, a "
            "different size, or a higher max price."
        )
        return session

    session["selected_item"] = results[0]

    session["outfit_suggestion"] = suggest_outfit(session["selected_item"], wardrobe)

    session["fit_card"] = create_fit_card(session["outfit_suggestion"], session["selected_item"])

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
