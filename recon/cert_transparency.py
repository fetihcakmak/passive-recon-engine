"""
Certificate Transparency Monitor - Queries crt.sh for SSL certificates
"""
import urllib.request
import json
from typing import List, Set
from dataclasses import dataclass

@dataclass
class CertEntry:
    common_name: str
    issuer: str
    not_before: str
    not_after: str
    serial: str

class CertTransparency:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.base_url = "https://crt.sh/?q={}&output=json"
    
    def search(self, domain: str) -> List[CertEntry]:
        """Searches crt.sh for certificates related to a domain"""
        url = self.base_url.format(domain)
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.loads(resp.read().decode())
            
            entries = []
            seen: Set[str] = set()
            for item in data:
                cn = item.get('common_name', '')
                if cn not in seen:
                    seen.add(cn)
                    entries.append(CertEntry(
                        common_name=cn,
                        issuer=item.get('issuer_name', ''),
                        not_before=item.get('not_before', ''),
                        not_after=item.get('not_after', ''),
                        serial=item.get('serial_number', ''),
                    ))
            return entries[:50]  # Limit results
        except Exception:
            return []
    
    def extract_subdomains(self, domain: str) -> Set[str]:
        """Extracts unique subdomains from certificate transparency logs"""
        certs = self.search(f"%.{domain}")
        subdomains = set()
        for cert in certs:
            cn = cert.common_name
            if cn.endswith(domain) and cn != domain:
                subdomains.add(cn.lstrip('*.'))
        return subdomains
    
    def demo(self) -> List[CertEntry]:
        return [
            CertEntry("www.example.com", "C=US, O=DigiCert", "2024-01-15", "2025-01-15", "0A1B2C3D"),
            CertEntry("*.example.com", "C=US, O=Let's Encrypt", "2024-06-01", "2024-09-01", "4E5F6A7B"),
            CertEntry("mail.example.com", "C=US, O=DigiCert", "2024-03-10", "2025-03-10", "8C9D0E1F"),
            CertEntry("api.example.com", "C=US, O=DigiCert", "2024-05-20", "2025-05-20", "2A3B4C5D"),
        ]
