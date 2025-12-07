import os
import re
import logging
from collections import defaultdict

# Try importing Scapy (Heavy Dependency)
try:
    from scapy.all import rdpcap, TCP, UDP, IP, DNS, Raw, packet
    from scapy.layers.http import HTTPRequest
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False

class PcapAnalyzer:
    def __init__(self, filepath):
        self.filepath = filepath
        self.findings = []
        self.creds_found = []
        self.dns_queries = set()
        self.http_requests = []

    def analyze(self):
        """Main analysis entry point"""
        if not SCAPY_AVAILABLE:
            return ["⚠️ Scapy not installed. Cannot analyze PCAP."]

        if not os.path.exists(self.filepath):
            return []

        try:
            # Read the PCAP
            packets = rdpcap(self.filepath)
            
            for pkt in packets:
                self._analyze_packet(pkt)

            # Post-Analysis Findings
            self._summarize_findings()

        except Exception as e:
            self.findings.append(f"PCAP Error: {str(e)}")

        return self.findings

    def _analyze_packet(self, pkt):
        # 1. Credential Harvesting (Cleartext)
        if pkt.haslayer(Raw):
            load = pkt[Raw].load
            try:
                # Basic Grep for user/pass in raw payload (FTP, Telnet, HTTP)
                # This is "dirty" but effective for CTFs
                decoded = load.decode('utf-8', errors='ignore')
                
                # FTP/Telnet patterns
                if "USER " in decoded or "PASS " in decoded:
                    self.creds_found.append(f"Cleartext Creds: {decoded.strip()}")

                # HTTP Basic Auth
                if "Authorization: Basic" in decoded:
                    import base64
                    try:
                        auth_str = decoded.split("Authorization: Basic ")[1].split("\r\n")[0]
                        creds = base64.b64decode(auth_str).decode('utf-8')
                        self.creds_found.append(f"HTTP Basic Auth: {creds}")
                    except:
                        pass
                        
            except:
                pass

        # 2. HTTP Analysis
        if pkt.haslayer("HTTPRequest"):
            # Scapy's HTTP layer is powerful
            http = pkt["HTTPRequest"]
            url = f"{http.Host.decode()}{http.Path.decode()}"
            self.http_requests.append(url)

        # 3. DNS Analysis
        if pkt.haslayer(DNS) and pkt.haslayer(UDP):
            if pkt[DNS].qr == 0: # Query
                qname = pkt[DNS].qd.qname.decode('utf-8')
                self.dns_queries.add(qname)

    def _summarize_findings(self):
        # Report Credentials
        if self.creds_found:
            for cred in set(self.creds_found): # Deduplicate
                self.findings.append(f"🔥 CREDENTIAL: {cred}")

        # Report Suspicious DNS
        for dns in self.dns_queries:
            if "flag" in dns or "ctf" in dns:
                self.findings.append(f"🚩 FLAG DNS: {dns}")

        # Report HTTP
        if len(self.http_requests) > 0:
            self.findings.append(f"INFO: {len(self.http_requests)} HTTP requests tracked.")
            # Check for flag in URLs
            for url in self.http_requests:
                if "flag" in url.lower() or "secret" in url.lower():
                    self.findings.append(f"🚩 FLAG URL: {url}")

