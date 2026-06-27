import os
from dotenv import load_dotenv

# Affiche le chemin absolu pour être sûr
print(f"📁 Dossier actuel : {os.getcwd()}")

load_dotenv()

class Config:
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    BOT_NICK = os.getenv("BOT_NICK")
    BOT_OAUTH = os.getenv("BOT_OAUTH")
    CHANNEL = os.getenv("CHANNEL")

# DEBUG : Affiche les valeurs (cache les secrets)
print(f"🔍 CLIENT_ID = {Config.CLIENT_ID}")
print(f"🔍 BOT_NICK = {Config.BOT_NICK}")
print(f"🔍 CHANNEL = {Config.CHANNEL}")