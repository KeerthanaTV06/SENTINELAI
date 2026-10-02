import logging
import subprocess

class FirewallManager:
    def block_ip(self, ip_address):
        logging.warning(f"[ACTION] Blocking IP: {ip_address}")
        # subprocess.run(["iptables", "-A", "INPUT", "-s", ip_address, "-j", "DROP"])
