"""
DNS Enumerator - Passive DNS record collection
"""
import socket
import struct
import os
from typing import List, Dict, Optional
from dataclasses import dataclass

@dataclass
class DNSRecord:
    domain: str
    record_type: str
    value: str
    ttl: int = 0

RECORD_TYPES = {
    1: 'A', 2: 'NS', 5: 'CNAME', 6: 'SOA',
    15: 'MX', 16: 'TXT', 28: 'AAAA',
}

QTYPE_MAP = {'A': 1, 'NS': 2, 'CNAME': 5, 'MX': 15, 'TXT': 16, 'AAAA': 28, 'SOA': 6}

class DNSEnumerator:
    def __init__(self, dns_server: str = "8.8.8.8", timeout: int = 5):
        self.dns_server = dns_server
        self.timeout = timeout
    
    def _build_query(self, domain: str, qtype: int) -> bytes:
        """Builds a raw DNS query packet"""
        transaction_id = struct.pack('>H', os.getpid() & 0xFFFF)
        flags = struct.pack('>H', 0x0100)  # Standard query, recursion desired
        counts = struct.pack('>HHHH', 1, 0, 0, 0)  # 1 question
        
        # Encode domain name
        question = b''
        for part in domain.split('.'):
            question += bytes([len(part)]) + part.encode('ascii')
        question += b'\x00'
        question += struct.pack('>HH', qtype, 1)  # QTYPE, QCLASS=IN
        
        return transaction_id + flags + counts + question
    
    def _parse_name(self, data: bytes, offset: int) -> tuple:
        """Parses a DNS name with compression support"""
        parts = []
        jumped = False
        original_offset = offset
        
        while offset < len(data):
            length = data[offset]
            if length == 0:
                offset += 1
                break
            if (length & 0xC0) == 0xC0:
                if not jumped:
                    original_offset = offset + 2
                pointer = struct.unpack_from('>H', data, offset)[0] & 0x3FFF
                offset = pointer
                jumped = True
                continue
            offset += 1
            parts.append(data[offset:offset+length].decode('ascii', errors='ignore'))
            offset += length
        
        name = '.'.join(parts)
        return name, original_offset if jumped else offset
    
    def _parse_response(self, data: bytes, domain: str) -> List[DNSRecord]:
        """Parses a DNS response packet"""
        records = []
        if len(data) < 12:
            return records
        
        ancount = struct.unpack_from('>H', data, 6)[0]
        offset = 12
        
        # Skip question section
        while offset < len(data) and data[offset] != 0:
            offset += data[offset] + 1
        offset += 5  # null byte + QTYPE + QCLASS
        
        # Parse answers
        for _ in range(ancount):
            if offset >= len(data):
                break
            name, offset = self._parse_name(data, offset)
            if offset + 10 > len(data):
                break
            rtype, rclass, ttl, rdlength = struct.unpack_from('>HHIH', data, offset)
            offset += 10
            
            rdata = data[offset:offset+rdlength]
            offset += rdlength
            
            type_str = RECORD_TYPES.get(rtype, f'TYPE{rtype}')
            value = ""
            
            if rtype == 1 and len(rdata) == 4:  # A
                value = '.'.join(str(b) for b in rdata)
            elif rtype == 28 and len(rdata) == 16:  # AAAA
                value = ':'.join(f'{rdata[i]:02x}{rdata[i+1]:02x}' for i in range(0, 16, 2))
            elif rtype in (2, 5):  # NS, CNAME
                value, _ = self._parse_name(data, offset - rdlength)
            elif rtype == 15:  # MX
                if len(rdata) >= 2:
                    priority = struct.unpack_from('>H', rdata, 0)[0]
                    mx_name, _ = self._parse_name(data, offset - rdlength + 2)
                    value = f"{priority} {mx_name}"
            elif rtype == 16:  # TXT
                if rdata:
                    txt_len = rdata[0]
                    value = rdata[1:1+txt_len].decode('ascii', errors='ignore')
            else:
                value = rdata.hex()
            
            records.append(DNSRecord(
                domain=name or domain,
                record_type=type_str,
                value=value,
                ttl=ttl
            ))
        
        return records
    
    def query(self, domain: str, record_type: str = 'A') -> List[DNSRecord]:
        """Sends a DNS query and returns parsed records"""
        qtype = QTYPE_MAP.get(record_type.upper(), 1)
        query_packet = self._build_query(domain, qtype)
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self.timeout)
            sock.sendto(query_packet, (self.dns_server, 53))
            response, _ = sock.recvfrom(4096)
            sock.close()
            return self._parse_response(response, domain)
        except Exception:
            return []
    
    def enumerate_all(self, domain: str) -> List[DNSRecord]:
        """Queries all common record types for a domain"""
        all_records = []
        for rtype in ['A', 'AAAA', 'NS', 'MX', 'TXT', 'CNAME', 'SOA']:
            records = self.query(domain, rtype)
            all_records.extend(records)
        return all_records
    
    def demo(self) -> List[DNSRecord]:
        return [
            DNSRecord("example.com", "A", "93.184.216.34", 3600),
            DNSRecord("example.com", "NS", "a.iana-servers.net", 86400),
            DNSRecord("example.com", "NS", "b.iana-servers.net", 86400),
            DNSRecord("example.com", "MX", "10 mail.example.com", 3600),
            DNSRecord("example.com", "TXT", "v=spf1 -all", 3600),
            DNSRecord("example.com", "AAAA", "2606:2800:0220:0001:0248:1893:25c8:1946", 3600),
        ]
