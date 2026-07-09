<div align="center">
<pre>
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝
███████╗███╗   ██╗ ██████╗ ██╗███╗   ██╗███████╗
██╔════╝████╗  ██║██╔════╝ ██║████╗  ██║██╔════╝
█████╗  ██╔██╗ ██║██║  ███╗██║██╔██╗ ██║█████╗  
██╔══╝  ██║╚██╗██║██║   ██║██║██║╚██╗██║██╔══╝  
███████╗██║ ╚████║╚██████╔╝██║██║ ╚████║███████╗
╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═╝  ╚═══╝╚══════╝
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

## ⚡ Kullanım

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

---

*Fetih Çakmak — Cybersecurity Portfolio*
