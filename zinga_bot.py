import random
import json

class ZingaBot:
    def __init__(self, dare_path="data/dares.json"):
        with open(dare_path) as f:
            self.dares = json.load(f)
        self.streak = 0
        self.mood = "Happy"
        self.current_dare = random.choice(self.dares)

    def get_dare(self):
        # Only generate a new dare if not already set
        self.current_dare = random.choice(self.dares)
        self.mood = self.current_dare.get("mood", "Happy")  # default fallback
        return self.current_dare

    def update_mood(self, accepted=True):
        if accepted:
            self.streak += 1
            self.mood = "Proud" if self.streak >= 3 else "Excited"
        else:
            self.mood = "Sad"  # Skip doesn't reset streak anymore
