#!/usr/bin/env python3
import sys
import json

if len(sys.argv) > 3:
    sys.stderr.write("Expected at least 2 arguments.")
    exit(1)

final_d = []
for i in sys.argv[1:-1]:
    f = open(i)
    jd = json.load(f)
    for j in jd[:-1]:
        final_d.append(j)
    f.close()

json.dump(final_d, open(sys.argv[-1], "w"))
