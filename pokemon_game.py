import random
import zlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import TypedDict


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


class Character(TypedDict):
    Type: list[Type]
    HP: int
    Moves: list[str]
    Attack: int
    Defense: int
    Speed: int
    Experience: int


class MoveDict(TypedDict):
    name: str
    power: int
    type: Type
    super_effective_against: list[Type]
    not_very_effective_against: list[Type]


WELCOME: str
CHARACTERS: dict[str, Character]
MOVES_DICTIONARY: dict[str, MoveDict]

with open("./data/welcome", "rb") as f:
    WELCOME = zlib.decompress(f.read()).decode()

with open("./data/characters", "rb") as f:
    exec(zlib.decompress(f.read()).decode())

with open("./data/moves", "rb") as f:
    exec(zlib.decompress(f.read()).decode())


@dataclass
class Move:
    name: str
    power: int
    type_: Type
    super_effective_against: list[Type]
    not_very_effective_against: list[Type]

    @staticmethod
    def from_dict(data: dict):
        """Transfer the data from the dictionary to the Move class."""
        return Move(data['name'], data['power'], data['type'], data['super effective against'],
                    data['not very effective against'])


@dataclass
class Pokémon(ABC):
    name: str
    type_: list[Type]
    hp: int
    attack: int
    defense: int
    speed: int
    experience: int
    moves: list[Move]
    default_hp: int

    @property
    def level(self):
        """Calculate the level of the Pokémon."""
        return int(self.experience ** (1 / 3)) + 1

    def battle(self, sb: 'Pokémon'):
        self.hp = self.default_hp
        sb.hp = sb.default_hp
        """Pokémon battle."""
        while self.hp > 0 and sb.hp > 0:
            print(f"{self.name}'s HP: {self.hp:.2f}")
            print(f"{sb.name}'s HP: {sb.hp:.2f}")
            move = self.choose_move()
            damage = self.calculate_damage(sb, move)
            sb.hp -= damage
            print(f"{self.name} used {move.name}!")
            print(f"{sb.name} lost {damage:.2f} HP!")
            if sb.hp <= 0:
                print(f"{sb.name} fainted!")
                self.experience += sb.experience
                return True
            move = sb.choose_move()
            damage = sb.calculate_damage(self, move)
            self.hp -= damage
            print(f"{sb.name} used {move.name}!")
            print(f"{self.name} lost {damage:.2f} HP!")
            if self.hp <= 0:
                print(f"{self.name} fainted!")
                return False

    def calculate_damage(self, sb: 'Pokémon', move: Move):
        """Calculate the damage of the move."""
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

    def reset_hp(self):
        """Reset the HP of the Pokémon."""
        self.hp = self.default_hp

    @abstractmethod
    def choose_move(self):
        """Choose a move to attack the other Pokémon."""
        pass

    @classmethod
    def from_dict(cls, name: str):
        """Transfer the data from the dictionary to the Pokémon class."""
        data = CHARACTERS[name]
        moves = [Move.from_dict(MOVES_DICTIONARY[move]) for move in data['Moves']]
        return cls(name, data['Type'], data['HP'], data['Attack'], data['Defense'], data['Speed'], data['Experience'],
                   moves, data['HP'])


class Player(Pokémon):
    def __init__(self, name: str, type_: list[Type], hp: int, attack: int, defense: int, speed: int, experience: int,
                 moves: list[Move], default_hp: int):
        super().__init__(name, type_, hp, attack, defense, speed, experience, moves, default_hp)

    def choose_move(self):
        print(f"{self.name}'s moves:")
        for i, move in enumerate(self.moves):
            print(f"{i + 1}. {move.name}")
        move = int(input(f"Choose a move (1-{len(self.moves)}): "))
        while move not in range(1, len(self.moves) + 1):
            move = int(input(f"Invalid input! Choose a move (1-{len(self.moves)}): "))
        return self.moves[move - 1]


class Computer(Pokémon):
    def __init__(self, name: str, type_: list[Type], hp: int, attack: int, defense: int, speed: int, experience: int,
                 moves: list[Move], default_hp: int):
        super().__init__(name, type_, hp, attack, defense, speed, experience, moves, default_hp)

    def choose_move(self):
        return self.moves[random.randint(0, len(self.moves) - 1)]


@dataclass
class Pokédex:
    pokemons: list[Pokémon]

    def add_pokemon(self, pokemon: Pokémon):
        """Add a Pokémon to the Pokédex."""
        self.pokemons.append(pokemon)
        return self.pokemons.index(pokemon)

    def remove_pokemon(self, pokemon: Pokémon):
        """Remove a Pokémon from the Pokédex."""
        self.pokemons.remove(pokemon)


def introduction():
    """Introduce the game to the user."""
    new = input("Are you new to this game? (yes/no): ")
    if new == 'yes':
        # introduce user how this game works
        print("This is a turn-based game. You will be given a Pokémon and you will have to battle other Pokémon.")
        print("You can choose 1 Pokémon from 3 Pokémon to start with. Each Pokémon has different stats and moves.")
        print("You can choose a move to attack the other Pokémon.")
        print("Your Pokémon has several stats such as HP, Attack, Defense, and Speed.")
        print("HP is the health points of your Pokémon. When it reaches 0, your Pokémon faints.")
        print("Attack is the strength of your Pokémon's attack.")
        print("Defense is the strength of your Pokémon's defense.")
        print("Speed is the speed of your Pokémon. The Pokémon with the higher speed will attack first.")
        # damage calculation
        print("The damage of your Pokémon's move is calculated by the following formula:")
        print("damage = (2 * level / 5 + 2) * move_power * attack / defense / 50 + 2")
        print("The level of your Pokémon is calculated by the following formula:")
        print("level = experience ** (1 / 3) + 1")
        print("The damage can be critical. The chance of a critical hit is determined by the speed of your Pokémon.")
        print("The damage can be random. The damage is multiplied by a random number between 0.85 and 1.0.")
        print("The game ends when all your Pokémon are fainted.")
    else:
        print("Goodbye!")


def begin_choose_pokémon() -> Pokémon:
    """Choose a Pokémon to start with."""
    print("Choose a Pokémon to start with:")
    print("1. Bulbusaur")
    print("2. Charmander")
    print("3. Squirtle")
    pokemon = input("Choose a Pokémon (1/2/3): ")
    while pokemon not in ['1', '2', '3']:
        print("Invalid input! Please choose a Pokémon from 1 to 3.")
        pokemon = input("Choose a Pokémon (1/2/3): ")
    match pokemon:
        case '1':
            return Player.from_dict("Bulbasaur")
        case '2':
            return Player.from_dict("Charmander")
        case '3':
            return Player.from_dict("Squirtle")


def computer_choose_pokémon() -> Pokémon:
    """The computer chooses a Pokémon."""
    pokemon = random.choice(list(CHARACTERS.keys()))
    return Computer.from_dict(pokemon)


def choose_pokémon(pokemons) -> Pokémon:
    """Choose a Pokémon to start with."""
    print("Choose a Pokémon to start with:")
    for i in range(len(pokemons)):
        print(f"{i + 1}. {pokemons[i].name}")
    pokemon = int(input(f"Choose a Pokémon (1-{len(pokemons)}): "))
    while pokemon not in range(1, len(pokemons) + 1):
        print(f"Invalid input! Please choose a Pokémon from 1 to {len(pokemons)}.")
        pokemon = int(input(f"Choose a Pokémon (1-{len(pokemons)}): "))
    return pokemons[pokemon - 1]


def main():
    """The main function of the game."""
    print(WELCOME)
    print('Welcome to the Pokémon game!')
    introduction()
    player = Pokédex([begin_choose_pokémon()])
    print(f"You chose {player.pokemons[0].name}!")
    computer_pokemon = computer_choose_pokémon()
    print(f"The computer chose {computer_pokemon.name}!")
    result = player.pokemons[0].battle(computer_pokemon)
    if not result and len(player.pokemons) == 1:
        print("You lost the game!")
        return
    if result:
        print("You won the game!")
        if computer_pokemon.name not in [pokemon.name for pokemon in player.pokemons]:
            player.add_pokemon(Player.from_dict(computer_pokemon.name))
            print(f"You got {computer_pokemon.name}!")
    print("Do you want to keep playing?")
    keep_playing = input("yes/no: ")
    if keep_playing == 'no':
        print("Goodbye!")
        return
    player_pokemon = player.add_pokemon(choose_pokémon(player.pokemons))
    while True:
        computer_pokemon = computer_choose_pokémon()
        result = player.pokemons[player_pokemon].battle(computer_pokemon)
        if not result and len(player.pokemons) == 1:
            print("You lost the game!")
            return
        if result:
            print("You won the game!")
            if computer_pokemon.name not in [pokemon.name for pokemon in player.pokemons]:
                player.add_pokemon(Player.from_dict(computer_pokemon.name))
                print(f"You got {computer_pokemon.name}!")
        print("Do you want to keep playing?")
        keep_playing = input("yes/no: ")
        if keep_playing == 'no':
            print("Goodbye!")
            return
        player_pokemon = player.pokemons.index(choose_pokémon(player.pokemons))


if __name__ == '__main__':
    main()
