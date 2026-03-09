import sys
import os
import pandas as pd
import numpy as np
import json

sys.path.append("/usr/share/freeling/APIs/python3")
import pyfreeling

pyfreeling.util_init_locale("C.UTF-8")

tr = pyfreeling.traces()
tr.set_trace_level(7)
tr.set_trace_level(0)
tr.set_trace_module(0xFFFFFF)

DATA = "/usr/share/freeling/"
# create language detector. Used just to show it. Results are printed
# but ignored (after, it is assumed language is LANG)
la = pyfreeling.lang_ident(DATA + "common/lang_ident/ident-few.dat")
LANG = "as"

# create options set for maco analyzer.
op = pyfreeling.analyzer_config()

# define creation options for morphological analyzer modules
op.config_opt.Lang = LANG
op.config_opt.MACO_PunctuationFile = DATA + "common/punct.dat"
op.config_opt.MACO_DictionaryFile = DATA + LANG + "/dicc.src"
op.config_opt.MACO_AffixFile = DATA + LANG + "/afixos.dat"
# op.config_opt.MACO_CompoundFile = DATA + LANG + "/compounds.dat"
op.config_opt.MACO_LocutionsFile = DATA + LANG + "/locucions.dat"
op.config_opt.MACO_NPDataFile = DATA + LANG + "/np.dat"
op.config_opt.MACO_QuantitiesFile = DATA + LANG + "/quantities.dat"
op.config_opt.MACO_ProbabilityFile = DATA + LANG + "/probabilitats.dat"

# chose which modules among those available will be used by default
# (can be changed at each call if needed)
op.invoke_opt.MACO_AffixAnalysis = True
# op.invoke_opt.MACO_CompoundAnalysis = True
op.invoke_opt.MACO_CompoundAnalysis = False
op.invoke_opt.MACO_MultiwordsDetection = True
op.invoke_opt.MACO_NumbersDetection = True
op.invoke_opt.MACO_PunctuationDetection = True
op.invoke_opt.MACO_DatesDetection = True
op.invoke_opt.MACO_QuantitiesDetection = True
op.invoke_opt.MACO_DictionarySearch = True
op.invoke_opt.MACO_ProbabilityAssignment = True
op.invoke_opt.MACO_NERecognition = True
op.invoke_opt.MACO_RetokContractions = True

# create analyzers
tk = pyfreeling.tokenizer(DATA + LANG + "/tokenizer.dat")

mf = pyfreeling.maco(op)

# create tagger, sense anotator, and parsers
op.config_opt.TAGGER_HMMFile = DATA + LANG + "/tagger.dat"
op.invoke_opt.TAGGER_Retokenize = True
op.invoke_opt.TAGGER_ForceSelect = pyfreeling.RETOK
mf = pyfreeling.maco(op)

# create tagger, sense anotator, and parsers
op.config_opt.TAGGER_HMMFile = DATA + LANG + "/tagger.dat"
op.invoke_opt.TAGGER_Retokenize = True
op.invoke_opt.TAGGER_ForceSelect = pyfreeling.RETOK
tg = pyfreeling.hmm_tagger(op)


def tokenize(sen):
    sen_proc = tk.tokenize(sen)
    sen_proc = pyfreeling.sentence(sen_proc)
    sen_proc = mf.analyze_sentence(sen_proc)
    sen_proc = tg.analyze_sentence(sen_proc)
    return sen_proc


wiki10 = pd.read_csv(
    "/ast_wikipedia_2021_10K/ast_wikipedia_2021_10K-sentences.txt",
    sep="\t",
    header=None,
    names=["sentence_id", "sentence"],
)
wiki10_pos = []
wiki10_l = wiki10["sentence"].to_numpy()

if len(sys.argv) != 2:
    print("Syntax: process-rep.sh <nº iter>")

n = int(sys.argv[1])
print("Doing iteration %d..." % n)
for i in wiki10_l[n : n + 10]:
    try:
        s = tokenize(i)
    except Exception as e:
        print(e)
        print("THIS SENTENCE FAILED")
        exit(1)
    wiki10_pos.append([])
    for w in s:
        wiki10_pos[-1].append((w.get_form(), w.get_lemma(), w.get_tag()))

json.dump(wiki10_pos, open("/out/wiki10_pos-%d.json" % n, "w"))
print("Finished! :)")
