from twitchio.ext import commands
import config

class TestBot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=config.Config.BOT_OAUTH,
            client_secret=config.Config.CLIENT_SECRET,
            prefix='!',
            initial_channels=[config.Config.CHANNEL]
        )

    async def event_ready(self):
        print(f"✅ Connecté et prêt !")
        print(f"User id is | {self.nick}")
        print(f"📡 Surveille le chat de : {config.Config.CHANNEL}")

    async def event_message(self, message):
        # Les messages envoyés par le bot lui-même ont echo=True, on les ignore
        if message.echo:
            return

        print(f"📨 MESSAGE BRUT : {message.author.name} -> {message.content}")

        # Comme on override event_message, on doit appeler ça nous-mêmes
        # pour que les commandes (comme !ping) fonctionnent toujours
        await self.handle_commands(message)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send('!pong')

if __name__ == "__main__":
    bot = TestBot()
    bot.run()