import time

import discord


COLORS = [
    0x0070D1,  # PS Blue
    0xFFE312,  # PS Plus
    0x7CB2E8,  # Cross
    0xFF6666,  # Circle
    0xFF69F8,  # Square
    0x40E2A0,  # Triangle
]

COLOR_COUNT = len(COLORS)


class Embed(discord.Embed):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Cycle through the six colors once an hour
        self.color = COLORS[int(time.time() / 3600 % COLOR_COUNT)]
