
from collections import defaultdict
from copy import deepcopy
from enum import Enum, auto


class Rank(Enum):
    WISP = auto()
    OTHER = auto()
    COMMON = auto()
    UNCOMMON = auto()
    SPECIAL = auto()
    RARE = auto()
    LIMITED = auto()
    ALTERNATE = auto()
    LEGENDARY = auto()
    HIDDEN = auto()
    TRANSCENDED = auto()
    IMMORTAL = auto()
    ETERNITY = auto()
    RANDOM = auto()


class Character:

    def __init__(self, name, rank, materials, command, other=0):
        self.name = name
        self.rank = rank
        self.materials = materials
        self.command = command
        self.other = other

    def get_all_commons(self) -> list:
        retorno = []
        for material in self.materials:
            if isinstance(material, Character):
                if material.rank != Rank.COMMON and material.rank != Rank.OTHER and material.rank != Rank.WISP:
                    retorno = retorno + material.get_all_commons()
                else:
                    retorno.append(material)
            else:
                retorno.append(material)
        return retorno

    def get_repr_all_commons(self) -> str:
        comms = self.get_all_commons()
        retorno = "["
        name_count = defaultdict(int)
        for character in comms:
            name_count[character.name] += 1
        for name, count in name_count.items():
            retorno += "x" + str(count) + " " + name + ", "
        return retorno[:-2] + "]"

    def get_missing_commons(self, owned: list) -> list:
        retorno = []
        for material in self.materials:
            if material in owned:
                owned.remove(material)
            elif material.rank != Rank.COMMON and material.rank != Rank.OTHER and material.rank != Rank.WISP:
                retorno = retorno + material.get_missing_commons(owned)
            else:
                retorno.append(material)

        return retorno

    def __mul__(self, other):
        if isinstance(other, int):
            return tuple(Character(self.name, self.rank, self.materials, self.command) for _ in range(other))
        else:
            raise TypeError("Expected int but got " + str(type(other)))

    def __eq__(self, other):
        if isinstance(other, str):
            return other == self.name
        elif isinstance(other, Character):
            return self.name == other.name
        else:
            raise TypeError("Expected Character or str, got " + str(type(other)))

    def __add__(self, other):
        if isinstance(other, tuple):
            return (self,) + other
        if isinstance(other, Character):
            if self.rank == other.rank and self.rank == Rank.OTHER and self.name == other.name:
                return Character(self.name, self.rank, self.materials, self.command, self.other+other.other)
            return Character(self.name, self.rank, self.materials, self.command), other
        if isinstance(other, int):
            return Character(self.name, self.rank, self.materials, self.command, self.other+other)
        if isinstance(other, str):
            return Character(self.name, self.rank, self.materials, self.command, other)
        else:
            raise TypeError("Expected Character or tuple, got " + str(type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return (f"{{Character:{self.name}"
                f"{f'; Rank:{self.rank.name}' if self.rank else ''}"
                f"{f'; Command:{self.command}' if self.command else ''}"
                f"{f'; Materiais:{self.materials}' if self.materials else ''}}}")

    def __repr__(self):
        return f"{self.name}"


def find_char_in_list(char_list: list[Character], string: str) -> Character:
    for character in char_list:
        if character == string:
            return character
    raise NameError("Character not found")


def find_best_char_opt(char_list: list[Character], owned: list[Character]) -> list[tuple[Character, list]]:
    all_specials = [char for char in char_list if char.rank == Rank.SPECIAL]
    missings = [(char, char.get_missing_commons(deepcopy(owned))) for char in all_specials]
    retorno = sorted(missings, key=lambda x: len(x[1]))

    return retorno
