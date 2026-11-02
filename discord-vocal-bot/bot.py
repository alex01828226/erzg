import asyncio
import os
import discord

TOKEN = os.environ["DISCORD_TOKEN"]
GUILD_ID = 1490063562658545724
CHANNEL_ID = 1565111104105877585

class VocalBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.guilds = True
        intents.voice_states = True
        super().__init__(intents=intents)
        self.target_channel = None
        self.voice_client = None

    async def on_ready(self):
        print(f"Connecté : {self.user}")
        await self.connect_vocal()

    async def connect_vocal(self):
        guild = self.get_guild(GUILD_ID)
        if guild is None:
            print("Serveur introuvable.")
            return

        channel = guild.get_channel(CHANNEL_ID)
        if channel is None:
            print("Salon vocal introuvable.")
            return

        self.target_channel = channel

        try:
            self.voice_client = await channel.connect(self_deaf=True, self_mute=True)
            print(f"Connecté au salon : {channel.name}")
        except Exception as e:
            print(f"Erreur connexion : {e}")
            await asyncio.sleep(5)
            await self.connect_vocal()

    async def on_voice_state_update(self, member, before, after):
        if member == self.user:
            if after.channel is None:
                print("Déconnecté du vocal, reconnexion...")
                await asyncio.sleep(3)
                await self.connect_vocal()

    async def on_disconnect(self):
        print("Bot déconnecté, reconnexion dans 10s...")
        await asyncio.sleep(10)
        try:
            await self.connect_vocal()
        except Exception:
            pass

client = VocalBot()

async def main():
    while True:
        try:
            await client.start(TOKEN)
        except Exception as e:
            print(f"Crash : {e} — relance dans 15s")
            await asyncio.sleep(15)

asyncio.run(main())
