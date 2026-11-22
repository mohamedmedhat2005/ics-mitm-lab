import sys; sys.path.insert(0, "/app")
import os, datetime
from scapy.all import sniff, IP, Raw
from shared.config import HMI_IP, MODBUS_PORT

os.makedirs("/app/logs", exist_ok=True)
ALLOWED_WRITERS = {HMI_IP}        # only the HMI may legitimately write
SAFE_FCS = {3, 6, 16}             # read, write single, write multiple

def log_alert(msg):
    ts = datetime.datetime.now().isoformat()
    line = f"{ts}  ALERT  {msg}"
    print(line, flush=True)
    with open("/app/logs/ids.log", "a") as f:
        f.write(line + "\n")

def inspect(pkt):
    if pkt.haslayer(Raw) and pkt.haslayer(IP):
        data = bytes(pkt[Raw].load)
        if len(data) < 8:
            return
        fc = data[7]
        src = pkt[IP].src
        if fc not in SAFE_FCS:
            log_alert(f"unexpected function code {fc} from {src}")
        if fc in (6, 16) and src not in ALLOWED_WRITERS:
            log_alert(f"UNAUTHORIZED WRITE from {src} (not the HMI)")

print("[*] IDS watching Modbus on port", MODBUS_PORT, flush=True)
sniff(filter=f"tcp port {MODBUS_PORT}", prn=inspect, store=0)
