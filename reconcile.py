#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

latest_events = {}

with open("payments.jsonl") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue

        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue

        txn_id = event.get("txn_id")
        if not txn_id:
            continue

        ts = event.get("ts", "")

        # Keep the latest attempt for this transaction.
        if txn_id not in latest_events or ts > latest_events[txn_id]["ts"]:
            latest_events[txn_id] = event

total = 0.0
count = 0

for event in latest_events.values():
    if event.get("status") == "success":
        # Amounts may contain commas, e.g. "55,707.77".
        amount = float(str(event["amount"]).replace(",", ""))
        total += amount
        count += 1

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")