"""Add Georgian ("ka") to a client JSON using an en->ka table.
Usage: python3 merge_ka.py clients/babua-marani.json babua-marani.ka.json
Every {"en": ...} value whose English text is in the table gets a "ka" key.
English texts not in the table are listed, so nothing is translated silently."""
import json, sys
path, table_path = sys.argv[1], sys.argv[2]
d = json.load(open(path, encoding="utf-8")); table = json.load(open(table_path, encoding="utf-8"))
missing = []
def walk(x):
    if isinstance(x, dict):
        if isinstance(x.get("en"), str):
            if x["en"] in table: x["ka"] = table[x["en"]]
            else: missing.append(x["en"])
        else:
            for v in x.values(): walk(v)
    elif isinstance(x, list):
        for v in x: walk(v)
walk(d)
if "ka" not in d.get("languages", []): d.setdefault("languages", ["en"]).append("ka")
json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("missing:", *missing, sep="\n  ") if missing else print("all texts have Georgian")
