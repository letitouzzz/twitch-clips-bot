import requests
import config

async def create_clip(broadcaster_name):
    """
    Crée un clip via l'API Twitch
    
    Args:
        broadcaster_name (str): Le nom du streamer (ex: "zerator")
    
    Returns:
        str: L'ID du clip créé, ou None si erreur
    """
    
    # 1. Récupérer l'ID du streamer (l'API Twitch utilise des IDs numériques)
    url_get_user = "https://api.twitch.tv/helix/users"
    headers = {
        "Client-ID": config.Config.CLIENT_ID,
        "Authorization": f"Bearer {config.Config.BOT_OAUTH}"
    }
    params = {"login": broadcaster_name}
    
    try:
        response = requests.get(url_get_user, headers=headers, params=params)
        response.raise_for_status()  # Lève une exception si erreur HTTP
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
            # Optionnel : durée du clip en secondes (par défaut 30)
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