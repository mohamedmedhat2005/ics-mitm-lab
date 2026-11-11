import time
from pymodbus.client import ModbusTcpClient
from shared.config import PLC_IP, MODBUS_PORT, REG_TANK_LEVEL, REG_PUMP, REG_VALVE

client = ModbusTcpClient(PLC_IP, port=MODBUS_PORT)
import time as _t; _t.sleep(2); client.connect()

while True:
    res = client.read_holding_registers(REG_TANK_LEVEL, count=4)
    if not res.isError():
        level, pump, valve, setpoint = res.registers
        if level >= setpoint and pump == 1:
            client.write_register(REG_PUMP, 0)   # stop pump
            client.write_register(REG_VALVE, 1)  # open drain
            print(f"[HMI] level {level} >= {setpoint}: stopping pump, opening valve")
        elif level <= setpoint - 20 and pump == 0:
            client.write_register(REG_PUMP, 1)   # start pump
            client.write_register(REG_VALVE, 0)  # close drain
            print(f"[HMI] level {level} <= {setpoint - 20}: starting pump")
    time.sleep(1)
