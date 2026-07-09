"""
Subdomain Enumerator - Wordlist-based passive subdomain discovery
"""
import socket
from typing import List, Set
from dataclasses import dataclass

@dataclass
class SubdomainResult:
    subdomain: str
    ip_address: str
    resolved: bool

# Common subdomain wordlist
DEFAULT_WORDLIST = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp",
    "pop", "ns1", "ns2", "dns", "dns1", "dns2",
    "vpn", "gateway", "api", "dev", "staging", "test",
    "admin", "portal", "app", "m", "mobile",
    "blog", "shop", "store", "secure", "login",
    "cdn", "static", "assets", "img", "images", "media",
    "docs", "wiki", "support", "help", "forum",
    "git", "svn", "jenkins", "ci", "jira", "confluence",
    "db", "database", "mysql", "postgres", "redis", "mongo",
    "backup", "bak", "old", "new", "beta", "alpha",
    "proxy", "lb", "load", "monitor", "grafana", "kibana",
    "elastic", "search", "solr", "log", "logs",
    "mx", "mx1", "mx2", "imap", "pop3",
    "cpanel", "whm", "plesk", "panel",
    "remote", "rdp", "ssh", "sftp",
    "intranet", "internal", "extranet", "corp",
    "owa", "exchange", "autodiscover",
]

class SubdomainEnumerator:
    def __init__(self, wordlist: List[str] = None, timeout: float = 2.0):
        self.wordlist = wordlist or DEFAULT_WORDLIST
        self.timeout = timeout
    
    def resolve(self, subdomain: str) -> SubdomainResult:
        """Tries to resolve a subdomain to an IP address"""
        try:
            socket.setdefaulttimeout(self.timeout)
            ip = socket.gethostbyname(subdomain)
            return SubdomainResult(subdomain=subdomain, ip_address=ip, resolved=True)
        except (socket.gaierror, socket.timeout, OSError):
            return SubdomainResult(subdomain=subdomain, ip_address="", resolved=False)
    
    def enumerate(self, domain: str) -> List[SubdomainResult]:
        """Enumerates subdomains by resolving each from the wordlist"""
        found = []
        for word in self.wordlist:
            sub = f"{word}.{domain}"
            result = self.resolve(sub)
            if result.resolved:
                found.append(result)
        return found
    
    def demo(self) -> List[SubdomainResult]:
        return [
            SubdomainResult("www.example.com", "93.184.216.34", True),
            SubdomainResult("mail.example.com", "93.184.216.35", True),
            SubdomainResult("api.example.com", "93.184.216.36", True),
            SubdomainResult("dev.example.com", "10.0.0.50", True),
            SubdomainResult("staging.example.com", "10.0.0.51", True),
            SubdomainResult("admin.example.com", "93.184.216.40", True),
            SubdomainResult("vpn.example.com", "203.0.113.10", True),
        ]
