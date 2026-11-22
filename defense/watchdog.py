import sys; sys.path.insert(0, "/app")
import os, time, datetime
from pymodbus.client import ModbusTcpClient
from shared.config import (PLC_IP, MODBUS_PORT, REG_TANK_LEVEL,
                           REG_SAFETY, TANK_MAX_CM)

os.makedirs("/app/logs", exist_ok=True)
SAFETY_LIMIT = TANK_MAX_CM - 5
client = ModbusTcpClient(PLC_IP, port=MODBUS_PORT); client.connect()
print("[*] Watchdog monitoring tank physics", flush=True)

tripped = False
while True:
    level, pump = client.read_holding_registers(REG_TANK_LEVEL, count=2).registers
    if level >= SAFETY_LIMIT and pump == 1 and not tripped:
        client.write_register(REG_SAFETY, 1)     # trip the privileged safety latch
        tripped = True
        ts = datetime.datetime.now().isoformat()
        msg = f"{ts}  WATCHDOG  level {level} >= {SAFETY_LIMIT}: SAFETY TRIP"
        print(msg, flush=True)
        with open("/app/logs/watchdog.log", "a") as f:
            f.write(msg + "\n")
    if level < SAFETY_LIMIT:
        tripped = False
    time.sleep(0.5)
