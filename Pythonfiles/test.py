import twitchio
from twitchio import Client
import asyncio
import config  # On utilise ton config pour récupérer les identifiants

class TestBot(Client):
    def __init__(self):
        super().__init__(
            token=config.Config.BOT_OAUTH,
            client_secret=config.Config.CLIENT_SECRET,
            client_id=config.Config.CLIENT_ID,
            nick=config.Config.BOT_NICK,
            prefix='!',
            initial_channels=[config.Config.CHANNEL]
        )

    async def event_ready(self):
        print(f"✅ {config.Config.BOT_NICK} est connecté et prêt !")

    async def event_message(self, message):
        # Ce bout de code s'exécute pour CHAQUE message dans le chat
        print(f"📨 MESSAGE BRUT : {message.author.name} -> {message.content}")

        # Si quelqu'un tape !ping, le bot répond !pong
        if message.content.startswith('!ping'):
            await message.channel.send('!pong')

if __name__ == "__main__":
    bot = TestBot()
    bot.run()