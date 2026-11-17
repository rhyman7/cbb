#!/usr/bin/env python3
"""Sanity checks on data/data.json before it is published. Exits non-zero on a failure."""
import json
import sys

d = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "data/data.json"))
fail = []
teams = d["teams"]
if not 340 <= len(teams) <= 380:
    fail.append(f"{len(teams)} teams, expected about 365 Division I teams")
for a, t in teams.items():
    if not t.get("players"):
        fail.append(f"{a}: no players")
    if not t["games"]:
        continue
    o, df = t["offense"], t["defense"]
    # one or two lopsided games can sit far out early in the season
    if o["ppg"] is not None and not (35 <= o["ppg"] <= 130 and 35 <= df["papg"] <= 130):
        fail.append(f"{a}: points per game out of range ({o['ppg']}, {df['papg']})")
    if o["adjOrtg"] is not None and not (70 <= o["adjOrtg"] <= 145 and 70 <= df["adjDrtg"] <= 145):
        fail.append(f"{a}: adjusted ratings out of range")
    if t["pace"] is not None and not (50 <= t["pace"] <= 95):
        fail.append(f"{a}: pace {t['pace']} out of range")
    for r in t["players"]:
        if r["log"] not in d["gameLogs"]:
            fail.append(f"{a}: {r['player']} has no game log")
w = sum(int(t["record"]["d1"].split("-")[0]) for t in teams.values())
l = sum(int(t["record"]["d1"].split("-")[1]) for t in teams.values())
if w != l or w != d["gamesCounted"]:
    fail.append(f"Division I wins {w}, losses {l}, games {d['gamesCounted']} don't agree")
if len(d["conferences"]) < 28:
    fail.append(f"only {len(d['conferences'])} conferences")
slate = [g for g in d["games"] if g["date"] == d["slateDate"]]
if not slate:
    fail.append("no games on the slate date")
for g in d["games"]:
    if g["away"] not in teams or g["home"] not in teams:
        fail.append(f"game {g['id']}: unknown team")
if fail:
    print("\n".join("FAIL: " + f for f in fail[:40]))
    sys.exit(1)
print(f"ok: {len(teams)} teams, {d['gamesCounted']} Division I games through {d['throughDate']}, "
      f"slate {d['slateDate']} with {len(slate)} games")
