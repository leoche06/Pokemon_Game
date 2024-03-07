class pokemon:
    def __init__(self, name, type, hp, attack, defense, speed, experience, moves, level):
        self.name = name
        self.type = type
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.experience = experience
        self.moves = moves
        self.level = level
    
    def battle(self):
        pass
    
    def calculate_damage(self):
        pass
    
    def update_level(self):
        pass

class pokedex(pokemon):
    def __init__(self, name, type, hp, attack, defense, speed, experience, moves, level, caught):
        super().__init__(name, type, hp, attack, defense, speed, experience, moves, level)
        self.caught = caught
    
    def catch_pokemon(self):
        pass
    
    def release_pokemon(self):
        pass
    
    def display_pokemon(self):
        pass
    