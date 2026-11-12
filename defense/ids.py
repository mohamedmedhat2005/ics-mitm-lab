import os, datetime
from scapy.all import sniff, IP, TCP, Raw
from shared.config import HMI_IP, MODBUS_PORT

os.makedirs("/app/logs", exist_ok=True)

ALLOWED_WRITERS = {HMI_IP}   # only the HMI may legitimately write
SAFE_FCS = {3, 6, 16}        # read, write single, write multiple

def log_alert(msg):
    ts = datetime.datetime.now().isoformat()
    line = f"{ts} ALERT {msg}"
    print(line, flush=True)
    with open("/app/logs/ids.log", "a") as f:
        f.write(line + "\n")

def inspect(pkt):
    if not (pkt.haslayer(IP) and pkt.haslayer(TCP) and pkt.haslayer(Raw)):
        return
    if pkt[TCP].dport != MODBUS_PORT:
        return  # only look at requests going TO the PLC, not its replies
    data = bytes(pkt[Raw].load)
    if len(data) < 8:
        return
    fc = data[7]  # Modbus function code
    src = pkt[IP].src
    if fc not in SAFE_FCS:
        log_alert(f"unexpected function code {fc} from {src}")
    if fc in (6, 16) and src not in ALLOWED_WRITERS:
        log_alert(f"UNAUTHORIZED WRITE from {src} (not the HMI)")

print("[*] IDS watching Modbus on port", MODBUS_PORT, flush=True)
sniff(filter=f"tcp port {MODBUS_PORT}", prn=inspect, store=0)
