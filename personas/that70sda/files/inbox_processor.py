#!/usr/bin/env python3
"""that70sda@gmail.com inbox filing processor — runs 3x daily via cron.

Rules (Ravi-approved 2026-10-18):
- Platform notification noise -> label Persona/Notifications + archive.
- Engagement notifications (likes etc.) -> label Persona/Engagement + archive.
- Stocky drafts -> label Persona/Stocky, STAY in inbox (no separate watcher/alerts).
- Real-person mail needing a reply -> label Persona/Engagement, STAY in inbox, reported.
- Google security alerts + anything unrecognized -> untouched.
- Archive, never delete. Nothing is ever sent.

State: processed message IDs + sender log kept in state.json next to this script.
Output: prints only mail needing a reply; stays quiet otherwise.
"""
import json, os, subprocess, sys

ACCT = "461f6065cd9b4c90a0ee04289fc9d9f6"
BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state.json")
CLI = ["/opt/hatch/bin/hatch_gws_cli", "gmail", "--account", ACCT]

LABEL_NAMES = ["Persona/Stocky", "Persona/Engagement", "Persona/Notifications"]

# Platform senders whose mail is pure notification noise
NOTIFY_SENDERS = {
    "no-reply@substack.com",
    "that70sda@substack.com",
    "that70sda+podcast@substack.com",
}
NOTIFY_SUBJECT_PREFIXES = ("Shareable assets for:", "Stats for your post")
# Engagement pings (no reply needed)
ENGAGE_SENDERS = {"reaction@mg1.substack.com"}
ENGAGE_DOMAINS = ("x.com", "twitter.com", "spotify.com", "linkedin.com")


def gws(*args):
    r = subprocess.run(CLI + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        print(f"gws error: {' '.join(args)}\n{r.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(r.stdout) if r.stdout.strip() else {}
    except json.JSONDecodeError:
        return {"raw": r.stdout}


def label_ids():
    res = gws("users", "labels", "list", "--params", '{"userId":"me"}')
    ids = {}
    for lb in (res or {}).get("labels", []):
        if lb.get("name") in LABEL_NAMES:
            ids[lb["name"]] = lb["id"]
    return ids


def load_state():
    if os.path.exists(STATE):
        with open(STATE) as f:
            return json.load(f)
    return {"processed": [], "senders": {}}


def save_state(s):
    s["processed"] = s["processed"][-5000:]
    with open(STATE, "w") as f:
        json.dump(s, f)


def sender_addr(frm):
    # "Name <addr>" -> addr ; bare addr -> itself
    if "<" in frm:
        return frm.split("<")[-1].split(">")[0].strip().lower()
    return frm.strip().lower()


def classify(frm, subject):
    addr = sender_addr(frm)
    subj = subject or ""
    # Stocky drafts: heuristic until sender address is confirmed
    if "stocky" in addr or "stocky" in subj.lower() or \
       ("draft" in subj.lower() and addr not in NOTIFY_SENDERS):
        return "Persona/Stocky", False
    if addr in ENGAGE_SENDERS or any(d in addr for d in ENGAGE_DOMAINS):
        return "Persona/Engagement", True
    if addr in NOTIFY_SENDERS or subj.startswith(NOTIFY_SUBJECT_PREFIXES):
        return "Persona/Notifications", True
    # Google security alerts: leave alone
    if "accounts.google.com" in addr:
        return None, False
    # Real-person mail: needs a human look; report it
    if addr and not any(x in addr for x in ("no-reply", "noreply", "donotreply")):
        return "Persona/Engagement", "report"
    return None, False


def main():
    state = load_state()
    processed = set(state["processed"])
    ids = label_ids()
    missing = [n for n in LABEL_NAMES if n not in ids]
    if missing:
        print(f"missing labels: {missing}", file=sys.stderr)
        return 1

    res = gws("users", "messages", "list", "--params",
              '{"userId":"me","q":"in:inbox newer_than:3d","maxResults":100}')
    msgs = (res or {}).get("messages", [])
    needs_reply, filed = [], 0

    for m in msgs:
        mid = m["id"]
        if mid in processed:
            continue
        meta = gws("users", "messages", "get", "--params",
                   json.dumps({"userId": "me", "id": mid, "format": "metadata",
                               "metadataHeaders": ["From", "Subject", "Date"]}))
        headers = {h["name"].lower(): h["value"]
                   for h in (meta or {}).get("payload", {}).get("headers", [])}
        frm, subj = headers.get("from", ""), headers.get("subject", "")
        label, archive = classify(frm, subj)
        addr = sender_addr(frm)
        state["senders"][addr] = state["senders"].get(addr, 0) + 1

        if label:
            body = {"addLabelIds": [ids[label]]}
            if archive is True:
                body["removeLabelIds"] = ["INBOX"]
            gws("users", "messages", "modify", "--params",
                json.dumps({"userId": "me", "id": mid}), "--json", json.dumps(body))
            filed += 1
            if archive == "report":
                needs_reply.append((frm, subj, headers.get("date", "")))
        processed.add(mid)

    state["processed"] = list(processed)
    save_state(state)

    if needs_reply:
        print("Mail needing a reply:")
        for frm, subj, date in needs_reply:
            print(f"  - {date} | {frm} | {subj}")
    elif filed:
        print(f"Filed {filed} notification(s); nothing needs a reply.")
    # else: stay quiet
    return 0


if __name__ == "__main__":
    sys.exit(main())
