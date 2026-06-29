import requests
import config

async def is_stream_live(broadcaster_name, headers):
    """Vérifie si le stream est actuellement en live."""
    url_get_stream = "https://api.twitch.tv/helix/streams"
    params = {"user_login": broadcaster_name}

    response = requests.get(url_get_stream, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    # Si "data" est vide, le stream n'est pas live
    return len(data.get("data", [])) > 0


async def create_clip(broadcaster_name):
    token = config.Config.BOT_OAUTH.replace("oauth:", "")
    headers = {
        "Client-ID": config.Config.CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    url_get_user = "https://api.twitch.tv/helix/users"
    params = {"login": broadcaster_name}

    try:
        # 0. Vérifier que le stream est bien en live AVANT de tenter le clip
        if not await is_stream_live(broadcaster_name, headers):
            print(f"⚠️ {broadcaster_name} n'est pas en live, impossible de créer un clip")
            return None

        # 1. Récupérer l'ID du streamer
        response = requests.get(url_get_user, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if not data.get("data"):
            print("❌ Streamer non trouvé")
            return None

        broadcaster_id = data["data"][0]["id"]
        print(f"✅ ID du streamer : {broadcaster_id}")

        # 2. Créer le clip
        url_create_clip = "https://api.twitch.tv/helix/clips"
        params_clip = {
            "broadcaster_id": broadcaster_id,
            # "duration": 60  # Décommente pour 60 secondes
        }

        response_clip = requests.post(url_create_clip, headers=headers, params=params_clip)
        response_clip.raise_for_status()
        clip_data = response_clip.json()

        if response_clip.status_code == 202:
            clip_id = clip_data["data"][0]["id"]
            print(f"✅ Clip en cours de création ! ID: {clip_id}")
            return clip_id
        else:
            print(f"❌ Erreur API : {clip_data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau : {e}")
        return None
    except KeyError as e:
        print(f"❌ Erreur de parsing : {e}")
        return None