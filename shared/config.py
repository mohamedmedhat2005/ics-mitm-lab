PLC_IP = "172.20.0.10"
HMI_IP = "172.20.0.20"
ATTACKER_IP = "172.20.0.30"
MODBUS_PORT = 502

# Holding register map
REG_TANK_LEVEL = 0     # cm, written by PLC only
REG_PUMP = 1           # 0=off, 1=on, written by HMI
REG_VALVE = 2          # 0=closed, 1=open
REG_HIGH_SETPOINT = 3  # overflow limit in cm

# Physics constants for the tank simulation
TANK_MAX_CM = 100      # tank overflows above this
PUMP_RATE_CM = 2       # cm added per tick when pump is on
DRAIN_RATE_CM = 1      # cm removed per tick when valve is open
TICK_SECONDS = 1       # simulation step length
