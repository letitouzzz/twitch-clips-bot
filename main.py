import asyncio
from twitchio.ext import commands
import config
from hypedetector import HypeDetector
from twitchclipper import create_clip

class HypeBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=config.Config.BOT_OAUTH,
            client_secret=config.Config.CLIENT_SECRET,
            prefix='!',
            initial_channels=[config.Config.CHANNEL]
        )
        # Seuils TRÈS bas pour tester (5 messages en 5 secondes)
        self.detector = HypeDetector(time_window=5, threshold=5)
        self.message_count = 0  # Pour compter les messages reçus

    async def event_ready(self):
        print(f"✅ Bot connecté en tant que {config.Config.BOT_NICK}")
        print(f"📡 Surveille le chat de : {config.Config.CHANNEL}")
        print(f"🔧 Seuils : {self.detector.threshold} messages en {self.detector.time_window}s")

    async def event_message(self, message):
        # Ignorer les messages envoyés par le bot lui-même
        if message.echo:
            return

        # DEBUG : Affiche chaque message reçu
        self.message_count += 1
        print(f"📨 [{self.message_count}] {message.author.name}: {message.content[:30]}...")

        # Ajouter au détecteur
        is_hype = self.detector.add_message()

        if is_hype:
            print("🔥🔥🔥 ALERTE HYPE DÉTECTÉE ! Création du clip... 🔥🔥🔥")
            await self.create_clip_and_notify()

        # Nécessaire pour que les éventuelles commandes (!xxx) fonctionnent toujours
        await self.handle_commands(message)

    async def create_clip_and_notify(self):
        try:
            clip_id = await create_clip(config.Config.CHANNEL)

            if clip_id:
                clip_url = f"https://clips.twitch.tv/{clip_id}"
                print(f"🎬 Clip créé avec succès ! {clip_url}")

                channel = self.get_channel(config.Config.CHANNEL)
                await channel.send(f"🎬 Hype détectée ! Clip enregistré : {clip_url}")

        except Exception as e:
            print(f"❌ Erreur lors de la création du clip : {e}")

if __name__ == "__main__":
    bot = HypeBot()
    bot.run()