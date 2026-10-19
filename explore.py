from src.preprocess import parse
from src.extract import extract_relations

doc = parse("Drought leads to crop failure. Crop failure causes prices to rise.")
for r in extract_relations(doc):
    print(f"{r.cause!r} -> {r.effect!r}   | {r.sentence}")