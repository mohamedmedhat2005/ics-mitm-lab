import asyncio
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer
from shared.config import (
    REG_TANK_LEVEL, TANK_MAX_CM, PUMP_RATE_CM,
    DRAIN_RATE_CM, TICK_SECONDS, MODBUS_PORT
)

# Initial values: level=50, pump=0 (off), valve=0 (closed), setpoint=80
store = ModbusSlaveContext(hr=ModbusSequentialDataBlock(0, [50, 0, 0, 80]), zero_mode=True)
context = ModbusServerContext(slaves=store, single=True)

async def simulate():
    while True:
        level, pump, valve, _ = store.getValues(3, 0, count=4)
        if pump == 1:
            level += PUMP_RATE_CM
        if valve == 1:
            level -= DRAIN_RATE_CM
        level = max(0, level)
        store.setValues(3, REG_TANK_LEVEL, [level])
        print(f"[PLC] level={level}cm | pump={pump} | valve={valve}")
        await asyncio.sleep(TICK_SECONDS)

async def main():
    asyncio.create_task(simulate())
    await StartAsyncTcpServer(context=context, address=("0.0.0.0", MODBUS_PORT))

asyncio.run(main())
