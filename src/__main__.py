import discord
import uvloop

from . import AstroBot, setup_logging


uvloop.install()


discord.VoiceClient.warn_nacl = False  # Disable startup warning


with setup_logging():
    AstroBot().run()
