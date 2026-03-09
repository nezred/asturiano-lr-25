#!/bin/bash

for i in {0..100}; do
  printf '+ Doing task %d' "$i"
  python3 /src/process.py "$i"
done

printf '+ Doing final task!'
python3 /src/merge.py /out/* /out/wiki10_pos-full.json
