import nmap
from db import insert_scan_result
from config import DANGEROUS_PORTS

def scan(ip_range, port_range):
    nm = nmap.PortScanner()
    nm.scan(hosts=ip_range, ports=port_range, arguments='-sT -T4 -sV')
    results = []

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            for port in nm[host][proto]:
                s = nm[host][proto][port]
                result = {
                    'ip': host,
                    'port': port,
                    'state': s['state'],
                    'service': s.get('name', ''),
                    'product': s.get('product', ''),
                    'version': s.get('version', '')
                }
                insert_scan_result(**result)
                results.append(result)
    return results
