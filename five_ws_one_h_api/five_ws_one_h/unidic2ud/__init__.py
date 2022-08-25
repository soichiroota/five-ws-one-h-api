import re

import unidic2ud.spacy
from pyknp import KNP

nlp=unidic2ud.load("spoken")
knp = KNP(option='-tab')     # Default is JUMAN++. If you use JUMAN, use KNP(jumanpp=False)


def add_modifiers(id_, s, excluded_ids=None):
    result = [id_]

    for t in reversed(s):
      if excluded_ids is not None and t.id in excluded_ids:
          continue
      if t.head.id == id_ and t.id < id_:
          result = add_modifiers(t.id, s, result) + result

    for t in s:
      if excluded_ids is not None and t.id in excluded_ids:
          continue
      if t.head.id == id_ and id_ < t.id:
          result = result + add_modifiers(t.id, s, result)

    return result


def main(text):
    whats = []
    whos = []
    s=nlp(text)

    hows = [t.id for t in s if t.deprel == "root"]

    for t in s:
        if not t.head.id in hows:
            continue
        if t.deprel == "nsubj":
            whos.append(t.id)
        if t.deprel == "obj":
            whats.append(t.id)

    whos = [id_ for who in whos for id_ in add_modifiers(who, s, hows+whats)]
    whats = [id_ for what in whats for id_ in add_modifiers(what, s, hows+whos)]
    hows = [id_ for how in hows for id_ in add_modifiers(how, s, whos+whats)]

    return dict(
        whats=[s[id_].form for id_ in whats],
        whos=[s[id_].form for id_ in whos],
        hows=[s[id_].form for id_ in hows]
    )