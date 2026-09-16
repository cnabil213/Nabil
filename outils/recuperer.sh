#!/usr/bin/env bash
# recuperer.sh — rapatrie un rush trop lourd pour le chat, à partir d'un lien de partage.
#
#   bash outils/recuperer.sh "<lien>" [nom-de-sortie]
#
# Gère : Google Drive (lien de partage), Dropbox, WeTransfer, et tout lien direct.
# Le fichier atterrit dans /mnt/user-data/working/ (ou $RUSH_DIR).
# Rien n'est envoyé nulle part : le container va chercher le fichier, point.
set -uo pipefail
LIEN="${1:-}"; [ -z "$LIEN" ] && { echo "usage : bash outils/recuperer.sh \"<lien>\" [nom]" >&2; exit 2; }
DEST="${RUSH_DIR:-/mnt/user-data/working}"; mkdir -p "$DEST"
NOM="${2:-}"

# Google Drive : on passe par l'URL de téléchargement direct (confirm=t évite
# l'écran antivirus qui, sur les gros fichiers, renvoie du HTML au lieu du mp4).
ID=""
case "$LIEN" in
  *drive.google.com*|*docs.google.com*)
    ID=$(sed -n -e 's#.*/file/d/\([^/?]*\).*#\1#p' -e 's#.*[?&]id=\([^&]*\).*#\1#p' <<<"$LIEN" | head -1)
    [ -n "$ID" ] && LIEN="https://drive.usercontent.google.com/download?id=${ID}&export=download&confirm=t"
    ;;
  *dropbox.com*) LIEN="${LIEN%%\?*}?dl=1" ;;
  # iCloud : un lien de partage est une page JavaScript, curl n'y verrait que du HTML.
  # icloud.py interroge l'API publique de resolution et rend l'URL signee du fichier.
  # Il REFUSE un lien d'album partage : Apple y re-encode les videos (voir CLAUDE.md §5).
  *icloud.com*)
    DIR_OUTILS="$(cd "$(dirname "$0")" && pwd)"
    if ! LIEN=$(python3 "$DIR_OUTILS/icloud.py" "$LIEN"); then exit 1; fi
    ;;
esac

SORTIE="$DEST/${NOM:-rush-$(date +%H%M%S).mp4}"
echo "→ téléchargement vers $SORTIE"
if ! curl -sS -L --max-time 900 -o "$SORTIE" -w "   http=%{http_code}  %{size_download} octets  %{speed_download} o/s\n" "$LIEN"; then
  echo "   curl a échoué, essai avec yt-dlp…"
  yt-dlp -q --no-warnings -o "$SORTIE" "$LIEN" || { echo "ERREUR : téléchargement impossible" >&2; exit 1; }
fi

# Un lien mal partagé renvoie une page HTML de connexion : on le voit tout de suite.
if file "$SORTIE" | grep -qi 'HTML\|XML\|ASCII text'; then
  echo "ERREUR : ce n'est pas une vidéo mais une page web ($(du -h "$SORTIE" | cut -f1))." >&2
  echo "         Le lien n'est probablement pas public : mets « Tout utilisateur disposant du lien »." >&2
  head -c 200 "$SORTIE" >&2; echo >&2; exit 1
fi
if ! ffprobe -v error -show_entries format=duration -of csv=p=0 "$SORTIE" >/dev/null 2>&1; then
  echo "ERREUR : fichier illisible par ffprobe (téléchargement tronqué ?)" >&2; exit 1
fi

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SORTIE")
AUD=$(ffprobe -v error -select_streams a -show_entries stream=codec_name -of csv=p=0 "$SORTIE" | head -1)
echo "✅ $SORTIE — $(du -h "$SORTIE" | cut -f1), ${DUR%.*} s, audio ${AUD:-AUCUN}"
echo
echo "Analyse :"
echo "  python3 outils/ecoute-video.py \"$SORTIE\" --profil profil-voix.json   # l'oreille"
echo "  python3 outils/vision-video.py \"$SORTIE\"                              # les yeux"
