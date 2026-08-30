#!/usr/bin/env bash
# Fail if any btn-* class used in markup has no base rule in the stylesheet.
# Catches the class of bug where a primary CTA silently renders as bare text
# because its class was never defined (see website#1).
#
# A pseudo-class rule alone does not count: ".btn-green:hover" without a plain
# ".btn-green" still leaves the button unstyled in its resting state.
set -euo pipefail

status=0
for file in "$@"; do
  used=$(grep -oE 'class="[^"]*"' "$file" \
    | grep -oE 'btn-[a-z0-9]+' | sort -u || true)
  # Base rule only: the selector must be followed by "{" or "," , not ":" .
  defined=$(grep -oE '\.btn-[a-z0-9]+[[:space:]]*[,{]' "$file" \
    | grep -oE 'btn-[a-z0-9]+' | sort -u || true)

  missing=$(comm -23 <(printf '%s\n' "$used") <(printf '%s\n' "$defined") || true)
  missing=$(printf '%s\n' "$missing" | grep -v '^$' || true)

  if [ -n "$missing" ]; then
    echo "$file: button classes used in markup but never defined in CSS:"
    printf '%s\n' "$missing" | sed 's/^/  /'
    status=1
  fi
done

[ "$status" -eq 0 ] && echo "All btn-* classes used in markup have a base CSS rule."
exit $status
