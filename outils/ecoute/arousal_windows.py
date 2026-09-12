#!/usr/bin/env python
"""Fenêtres glissantes (2 s, pas 1 s, 16 kHz) -> arousal/valence/dominance (audeering),
classes superb-er (4 classes EN), classes Lajavaness (5 classes FR). + RMS dB par fenêtre.
Sortie: JSON + PNG. Mesure temps et RAM pic (RSS) par modèle."""
import sys, json, time, os, argparse, resource
import numpy as np, soundfile as sf, librosa, torch, psutil
import torch.nn as nn
from transformers import Wav2Vec2Processor, Wav2Vec2Model, Wav2Vec2PreTrainedModel, Wav2Vec2ForSequenceClassification, Wav2Vec2FeatureExtractor, AutoConfig

torch.set_num_threads(2)  # laisser des coeurs aux autres agents

def rss_gb(): return psutil.Process().memory_info().rss/1e9
def maxrss_gb(): return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e6

# ---- audeering (README officiel du modèle) ----
class RegressionHead(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.dropout = nn.Dropout(config.final_dropout)
        self.out_proj = nn.Linear(config.hidden_size, config.num_labels)
    def forward(self, x, **kw):
        x = self.dropout(x); x = self.dense(x); x = torch.tanh(x); x = self.dropout(x); return self.out_proj(x)
class EmotionModel(Wav2Vec2PreTrainedModel):
    def __init__(self, config):
        super().__init__(config)
        self.config = config
        self.wav2vec2 = Wav2Vec2Model(config)
        self.classifier = RegressionHead(config)
        self.post_init()
    def forward(self, input_values):
        h = self.wav2vec2(input_values)[0]
        h = torch.mean(h, dim=1)
        return h, self.classifier(h)

def windows(y, sr, win=2.0, hop=1.0):
    n = len(y); W = int(win*sr); H = int(hop*sr)
    out = []
    start = 0
    while start < n:
        seg = y[start:start+W]
        if len(seg) < int(0.5*sr): break
        out.append((start/sr, min(start+W, n)/sr, seg))
        start += H
    return out

def run_audeering(segs, sr):
    name = 'audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim'
    t0=time.time(); r0=rss_gb()
    proc = Wav2Vec2Processor.from_pretrained(name)
    model = EmotionModel.from_pretrained(name).eval()
    tload=time.time()-t0
    res=[]; t1=time.time()
    with torch.no_grad():
        for (a,b,seg) in segs:
            x = proc(seg, sampling_rate=sr)['input_values'][0]
            x = torch.from_numpy(np.asarray(x, dtype=np.float32)).unsqueeze(0)
            _, logits = model(x)
            ar, dom, val = logits[0].tolist()
            res.append(dict(t0=round(a,2), t1=round(b,2), arousal=round(ar,3), dominance=round(dom,3), valence=round(val,3)))
    tinf=time.time()-t1
    info=dict(model=name, load_s=round(tload,1), infer_s=round(tinf,2), n_windows=len(segs), rss_after_gb=round(rss_gb(),2), rss_delta_gb=round(rss_gb()-r0,2))
    del model, proc
    return res, info

def run_cls(name, segs, sr):
    t0=time.time(); r0=rss_gb()
    fe = Wav2Vec2FeatureExtractor.from_pretrained(name)
    model = Wav2Vec2ForSequenceClassification.from_pretrained(name).eval()
    labels = model.config.id2label
    tload=time.time()-t0
    res=[]; t1=time.time()
    with torch.no_grad():
        for (a,b,seg) in segs:
            x = fe(seg, sampling_rate=sr, return_tensors='pt')
            logits = model(**x).logits[0]
            p = torch.softmax(logits, -1).tolist()
            d = {labels[i]: round(p[i],3) for i in range(len(p))}
            top = max(d, key=d.get)
            res.append(dict(t0=round(a,2), t1=round(b,2), top=top, probs=d))
    tinf=time.time()-t1
    info=dict(model=name, load_s=round(tload,1), infer_s=round(tinf,2), n_windows=len(segs), rss_after_gb=round(rss_gb(),2), rss_delta_gb=round(rss_gb()-r0,2), labels=list(labels.values()))
    del model, fe
    return res, info

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('audio'); ap.add_argument('--out', required=True)
    ap.add_argument('--models', default='audeering,superb,lajavaness'); ap.add_argument('--win', type=float, default=2.0); ap.add_argument('--hop', type=float, default=1.0)
    ap.add_argument('--title', default=''); ap.add_argument('--no-plot', action='store_true')
    a=ap.parse_args()
    y, sr0 = sf.read(a.audio, dtype='float32')
    if y.ndim>1: y=y.mean(1)
    sr=16000
    if sr0!=sr: y = librosa.resample(y, orig_sr=sr0, target_sr=sr)
    dur=len(y)/sr
    segs = windows(y, sr, a.win, a.hop)
    # RMS par fenêtre (dBFS) + RMS fin (50 ms) pour le tracé
    rms = [dict(t0=round(s,2), t1=round(e,2), rms_db=round(float(20*np.log10(np.sqrt(np.mean(seg**2))+1e-9)),1)) for (s,e,seg) in segs]
    fine = librosa.feature.rms(y=y, frame_length=1024, hop_length=320)[0]
    fine_t = librosa.frames_to_time(np.arange(len(fine)), sr=sr, hop_length=320)
    out=dict(audio=a.audio, duration_s=round(dur,2), sr=sr, win=a.win, hop=a.hop, rms=rms, models={}, infos={})
    for m in a.models.split(','):
        try:
            if m=='audeering': r,i = run_audeering(segs, sr)
            elif m=='superb': r,i = run_cls('superb/wav2vec2-base-superb-er', segs, sr)
            elif m=='lajavaness': r,i = run_cls('Lajavaness/wav2vec2-lg-xlsr-fr-speech-emotion-recognition', segs, sr)
            else: continue
            out['models'][m]=r; out['infos'][m]=i
            print(f"[{m}] load {i['load_s']}s | infer {i['infer_s']}s for {i['n_windows']} win ({dur:.1f}s audio) | RSS now {i['rss_after_gb']} GB", file=sys.stderr)
        except Exception as e:
            out['infos'][m]=dict(error=repr(e)); print(f"[{m}] ERROR {e!r}", file=sys.stderr)
    out['peak_rss_gb']=round(maxrss_gb(),2)
    json.dump(out, open(a.out+'.json','w'), indent=1, ensure_ascii=False)
    rates = [m for m in a.models.split(',') if m in ('audeering','superb','lajavaness') and m not in out['models']]
    if rates: print(f"ECHEC modele(s) {rates} : voir infos.<modele>.error dans {a.out}.json", file=sys.stderr); sys.exit(1)
    if a.no_plot: return
    # ---- tracé ----
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    nrow = 1 + len(out['models'])
    fig, axes = plt.subplots(nrow, 1, figsize=(12, 2.4*nrow), sharex=True, dpi=100)
    if nrow==1: axes=[axes]
    tc = [ (w['t0']+w['t1'])/2 for w in rms ]
    ax=axes[0]; ax.plot(fine_t, 20*np.log10(fine+1e-9), color='#999', lw=0.8, label='RMS 50 ms (dBFS)')
    ax.plot(tc, [w['rms_db'] for w in rms], 'o-', color='#222', label='RMS fenêtre 2 s (dBFS)'); ax.set_ylabel('dBFS'); ax.legend(loc='lower left', fontsize=8); ax.set_title(a.title or os.path.basename(a.audio)); ax.grid(alpha=.3)
    k=1
    if 'audeering' in out['models']:
        ax=axes[k]; k+=1; r=out['models']['audeering']
        for key,c in (('arousal','#d62728'),('valence','#2ca02c'),('dominance','#1f77b4')):
            ax.plot(tc, [w[key] for w in r], 'o-', color=c, label=key)
        ax.set_ylim(0,1); ax.set_ylabel('audeering A/V/D'); ax.legend(loc='lower left', fontsize=8, ncol=3); ax.grid(alpha=.3)
    for m in ('superb','lajavaness'):
        if m in out['models']:
            ax=axes[k]; k+=1; r=out['models'][m]; labs=out['infos'][m]['labels']
            for lab in labs: ax.plot(tc, [w['probs'][lab] for w in r], 'o-', label=lab, lw=1)
            ax.set_ylim(0,1); ax.set_ylabel(m+' p(classe)'); ax.legend(loc='upper right', fontsize=7, ncol=len(labs)); ax.grid(alpha=.3)
    for ax in axes:
        for (s,e) in getattr(a,'shade',[]) or []: pass
    axes[-1].set_xlabel('temps (s)')
    plt.tight_layout(); plt.savefig(a.out+'.png'); print('PNG', a.out+'.png', file=sys.stderr)

if __name__=='__main__': main()
