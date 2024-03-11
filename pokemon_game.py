import random

from dataclasses import dataclass
from enum import Enum


class Type(Enum):
    NORMAL = 1
    FIRE = 2
    WATER = 3
    ELECTRIC = 4
    GRASS = 5
    ICE = 6
    FIGHTING = 7
    POISON = 8
    GROUND = 9
    FLYING = 10
    PSYCHIC = 11
    BUG = 12
    ROCK = 13
    GHOST = 14
    DRAGON = 15
    DARK = 16
    STEEL = 17
    FAIRY = 18


CHARACTERS = {
    'Pikachu': {'Type': [Type.NORMAL], 'HP': 35, 'Moves': ['Thunder Shock', 'Double Kick', 'Thunderbolt'],
                'Attack': 55, 'Defense': 40, 'Speed': 90, 'Experience': 112},
    'Charizard': {'Type': [Type.FIRE, Type.FLYING], 'HP': 78, 'Moves': ['Crunch', 'Ember', 'Scratch', 'Wing Attack'],
                  'Attack': 84, 'Defense': 78, 'Speed': 100, 'Experience': 240},
    'Squirtle': {'Type': [Type.WATER], 'HP': 44, 'Moves': ['Tackle', 'Bubble', 'Bite'], 'Attack': 48,
                 'Defense': 65, 'Speed': 43, 'Experience': 63},
    'Jigglypuff': {'Type': [Type.NORMAL, Type.FAIRY], 'HP': 115, 'Moves': ['Pound', 'Body Slam', 'Double Slap'],
                   'Attack': 45, 'Defense': 20, 'Speed': 20, 'Experience': 95},
    'Gengar': {'Type': [Type.GHOST, Type.POISON], 'HP': 60, 'Moves': ['Lick', 'Smog', 'Dream Eater', 'Shadow Ball'],
               'Attack': 65, 'Defense': 60, 'Speed': 110, 'Experience': 225},
    'Magnemite': {'Type': [Type.ELECTRIC, Type.STEEL], 'HP': 25,
                  'Moves': ['Tackle', 'Flash Cannon', 'Thunder Shock', 'Thunderbolt'], 'Attack': 35,
                  'Defense': 70, 'Speed': 45, 'Experience': 65},
    'Bulbasaur': {'Type': [Type.GRASS, Type.POISON], 'HP': 45, 'Moves': ['Tackle', 'Vine Whip', 'Razor Leaf'],
                  'Attack': 49, 'Defense': 49, 'Speed': 45, 'Experience': 64},
    'Charmander': {'Type': [Type.FIRE], 'HP': 39, 'Moves': ['Scratch', 'Ember', 'Fire Spin'], 'Attack': 52,
                   'Defense': 43, 'Speed': 65, 'Experience': 62},
    'Beedrill': {'Type': [Type.BUG, Type.POISON], 'HP': 65,
                 'Moves': ['Peck', 'Twineedle', 'Rage', 'Fury Attack', 'Outrage'], 'Attack': 90, 'Defense': 40,
                 'Speed': 75, 'Experience': 178},
    'Golem': {'Type': [Type.ROCK, Type.GROUND], 'HP': 80,
              'Moves': ['Tackle', 'Rock Throw', 'Rock Slide', 'Earthquake'], 'Attack': 120, 'Defense': 130,
              'Speed': 45, 'Experience': 223},
    'Dewgong': {'Type': [Type.WATER, Type.ICE], 'HP': 90, 'Moves': ['Aqua Jet', 'Ice Shard', 'Headbutt'],
                'Attack': 70, 'Defense': 80, 'Speed': 70, 'Experience': 166},
    'Hypno': {'Type': [Type.PSYCHIC], 'HP': 85, 'Moves': ['Pound', 'Confusion', 'Dream Eater'], 'Attack': 73,
              'Defense': 70, 'Speed': 67, 'Experience': 169},
    'Cleffa': {'Type': [Type.FAIRY], 'HP': 50, 'Moves': ['Pound', 'Magical Leaf'], 'Attack': 25, 'Defense': 28,
               'Speed': 15, 'Experience': 44},
    'Cutiefly': {'Type': [Type.FAIRY, Type.BUG], 'HP': 40,
                 'Moves': ['Absorb', 'Fairy Wind', 'Struggle Bug', 'Draining Kiss'], 'Attack': 45,
                 'Defense': 40, 'Speed': 84, 'Experience': 61}
}

MOVES_DICTIONARY = {
    'Scratch':
        {
            'name': 'Scratch',
            'power': 40,
            'type': Type.NORMAL,
            'super effective against': [],
            'not very effective against': [Type.ROCK, Type.STEEL]
        },
    'Tackle':
        {
            'name': 'Tackle',
            'power': 40,
            'type': Type.NORMAL,
            'super effective against': [],
            'not very effective against': [Type.ROCK, Type.STEEL]
        },
    'Pound': {'name': 'Pound', 'power': 40, 'type': Type.NORMAL, 'super effective against': [],
              'not very effective against': [Type.ROCK, Type.STEEL]},
    'Rage': {'name': 'Rage', 'power': 20, 'type': Type.NORMAL, 'super effective against': [],
             'not very effective against': [Type.ROCK, Type.STEEL]},
    'Fury Attack': {'name': 'Fury Attack', 'power': 15, 'type': Type.NORMAL, 'super effective against': [],
                    'not very effective against': [Type.ROCK, Type.STEEL]},
    'Ember': {'name': 'Ember', 'power': 40, 'type': Type.FIRE,
              'super effective against': [Type.GRASS, Type.ICE, Type.BUG, Type.STEEL],
              'not very effective against': [Type.FIRE, Type.WATER, Type.ROCK, Type.DRAGON]},
    'Fire Spin': {'name': 'Fire Spin', 'power': 35, 'type': Type.FIRE,
                  'super effective against': [Type.GRASS, Type.ICE, Type.BUG, Type.STEEL],
                  'not very effective against': [Type.FIRE, Type.WATER, Type.ROCK, Type.DRAGON]},
    'Bubble': {'name': 'Bubble', 'power': 40, 'type': Type.WATER,
               'super effective against': [Type.FIRE, Type.GROUND, Type.ROCK],
               'not very effective against': [Type.WATER, Type.GRASS, Type.DRAGON]},
    'Aqua Jet': {'name': 'Aqua Jet', 'power': 40, 'type': Type.WATER,
                 'super effective against': [Type.FIRE, Type.GROUND, Type.ROCK],
                 'not very effective against': [Type.WATER, Type.GRASS, Type.DRAGON]},
    'Thunder Shock': {'name': 'Thunder Shock', 'power': 40, 'type': Type.ELECTRIC,
                      'super effective against': [Type.WATER, Type.FLYING],
                      'not very effective against': [Type.ELECTRIC, Type.GRASS, Type.DRAGON]},
    'Thunderbolt': {'name': 'Thunderbolt', 'power': 90, 'type': Type.ELECTRIC,
                    'super effective against': [Type.WATER, Type.FLYING],
                    'not very effective against': [Type.ELECTRIC, Type.GRASS, Type.DRAGON]},
    'Vine Whip': {'name': 'Vine Whip', 'power': 45, 'type': Type.GRASS,
                  'super effective against': [Type.WATER, Type.GROUND, Type.ROCK],
                  'not very effective against': [Type.FIRE, Type.GRASS, Type.POISON, Type.FLYING, Type.BUG, Type.DRAGON,
                                                 Type.STEEL]},
    'Magical Leaf': {'name': 'Magical Leaf', 'power': 60, 'type': Type.GRASS,
                     'super effective against': [Type.WATER, Type.GROUND, Type.ROCK],
                     'not very effective against': [Type.FIRE, Type.GRASS, Type.POISON, Type.FLYING, Type.BUG,
                                                    Type.DRAGON, Type.STEEL]},
    'Ice Shard': {'name': 'Ice Shard', 'power': 40, 'type': Type.ICE,
                  'super effective against': [Type.GRASS, Type.GROUND, Type.FLYING, Type.DRAGON],
                  'not very effective against': [Type.FIRE, Type.WATER, Type.ICE, Type.STEEL]},
    'Double Kick': {'name': 'Double Kick', 'power': 30, 'type': Type.FIGHTING,
                    'super effective against': [Type.NORMAL, Type.ICE, Type.ROCK, Type.DARK, Type.STEEL],
                    'not very effective against': [Type.POISON, Type.FLYING, Type.PSYCHIC, Type.BUG, Type.FAIRY]},
    'Earthquake': {'name': 'Earthquake', 'power': 100, 'type': Type.GROUND,
                   'super effective against': [Type.FIRE, Type.ELECTRIC, Type.POISON, Type.ROCK, Type.STEEL],
                   'not very effective against': [Type.GRASS, Type.BUG]},
    'Wing Attack': {'name': 'Wing Attack', 'power': 60, 'type': Type.FLYING,
                    'super effective against': [Type.GRASS, Type.FIGHTING, Type.BUG],
                    'not very effective against': [Type.ELECTRIC, Type.ROCK, Type.STEEL]},
    'Peck': {'name': 'Peck', 'power': 35, 'type': Type.FLYING,
             'super effective against': [Type.GRASS, Type.FIGHTING, Type.BUG],
             'not very effective against': [Type.ELECTRIC, Type.ROCK, Type.STEEL]},
    'Confusion': {'name': 'Confusion', 'power': 50, 'type': Type.PSYCHIC,
                  'super effective against': [Type.FIGHTING, Type.POISON],
                  'not very effective against': [Type.PSYCHIC, Type.STEEL]},
    'Twineedle': {'name': 'Twineedle', 'power': 25, 'type': Type.BUG,
                  'super effective against': [Type.GRASS, Type.PSYCHIC, Type.DARK],
                  'not very effective against': [Type.FIRE, Type.FIGHTING, Type.POISON, Type.FLYING, Type.GHOST,
                                                 Type.STEEL, Type.FAIRY]},
    'Rock Throw': {'name': 'Rock Throw', 'power': 50, 'type': Type.ROCK,
                   'super effective against': [Type.FIRE, Type.ICE, Type.FLYING, Type.BUG],
                   'not very effective against': [Type.FIGHTING, Type.GROUND, Type.STEEL]},
    'Rock Slide': {'name': 'Rock Slide', 'power': 75, 'type': Type.ROCK,
                   'super effective against': [Type.FIRE, Type.ICE, Type.FLYING, Type.BUG],
                   'not very effective against': [Type.FIGHTING, Type.GROUND, Type.STEEL]},
    'Lick': {'name': 'Lick', 'power': 30, 'type': Type.GHOST, 'super effective against': [Type.PSYCHIC, Type.GHOST],
             'not very effective against': [Type.DARK]},
    'Outrage': {'name': 'Outrage', 'power': 120, 'type': Type.DRAGON, 'super effective against': [Type.DRAGON],
                'not very effective against': [Type.STEEL]},
    'Crunch': {'name': 'Crunch', 'power': 80, 'type': Type.DARK, 'super effective against': [Type.PSYCHIC, Type.GHOST],
               'not very effective against': [Type.FIGHTING, Type.DARK, Type.FAIRY]},
    'Bite': {'name': 'Bite', 'power': 60, 'type': Type.DARK, 'super effective against': [Type.PSYCHIC, Type.GHOST],
             'not very effective against': [Type.FIGHTING, Type.DARK, Type.FAIRY]},
    'Flash Cannon': {'name': 'Flash Cannon', 'power': 80, 'type': Type.STEEL,
                     'super effective against': [Type.ICE, Type.ROCK, Type.FAIRY],
                     'not very effective against': [Type.FIRE, Type.WATER, Type.ELECTRIC, Type.STEEL]},
    'Smog': {'name': 'Smog', 'power': 30, 'type': Type.POISON, 'super effective against': [Type.GRASS, Type.FAIRY],
             'not very effective against': [Type.POISON, Type.GROUND, Type.ROCK, Type.GHOST]},
    'Dream Eater': {'name': 'Dream Eater', 'power': 100, 'type': Type.PSYCHIC,
                    'super effective against': [Type.FIGHTING, Type.POISON],
                    'not very effective against': [Type.PSYCHIC, Type.STEEL]},
    'Body Slam': {'name': 'Body Slam', 'power': 85, 'type': Type.NORMAL, 'super effective against': [],
                  'not very effective against': [Type.ROCK, Type.STEEL]},
    'Double Slap': {'name': 'Double Slap', 'power': 15, 'type': Type.NORMAL, 'super effective against': [],
                    'not very effective against': [Type.ROCK, Type.STEEL]},
    'Razor Leaf': {'name': 'Razor Leaf', 'power': 55, 'type': Type.GRASS,
                   'super effective against': [Type.WATER, Type.GROUND, Type.ROCK],
                   'not very effective against': [Type.FIRE, Type.GRASS, Type.POISON, Type.FLYING, Type.BUG,
                                                  Type.DRAGON, Type.STEEL]},
    'Headbutt': {'name': 'Headbutt', 'power': 70, 'type': Type.NORMAL, 'super effective against': [],
                 'not very effective against': [Type.ROCK, Type.STEEL]},
    'Absorb': {'name': 'Absorb', 'power': 20, 'type': Type.GRASS,
               'super effective against': [Type.WATER, Type.GROUND, Type.ROCK],
               'not very effective against': [Type.FIRE, Type.GRASS, Type.POISON, Type.FLYING, Type.BUG, Type.DRAGON,
                                              Type.STEEL]},
    'Fairy Wind': {'name': 'Fairy Wind', 'power': 40, 'type': Type.FAIRY,
                   'super effective against': [Type.FIGHTING, Type.DRAGON, Type.DARK],
                   'not very effective against': [Type.FIRE, Type.POISON, Type.STEEL]},
    'Struggle Bug': {'name': 'Struggle Bug', 'power': 50, 'type': Type.BUG,
                     'super effective against': [Type.GRASS, Type.PSYCHIC, Type.DARK],
                     'not very effective against': [Type.FIRE, Type.FIGHTING, Type.POISON, Type.FLYING, Type.GHOST,
                                                    Type.STEEL, Type.FAIRY]},
    'Draining Kiss': {'name': 'Draining Kiss', 'power': 50, 'type': Type.FAIRY,
                      'super effective against': [Type.FIGHTING, Type.DRAGON, Type.DARK],
                      'not very effective against': [Type.FIRE, Type.POISON, Type.STEEL]},
    'Shadow Ball': {'name': 'Shadow Ball', 'power': 80, 'type': Type.GHOST,
                    'super effective against': [Type.PSYCHIC, Type.GHOST], 'not very effective against': [Type.DARK]}
}


@dataclass
class Move:
    name: str
    power: int
    type_: Type
    super_effective_against: list[Type]
    not_very_effective_against: list[Type]


@dataclass
class Pokémon:
    name: str
    type_: list[Type]
    hp: int
    attack: int
    defense: int
    speed: int
    experience: int
    moves: list[Move]
    level: int
    default_hp: int

    def battle(self, sb: 'Pokémon'):
        cmp = self.speed - sb.speed

    def calculate_damage(self, sb: 'Pokémon', move: Move):
        damage = (2 * self.level / 5 + 2) * move.power * self.attack / sb.defense / 50
        critical = 2 if random.randint(0, 511) < self.speed else 1
        damage *= critical
        rand_num = random.uniform(0.85, 1.0)
        damage *= rand_num
        if sb.type_ in move.super_effective_against:
            damage *= 2
        elif sb.type_ in move.not_very_effective_against:
            damage /= 2
        return damage

    def update_level(self):
        pass

    def reset_hp(self):
        self.hp = self.default_hp


@dataclass
class Pokédex:
    pokemons: list[Pokémon]

    def add_pokemon(self):
        pass

    def remove_pokemon(self):
        pass

    def search_pokemon(self):
        pass
