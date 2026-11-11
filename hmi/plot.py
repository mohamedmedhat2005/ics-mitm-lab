import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pymodbus.client import ModbusTcpClient
from shared.config import PLC_IP, MODBUS_PORT, REG_TANK_LEVEL, TANK_MAX_CM

client = ModbusTcpClient(PLC_IP, port=MODBUS_PORT)
client.connect()

xs, ys = [], []
fig, ax = plt.subplots()

def update(frame):
    res = client.read_holding_registers(REG_TANK_LEVEL, count=1)
    if not res.isError():
        level = res.registers[0]
        xs.append(frame)
        ys.append(level)
        ax.clear()
        ax.axhline(TANK_MAX_CM, color="red", linestyle="--", label="overflow")
        ax.plot(xs[-60:], ys[-60:], label="tank level")
        ax.set_ylim(0, TANK_MAX_CM + 30)
        ax.legend()

ani = FuncAnimation(fig, update, interval=1000)
plt.show()
