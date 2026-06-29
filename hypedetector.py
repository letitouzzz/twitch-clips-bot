import time
from collections import deque

class HypeDetector:
    def __init__(self, time_window=5, threshold=5):
        self.time_window = time_window
        self.threshold = threshold
        self.message_timestamps = deque()
        self.total_messages = 0

    def add_message(self):
        now = time.time()
        self.total_messages += 1
        self.message_timestamps.append(now)

        # Nettoyer les anciens
        old_count = 0
        while self.message_timestamps and self.message_timestamps[0] < now - self.time_window:
            self.message_timestamps.popleft()
            old_count += 1

        current_count = len(self.message_timestamps)
        
        # DEBUG : Affiche l'état actuel
        if current_count >= self.threshold - 2:  # Affiche quand on approche du seuil
            print(f"📊 {current_count} messages dans la fenêtre de {self.time_window}s (seuil: {self.threshold})")

        if current_count >= self.threshold:
            print(f"🔥🔥🔥 DÉCLENCHEMENT ! {current_count} messages en {self.time_window}s")
            self.message_timestamps.clear()
            return True
        
        return False