#!/usr/bin/env python3
"""Transcription mot a mot : faster-whisper large-v3-turbo (deepdml/faster-whisper-large-v3-turbo-ct2, int8, CPU).
Decision verif vad-turbo : vad_filter=False (le VAD n'apporte rien sur turbo et pad le 1er mot 0,4 s trop tot), beam 5, 4 threads.
Usage : transcribe.py fichier16k.wav prefixe_sortie  ->  <prefixe>_mots.json (segments[].words[] {w,start,end,p})"""
import sys, json, time
wav, prefix = sys.argv[1], sys.argv[2]
from faster_whisper import WhisperModel
t0 = time.time()
m = WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2", device="cpu", compute_type="int8", cpu_threads=4)
tl = time.time() - t0
t1 = time.time()
segs, info = m.transcribe(wav, language="fr", word_timestamps=True, beam_size=5, vad_filter=False)
res = [{"start": s.start, "end": s.end, "text": s.text,
        "words": [{"w": w.word, "start": w.start, "end": w.end, "p": w.probability} for w in (s.words or [])]} for s in segs]
dt = time.time() - t1
json.dump({"wav": wav, "model": "deepdml/faster-whisper-large-v3-turbo-ct2 int8", "vad": False, "load_s": round(tl, 2), "transcribe_s": round(dt, 2), "segments": res},
          open(prefix + "_mots.json", "w"), ensure_ascii=False, indent=1)
print(f"load {tl:.1f}s transcribe {dt:.1f}s mots={sum(len(s['words']) for s in res)}")
for s in res: print(f"  [{s['start']:.2f}-{s['end']:.2f}] {s['text']}")
