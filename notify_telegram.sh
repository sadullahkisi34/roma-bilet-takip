#!/bin/bash
# GitHub Actions icinde calisir: bileti kontrol eder, sonucu Telegram'a gonderir.
OUT=$(python3 check_tickets.py 2>&1)
RC=$?
echo "$OUT"

if [ $RC -eq 0 ]; then
  DETAIL=$(echo "$OUT" | tail -n +2 | sed 's/^  - //' | paste -sd '; ' -)
  SUB="Bilet VAR"; ICON="🎟️"; SILENT=false
elif [ $RC -eq 1 ]; then
  DETAIL="Hic bilet yok"; SUB="Bilet YOK"; ICON="❌"; SILENT=true
else
  DETAIL="$(echo "$OUT" | head -1)"; SUB="Kontrol hatasi"; ICON="⚠️"; SILENT=false
fi

MSG="$ICON AS ROMA - REAL MADRID
$SUB
$DETAIL
$(TZ=Europe/Istanbul date '+%d.%m.%Y %H:%M')"

curl -s -m 20 -o /dev/null \
  "https://api.telegram.org/bot${TG_BOT_TOKEN}/sendMessage" \
  --data-urlencode "chat_id=${TG_CHAT_ID}" \
  --data-urlencode "text=${MSG}" \
  --data-urlencode "disable_notification=${SILENT}"
