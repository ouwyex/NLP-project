from dataclasses import dataclass

CAUSE_VERBS = {"cause", "lead", "trigger", "produce", "bring", "result"}
SKIP_DEPS = {"det", "aux", "case", "punct"}

@dataclass
class Relation:
    cause: str
    effect: str
    sentence: str

def phrase(tokens) -> str:
    """Склеивает токены в нормализованную фразу (леммы, нижний регистр)."""
    toks = sorted(tokens, key=lambda t: t.i)
    return " ".join(t.lemma_.lower() for t in toks
                    if t.dep_ not in SKIP_DEPS and not t.is_punct)

def extract_relations(doc) -> list[Relation]:
    relations = []
    for sent in doc.sents:
        for tok in sent:
            if tok.pos_ != "VERB" or tok.lemma_ not in CAUSE_VERBS:
                continue
            subj = [c for c in tok.children if c.dep_ == "nsubj"]
            if not subj:
                continue
            effect_tokens = []
            for c in tok.children:
                if c.dep_ in ("dobj", "xcomp", "ccomp"):
                    effect_tokens += list(c.subtree)
                elif c.dep_ == "prep" and c.text in ("to", "in"):
                    effect_tokens += [t for t in c.subtree if t.dep_ != "prep"]
            if effect_tokens:
                relations.append(Relation(
                    cause=phrase(subj[0].subtree),
                    effect=phrase(set(effect_tokens)),
                    sentence=sent.text.strip(),
                ))
    return relations