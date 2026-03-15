#!/bin/bash
rm /out/*
task() {
  touch /out/"$1".json
  for i in {0..999}; do
    i=$((i + $2))
    printf '+ Doing task %d' "$i"
    python3 /src/process.py "$i" >>/out/"$1".json
    printf '\n' >>/out/"$1".json
  done
  printf '\n' >>/out/"$1".json
  printf '[\n' >/out/"$1"p.json
  sed 's/^\(..*\)$/\1,/' /out/"$1".json >>/out/"$1"p.json
  printf '\n[]]' >>/out/"$1"p.json
}

task wiki10_pos-0 0 &
task wiki10_pos-1 1000 &
task wiki10_pos-2 2000 &
task wiki10_pos-3 3000 &
task wiki10_pos-4 4000 &
task wiki10_pos-5 5000 &
task wiki10_pos-6 6000 &
task wiki10_pos-7 7000 &
task wiki10_pos-8 8000 &
task wiki10_pos-9 9000 &
wait

printf '+ Doing final task!'
printf '%s\n' /out/wiki10*.json
python3 /src/merge.py /out/wiki10*p.json /out/wiki10_pos-full.json
python3 /src/fprocess.py /out/wiki10_pos-full.json /out/wiki10_pos-full-dic.json /out/wiki10_pos-full-freqs.json
