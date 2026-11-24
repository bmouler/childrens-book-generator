"""Deterministic EN+RU story compiler (spike). No LLM and no sampling.

A story is a list of clauses that reference lexicon ids (lexicon.py). Both languages are rendered
from the same clause, so the translation is a pure function of the story and the word alignment
exists by construction: every highlighted pair is two surface forms that came from one lexicon entry.

Clause forms: subject + verb (+ object, indirect object, preposition phrase, adverb), a predicate
adjective ("The ice is cold."), the questions "Will X V1 or V2?", "Is X A1 or A2?" and "Where is X?",
a command ("Touch the ice!") and fixed phrases.

Russian forms come from pymorphy3 dictionary lookup, never from its guesser. The compiler stops
(LexiconError) when
  - a word is not in the lexicon, or pymorphy3 only knows it by guessing (is_known = False),
  - the dictionary has no form for the slot (e.g. a perfective verb in the present tense),
  - the dictionary has SEVERAL valid forms for the slot and the curator has not chosen one
    (OVERRIDES). Example: the plural of лист is both листы (sheets) and листья (leaves),
  - a mass noun has no explicit article, or a verb has no lemma for the tense the clause needs.
"""
from __future__ import annotations

import hashlib
import json

import pymorphy3

from lexicon import ADJS, ADVS, CHROME, COMPS, CONN, NAMES, NOUNS, OVERRIDES, PHRASES, PREP_DIR, PREPS, PRONOUNS, VERBS

_morph = pymorphy3.MorphAnalyzer()


class LexiconError(ValueError):
    pass



# --------------------------------------------------------------------------------------------
# Morphology helpers
# --------------------------------------------------------------------------------------------
_SKIP = {"Arch", "Abbr", "Supr", "Infr", "Slng", "Erro", "Dist", "Cmp2"}  # never a default choice


def _core(tag) -> bool:
    g = set(tag.grammemes)
    return not (g & _SKIP) and not any(x.startswith("V-") for x in g)


def _lookup(table: dict, key: str, kind: str):
    if key not in table:
        raise LexiconError(f"{kind} {key!r} is not in the lexicon")
    return table[key]


def _lemma(v: dict, key: str, vid: str):
    """The Russian lemma the curator chose for this use of a verb. A missing key is refused."""
    if key not in v:
        raise LexiconError(f"verb {vid!r} has no {key} lemma in the lexicon")
    return v[key]


def check_lexicon() -> None:
    """A concept id names a pill colour and a sticker, so no id may sit in two tables."""
    owner: dict[str, str] = {}
    for name, table in (("NAMES", NAMES), ("NOUNS", NOUNS), ("ADJS", ADJS), ("ADVS", ADVS), ("PREPS", PREPS),
                        ("PRONOUNS", PRONOUNS), ("PHRASES", PHRASES), ("VERBS", VERBS), ("CONN", CONN)):
        for k in table:
            if k in owner:
                raise LexiconError(f"concept id {k!r} is in both {owner[k]} and {name}")
            owner[k] = name


check_lexicon()

def card_text(p: dict) -> tuple[str, str]:
    """The teaching-card face of a highlighted pair: the citation forms from the lexicon.

    A card teaches the word, so it shows the dictionary form: nominative singular for a noun or
    a name, nominative masculine singular for an adjective ("fox / лиса", never "лису" from an
    accusative sentence). Verb, adverb, preposition, pronoun and phrase cards show the sentence
    forms, because those forms already match across the two languages ("fell / упала")."""
    c = p["concept"]
    if c in NOUNS:
        return NOUNS[c][0], NOUNS[c][1]
    if c in NAMES:
        return NAMES[c]
    if c in ADJS:
        return ADJS[c][0], ADJS[c][1]
    return p["en"], p["ru"]


def _parse(lemma: str, pos: str):
    # is_known=False means pymorphy3 is GUESSING the word from its suffix: never accept that.
    hits = [p for p in _morph.parse(lemma)
            if p.is_known and p.tag.POS == pos and p.normal_form == lemma]
    if not hits:
        raise LexiconError(f"Russian {pos} {lemma!r} is not a known dictionary lemma (check spelling, ё)")
    if len(hits) > 1 and pos == "INFN":
        # считать/уходить: one imperfective lemma, one perfective. Present-tense forms live only
        # on the imperfective, and every future-tense lemma in the lexicon is its own word
        # (утонуть, угадать), so the imperfective is the reading the engine wants.
        impf = [p for p in hits if "impf" in p.tag.grammemes]
        if len(impf) == 1:
            return impf[0]
    return hits[0]  # noun and adjective homonyms (animacy, name readings): _form still refuses
                    # a slot with two different spellings, so a wrong reading cannot slip through


def _form(parse, grams: set, label: str) -> str:
    """The single dictionary form for this slot. Refuses to pick between valid alternatives."""
    want = frozenset(grams)
    hits = [f for f in parse.lexeme if want <= set(f.tag.grammemes)]
    override = OVERRIDES.get((parse.normal_form, want))
    if override is not None:
        if override not in {f.word for f in hits}:
            raise LexiconError(f"{parse.normal_form}: override {override!r} is not a dictionary form "
                               f"for {sorted(want)} ({label})")
        return override
    words = sorted({f.word for f in hits if _core(f.tag)})
    if not words:
        raise LexiconError(f"{parse.normal_form}: no form {sorted(want)} ({label})")
    if len(words) > 1:
        raise LexiconError(f"{parse.normal_form}: several valid forms {words} for {sorted(want)} "
                           f"({label}). The curator must choose one in OVERRIDES")
    return words[0]


class Ctx:
    """Per-clause state: pair table, discourse memory, and the forms used (for the review audit).
    `base` is the number of pairs already on the page, so pair ids are unique within a page."""

    def __init__(self, tense: str, seen: set, audit: set, base: int = 0):
        self.tense, self.seen, self.audit, self.base = tense, seen, audit, base
        self.pairs: list[dict] = []

    def pair(self, concept: str, en: str, ru: str) -> int:
        pid = self.base + len(self.pairs)
        self.pairs.append({"id": pid, "concept": concept, "en": en, "ru": ru})
        return pid


def _seg(t: str, pair=None, sp=True) -> dict:
    return {"t": t, "pair": pair, "sp": sp}


_PUNCT = {".", "!", "?", ",", ":"}


# --------------------------------------------------------------------------------------------
# Noun phrases, verbs, clauses
# --------------------------------------------------------------------------------------------
def _pron(pid: str, case: str, ctx: Ctx):
    en_t, ru_t, person, number, *rest = _lookup(PRONOUNS, pid, "pronoun")
    if case != "nomn":
        raise LexiconError(f"pronoun {pid!r}: only the nominative is in the lexicon")
    pair = ctx.pair(pid, en_t, ru_t)
    ctx.audit.add((pid, "pronoun", ru_t))
    gender = rest[0] if rest else None  # кто and никто agree as masculine singular
    return [_seg(en_t, pair)], [_seg(ru_t, pair)], {"gender": gender, "person": person, "number": number}


def _adj_form(a: str, case: str, plural: bool, gender, anim, ctx: Ctx):
    """One adjective as (EN seg, RU seg). The Russian form agrees with its noun in case, number, gender."""
    en_a, ru_a, _hue = _lookup(ADJS, a, "adjective")
    g = {case, "plur"} if plural else {case, gender, "sing"}
    if case == "accs" and (plural or gender == "masc"):
        g.add(anim)  # animate accusative = genitive form
    form = _form(_parse(ru_a, "ADJF"), g, f"adjective {a} in {case}")
    pid = ctx.pair(a, en_a, form)
    ctx.audit.add((a, f"{case}/plur" if plural else f"{case}/{gender}", form))
    return _seg(en_a, pid), _seg(form, pid)


def _np(spec, case: str, ctx: Ctx):
    """Noun phrase -> (EN segs, RU segs, features for verb agreement)."""
    spec = {"n": spec} if isinstance(spec, str) else spec
    if "pron" in spec:
        return _pron(spec["pron"], case, ctx)
    nid, adjs = spec["n"], spec.get("adj", [])
    plural = spec.get("num") == "pl"
    is_name = nid in NAMES
    en_sg, ru_noun, *rest = _lookup(NAMES if is_name else NOUNS, nid, "noun")
    if plural:
        if is_name or not rest or rest[0] is None:
            raise LexiconError(f"noun {nid!r} has no plural in the lexicon")
        en_noun = rest[0]
    else:
        en_noun = en_sg
    p = _parse(ru_noun, "NOUN")
    gender, anim = p.tag.gender, p.tag.animacy
    num = "plur" if plural else "sing"
    en, ru = [], []
    art = spec.get("art")
    if art is None:
        if is_name or plural:
            art = ""
        elif rest and rest[0] is None:
            raise LexiconError(f"noun {nid!r} has no plural, so it is a mass or unique noun: "
                               f"the story must say art 'the' or ''")
        else:
            first = _lookup(ADJS, adjs[0], "adjective")[0] if adjs else en_noun
            art = "the" if nid in ctx.seen else ("an" if first[0] in "aeiou" else "a")
    if art:
        en.append(_seg(art))
    for a in adjs:
        e, r = _adj_form(a, case, plural, gender, anim, ctx)
        en.append(e)
        ru.append(r)
    grams = {case, num}
    if is_name and case == "accs" and anim == "inan" and (gender == "masc" or plural):
        # a character is a "someone", not a thing: the animate accusative is the genitive form
        grams = {"gent", num}
    form = _form(p, grams, f"noun {nid}")
    if is_name:
        form = form[0].upper() + form[1:]
    pid = ctx.pair(nid, en_noun, form)
    en.append(_seg(en_noun, pid))
    ru.append(_seg(form, pid))
    ctx.audit.add((nid, f"{case}/{num}", form))
    ctx.seen.add(nid)
    return en, ru, {"gender": gender, "person": 3, "number": num}


def _agree(subjects: list):
    person = min(s["person"] for s in subjects)  # 1 beats 2 beats 3
    plural = len(subjects) > 1 or any(s["number"] == "plur" for s in subjects)
    return person, plural


def _verb(vid: str, subjects: list, ctx: Ctx):
    v = _lookup(VERBS, vid, "verb")
    person, plural = _agree(subjects)
    if v.get("third_only") and person != 3:
        raise LexiconError(f"verb {vid!r} is only in the lexicon for third-person subjects")
    num = "plur" if plural else "sing"
    third_sg = person == 3 and not plural
    tense = ctx.tense
    if tense == "pres":
        en_text = v["en"]["pres_sg" if third_sg else "pres_pl"]
        lemma, grams = _lemma(v, "ru_pres", vid), {"VERB", "pres", f"{person}per", num}
    elif tense == "past":
        en_text = v["en"]["past_pl" if plural else "past_sg"]
        lemma = _lemma(v, "ru_past", vid)
        if plural:
            grams = {"VERB", "past", "plur"}
        else:
            if subjects[0]["gender"] is None:
                raise LexiconError(f"verb {vid!r}: Russian past tense needs a subject with a known gender")
            grams = {"VERB", "past", subjects[0]["gender"], "sing"}
    elif tense == "futr":
        en_text = v["en"]["pres_pl"]
        lemma = v.get("ru_futr")
        if lemma is None:
            raise LexiconError(f"verb {vid!r} has no future-tense lemma in the lexicon")
        grams = {"VERB", "futr", f"{person}per", num}
    else:
        raise LexiconError(f"unknown tense {tense!r}")
    lead = [_seg("will")] if tense == "futr" else []
    if lemma is None:  # null copula
        return lead + [_seg(w) for w in en_text.split()], [], v
    form = _form(_parse(lemma, "INFN"), grams, f"verb {vid} {tense}")
    pid = ctx.pair(vid, en_text, form)
    ctx.audit.add((vid, "+".join(sorted(grams)), form))
    return lead + [_seg(w, pid) for w in en_text.split()], [_seg(form, pid)], v


def _phrase(phrase_id: str, ctx: Ctx):
    ph = _lookup(PHRASES, phrase_id, "phrase")
    ids: dict[str, int] = {}

    want = {c for _, c in ph["en"]} ^ {c for _, c in ph["ru"]}  # concepts on one side only
    if want - {None}:
        raise LexiconError(f"phrase {phrase_id!r}: concepts {sorted(want - {None})} are not aligned "
                           "on both sides")

    def build(side: str) -> list:
        out = []
        glue = False  # a hyphen glues both sides: Тянут-потянут
        for text, concept in ph[side]:
            pair = None
            if concept is not None:
                if concept not in ids:
                    en_t = next(t for t, c in ph["en"] if c == concept)
                    ru_t = next(t for t, c in ph["ru"] if c == concept)
                    ids[concept] = ctx.pair(concept, en_t, ru_t)
                pair = ids[concept]
            sp = text not in _PUNCT and text != "-" and not glue
            glue = text == "-"
            out.append(_seg(text, pair, sp=sp))
        return out

    en, ru = build("en"), build("ru")
    ctx.audit.add((phrase_id, "fixed phrase", text_of(ru)))
    return en, ru


def _q_or(spec: dict, ctx: Ctx):
    """Will X V1 or V2?  ->  X V1.futr или V2.futr?"""
    en_s, ru_s, feats = _np(spec["subj"], "nomn", ctx)
    person, plural = _agree([feats])
    en, ru = [_seg("will")] + en_s, list(ru_s)
    for i, vid in enumerate(spec["verbs"]):
        v = _lookup(VERBS, vid, "verb")
        if v.get("ru_futr") is None:
            raise LexiconError(f"verb {vid!r} has no future-tense lemma in the lexicon")
        base = v["en"]["pres_pl"]
        grams = {"VERB", "futr", f"{person}per", "plur" if plural else "sing"}
        form = _form(_parse(v["ru_futr"], "INFN"), grams, f"verb {vid} future")
        pid = ctx.pair(vid, base, form)
        ctx.audit.add((vid, "+".join(sorted(grams)), form))
        if i:
            en.append(_seg("or"))
            ru.append(_seg("или"))
        en.append(_seg(base, pid))
        ru.append(_seg(form, pid))
    return en, ru


def _tail(c: dict, v: dict, ctx: Ctx):
    """Object, indirect object, preposition phrase and adverb of a clause, in that order."""
    en, ru = [], []
    if c.get("obj"):
        e, r, _ = _np(c["obj"], "accs", ctx)
        en += e
        ru += r
    if c.get("io"):
        e, r, _ = _np(c["io"], "datv", ctx)
        e.insert(0, _seg(v.get("io", "to"), e[-1]["pair"]))  # "to" joins the noun's highlight
        en += e
        ru += r
    if c.get("instr"):  # an instrumental object with no preposition: махнула хвостиком
        e, r, _ = _np(c["instr"], "ablt", ctx)
        joiner = v.get("instr_join", "its")  # an empty joiner: water becomes ice = вода становится льдом
        e = [s for s in e if s["t"] not in ("a", "an", "the")]
        if joiner:
            e = [_seg(joiner)] + e
        en += e
        ru += r
    if c.get("pp") and c.get("pp_to"):
        raise LexiconError("a clause has one prepositional phrase: pp (where) or pp_to (where to)")
    if c.get("pp") or c.get("pp_to"):
        moving = bool(c.get("pp_to"))
        prep, spec = c["pp_to"] if moving else c["pp"]
        en_p, ru_p, case = _lookup(PREPS, prep, "preposition")
        if moving:  # put it IN the box: the Russian noun takes another case than for "it is in the box"
            case = PREP_DIR.get(prep)
            if case is None:
                raise LexiconError(f"preposition {prep!r} has no direction case in the lexicon")
        pid = ctx.pair(prep, en_p, ru_p)
        e, r, _ = _np(spec, case, ctx)
        en += [_seg(en_p, pid)] + e
        ru += [_seg(ru_p, pid)] + r
    if c.get("pp_from"):  # we take the ball out of the box = мы достаём мячик из коробки
        en_p, ru_p, case = _lookup(PREPS, "out_of", "preposition")
        pid = ctx.pair("out_of", en_p, ru_p)
        e, r, _ = _np(c["pp_from"], case, ctx)
        en += [_seg(en_p, pid)] + e
        ru += [_seg(ru_p, pid)] + r
    if c.get("adv"):
        en_a, ru_a = _lookup(ADVS, c["adv"], "adverb")
        pid = ctx.pair(c["adv"], en_a, ru_a)
        en.append(_seg(en_a, pid))
        ru.append(_seg(ru_a, pid))
    return en, ru


def _noun_subject(spec, ctx: Ctx, what: str, past: bool = False):
    """Subject of a predicate or question: one noun, or several joined by 'and'.
    Returns (EN, RU, plural, gender). The gender is set for a single subject only."""
    if ctx.tense != "pres" and not (past and ctx.tense == "past"):
        tenses = "present and past" if past else "present"
        raise LexiconError(f"{what} is in the lexicon for the {tenses} tense only")
    specs = spec if isinstance(spec, list) else [spec]
    en, ru, genders = [], [], set()
    plural = len(specs) > 1
    for i, sp in enumerate(specs):
        if i:
            en.append(_seg("and"))
            ru.append(_seg("и"))
        e, r, f = _np(sp, "nomn", ctx)
        if f["gender"] is None:
            raise LexiconError(f"{what} needs a noun as its subject, not a pronoun")
        en += e
        ru += r
        genders.add(f["gender"])
        plural = plural or f["number"] == "plur"
    return en, ru, plural, genders.pop() if len(genders) == 1 else None


def _pred(c: dict, ctx: Ctx):
    """X is ADJ, or X is ADJ and ADJ.  ->  X ADJ (и ADJ)  (the Russian present tense has no verb).
    Past: X was ADJ  ->  X был ADJ, the copula agrees and the adjective stays nominative.
    A comparative takes no 'and' partner: X is heavier (than Y)  ->  X тяжелее (Y genitive)."""
    preds = c["pred"] if isinstance(c["pred"], list) else [c["pred"]]
    if len(preds) > 2:
        raise LexiconError("a predicate takes one adjective, or two joined by 'and'")
    en, ru, plural, gender = _noun_subject(c["subj"], ctx, "a predicate adjective", past=True)
    if ctx.tense == "past":
        cop = _form(_parse("быть", "INFN"), {"VERB", "past"} | ({"plur"} if plural else {gender, "sing"}),
                    "past-tense copula")
        en_cop, ru_cop = [_seg("were" if plural else "was")], [_seg(cop)]
    else:
        en_cop, ru_cop = [_seg("are" if plural else "is")], []
    if preds and isinstance(preds[0], dict):  # the comparative form of an adjective in the lexicon
        if len(preds) > 1:
            raise LexiconError("a comparative predicate stands alone, with an optional 'than'")
        spec = preds[0]
        en_c, ru_c = _lookup(COMPS, spec["comp"], "comparative")
        pid = ctx.pair(spec["comp"], en_c, ru_c)  # the concept id is the ADJS id: one colour, one sticker
        en_cop += [_seg(en_c, pid)]
        ru_cop += [_seg(ru_c, pid)]
        if spec.get("than"):
            e, r, _ = _np(spec["than"], "gent", ctx)  # heavier than the ball = тяжелее мяча
            en_cop += [_seg("than")] + e
            ru_cop += r
        return en + en_cop, ru + ru_cop
    for i, a in enumerate(preds):
        if i:
            en_cop.append(_seg("and"))
            ru_cop.append(_seg("и"))
        e, r = _adj_form(a, "nomn", plural, gender, None, ctx)
        en_cop.append(e)
        ru_cop.append(r)
    return en + en_cop, ru + ru_cop


def _q_or_adj(spec: dict, ctx: Ctx):
    """Is X A1 or A2?  ->  X A1 или A2?"""
    en_s, ru_s, plural, gender = _noun_subject(spec["subj"], ctx, "a question with adjectives")
    en, ru = [_seg("Are" if plural else "Is")] + en_s, list(ru_s)
    for i, a in enumerate(spec["adjs"]):
        if i:
            en.append(_seg("or"))
            ru.append(_seg("или"))
        e, r = _adj_form(a, "nomn", plural, gender, None, ctx)
        en.append(e)
        ru.append(r)
    return en, ru


def _q_where(spec, ctx: Ctx):
    """Where is X?  ->  Где X?"""
    en_w, ru_w = _lookup(ADVS, "where", "adverb")
    pid = ctx.pair("where", en_w, ru_w)
    en_s, ru_s, plural, _gender = _noun_subject(spec, ctx, "a question with where")
    return [_seg(en_w, pid), _seg("are" if plural else "is")] + en_s, [_seg(ru_w, pid)] + ru_s

def _q_why(spec: dict, ctx: Ctx):
    """Why does X V?  ->  Почему X V?  Present tense only: the English needs do-support."""
    if ctx.tense != "pres":
        raise LexiconError("'why' questions are in the lexicon for the present tense only")
    subj = spec["subj"] if isinstance(spec["subj"], list) else [spec["subj"]]
    en, ru, feats = [], [], []
    for i, sp in enumerate(subj):
        if i:
            en.append(_seg("and"))
            ru.append(_seg("и"))
        e, r, f = _np(sp, "nomn", ctx)
        en += e
        ru += r
        feats.append(f)
    person, plural = _agree(feats)
    vid = spec["verb"]
    v = _lookup(VERBS, vid, "verb")
    base = v["en"]["pres_pl"]
    grams = {"VERB", "pres", f"{person}per", "plur" if plural else "sing"}
    form = _form(_parse(_lemma(v, "ru_pres", vid), "INFN"), grams, f"verb {vid} in a why-question")
    pid = ctx.pair(vid, base, form)
    ctx.audit.add((vid, "+".join(sorted(grams)), form))
    en_w, ru_w = _lookup(CONN, "why", "connective")
    wid = ctx.pair("why", en_w, ru_w)
    aux = "does" if (person == 3 and not plural) else "do"
    return [_seg(en_w.capitalize(), wid), _seg(aux)] + en + [_seg(base, pid)], \
        [_seg(ru_w.capitalize(), wid)] + ru + [_seg(form, pid)]


def _q_which_comp(spec: dict, ctx: Ctx):
    """Which is heavier: the stone or the ball?  ->  Что тяжелее: камень или мячик?
    The Russian comparative does not decline, so one form serves every slot."""
    en_c, ru_c = _lookup(COMPS, spec["comp"], "comparative")
    cid = ctx.pair(spec["comp"], en_c, ru_c)
    en_w, ru_w = _lookup(CONN, "which", "connective")
    wid = ctx.pair("which", en_w, ru_w)
    colon = _seg(":", None, sp=False)
    en = [_seg(en_w.capitalize(), wid), _seg("is"), _seg(en_c, cid), colon]
    ru = [_seg(ru_w.capitalize(), wid), _seg(ru_c, cid), colon]
    if not isinstance(spec["subj"], list) or len(spec["subj"]) != 2:
        raise LexiconError("'which' compares exactly two things")
    for i, s in enumerate(spec["subj"]):
        if i:
            en.append(_seg("or"))
            ru.append(_seg("или"))
        e, r, _ = _np(s, "nomn", ctx)
        en += e
        ru += r
    return en, ru


def _has(c: dict, ctx: Ctx):
    """The cat has a kitten.  ->  У кошки есть котёнок.  The possessor sits in the genitive."""
    h = c["has"]
    en_s, _, feats = _np(h["subj"], "nomn", ctx)
    _, ru_s, _ = _np(h["subj"], "gent", ctx)
    en_o, ru_o, _ = _np(h["obj"], "nomn", ctx)
    plural = feats["number"] == "plur"
    return en_s + [_seg("have" if plural else "has")] + en_o, \
        [_seg("У")] + ru_s + [_seg("есть")] + ru_o



def _imp(c: dict, ctx: Ctx):
    """A command to one child: Touch the ice!  ->  Потрогай лёд!  Commands have no past tense."""
    if ctx.tense != "pres":
        raise LexiconError("a command is in the lexicon for the present tense only")
    vid = c["imp"]
    v = _lookup(VERBS, vid, "verb")
    grams = {"VERB", "impr", "sing", "excl"}  # excl = said to the listener, not "let us ..."
    form = _form(_parse(_lemma(v, "ru_impr", vid), "INFN"), grams, f"verb {vid} command")
    en_text = v["en"]["pres_pl"]
    pid = ctx.pair(vid, en_text, form)
    ctx.audit.add((vid, "+".join(sorted(grams)), form))
    en, ru = _tail(c, v, ctx)
    return [_seg(en_text, pid)] + en, [_seg(form, pid)] + ru

def _be_np(c: dict, ctx: Ctx):
    """I am a mouse.  ->  Я мышь.  Present tense only: the Russian copula is null, so there is
    nothing to inflect. Used for the answers of the house animals in Теремок."""
    if ctx.tense != "pres":
        raise LexiconError("'be' with a noun complement is in the lexicon for the present tense only")
    en_s, ru_s, feats = _np(c["subj"], "nomn", ctx)
    person, plural = feats["person"], feats["number"] == "plur"
    cop = "am" if (person == 1 and not plural) else ("are" if plural or person == 2 else "is")
    en_n, ru_n, _ = _np(c["be_np"], "nomn", ctx)
    return en_s + [_seg(cop)] + en_n, ru_s + ru_n


def _chain(c: dict, ctx: Ctx):
    """The grasp chain of Репка: Grandma held Grandpa, and Grandpa held the turnip.
    Russian needs no verb here: X за Y (accusative). English says 'held' once, in the first link;
    the later links are elliptical, as in the canonical translations. Only the first 'held' and the
    first 'за' carry the pill of 'hold'; every participant noun is highlighted as usual."""
    items = c["chain"]
    if len(items) < 2:
        raise LexiconError("a chain needs at least two nouns")
    if ctx.tense != "past":
        raise LexiconError("a chain is in the lexicon for the past tense only")
    v = _lookup(VERBS, "hold", "verb")
    en_v = v["en"]["past_pl"]
    en, ru = [], []
    for i, (x, y) in enumerate(zip(items, items[1:])):
        pid = ctx.pair("hold", en_v, "за") if i == 0 else None
        if i == 0:
            ctx.audit.add(("hold", "chain", "за"))
        xe, xr, _ = _np(x, "nomn", ctx)
        ye, yr, _ = _np(y, "accs", ctx)
        if i and i == len(items) - 2:
            en.append(_seg("and"))
        en += xe + ([_seg(en_v, pid)] if i == 0 else []) + ye
        ru += xr + [_seg("за", pid)] + yr
        if i < len(items) - 2:
            en.append(_seg(",", None, sp=False))
            ru.append(_seg(",", None, sp=False))
    return en, ru


def _join(c: dict, ctx: Ctx):
    """Two clauses under one connective, after a comma: it sinks, because it is heavy.
    The connective carries the pill: 'because' is a word we teach."""
    if isinstance(c["join"], list):
        raise LexiconError("'join' is a connective id; the clauses sit in 'parts'")
    en_w, ru_w = _lookup(CONN, c["join"], "connective")
    pid = ctx.pair(c["join"], en_w, ru_w)
    if len(c["parts"]) != 2:
        raise LexiconError("a join takes two clauses")
    pe, pr = compile_clause(c["parts"][0], ctx, end="")
    qe, qr = compile_clause(c["parts"][1], ctx, end="")
    for side in (qe, qr):  # the second clause follows the comma, so it starts small
        side[0]["t"] = side[0]["t"][0].lower() + side[0]["t"][1:]
    comma = _seg(",", None, sp=False)
    # Russian puts a comma before потому что and поэтому; English takes none before 'because'
    return pe + [_seg(en_w, pid)] + qe, pr + [comma, _seg(ru_w, pid)] + qr


def compile_clause(c: dict, ctx: Ctx, end=None) -> tuple[list, list]:
    if "phrase" in c and end is None:
        # a standalone phrase brings its own punctuation and capital, as in the early books
        return _phrase(c["phrase"], ctx)
    end = c.get("end", ".") if end is None else end
    if "join" in c:
        en, ru = _join(c, ctx)
    elif "phrase" in c:
        # a phrase inside a join drops its own terminal punctuation and gains no other
        en, ru = _phrase(c["phrase"], ctx)
        for side in (en, ru):
            if side and side[-1]["t"] in _PUNCT and side[-1]["pair"] is None:
                side.pop()
    elif "q_or" in c:
        en, ru = _q_or(c["q_or"], ctx)
        end = "?"
    elif "q_or_adj" in c:
        en, ru = _q_or_adj(c["q_or_adj"], ctx)
        end = "?"
    elif "q_where" in c:
        en, ru = _q_where(c["q_where"], ctx)
        end = "?"
    elif "q_why" in c:
        en, ru = _q_why(c["q_why"], ctx)
        end = "?"
    elif "q_which_comp" in c:
        en, ru = _q_which_comp(c["q_which_comp"], ctx)
        end = "?"
    elif "imp" in c:
        en, ru = _imp(c, ctx)
    elif "chain" in c:
        en, ru = _chain(c, ctx)
    elif "be_np" in c:
        en, ru = _be_np(c, ctx)
    elif "has" in c:
        en, ru = _has(c, ctx)
    elif "pred" in c:
        en, ru = _pred(c, ctx)
    else:
        subjects = c["subj"] if isinstance(c["subj"], list) else [c["subj"]]
        en, ru, feats = [], [], []
        for i, sp in enumerate(subjects):
            if i:
                en.append(_seg("and"))
                ru.append(_seg("и"))
            e, r, f = _np(sp, "nomn", ctx)
            en += e
            ru += r
            feats.append(f)
        ve, vr, v = _verb(c["verb"], feats, ctx)
        if c.get("neg"):
            # Никто не ответил: Russian negates the verb with не. English does not, because a
            # negative pronoun already carries the negation; any other subject takes do-support.
            if v.get("third_only"):
                raise LexiconError("negation is not in the lexicon for the 'be' verbs")
            vr = [_seg("не")] + vr
            nobody = any(isinstance(sp, dict) and sp.get("pron") == "nobody" for sp in subjects)
            if not nobody:
                if len(ve) != 1:
                    raise LexiconError("negation is in the lexicon for one-word English verbs only")
                person, plural = _agree(feats)
                if ctx.tense == "past":
                    aux = "did"
                elif ctx.tense == "pres":
                    aux = "does" if (person == 3 and not plural) else "do"
                else:
                    raise LexiconError("negation is in the lexicon for the present and past only")
                ve = [_seg(aux), _seg("not"), _seg(v["en"]["pres_pl"], ve[0]["pair"])]
        te, tr = _tail(c, v, ctx)
        en += ve + te
        ru += vr + tr
    if c.get("lead"):  # a framing word before the clause: First we guess. = Сначала мы угадываем.
        en_w, ru_w = _lookup(CONN, c["lead"], "connective")
        pid = ctx.pair(c["lead"], en_w, ru_w)
        en = [_seg(en_w.capitalize(), pid)] + en
        ru = [_seg(ru_w.capitalize(), pid)] + ru
    for side in (en, ru):
        side[0]["t"] = side[0]["t"][0].upper() + side[0]["t"][1:]
        side.append(_seg(end, None, sp=False))
    return en, ru


def text_of(segs: list) -> str:
    return "".join((" " if s["sp"] and i else "") + s["t"] for i, s in enumerate(segs))


# --------------------------------------------------------------------------------------------
# Story level: discourse state (articles), consistent colour per concept across the book
# --------------------------------------------------------------------------------------------
PALETTE = ("red", "blue", "green", "yellow")  # colour id n = PALETTE[n]; the renderer maps ids to inks


def _verse_line(line: str) -> list[dict]:
    """One verse line as segments. Verse is literal text: no lexicon, no pills, one line per list."""
    return [{"t": w, "pair": None, "sp": i > 0} for i, w in enumerate(line.split())]


def _compile_verse(pg: dict) -> dict:
    """A verse page. Each side is a list of lines and is drawn one line per line, never rewrapped."""
    v = pg["verse"]
    if len(v["en"]) != len(v["ru"]):
        raise LexiconError(f"verse has {len(v['en'])} English and {len(v['ru'])} Russian lines")
    en_lines = [_verse_line(ln) for ln in v["en"]]
    ru_lines = [_verse_line(ln) for ln in v["ru"]]
    return {"art": pg.get("art"), "verse": True,
            "en": " ".join(v["en"]), "ru": " ".join(v["ru"]),
            "en_lines": en_lines, "ru_lines": ru_lines,
            "en_segs": [s for ln in en_lines for s in ln], "ru_segs": [s for ln in ru_lines for s in ln],
            "pairs": []}


def _compile_page(pg: dict, tense: str, seen: set, audit: set, hues_only: bool = False) -> dict:
    if pg.get("verse"):
        return _compile_verse(pg)
    en_all, ru_all, pairs = [], [], []
    for cl in pg["clauses"]:
        ctx = Ctx(cl.get("tense", tense), seen, audit, base=len(pairs))
        en, ru = compile_clause(cl, ctx)
        en_all += en
        ru_all += ru
        pairs += ctx.pairs
    if hues_only:  # a colours book: only the colour words and the key words of the page are highlighted
        keep = {p["id"] for p in pairs if ADJS.get(p["concept"], (None, None, None))[2] in PALETTE
                or p["concept"] in pg.get("focus", ())}
        for s in en_all + ru_all:
            if s["pair"] not in keep:
                s["pair"] = None
        pairs = [p for p in pairs if p["id"] in keep]
    page = {"art": pg.get("art"), "en": text_of(en_all), "ru": text_of(ru_all),
            "en_segs": en_all, "ru_segs": ru_all, "pairs": pairs}
    if pg.get("chart"):  # the results chart of an experiment book, drawn by code in wordcard.py
        page["chart"] = pg["chart"]
    if pg.get("focus"):  # curator-chosen key words of the page, as pair ids
        ids = []
        for concept in pg["focus"]:
            hit = [p["id"] for p in pairs if p["concept"] == concept]
            if not hit:
                raise LexiconError(f"focus {concept!r} is not a highlighted word on the page {page['en']!r}")
            ids.append(hit[0])
        page["focus"] = ids
    return page


def _adjacent_concepts(page: dict) -> set:
    """Pairs of concepts whose words sit side by side in the English or the Russian line."""
    concept = {p["id"]: p["concept"] for p in page["pairs"]}
    out = set()
    for segs in (page["en_segs"], page["ru_segs"]):
        for a, b in zip(segs, segs[1:]):
            if a["pair"] is not None and b["pair"] is not None and a["pair"] != b["pair"]:
                out.add(frozenset((concept[a["pair"]], concept[b["pair"]])))
    return out


def _conflict_weights(pages: list) -> dict:
    """(concept, concept) -> how bad it is when the two share a colour. On one page, two concepts that
    share a sentence cost 1 and two that sit side by side cost 10 (the pills would look like one)."""
    weights: dict = {}
    for pg in pages:
        concepts = sorted({p["concept"] for p in pg["pairs"]})
        side_by_side = _adjacent_concepts(pg)
        for i, a in enumerate(concepts):
            for c in concepts[i + 1:]:
                weights[(a, c)] = weights.get((a, c), 0) + (10 if frozenset((a, c)) in side_by_side else 1)
    return weights


def _conflict_cost(color: dict, weights: dict) -> int:
    return sum(w for (a, c), w in weights.items() if a in color and c in color and color[a] == color[c])


def _exact_colours(order: list, fixed: dict, weights: dict, n_colors: int, start: dict) -> dict:
    """The colouring with the smallest conflict cost, by exact search. Colours in `fixed` stay. The search
    is deterministic: colours are tried by least use, then by index, and only a strictly better one wins."""
    free = [c for c in order if c not in fixed]
    nbrs: dict[str, list] = {c: [] for c in order}
    for (a, c), w in weights.items():
        if a in nbrs and c in nbrs:
            nbrs[a].append((c, w))
            nbrs[c].append((a, w))
    best = [_conflict_cost(start, weights), dict(start)]
    assign = dict(fixed)
    use = [list(fixed.values()).count(k) for k in range(n_colors)]

    def walk(i: int, cost: int) -> None:
        if cost >= best[0]:
            return
        if i == len(free):
            best[0], best[1] = cost, dict(assign)
            return
        c = free[i]
        for k in sorted(range(n_colors), key=lambda k: (use[k], k)):
            assign[c] = k
            use[k] += 1
            walk(i + 1, cost + sum(w for n, w in nbrs[c] if assign.get(n) == k))
            use[k] -= 1
            del assign[c]

    walk(0, _conflict_cost(fixed, weights))
    return best[1]


def _polish_colours(order: list, fixed: dict, weights: dict, n_colors: int, start: dict) -> dict:
    """A colouring with a low conflict cost, by deterministic descent: sweep the free words in order;
    move each word to the colour that cuts the total cost most (ties keep the lower colour index);
    repeat until a full sweep changes nothing. Every move strictly lowers the integer cost, so the
    sweep terminates, and the fixed order makes the result identical in every process.
    This is a local optimum, not a proven global one: a word can stay in a colour it shares with a
    sentence-mate. check_books.py then fails the book if a SIDE-BY-SIDE pair shares a colour, so a
    bad outcome is caught, never shipped."""
    color = dict(start)
    free = [c for c in order if c not in fixed]

    def cost_of(c: str, k: int) -> int:
        old, color[c] = color[c], k
        cost = sum(w for (a, b), w in weights.items() if color[a] == color[b])
        color[c] = old
        return cost

    for _ in range(1000):  # each sweep but the last strictly lowers the cost, so this ends early
        moved = False
        for c in free:
            cur = cost_of(c, color[c])
            best = min((cost_of(c, k), k) for k in range(n_colors))
            if best[0] < cur:
                color[c] = best[1]
                moved = True
        if not moved:
            return color
    raise LexiconError("the pill-colour search did not settle in 1000 sweeps")


def _best_colours(order: list, fixed: dict, weights: dict, n_colors: int, start: dict) -> dict:
    """Exact search for a small book (the verified colouring of the early books is kept stable);
    deterministic descent for a big one, where the exact search is exponential. If the descent
    leaves a clash, the clashing concepts alone are re-coloured exactly: a repair that is small
    by construction, because it touches only the words that still share a colour."""
    free = [c for c in order if c not in fixed]
    if len(free) <= 14:
        return _exact_colours(order, fixed, weights, n_colors, start)
    best = _polish_colours(order, fixed, weights, n_colors, start)
    cost = _conflict_cost(best, weights)
    if cost == 0:
        return best
    clash = {c for (a, b) in weights if best.get(a) == best.get(b) for c in (a, b)}
    if 0 < len(clash) <= 14:
        held = {c: k for c, k in best.items() if c not in clash}
        sub = [c for c in order if c in held or c in clash]
        repaired = _exact_colours(sub, held, weights, n_colors, best)
        if _conflict_cost(repaired, weights) < cost:
            return repaired
    return best


def compile_story(story: dict, n_colors: int = 4) -> dict:
    seen: set = set()
    audit: set = set()
    tense = story.get("tense", "pres")
    pills = story.get("pills", "all")  # "hues" = highlight only the colour words (a colours book)
    if pills not in ("all", "hues"):
        raise LexiconError(f"pills must be 'all' or 'hues', not {pills!r}")
    pages = [_compile_page(pg, tense, seen, audit, pills == "hues") for pg in story["pages"]]
    cover = (_compile_page(story["cover"], tense, seen, audit, pills == "hues")
             if story.get("cover") else None)
    # concept colouring: concepts that share a sentence never share a colour when avoidable
    nbrs: dict[str, set] = {}
    order: list[str] = []
    for pg in pages:
        cs = [p["concept"] for p in pg["pairs"]]
        for c in cs:
            if c not in nbrs:
                nbrs[c] = set()
                order.append(c)
            nbrs[c] |= set(cs) - {c}
    # a colour word keeps its own colour; everything else is graph-coloured around it
    color: dict[str, int] = {
        c: PALETTE.index(ADJS[c][2]) for c in order if c in ADJS and ADJS[c][2] in PALETTE
    }
    use = [list(color.values()).count(k) for k in range(n_colors)]
    forced = set(color)
    for c in order:
        if c in forced:
            continue
        taken = [color[n] for n in nbrs[c] if n in color]
        free = [k for k in range(n_colors) if k not in taken] or [min(range(n_colors), key=taken.count)]
        color[c] = min(free, key=lambda k: (use[k], k))
        use[color[c]] += 1
    weights = _conflict_weights(pages + ([cover] if cover else []))
    if _conflict_cost(color, weights):  # the greedy pass left two words of one sentence in one colour
        fixed = {c: color[c] for c in forced}  # the colour words never move; all else may
        color = _best_colours(order, fixed, weights, n_colors, color)
    for pg in pages:
        for p in pg["pairs"]:
            p["color"] = color[p["concept"]]
    if cover:  # the cover may only use words the story already colours
        for p in cover["pairs"]:
            if p["concept"] not in color:
                raise LexiconError(f"the cover uses {p['concept']!r}, which no story page uses")
            p["color"] = color[p["concept"]]
    out = {"title": story.get("title"), "pages": pages, "colors": color, "audit": sorted(audit)}
    if cover:
        out["cover"] = cover
    return out


def compile_counter(n: int, total: int) -> dict:
    """Page furniture '3 out of 10' / '3 из 10' with matched highlights.
    The colour ids are chrome keys ('n', 'of', 'total'), never story colours."""
    if not 1 <= n <= total:
        raise LexiconError(f"page {n} is outside 1..{total}")
    ph = CHROME["counter"]
    sub = {"{n}": str(n), "{total}": str(total)}
    ids = {c: i for i, (_, c) in enumerate(ph["en"])}

    def side(key: str) -> list:
        return [_seg(sub.get(t, t), _lookup(ids, c, "counter concept")) for t, c in ph[key]]

    en, ru = side("en"), side("ru")
    en_t = {c: sub.get(t, t) for t, c in ph["en"]}
    ru_t = {c: sub.get(t, t) for t, c in ph["ru"]}
    pairs = [{"id": i, "concept": c, "color": c, "en": en_t[c], "ru": ru_t[c]} for c, i in ids.items()]
    return {"en": text_of(en), "ru": text_of(ru), "en_segs": en, "ru_segs": ru, "pairs": pairs}


def digest(compiled: dict) -> str:
    blob = json.dumps(compiled, sort_keys=True, ensure_ascii=False).encode()
    return hashlib.sha256(blob).hexdigest()
