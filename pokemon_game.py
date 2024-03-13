import random
from rich.console import Console
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


INTRO: str
WELCOME: str
CHARACTERS: dict[str, Character]
MOVES_DICTIONARY: dict[str, MoveDict]
console = Console()

with open("./data/intro", "rb") as f:
    INTRO = zlib.decompress(f.read()).decode()

with open("./data/welcome", "rb") as f:
    WELCOME = zlib.decompress(f.read()).decode()

with open("./data/characters", "rb") as f:
    exec(zlib.decompress(f.read()).decode())

with open("./data/moves", "rb") as f:
    exec(zlib.decompress(f.read()).decode())


def buy_me_a_coffee():
    """Buy me a coffee!"""
    console.print("If you like the game, please consider buying me a coffee!", style="bold green")
    console.print("https://www.buymeacoffee.com/brandenxia", style="bold green")


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
class Pokemon(ABC):
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

    def battle(self, sb: 'Pokemon'):
        cmp = self.speed - sb.speed
        if cmp > 0:
            atk, defend = self, sb
        elif cmp < 0:
            atk, defend = sb, self
        else:
            atk, defend = self, sb
            if random.randint(0, 1):
                atk, defend = sb, self

        atk.reset_hp()
        defend.reset_hp()
        """Pokémon battle."""
        while atk.hp > 0 and defend.hp > 0:
            console.print(f"{atk.name}'s HP: {atk.hp:.2f}/{atk.default_hp} DEF: {atk.defense} ATK: {atk.attack} LV: {atk.level} SPEED: {atk.speed}", style="bold green")
            console.print(f"{defend.name}'s HP: {defend.hp:.2f}/{defend.default_hp} DEF: {defend.defense} ATK: {defend.attack} LV: {defend.level} SPEED: {defend.speed}", style="bold yellow")
            move = atk.choose_move()
            damage = atk.calculate_damage(defend, move)
            defend.hp -= damage
            console.print(f"{atk.name} used {move.name}!", style="bold green")
            console.print(f"{defend.name} lost {damage:.2f} HP!", style="bold yellow")
            if defend.hp <= 0:
                console.print(f"{defend.name} fainted!", style="bold yellow")
                atk.experience += defend.experience
                return True
            move = defend.choose_move()
            damage = defend.calculate_damage(atk, move)
            atk.hp -= damage
            console.print(f"{defend.name} used {move.name}!", style="bold yellow")
            console.print(f"{atk.name} lost {damage:.2f} HP!", style="bold green")
            if atk.hp <= 0:
                console.print(f"{atk.name} fainted!", style="bold red")
                return False

    def calculate_damage(self, sb: 'Pokemon', move: Move):
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


class Player(Pokemon):
    def __init__(self, name: str, type_: list[Type], hp: int, attack: int, defense: int, speed: int, experience: int,
                 moves: list[Move], default_hp: int):
        super().__init__(name, type_, hp, attack, defense, speed, experience, moves, default_hp)

    def choose_move(self):
        console.print(f"Choose a move for {self.name}:", style="bold green")
        for i in range(len(self.moves)):
            console.print(f"{i + 1}. {self.moves[i].name}", style="bold blue", end=" ")
            console.print(f"({self.moves[i].type_.name})", style="white", end=" ")
            console.print(f"({self.moves[i].power} power)", style="white")
        move = int(console.input(f"Choose a move (1-{len(self.moves)}): "))
        while move not in range(1, len(self.moves) + 1):
            console.print(f"Invalid input! Please choose a move from 1 to {len(self.moves)}.", style="bold red")
            move = int(console.input(f"Choose a move (1-{len(self.moves)}): "))
        return self.moves[move - 1]


class Computer(Pokemon):
    def __init__(self, name: str, type_: list[Type], hp: int, attack: int, defense: int, speed: int, experience: int,
                 moves: list[Move], default_hp: int):
        super().__init__(name, type_, hp, attack, defense, speed, experience, moves, default_hp)

    def choose_move(self):
        return self.moves[random.randint(0, len(self.moves) - 1)]


@dataclass
class Pokedex:
    pokemons: list[Pokemon]

    def add_pokemon(self, pokemon: Pokemon):
        """Add a Pokémon to the Pokédex."""
        self.pokemons.append(pokemon)
        return self.pokemons.index(pokemon)

    def remove_pokemon(self, pokemon: Pokemon):
        """Remove a Pokémon from the Pokédex."""
        self.pokemons.remove(pokemon)


def introduction():
    """Introduce the game to the user."""
    new = console.input("Are you new to this game? (yes/no): ")
    if new == 'yes':
        console.print(INTRO, style="bold green")
    else:
        console.print("Welcome back to the Pokémon game!", style="bold green")


def begin_choose_pokemon() -> Pokemon:
    """Choose a Pokémon to start with."""
    console.print("Choose a Pokémon to start with:", style="bold green")
    console.print("1. Bulbusaur [Poison, Grass]", style="bold green")
    console.print("2. Charmander [Fire]", style="bold green")
    console.print("3. Squirtle [Water]", style="bold green")
    pokemon = console.input("Choose a Pokémon (1/2/3): ")
    while pokemon not in ['1', '2', '3']:
        console.print("Invalid input! Please choose a Pokémon from 1 to 3.", style="bold red")
        pokemon = console.input("Choose a Pokémon (1/2/3): ")
    match pokemon:
        case '1':
            return Player.from_dict("Bulbasaur")
        case '2':
            return Player.from_dict("Charmander")
        case '3':
            return Player.from_dict("Squirtle")


def computer_choose_pokemon() -> Pokemon:
    """The computer chooses a Pokémon."""
    pokemon = random.choice(list(CHARACTERS.keys()))
    return Computer.from_dict(pokemon)


def choose_pokemon(pokemons) -> Pokemon:
    """Choose a Pokémon to start with."""
    console.print("Choose a Pokémon to start with:", style="bold green")
    for i in range(len(pokemons)):
        console.print(f"{i + 1}. {pokemons[i].name}", style="bold green")
    pokemon = int(console.input(f"Choose a Pokémon (1-{len(pokemons)}): "))
    while pokemon not in range(1, len(pokemons) + 1):
        console.print(f"Invalid input! Please choose a Pokémon from 1 to {len(pokemons)}.", style="bold red")
        pokemon = int(console.input(f"Choose a Pokémon (1-{len(pokemons)}): "))
    return pokemons[pokemon - 1]


def main():
    """The main function of the game."""
    console.print(WELCOME, style="bold red")
    console.print("Welcome to the Pokémon game!", style="bold green")
    introduction()
    player = Pokedex([begin_choose_pokemon()])

    while True:
        computer_pokemon = computer_choose_pokemon()
        console.print(f"The computer chose {computer_pokemon.name} ({[type_.name for type_ in computer_pokemon.type_]})", style="bold yellow")
        player_pokemon = player.pokemons.index(choose_pokemon(player.pokemons))
        result = player.pokemons[player_pokemon].battle(computer_pokemon)
        if not result and len(player.pokemons) == 1:
            console.print("You lost the game!", style="bold red")
            return
        if result:
            console.print("You won the game!", style="bold green")
            if computer_pokemon.name not in [pokemon.name for pokemon in player.pokemons]:
                player.add_pokemon(Player.from_dict(computer_pokemon.name))
                console.print(f"You caught {computer_pokemon.name}!", style="bold green")
        console.print("Do you want to continue playing?", style="bold green")
        keep_playing = console.input("yes/no: ")
        if keep_playing == 'no':
            console.print("Thank you for playing the game! Goodbye!", style="bold green")
            return


if __name__ == '__main__':
    buy_me_a_coffee()
    main()
