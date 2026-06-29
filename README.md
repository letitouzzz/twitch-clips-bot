# 🎬 Twitch Hype Clip Bot

Bot Twitch qui surveille le chat en temps réel, détecte les pics de "hype" (rafales de messages), et crée automatiquement un clip via l'API Twitch quand un pic est détecté.

## 📋 Prérequis

- Python 3.10+ (testé sur Python 3.13)
- Un compte Twitch dédié au bot (ex: `clipbot128`)
- Une application enregistrée sur la [console développeur Twitch](https://dev.twitch.tv/console/apps)

## 📦 Installation

### 1. Cloner / récupérer le projet

```bash
cd twitch-clips-bot
```

### 2. Installer les dépendances Python

#### a) Le cœur du bot (obligatoire)

```bash
pip install "twitchio<3.0" python-dotenv requests
```

| Bibliothèque | Utilité |
|---|---|
| `twitchio` | Connexion au chat Twitch (IRC) et appels API |
| `python-dotenv` | Charger les variables du fichier `.env` (Client ID, tokens, etc.) |
| `requests` | Appels HTTP à l'API Twitch (créer des clips, récupérer des infos) |

> ⚠️ **Important** : ce projet utilise **TwitchIO 2.x**, pas la version 3.x. La v3 a changé son fonctionnement interne (système EventSub avec abonnements explicites au lieu de la réception automatique des messages IRC), ce qui casse le code de ce bot. **Ne fais jamais `pip install twitchio` seul** — ça installera la dernière version (3.x) par défaut. Vérifie ta version avec `pip show twitchio` — si elle affiche `3.x.x`, réinstalle avec la commande ci-dessus.

#### b) Téléchargement des clips (étape 2 — montage)

```bash
pip install yt-dlp
```

| Bibliothèque | Utilité |
|---|---|
| `yt-dlp` | Télécharger les clips Twitch depuis leur URL (`clips.twitch.tv/{clip_id}`) |

#### c) Analyse VOD / transcription (étape future — optionnel)

```bash
pip install openai-whisper
```

| Bibliothèque | Utilité |
|---|---|
| `openai-whisper` | Transcrire l'audio des VODs en texte, pour détecter des mots-clés (utilisé par le futur module `twitch-clip-miner`) |

> Cette dépendance n'est pas nécessaire pour faire fonctionner le bot de détection de hype actuel — elle sert uniquement à une fonctionnalité d'analyse VOD pas encore implémentée. Installe-la seulement si tu travailles sur cette partie.

### 3. Créer une application Twitch

1. Va sur https://dev.twitch.tv/console/apps
2. Crée une nouvelle application
3. Note le **Client ID** et génère un **Client Secret**
4. Ajoute `http://localhost` (ou `http://localhost:3000`) dans les **OAuth Redirect URLs**

### 4. Générer un token OAuth pour le bot

Connecte-toi sur le navigateur avec le **compte du bot** (pas ton compte perso), puis ouvre cette URL en remplaçant `TON_CLIENT_ID` :

```
https://id.twitch.tv/oauth2/authorize?client_id=TON_CLIENT_ID&redirect_uri=http://localhost&response_type=token&scope=chat:read+chat:edit+clips:edit
```

Autorise l'application. Tu seras redirigé vers une page d'erreur (normal, rien n'écoute sur ce port) mais l'URL contiendra ton token :

```
http://localhost/#access_token=XXXXXXXXXX&scope=...&token_type=bearer
```

⚠️ **Copie uniquement la valeur entre `access_token=` et le `&` qui suit** — ne copie pas le `&scope=...` à la suite, c'est une erreur fréquente qui invalide le token.

### 5. Configurer le fichier `.env`

Crée un fichier `.env` à la racine du projet :

```dotenv
CLIENT_ID=ton_client_id
CLIENT_SECRET=ton_client_secret
BOT_NICK=clipbot128
BOT_OAUTH=oauth:ton_token_sans_le_prefixe_oauth_colle_ici
CHANNEL=nom_de_la_chaine_a_surveiller
```

⚠️ Vérifie qu'il n'y a **aucun espace en fin de ligne** et que `BOT_OAUTH` contient bien le préfixe `oauth:` suivi du token brut (sans rien d'autre collé derrière).

## ▶️ Lancer le bot

```bash
python main.py
```

Si tout est bien configuré, tu devrais voir :

```
✅ Bot connecté en tant que clipbot128
📡 Surveille le chat de : nom_de_la_chaine
🔧 Seuils : 5 messages en 5s
```

Puis, à chaque message du chat :

```
📨 [1] pseudo: contenu du message...
```

Et quand le seuil de hype est atteint :

```
🔥🔥🔥 ALERTE HYPE DÉTECTÉE ! Création du clip... 🔥🔥🔥
✅ Clip en cours de création ! ID: xxxxxxxx
```

> ℹ️ La création de clip ne fonctionne **que si le streamer est actuellement en live**. Si la chaîne est hors-ligne, le bot l'indique clairement au lieu de planter.

## ⚙️ Comment ça marche

```
┌─────────────────┐
│   Chat Twitch    │
└────────┬─────────┘
         │ messages en temps réel (IRC)
         ▼
┌─────────────────┐
│    main.py       │  ← reçoit chaque message via event_message()
└────────┬─────────┘
         │
         ▼
┌─────────────────┐
│ hypedetector.py  │  ← compte les messages sur une fenêtre glissante
└────────┬─────────┘
         │ si seuil atteint (ex: 5 messages en 5 sec)
         ▼
┌─────────────────┐
│ twitchclipper.py │  ← appelle l'API Twitch Helix
└────────┬─────────┘
         │
         ▼
   🎬 Clip créé sur Twitch
```

### Détail des fichiers

| Fichier | Rôle |
|---|---|
| `main.py` | Point d'entrée. Se connecte au chat, écoute les messages, déclenche la détection et la création de clip. |
| `hypedetector.py` | Détecte les pics d'activité via une fenêtre glissante (`deque`). Indépendant de Twitch, logique pure. |
| `twitchclipper.py` | Gère les appels à l'API Twitch Helix : vérifie si le stream est live, récupère l'ID du broadcaster, crée le clip. |
| `config.py` | Charge les variables d'environnement depuis `.env`. |
| `test.py` | Bot minimal pour debug isolé de la connexion au chat (sans logique de hype). |
| `.env` | Identifiants et configuration (jamais à versionner sur Git). |

### Pourquoi deux systèmes d'authentification différents ?

- **Connexion au chat (IRC)** : géré par `commands.Bot` dans `main.py`, utilise le token avec préfixe `oauth:`. TwitchIO déduit le `client_id` automatiquement à partir du token, pas besoin de le préciser.
- **Appels API Helix** (création de clip, infos streamer) : géré dans `twitchclipper.py` via `requests`, nécessite le `Client-ID` en en-tête **et** le token **sans** préfixe `oauth:` dans le header `Authorization: Bearer ...`.

Les deux utilisent le même token de base, juste formaté différemment selon le contexte.

## 🐛 Problèmes fréquents

| Symptôme | Cause probable |
|---|---|
| Bot connecté mais aucun message reçu | Tu utilises TwitchIO 3.x au lieu de 2.x — downgrade nécessaire |
| `TypeError: Client.__init__() got an unexpected keyword argument 'client_id'` | Mauvaise classe héritée — utilise `commands.Bot` et non `Client` directement si tu veux passer `prefix` |
| `401 Unauthorized` sur l'API Helix | Token expiré, mal copié, ou contient encore le préfixe `oauth:` (à retirer pour les appels Helix) |
| `404 Not Found` sur `/helix/clips` | Le streamer n'est pas en live au moment de l'appel |
| `redirect_mismatch` lors de la génération du token | L'URL `redirect_uri` ne correspond pas à celle enregistrée dans la console développeur Twitch |

## 🔒 Sécurité

- Ne jamais commit le fichier `.env` (ajoute-le à `.gitignore`)
- Les tokens OAuth expirent après quelques heures — il est normal de devoir les régénérer régulièrement pendant le développement
- Ne partage jamais ton `CLIENT_SECRET` ou ton token en clair (capture d'écran, forum, etc.)

## 🚧 Roadmap (prochaines étapes)

- [ ] Téléchargement automatique des clips créés (`yt-dlp` — déjà installé, à intégrer dans le flux)
- [ ] Envoi automatique vers un salon Discord privé
- [ ] Module de montage automatique : découpe des silences (MoviePy/Pydub)
- [ ] Smart Crop 16:9 → 9:16 pour format TikTok/Shorts (MediaPipe/OpenCV)
- [ ] Transcription et analyse de VOD pour `twitch-clip-miner` (`openai-whisper` — déjà installé, à intégrer)