import asyncio
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer
from shared.config import (
    REG_TANK_LEVEL, REG_PUMP, REG_VALVE, REG_SAFETY,
    TANK_MAX_CM, PUMP_RATE_CM, DRAIN_RATE_CM, TICK_SECONDS,
    SAFE_RELEASE_CM, MODBUS_PORT
)

# Initial values: level=50, pump=0, valve=0, setpoint=80, safety=0
store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [50, 0, 0, 80, 0]), zero_mode=True)
context = ModbusServerContext(slaves=store, single=True)

async def simulate():
    while True:
        level, pump, valve, setpoint, safety = store.getValues(3, 0, count=5)
        # SAFETY INTERLOCK: once tripped, overrides any command until safe again.
        # The attacker cannot clear it - this is the privileged safety channel.
        if safety == 1:
            pump, valve = 0, 1
            store.setValues(3, REG_PUMP, [0])
            store.setValues(3, REG_VALVE, [1])
            if level <= SAFE_RELEASE_CM:
                store.setValues(3, REG_SAFETY, [0])
        if pump == 1:
            level += PUMP_RATE_CM
        if valve == 1:
            level -= DRAIN_RATE_CM
        level = max(0, min(level, TANK_MAX_CM + 20))
        store.setValues(3, REG_TANK_LEVEL, [level])
        print(f"[PLC] level={level}cm | pump={pump} | valve={valve} | safety={safety}")
        await asyncio.sleep(TICK_SECONDS)

async def main():
    asyncio.create_task(simulate())
    await StartAsyncTcpServer(context=context, address=("0.0.0.0", MODBUS_PORT))

asyncio.run(main())
