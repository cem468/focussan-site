#!/usr/bin/env bash
# Rebuild the site and publish it on GitHub Pages as https://focussan.com (branch gh-pages).
# Run from the project root in Git Bash:  bash _araclar/deploy_pages.sh
set -euo pipefail
export MSYS_NO_PATHCONV=1 PYTHONIOENCODING=utf-8
python _araclar/make_en.py _kaynak/site-tr.html _kaynak/site-en.html >/dev/null
python _araclar/build_site.py
rm -rf _pages
python _araclar/build_site.py --out _pages --cname focussan.com
cd _pages
git init -q -b gh-pages
printf '* -text\n' > .gitattributes
git add -A
git -c user.name=cem468 -c user.email=cem468@users.noreply.github.com commit -q -m "Yayın: focussan.com ($(date +%Y-%m-%d))"
git push -q -f https://github.com/cem468/focussan-site.git gh-pages
echo "Yayınlandı: https://focussan.com/"
