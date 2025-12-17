class Difficulty:
    def __init__(self, difficultyInitial):
        self.difficulty = difficultyInitial
    
    def increaseDifficulty(self):
        self.difficulty += 1

    def getDifficulty(self):
        return self.difficulty