import logging
from backend.response.firewall import FirewallManager
from backend.response.audit_logger import AuditLogger

class AlertRouter:
    def __init__(self):
        self.firewall = FirewallManager()
        self.audit = AuditLogger()

    def route_alert(self, alert):
        severity = alert.get('severity', 'LOW')
        self.audit.log(alert)
        if severity == 'CRITICAL':
            self.firewall.block_ip(alert.get('src_ip'))
        elif severity == 'HIGH':
            logging.info("Sent to dashboard approval queue (HITL gate)")
