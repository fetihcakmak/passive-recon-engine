<div align="center">
<pre>
    ____  ___   __________ _____    ________
   / __ \/   | / ___/ ___//  _/ |  / / ____/
  / /_/ / /| | \__ \__ \ / / | | / / __/   
 / ____/ ___ |___/ /__/ // /  | |/ / /___   
/_/   /_/  |_/____/____/___/  |___/_____/   
    ____  ________________  _   __
   / __ \/ ____/ ____/ __ \/ | / /
  / /_/ / __/ / /   / / / /  |/ / 
 / _, _/ /___/ /___/ /_/ / /|  /  
/_/ |_/_____/\____/\____/_/ |_/   
</pre>
</div>

# 🔍 Passive Recon Engine

> Hedef alan adı hakkında WHOIS sorgusu, DNS kayıt enumerasyonu, wordlist tabanlı subdomain keşfi ve crt.sh üzerinden sertifika şeffaflığı analizi yapan pasif keşif (OSINT) aracı.

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)](https://python.org)
[![Stdlib](https://img.shields.io/badge/Dep-Stdlib_Only-success)](./)
[![Status](https://img.shields.io/badge/Status-Active-success)](./)

---

## 📈 Proje Hakkında

Bu araç, hedef sistemlere hiçbir paket göndermeden (veya minimum düzeyde DNS sorgusu ile) istihbarat toplamak için tasarlanmıştır.

**Commit Geçmişi:**
| Commit | Açıklama |
|--------|----------|
| `dns record enumerator and whois client` | Saf soket tabanlı DNS sorgusu ve WHOIS istemcisi. |
| `subdomain discovery and certificate transparency` | 70+ kelimelik wordlist ile subdomain keşfi ve crt.sh entegrasyonu. |
| `cli interface and reconnaissance report generator` | Argparse CLI, JSON çıktısı, demo modu ve modüler tarama seçenekleri. |

---

## 🧠 Mimari

```
main.py
  ├── recon/dns_enum.py          ← Saf soket ile DNS A/AAAA/NS/MX/TXT/SOA sorguları
  ├── recon/whois_lookup.py      ← TLD tabanlı WHOIS sunucu seçimi ve kayıt ayrıştırma
  ├── recon/subdomain_enum.py    ← 70+ kelimelik wordlist ile subdomain bruteforce
  └── recon/cert_transparency.py ← crt.sh API ile sertifika şeffaflığı logları
```

---

## ⚡ Kurulum

```bash
git clone https://github.com/fetihcakmak/passive-recon-engine.git
cd passive-recon-engine
python main.py --demo   # Ek bağımlılık gerekmez (yalnızca stdlib)
```

## 🚀 Kullanım

```bash
# Demo modu
python main.py --demo

# Tam keşif (WHOIS + DNS + Subdomain + Cert)
python main.py --domain example.com

# Sadece DNS sorgusu
python main.py --domain example.com --dns

# Sadece subdomain keşfi
python main.py --domain example.com --subs

# Sadece sertifika şeffaflığı
python main.py --domain example.com --certs
```

## 🖥️ Örnek Çıktı

```
============================================================
  DNS KAYITLARI
============================================================
  [    A] 93.184.216.34 (TTL: 3600)
  [   NS] a.iana-servers.net (TTL: 86400)
  [   MX] 10 mail.example.com (TTL: 3600)
  [  TXT] v=spf1 -all (TTL: 3600)

============================================================
  ALT ALAN ADI KEŞFİ
============================================================
  [+] www.example.com → 93.184.216.34
  [+] api.example.com → 93.184.216.36
```

## ⚠️ Etik Kullanım

Bu araç WHOIS, DNS ve crt.sh gibi tamamen **pasif/açık kaynak** (OSINT) veri kaynaklarını kullanır — hedefe doğrudan paket göndermez. Yine de subdomain keşfi sırasında yapılan DNS sorguları hedef altyapıya ulaşır; aracı yalnızca sahibi olduğunuz alan adları veya izinli bug bounty/pentest kapsamındaki hedefler için kullanın.

## 📄 Lisans

Bu depo şu an bir lisans dosyası içermiyor. Kullanım koşulları için proje sahibiyle iletişime geçin.

---

*Fetih Çakmak — Cybersecurity Portfolio*
