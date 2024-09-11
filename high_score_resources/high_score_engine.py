from os.path import exists
import json

class HighScoresManager:
    def __init__(self, filename='high_score_resources/high_scores.json'):
        self.filename = filename
        self.score = 0
        self.high_scores = self.load_high_scores()

    def load_high_scores(self):
        if exists(self.filename):
            with open(self.filename, 'r') as file:
                return json.load(file)
        return []

    def save_high_scores(self):
        with open(self.filename, 'w') as file:
            json.dump(self.high_scores, file, indent=4)

    def add_high_score(self, name, score):
        self.high_scores.append({'name': name, 'score': score})
        self.high_scores = sorted(self.high_scores, key=lambda x: x['score'], reverse=True)[:10]
        self.save_high_scores()

    def get_high_scores(self):
        return self.high_scores
