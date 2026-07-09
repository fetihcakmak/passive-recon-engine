#!/usr/bin/env python3
"""
Passive Recon Engine - Ana CLI Modülü
Kullanım: python main.py --domain example.com
"""
import argparse
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from recon.dns_enum import DNSEnumerator
from recon.whois_lookup import WhoisLookup
from recon.subdomain_enum import SubdomainEnumerator
from recon.cert_transparency import CertTransparency

# --- ANSI ---
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
MAGENTA= "\033[95m"
BOLD   = "\033[1m"
RESET  = "\033[0m"
GRAY   = "\033[90m"

BANNER = f"""{BOLD}{CYAN}
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
       PASSIVE RECON ENGINE v1.0{RESET}
"""

def print_section(title: str):
    print(f"\n{BOLD}{MAGENTA}{'='*60}{RESET}")
    print(f"{BOLD}{MAGENTA}  {title}{RESET}")
    print(f"{BOLD}{MAGENTA}{'='*60}{RESET}")

def run_demo():
    domain = "example.com"
    print(f"{GRAY}Hedef: {domain}{RESET}")
    
    # WHOIS
    print_section("WHOIS BİLGİLERİ")
    whois = WhoisLookup()
    result = whois.demo()
    print(f"  {CYAN}Kayıt Firması:{RESET} {result.registrar}")
    print(f"  {CYAN}Oluşturulma:{RESET} {result.creation_date}")
    print(f"  {CYAN}Bitiş:{RESET} {result.expiry_date}")
    print(f"  {CYAN}Name Servers:{RESET}")
    for ns in result.name_servers:
        print(f"    → {ns}")
    print(f"  {CYAN}Durum:{RESET}")
    for s in result.status:
        print(f"    → {s}")
    
    # DNS
    print_section("DNS KAYITLARI")
    dns = DNSEnumerator()
    for rec in dns.demo():
        color = GREEN if rec.record_type == 'A' else CYAN
        print(f"  {color}[{rec.record_type:>5}]{RESET} {rec.value} (TTL: {rec.ttl})")
    
    # Subdomains
    print_section("ALT ALAN ADI KEŞFİ")
    sub = SubdomainEnumerator()
    for r in sub.demo():
        print(f"  {GREEN}[+]{RESET} {r.subdomain} → {r.ip_address}")
    
    # Cert Transparency
    print_section("SERTİFİKA ŞEFFAFLIĞI")
    ct = CertTransparency()
    for cert in ct.demo():
        print(f"  {CYAN}[CERT]{RESET} {cert.common_name}")
        print(f"         Veren: {cert.issuer}")
        print(f"         Geçerlilik: {cert.not_before} → {cert.not_after}")

def main():
    parser = argparse.ArgumentParser(
        description='Passive Recon Engine - Pasif Keşif ve İstihbarat Toplama'
    )
    parser.add_argument('--domain', help='Hedef alan adı')
    parser.add_argument('--demo', action='store_true', help='Demo modunda çalıştır')
    parser.add_argument('--dns', action='store_true', help='Sadece DNS taraması')
    parser.add_argument('--whois', action='store_true', help='Sadece WHOIS sorgusu')
    parser.add_argument('--subs', action='store_true', help='Sadece subdomain keşfi')
    parser.add_argument('--certs', action='store_true', help='Sadece sertifika şeffaflığı')
    parser.add_argument('--json', action='store_true', help='JSON formatında çıktı')
    
    args = parser.parse_args()
    print(BANNER)
    
    if not (args.domain or args.demo):
        print(f"{YELLOW}Kullanım örnekleri:{RESET}")
        print("  python main.py --demo")
        print("  python main.py --domain example.com")
        print("  python main.py --domain example.com --dns")
        print("  python main.py --domain example.com --subs")
        sys.exit(0)
    
    if args.demo:
        run_demo()
        sys.exit(0)
    
    domain = args.domain
    run_all = not any([args.dns, args.whois, args.subs, args.certs])
    
    if run_all or args.whois:
        print_section(f"WHOIS: {domain}")
        whois = WhoisLookup()
        result = whois.lookup(domain)
        if result.registrar:
            print(f"  {CYAN}Kayıt Firması:{RESET} {result.registrar}")
            print(f"  {CYAN}Oluşturulma:{RESET} {result.creation_date}")
            print(f"  {CYAN}Bitiş:{RESET} {result.expiry_date}")
            for ns in result.name_servers:
                print(f"  {CYAN}NS:{RESET} {ns}")
        else:
            print(f"  {YELLOW}WHOIS verisi alinamadi.{RESET}")
    
    if run_all or args.dns:
        print_section(f"DNS: {domain}")
        dns = DNSEnumerator()
        records = dns.enumerate_all(domain)
        if records:
            for rec in records:
                print(f"  {GREEN}[{rec.record_type:>5}]{RESET} {rec.value}")
        else:
            print(f"  {YELLOW}DNS kaydi bulunamadi.{RESET}")
    
    if run_all or args.subs:
        print_section(f"SUBDOMAIN: {domain}")
        sub = SubdomainEnumerator()
        found = sub.enumerate(domain)
        if found:
            for r in found:
                print(f"  {GREEN}[+]{RESET} {r.subdomain} → {r.ip_address}")
            print(f"\n  {CYAN}Toplam:{RESET} {len(found)} alt alan adi bulundu.")
        else:
            print(f"  {YELLOW}Alt alan adi bulunamadi.{RESET}")
    
    if run_all or args.certs:
        print_section(f"CERT TRANSPARENCY: {domain}")
        ct = CertTransparency()
        certs = ct.search(domain)
        if certs:
            for cert in certs[:10]:
                print(f"  {CYAN}[CERT]{RESET} {cert.common_name} ({cert.not_before} → {cert.not_after})")
        else:
            print(f"  {YELLOW}Sertifika bulunamadi veya crt.sh erisim hatasi.{RESET}")
    
    print()

if __name__ == '__main__':
    main()
