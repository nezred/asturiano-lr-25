#!/usr/bin/env python3
from collections import defaultdict
import sys
import json
from typing import Iterable
from itertools import chain

token = tuple[str, str, str]


def is_verb(w: token) -> bool:
    return w[2][0] == "V"


def count_verbs(list_w: Iterable[token]) -> dict[str, int]:
    """
    outputs number of each verb found, as dictionary with the verb lemma and its respective counts
    """
    out = defaultdict(lambda: 0)
    for w in list_w:
        if is_verb(w):
            out[w[1]] += 1
    return out


def make_token_list(in_dat):
    for s in in_dat:
        for w in s:
            yield w


def main(self, in_dat_path, out_dic, out_freq):
    in_dat = json.load(open(in_dat_path))
    vc = count_verbs(make_token_list(in_dat))
    vcl = list(vc.items())
    vcl.sort(key=lambda x: x[1], reverse=True)
    f = open(out_freq, "w")
    for i, v in vcl:
        f.write("%s\t%s\n" % (i, v))
        pass
    print(list(vc.items())[:10])
    pass


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.stderr.write("Syntax: fprocess.py <in_dat> <out_dic> <out_freq>\n")
        exit(1)
    main(*sys.argv)
