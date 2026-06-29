import yt_dlp
import os
import config

def download_clip(clip_id):
    """Télécharge un clip Twitch et retourne le chemin du fichier"""
    
    # L'URL du clip
    clip_url = f"https://clips.twitch.tv/{clip_id}"
    
    # Dossier de destination
    output_dir = "clips"
    os.makedirs(output_dir, exist_ok=True)
    
    # Options de téléchargement
    ydl_opts = {
        'outtmpl': f'{output_dir}/{clip_id}.mp4',  # Nom du fichier
        'format': 'best[height<=1080]',            # Qualité max 1080p
        'quiet': True,                             # Moins de logs
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([clip_url])
        
        file_path = f"{output_dir}/{clip_id}.mp4"
        print(f"✅ Clip téléchargé : {file_path}")
        return file_path
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement : {e}")
        return None