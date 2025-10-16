"""
Code for controlling a M40057A/B (or similar) LED Matrix, used in some trains to display
travel information. This will probably flicker a lot.

NOTE: For the B port, do not connect the middle pin, since it's bridged to the middle in port A.

To run the script just run:
    glasgow script train-led-matrix.py control-gpio -V 5.0 --pins A0,A1,A2,A3,A4,A5,A6,B0,B1,B2,B3,B4,
"""

import asyncio
import random
from glasgow.abstract import PullState

# NOTE: We select a digit by doing VIO on the column and GND on the row.

# Flash all pixels on startup
await gpio_iface.output(0, True) # Column 5
await gpio_iface.output(1, True) # Column 7
await gpio_iface.output(2, False) # Row 2
await gpio_iface.output(3, False) # Row 3
await gpio_iface.output(4, True) # Column 4
await gpio_iface.output(5, False) # Row 5
await gpio_iface.output(6, True) # Column 6
await gpio_iface.output(7, True) # Column 2
await gpio_iface.output(8, False) # Row 1
await gpio_iface.output(9, True) # Column 4
await gpio_iface.output(10, False) # Row 4
await gpio_iface.output(11, True) # Column 1
await gpio_iface.output(12, True) # Column 3
await asyncio.sleep(1)

rows = (8, 2, 3, 10, 5) # B2, A2, A3, B3, A5
cols = (11, 7, 12, 4, 0, 6, 1) # B4, A1, B1, A4, A0, A6, B0

async def clear():
    for row in rows:
        await gpio_iface.set(row, True)
    for col in cols:
        await gpio_iface.set(col, False)

async def set_pixel(x: int, y: int, on: bool) -> None:
    if on:
        await gpio_iface.set(cols[x], True) # Set column to VIO
        await gpio_iface.set(rows[y], False) # Set row to GND
    else:
        await gpio_iface.set(cols[x], False) # Set column to GND
        await gpio_iface.set(rows[y], True) # Set row to VIO

while True:
    await clear()
    for _ in range(10):
        x = random.randint(0, 6)
        y = random.randint(0, 4)
        await set_pixel(x, y, True)
        await asyncio.sleep(0.05)
        await set_pixel(x, y, False)