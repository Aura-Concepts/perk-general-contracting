#!/bin/bash
# Double-click this file to rebuild the website photos after you've added,
# removed, or renamed images in the "site-photos" folder.
cd "$(dirname "$0")" || exit 1
echo "Rebuilding Perk General Contracting photos…"
echo ""
python3 build_site.py
status=$?
echo ""
if [ $status -eq 0 ]; then
  echo "✅ All set. Open (or refresh) the website to see your changes."
else
  echo "⚠️  Something went wrong (see the message above)."
fi
echo ""
echo "You can close this window."
