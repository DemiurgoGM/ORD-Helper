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
    """
    A class to represent a character with a name, rank, required materials, and optional attributes like command and other.
    """

    def __init__(self, name: str, rank: Rank, materials: tuple, command: str = "", other: int | str = 0):
        """
        Initialize the Character object.

        :param name: The name of the character.
        :param rank: The rank of the character.
        :param materials: A list of materials needed by the character. These can be other Character objects.
        :param command: The optional command to merge the necessary materials into this character.
        :param other: An additional optional attribute, defaulting to 0. Usually for Wood and Gold.
        """
        self.name = name
        self.rank = rank
        self.materials = materials
        self.command = command
        self.other = other

    def get_all_commons(self) -> list:
        """
        Recursively retrieve all materials with the rank of COMMON from the character's materials list.

        :return: A list of all common materials required by the character.
        """
        retorno = []  # Initialize an empty list to store common materials
        for material in self.materials:
            if isinstance(material, Character):
                # Recursively retrieve common materials from nested Character objects if they are not of a certain rank
                if material.rank != Rank.COMMON and material.rank != Rank.OTHER and material.rank != Rank.WISP:
                    retorno += material.get_all_commons()
                else:
                    retorno.append(material)
            else:
                # If the material is not a Character, simply add it to the list
                retorno.append(material)
        return retorno

    def get_repr_all_commons(self) -> str:
        """
        Get a string representation of all common materials required by the character.

        :return: A string listing all common materials and their quantities.
        """
        comms = self.get_all_commons()  # Retrieve all common materials
        return format_missing_char(comms)

    def get_missing_commons(self, owned: list) -> list:
        """
        Determine which common materials are still needed, based on a list of owned materials.

        :param owned: A list of materials that are already owned.
        :return: A list of common materials that are still missing.
        """
        retorno = []  # Initialize an empty list to store missing common materials
        for material in self.materials:
            if material in owned:
                owned.remove(material)  # Remove owned materials from the list
            elif material.rank != Rank.COMMON and material.rank != Rank.OTHER and material.rank != Rank.WISP:
                # Recursively check for missing commons in nested Character objects
                retorno += material.get_missing_commons(owned)
            else:
                retorno.append(material)  # Add missing materials to the list

        return retorno

    def __mul__(self, other):
        """
        Define the multiplication operation for the Character class.
        If multiplied by an integer, it returns a tuple with the Character repeated that many times.

        :param other: An integer specifying the number of repetitions.
        :return: A tuple of repeated Character objects.
        """
        if isinstance(other, int):
            if str(self.other) == str(0):
                return tuple(Character(self.name, self.rank, self.materials, self.command, self.other) for _ in range(other))
            else:
                return Character(self.name, self.rank, self.materials, self.command, self.other*other)
        else:
            raise TypeError("Expected int but got " + str(type(other)))

    def __eq__(self, other):
        """
        Define the equality operation for the Character class.
        Allows comparison with either a string (name) or another Character object.

        :param other: A string or Character object to compare.
        :return: True if the names match, otherwise False.
        """
        if isinstance(other, str):
            return other == self.name
        elif isinstance(other, Character):
            return self.name == other.name
        else:
            raise TypeError("Expected Character or str, got " + str(type(other)))

    def __add__(self, other):
        """
        Define the addition operation for the Character class.
        Supports adding a Character to a tuple, list, another Character, an integer, or a string.

        :param other: The object to add to the Character.
        :return: A new Character object or a collection containing the Character.
        """
        if isinstance(other, tuple):
            return (self,) + other
        if isinstance(other, list):
            return other + [self]
        if isinstance(other, Character):
            return Character(self.name, self.rank, self.materials, self.command), other
        if isinstance(other, int):
            return Character(self.name, self.rank, self.materials, self.command, int(self.other) + other)
        if isinstance(other, str):
            return Character(self.name, self.rank, self.materials, self.command, str(self.other) + other)
        else:
            raise TypeError("Expected Character or tuple, got " + str(type(other)))

    def __rmul__(self, other):
        """
        Define the right-multiplication operation for the Character class.
        Allows an integer to multiply a Character.

        :param other: An integer specifying the number of repetitions.
        :return: A tuple of repeated Character objects.
        """
        return self.__mul__(other)

    def __radd__(self, other):
        """
        Define the right-addition operation for the Character class.
        Supports adding the Character to the left-hand side of a tuple, list, or another Character.

        :param other: The object to add the Character to.
        :return: A new Character object or a collection containing the Character.
        """
        return self.__add__(other)

    def __str__(self):
        """
        Define the string representation of the Character.

        :return: A formatted string showing the Character's details.
        """
        return (f"{{Character:{self.name}"
                f"{f'; Rank:{self.rank.name}' if self.rank else ''}"
                f"{f'; Command:{self.command}' if self.command else ''}"
                f"{f'; Other:{self.other}' if self.other else ''}"
                f"{f'; Materials:{self.materials}' if self.materials else ''}}}")

    def __repr__(self):
        """
        Define the formal representation of the Character.

        :return: The name of the Character.
        """
        return f"{self.name}"


def find_char_in_list(char_list: list[Character], string: str) -> Character:
    """
    Search for a Character in a list by name.

    :param char_list: The list of Character objects to search through.
    :param string: The name of the Character to find.
    :return: The Character object with the matching name.
    :raises NameError: If the Character is not found in the list.
    """

    for character in char_list:
        if character.name == string:
            return character
    raise NameError("Character not found")


def find_best_char_opt(char_list: list[Character], owned: list[Character]) -> list[tuple[Character, list]]:
    """
    Find the best Character options based on which have the fewest missing common materials.

    :param char_list: The list of potential Character objects to evaluate.
    :param owned: A list of already owned Character objects.
    :return: A sorted list of tuples, each containing a Character and a list of its missing common materials.
    """

    best_chars = [char for char in char_list if char.rank == Rank.LEGENDARY]  # Filter characters with the best rank
    # Determine missing materials for each character
    missings = [(char, char.get_missing_commons(deepcopy(owned))) for char in best_chars]
    retorno = sorted(missings, key=lambda x: len(x[1]))  # Sort the characters by the number of missing materials

    return retorno


def format_missing_char(chars: list[Character]) -> str:
    """
    Generate a formatted string that lists the names of characters and their counts from a given list of Character objects.

    :param chars: A list of Character objects, potentially containing duplicates.
    :return: A string that represents the characters and their counts in the format "[xN Name, xM Name, ...]".
    """
    retorno = "["  # Initialize the string representation
    name_count = defaultdict(int)  # Dictionary to count occurrences of each character's name

    # Iterate over the list of Character objects
    for character in chars:
        if str(character.other) != str(0):
            name_count[character.name] += character.other
        else:
            name_count[character.name] += 1  # Increment the count for each character name

    # Build the formatted string with character names and their respective counts
    for name, count in name_count.items():
        retorno += "x" + str(count) + " " + name + ", "  # Append the count and name to the string

    return retorno[:-2] + "]"  # Return the string, removing the trailing comma and space, and closing with a bracket


def find_possible_evolutions(all_characters: list[Character], character: Character) -> list[Character]:
    """
    Finds and returns a list of characters for which the given character can serve as a material,
    either directly or indirectly (through recursive chains of materials).

    The results are sorted by the rank of the characters in descending order, with higher-ranked characters appearing first.

    :param all_characters: A list of all possible characters in the game.
    :param character: The character to check as a potential material for others.
    :return: A sorted list of characters that can use the given character as a material, directly or indirectly.
    """
    # filtered = list(filter(lambda char_: char_.rank == Rank.LEGENDARY, all_characters))
    filtered = all_characters

    # Helper function to perform recursive search
    def is_material_for(target: Character, material: Character) -> bool:
        # Base case: if the material is directly in the target's materials
        if material.rank > target.rank:
            return False
        if target.rank == material.rank:
            return target == material
        # Recursive case: check if the material is indirectly used in the target's materials
        for sub_material in target.materials:
            if is_material_for(sub_material, material):
                return True
        return False

    possible_evolutions = []

    # Iterate over all characters in the list
    for char in filtered:
        if is_material_for(char, character):
            possible_evolutions.append(char)

    return possible_evolutions
