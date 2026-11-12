import os, time, datetime
from pymodbus.client import ModbusTcpClient
from shared.config import (PLC_IP, MODBUS_PORT, REG_TANK_LEVEL,
                            REG_PUMP, REG_VALVE, TANK_MAX_CM)

os.makedirs("/app/logs", exist_ok=True)
SAFETY_LIMIT = TANK_MAX_CM - 5  # act just before actual overflow

client = ModbusTcpClient(PLC_IP, port=MODBUS_PORT); client.connect()
print("[*] Watchdog monitoring tank physics", flush=True)

while True:
    level, pump, valve = client.read_holding_registers(
        REG_TANK_LEVEL, count=3).registers
    if level >= SAFETY_LIMIT and pump == 1:
        client.write_register(REG_PUMP, 0)   # force pump OFF
        client.write_register(REG_VALVE, 1)  # force drain OPEN
        ts = datetime.datetime.now().isoformat()
        msg = f"{ts} WATCHDOG level {level} >= {SAFETY_LIMIT}: EMERGENCY SHUTDOWN"
        print(msg, flush=True)
        with open("/app/logs/watchdog.log", "a") as f:
            f.write(msg + "\n")
    time.sleep(1)
