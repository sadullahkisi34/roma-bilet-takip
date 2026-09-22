#!/usr/bin/env python3
"""AS Roma bilet kontrolu: Regular Tickets (tipiPosto) icinde satista bilet var mi?"""
import json, re, sys, subprocess, datetime

URL = "https://biglietti.asroma.com/tickets/match/MAN133/001?back=true&vendor=whospmm"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36")

def fetch(url=URL):
    return subprocess.run(["curl", "-sL", "-A", UA, url],
                          capture_output=True, text=True, timeout=60).stdout

def extract(html, varname):
    m = re.search(r"var\s+%s\s*=\s*(\[.*?\]);" % varname, html, re.S)
    if not m:
        return None
    return json.loads(m.group(1))

def main():
    html = fetch()
    tipi = extract(html, "tipiPosto")
    if tipi is None:
        print("HATA: sayfadan tipiPosto verisi cikarilamadi (sayfa yapisi degismis olabilir)")
        sys.exit(2)

    available = []
    for t in tipi:
        if t.get("notAvailable"):
            continue
        free = t.get("totalePostiLiberi") or 0
        if free <= 0:
            continue
        prices = [p.get("importoTotale") for p in (t.get("prezzi") or []) if p.get("abilitazioneVendita")]
        name = t.get("descrizione") or t.get("codice")
        available.append((name, free, min(prices) if prices else None))

    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if available:
        print(f"[{ts}] BILET VAR! ({len(available)} kategori)")
        for name, free, price in sorted(available, key=lambda x: -x[1]):
            p = f"{price:.0f} EUR" if price is not None else "fiyat yok"
            print(f"  - {name}: {free} koltuk, {p}")
        sys.exit(0)
    else:
        print(f"[{ts}] Bilet yok (Regular Tickets bos)")
        sys.exit(1)

if __name__ == "__main__":
    main()
