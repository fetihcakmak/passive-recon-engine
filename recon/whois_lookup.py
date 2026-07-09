"""
WHOIS Lookup - Pure socket-based WHOIS client
"""
import socket
from typing import Dict, Optional
from dataclasses import dataclass

WHOIS_SERVERS = {
    "com": "whois.verisign-grs.com",
    "net": "whois.verisign-grs.com",
    "org": "whois.pir.org",
    "io": "whois.nic.io",
    "dev": "whois.nic.google",
    "xyz": "whois.nic.xyz",
    "info": "whois.afilias.net",
    "me": "whois.nic.me",
    "tr": "whois.nic.tr",
    "default": "whois.iana.org",
}

@dataclass
class WhoisResult:
    domain: str
    registrar: str
    creation_date: str
    expiry_date: str
    name_servers: list
    status: list
    raw: str

class WhoisLookup:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
    
    def _get_whois_server(self, domain: str) -> str:
        tld = domain.rsplit('.', 1)[-1].lower()
        return WHOIS_SERVERS.get(tld, WHOIS_SERVERS["default"])
    
    def _raw_query(self, domain: str, server: str) -> str:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((server, 43))
            sock.sendall((domain + "\r\n").encode())
            
            response = b""
            while True:
                try:
                    chunk = sock.recv(4096)
                    if not chunk:
                        break
                    response += chunk
                except socket.timeout:
                    break
            sock.close()
            return response.decode('utf-8', errors='ignore')
        except Exception:
            return ""
    
    def _parse_whois(self, raw: str, domain: str) -> WhoisResult:
        registrar = ""
        creation = ""
        expiry = ""
        name_servers = []
        status = []
        
        for line in raw.splitlines():
            line_lower = line.lower().strip()
            if ':' not in line:
                continue
            key, _, value = line.partition(':')
            key = key.strip().lower()
            value = value.strip()
            
            if 'registrar' == key:
                registrar = value
            elif key in ('creation date', 'created', 'registered'):
                creation = value
            elif key in ('registry expiry date', 'expiry date', 'expiration date', 'paid-till'):
                expiry = value
            elif key in ('name server', 'nserver'):
                if value and value.lower() not in [ns.lower() for ns in name_servers]:
                    name_servers.append(value)
            elif key in ('domain status', 'status'):
                status.append(value.split()[0] if value else value)
        
        return WhoisResult(
            domain=domain,
            registrar=registrar,
            creation_date=creation,
            expiry_date=expiry,
            name_servers=name_servers,
            status=status,
            raw=raw
        )
    
    def lookup(self, domain: str) -> WhoisResult:
        server = self._get_whois_server(domain)
        raw = self._raw_query(domain, server)
        return self._parse_whois(raw, domain)
    
    def demo(self) -> WhoisResult:
        return WhoisResult(
            domain="example.com",
            registrar="RESERVED-Internet Assigned Numbers Authority",
            creation_date="1995-08-14T04:00:00Z",
            expiry_date="2025-08-13T04:00:00Z",
            name_servers=["a.iana-servers.net", "b.iana-servers.net"],
            status=["clientDeleteProhibited", "clientTransferProhibited",
                    "clientUpdateProhibited"],
            raw="(demo mode - no live data)"
        )
