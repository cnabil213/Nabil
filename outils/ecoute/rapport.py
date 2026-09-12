#!/usr/bin/env python3
"""RAPPORT PROSODIQUE lisible par Claude, généré depuis <prefixe>_mesures.json (sortie de prosodie.py).
Seuils = propositions à calibrer sur la voix de Nabil (voir section SEUILS)."""
import sys, json
d = json.load(open(sys.argv[1])); g = d["global"]
S = {"mono_st": 0.8, "peu_varie_st": 1.5, "expressif_st": 2.6, "mou_db": -5.0, "lent_ratio": 0.65, "envoyee_db": 2.0, "envoyee_f0_st": 3.0, "plate_db": -3.0, "plate_f0_st": 1.5,
     "pause_comique": (0.4, 1.2), "debit_lent": 3.5, "debit_rapide": 5.5, "jitter": 1.5, "shimmer": 10.0, "hnr": 10.0}
def verdict_f0(sd): return "MONOTONE" if sd < S["mono_st"] else ("peu varié" if sd < S["peu_varie_st"] else ("normal" if sd < S["expressif_st"] else "VARIÉ/expressif"))
def verdict_debit(r): return "LENT" if r < S["debit_lent"] else ("RAPIDE" if r > S["debit_rapide"] else "normal")
L = []; P = L.append
P(f"RAPPORT PROSODIQUE — {d['fichier'].rsplit('/',1)[-1]} — {g['duree_s']} s")
P("=" * 78)
P("1. CARTE D'IDENTITÉ VOCALE")
P(f"   Hauteur : F0 médiane {g['f0_mediane_hz']} Hz, plage habituelle {g['f0_p5_p95_hz'][0]}–{g['f0_p5_p95_hz'][1]} Hz, "
  f"écart-type {g['f0_ecart_type_st']} demi-tons -> {verdict_f0(g['f0_ecart_type_st'])}")
P(f"   Volume  : pics (p90) {g['int_p90_parole_db']} dB, moyenne parole {g['int_moy_parole_db']} dB (dBFS RMS, 0 dBFS = pleine échelle)")
P(f"   Débit   : {g['syll_par_s_articulation']} syll/s hors pauses ({verdict_debit(g['syll_par_s_articulation'])}), "
  f"{g['syll_par_s_global']} syll/s brut, {g['mots_par_s']} mots/s ; parole {g['part_parole_pct']} % du temps")
pm = g['pause_max']
P(f"   Pauses  : {g['pauses_n']} pauses >= 0,15 s, total {g['pauses_total_s']} s, la plus longue {pm['duree']} s à {pm['debut']} s" if pm else "   Pauses  : aucune")
q = []
if g['jitter_local_pct'] > S['jitter']: q.append(f"jitter {g['jitter_local_pct']} % (> {S['jitter']} : voix instable/rauque ?)")
if g['shimmer_local_pct'] > S['shimmer']: q.append(f"shimmer {g['shimmer_local_pct']} % (> {S['shimmer']} : volume tremblé / voix fatiguée ?)")
if g['hnr_db'] < S['hnr']: q.append(f"HNR {g['hnr_db']} dB (< {S['hnr']} : souffle/rauque)")
P(f"   Timbre  : jitter {g['jitter_local_pct']} %, shimmer {g['shimmer_local_pct']} %, HNR {g['hnr_db']} dB" + (" -> " + " ; ".join(q) if q else " -> RAS"))
P("")
P("2. LIGNE DE TEMPS PAR PHRASE (Δ = par rapport à la phrase précédente)")
P("   [début-fin]   pause avant | int p90 (Δ)     | F0 moy / pic rel. médiane / écart-type | débit    | verdict   | texte")
prev = None
for p in d["phrases"]:
    dI = None if prev is None or prev.get("int_p90_db") is None or p.get("int_p90_db") is None else p["int_p90_db"] - prev["int_p90_db"]
    if p.get("int_p90_db") is None: v = "(muet)"
    elif dI is None: v = "ouverture"
    elif dI >= S["envoyee_db"] or ((p.get("f0_pic_rel_mediane_st") or 0) - (prev.get("f0_pic_rel_mediane_st") or 0)) >= S["envoyee_f0_st"]: v = "ENVOYÉE"
    elif dI <= S["plate_db"] and ((p.get("f0_pic_rel_mediane_st") or 0) - (prev.get("f0_pic_rel_mediane_st") or 0)) < S["plate_f0_st"]: v = "PLATE"
    else: v = "normale"
    pc = S["pause_comique"][0] <= p["pause_avant_s"] <= S["pause_comique"][1] and (p["fin"] - p["debut"]) < 1.5
    P(f"   [{p['debut']:5.2f}-{p['fin']:5.2f}] {p['pause_avant_s']:4.2f} s{' (pause comique ?)' if pc else '      '} | "
      f"{str(p.get('int_p90_db')):>5} dB ({'' if dI is None else f'{dI:+.1f}'}) | {str(p.get('f0_moy_hz')):>5} Hz / {str(p.get('f0_pic_rel_mediane_st')):>4} st / {str(p.get('f0_ecart_type_st')):>4} st | "
      f"{str(p.get('syll_par_s_articulation')):>4} s/s | {v:9} | {p['texte'][:60]}")
    prev = p
P("")
P("3. ALERTES AUTOMATIQUES")
for z in d["zones_molles_auto"]:
    P(f"   ZONE MOLLE  {z['debut']}–{z['fin']} s ({z['duree']} s, {z['syllabes']} syll.) : pics {z['int_p90_db']} dB soit {z['ecart_pics_vs_global_db']} dB sous les pics du reste -> voix qui retombe")
for z in d["zones_lentes_auto"]:
    P(f"   ZONE LENTE  {z['debut']}–{z['fin']} s ({z['duree']} s) : {z['syll_par_s_min']} syll/s = {int(100*z['ratio_vs_global'])} % du débit global")
for z in d["passages_monotones_auto"]:
    P(f"   MONOTONE    {z['debut']}–{z['fin']} s ({z['duree']} s) : écart-type F0 {z['f0_ecart_type_st']} st (< {S['mono_st']}) -> tu parles sur une note")
for z in d.get("passages_peu_varies_auto", []):
    P(f"   PEU VARIÉ   {z['debut']}–{z['fin']} s ({z['duree']} s) : écart-type F0 {z['f0_ecart_type_st']} st (0,8-1,3)")
for z in d.get("chutes_intonation_auto", []):
    P(f"   CHUTE D'INTONATION {z['debut']}–{z['fin']} s ({z['duree']} s) : écart-type F0 {z['f0_ecart_type_st']} st, moitié de ta variation habituelle ({g.get('f0_sd_mediane_fenetres_2s_st')} st)")
if g.get("bruit_fort"): P(f"   BRUIT DE FOND FORT : pics {g.get('pics_p99_db')} dB vs plancher {g.get('plancher_p5_db')} dB (< 30 dB d'écart) -> pauses / débit / HNR incertains")
if not (d["zones_molles_auto"] or d["zones_lentes_auto"] or d["passages_monotones_auto"] or d.get("passages_peu_varies_auto") or d.get("chutes_intonation_auto")): P("   aucune")
P("")
P("4. MOTS LES PLUS APPUYÉS (pic de volume + pic de hauteur) / LES PLUS PLATS  (F0 en demi-tons au-dessus de la hauteur habituelle du locuteur)")
P("   appuyés : " + " ; ".join(f"« {w['mot']} » @{w['debut']} s ({w['int_max_db']} dB, F0 pic {w['f0_max_st']} st)" for w in d["mots_les_plus_accentues"][:5]))
P("   plats   : " + " ; ".join(f"« {w['mot']} » @{w['debut']} s ({w['int_max_db']} dB, F0 pic {w['f0_max_st']} st)" for w in d["mots_les_plus_plats"][:4]))
P("")
P("5. TIMING : pauses >= 0,4 s et ce qui les suit")
mots = d["mots"]
for p in d["pauses"]:
    if p["duree"] < 0.4: continue
    nxt = next((w for w in mots if w["debut"] >= p["fin"] - 0.05), None)
    if nxt: P(f"   pause {p['duree']} s à {p['debut']}–{p['fin']} s -> reprise sur « {nxt['mot']} » ({nxt['int_max_db']} dB, F0 pic {nxt['f0_max_st']} st)")
    else: P(f"   pause {p['duree']} s à {p['debut']}–{p['fin']} s -> fin du clip")
P("")
P("SEUILS UTILISÉS (propositions, à calibrer sur la voix réelle de Nabil) :")
P(f"   monotone : écart-type F0 < {S['mono_st']} st sur 2 s (peu varié 0,8-1,3) | zone molle : pics 1 s < pics globaux {S['mou_db']} dB pendant >= 1,5 s | zone lente : débit < {int(S['lent_ratio']*100)} % du global")
P(f"   phrase ENVOYÉE : int p90 >= précédente +{S['envoyee_db']} dB ou pic F0 >= pic précédent +{S['envoyee_f0_st']} st | PLATE : <= {S['plate_db']} dB et pic F0 pas plus haut que la précédente (+{S['plate_f0_st']} st)")
P(f"   pause comique : {S['pause_comique'][0]}–{S['pause_comique'][1]} s juste avant une phrase courte (< 1,5 s) | débit lent < {S['debit_lent']} syll/s, rapide > {S['debit_rapide']} syll/s")
P(f"   timbre : jitter > {S['jitter']} %, shimmer > {S['shimmer']} %, HNR < {S['hnr']} dB = voix fatiguée/rauque (indicatif)")
P(f"   images à lire avec ce rapport : {d['images'][0].rsplit('/',1)[-1]} (partition F0 + intensité, mots en étiquettes) et {d['images'][1].rsplit('/',1)[-1]} (mel-spectrogramme)")
txt = "\n".join(L); print(txt); open(sys.argv[1].replace("_mesures.json", "_RAPPORT.txt"), "w").write(txt + "\n")
