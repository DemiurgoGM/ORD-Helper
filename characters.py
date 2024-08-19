from collections import defaultdict
from enum import Enum, auto


class Rank(Enum):
    WISP = auto()
    OTHER = auto()
    COMMON = auto()
    UNCOMMON = auto()
    SPECIAL = auto()
    HIDDEN = auto()
    RARE = auto()
    LIMITED = auto()
    ALTERNATE = auto()
    LEGENDARY = auto()
    TRANSCENDED = auto()
    IMMORTAL = auto()
    ETERNITY = auto()


class Character:
    def __init__(self, name, rank, materials, command):
        self.name = name
        self.rank = rank
        self.materials = materials
        self.command = command

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
        name_count = defaultdict(int)  # Creates a dictionary with default integer values
        for character in comms:
            name_count[character.name] += 1
        for name, count in name_count.items():
            retorno += "x" + str(count) + " " + name + ", "
        return retorno[:-2] + "]"

    def __mul__(self, other):
        if isinstance(other, int):
            return tuple(Character(self.name, self.rank, self.materials, self.command) for _ in range(other))

    def __add__(self, other):
        if isinstance(other, tuple):
            return (self,) + other

    def __rmul__(self, other):
        return self.__mul__(other)

    def __radd__(self, other):
        return self.__add__(other)

    def __str__(self):
        return (f"{{Character:{self.name}"
                f"{f'; Rank:{self.rank.name}' if self.rank else ''}"
                f"{f'; Comando:{self.command}' if self.command else ''}"
                f"{f'; Materiais:{self.materials}' if self.materials else ''}}}")

    def __repr__(self):
        return f"{self.name}"


def find_char_in_list(char_list: list[Character], string: str):
    for character in char_list:
        if character.name == string:
            return character
    return False


def setup():
    all_characters = []
    all_characters = all_characters + [
        Character("Wood", Rank.OTHER, (), ""),
        Character("Lucky Token", Rank.OTHER, (), ""),
        Character("Kuma", Rank.OTHER, (), ""),
        Character("Save Count", Rank.OTHER, (), ""),
        Character("Zombie", Rank.OTHER, (), ""),
        Character("Expansion Pack", Rank.OTHER, (), ""),
        Character("Gold", Rank.OTHER, (), ""),
    ]
    all_characters = all_characters + [
        Character("Wisp", Rank.WISP, (), "")
    ]
    all_characters = all_characters + [
        Character("Luffy", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Zoro", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Nami", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Usopp", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Sanji", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Chopper", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Buggy", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Gunman", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),
        Character("Swordsman", Rank.COMMON, (find_char_in_list(all_characters, "Wisp"),), ""),

    ]
    all_characters = all_characters + [
        Character("Ace", Rank.UNCOMMON, (find_char_in_list(all_characters, "Luffy"),
                                         find_char_in_list(all_characters, "Gunman")), ""),
        Character("Robin", Rank.UNCOMMON, (find_char_in_list(all_characters, "Nami"),
                                           find_char_in_list(all_characters, "Sanji")), ""),
        Character("Brook", Rank.UNCOMMON, (find_char_in_list(all_characters, "Zoro"),
                                           find_char_in_list(all_characters, "Chopper")), ""),
        Character("Sogeking", Rank.UNCOMMON, find_char_in_list(all_characters, "Usopp") * 2, ""),
        Character("Franky", Rank.UNCOMMON, (find_char_in_list(all_characters, "Usopp"),
                                            find_char_in_list(all_characters, "Luffy")), ""),
        Character("Fukuro", Rank.UNCOMMON, find_char_in_list(all_characters, "Swordsman") * 2, ""),
        Character("Tashigi", Rank.UNCOMMON, (find_char_in_list(all_characters, "Swordsman"),
                                             find_char_in_list(all_characters, "Gunman")), ""),
        Character("Blueno", Rank.UNCOMMON, find_char_in_list(all_characters, "Gunman") * 2, ""),
        Character("Hatchan", Rank.UNCOMMON, (find_char_in_list(all_characters, "Gunman"),
                                             find_char_in_list(all_characters, "Nami")), ""),
        Character("Perona", Rank.UNCOMMON, (find_char_in_list(all_characters, "Buggy"),
                                            find_char_in_list(all_characters, "Nami")), ""),
        Character("Inazuma", Rank.UNCOMMON, (find_char_in_list(all_characters, "Sanji"),
                                             find_char_in_list(all_characters, "Zoro")), ""),
        Character("Bepo", Rank.UNCOMMON, (find_char_in_list(all_characters, "Chopper"),
                                          find_char_in_list(all_characters, "Luffy")), ""),
        Character("Chopper 2", Rank.UNCOMMON, find_char_in_list(all_characters, "Chopper") * 2, ""),

    ]
    all_characters = all_characters + [
        Character("Luffy 2", Rank.SPECIAL, find_char_in_list(all_characters, "Luffy") * 3, ""),
        Character("Nami 2", Rank.SPECIAL, find_char_in_list(all_characters, "Nami") * 3, ""),
        Character("Sanji 2", Rank.SPECIAL, find_char_in_list(all_characters, "Sanji") * 3, ""),
        Character("Zoro 2", Rank.SPECIAL, find_char_in_list(all_characters, "Zoro") * 3, ""),
        Character("Buggy 2", Rank.SPECIAL, find_char_in_list(all_characters, "Buggy") * 3, ""),
        Character("Robin 2", Rank.SPECIAL, find_char_in_list(all_characters, "Chopper") + find_char_in_list(all_characters, "Robin") * 2
                  , ""),
        Character("Marco", Rank.SPECIAL, (find_char_in_list(all_characters, "Ace"),
                                          find_char_in_list(all_characters, "Blueno"),
                                          find_char_in_list(all_characters, "Sanji")), ""),
        Character("Chaka", Rank.SPECIAL, (find_char_in_list(all_characters, "Blueno"),
                                          find_char_in_list(all_characters, "Fukuro"),
                                          find_char_in_list(all_characters, "Chopper")), ""),
        Character("Lucchi", Rank.SPECIAL, (find_char_in_list(all_characters, "Fukuro"),
                                           find_char_in_list(all_characters, "Robin"),
                                           find_char_in_list(all_characters, "Luffy")), ""),
        Character("Capone", Rank.SPECIAL, (find_char_in_list(all_characters, "Fukuro"),
                                           find_char_in_list(all_characters, "Gunman"),
                                           find_char_in_list(all_characters, "Buggy")), ""),
        Character("Law", Rank.SPECIAL, (find_char_in_list(all_characters, "Bepo"),
                                        find_char_in_list(all_characters, "Tashigi"),
                                        find_char_in_list(all_characters, "Buggy")), ""),
        Character("Kuma", Rank.SPECIAL, (find_char_in_list(all_characters, "Bepo"),
                                         find_char_in_list(all_characters, "Franky"),
                                         find_char_in_list(all_characters, "Zoro")), ""),
        Character("Drake", Rank.SPECIAL, (find_char_in_list(all_characters, "Tashigi"),
                                          find_char_in_list(all_characters, "Fukuro"),
                                          find_char_in_list(all_characters, "Chopper")), ""),
        Character("Killer", Rank.SPECIAL, (find_char_in_list(all_characters, "Tashigi"),
                                           find_char_in_list(all_characters, "Brook"),
                                           find_char_in_list(all_characters, "Buggy")), ""),
        Character("Smoker", Rank.SPECIAL, (find_char_in_list(all_characters, "Gunman")
                                           , find_char_in_list(all_characters, "Tashigi"),
                                           find_char_in_list(all_characters, "Swordsman")), ""),
        Character("Bon Clay", Rank.SPECIAL, (find_char_in_list(all_characters, "Inazuma"),
                                             find_char_in_list(all_characters, "Robin"),
                                             find_char_in_list(all_characters, "Nami")), ""),
        Character("Inazuma 2", Rank.SPECIAL, find_char_in_list(all_characters, "Inazuma") * 2, ""),
        Character("Franky 2", Rank.SPECIAL,
                  find_char_in_list(all_characters, "Franky") * 2 + find_char_in_list(all_characters, "Zoro"), ""),
        Character("Crocodile", Rank.SPECIAL, (find_char_in_list(all_characters, "Franky"),
                                              find_char_in_list(all_characters, "Sogeking"),
                                              find_char_in_list(all_characters, "Buggy")), ""),
        Character("Moria", Rank.SPECIAL,
                  find_char_in_list(all_characters, "Brook") * 2 + find_char_in_list(all_characters, "Sanji"), ""),
        Character("Helmeppo", Rank.SPECIAL, (find_char_in_list(all_characters, "Brook")
                                             , find_char_in_list(all_characters, "Zoro"),
                                             find_char_in_list(all_characters, "Sanji")), ""),
        Character("Ace 2", Rank.SPECIAL,
                  find_char_in_list(all_characters, "Ace") * 2 + find_char_in_list(all_characters, "Usopp"), ""),
        Character("Jinbe", Rank.SPECIAL, (find_char_in_list(all_characters, "Ace"),
                                          find_char_in_list(all_characters, "Fukuro"),
                                          find_char_in_list(all_characters, "Buggy")), ""),
        Character("Arlong", Rank.SPECIAL,
                  find_char_in_list(all_characters, "Hatchan") * 2 + find_char_in_list(all_characters, "Luffy"), ""),
        Character("Kuro", Rank.SPECIAL, (find_char_in_list(all_characters, "Hatchan"),
                                         find_char_in_list(all_characters, "Swordsman"),
                                         find_char_in_list(all_characters, "Zoro")), ""),
        Character("Squard", Rank.SPECIAL, (find_char_in_list(all_characters, "Chopper 2"),
                                           find_char_in_list(all_characters, "Franky"),
                                           find_char_in_list(all_characters, "Nami")), ""),
        Character("Chopper Guard", Rank.SPECIAL, (find_char_in_list(all_characters, "Chopper 2"),
                                                  find_char_in_list(all_characters, "Inazuma"),
                                                  find_char_in_list(all_characters, "Swordsman")), ""),
        Character("Chopper Brain", Rank.SPECIAL, (find_char_in_list(all_characters, "Chopper 2"),
                                                  find_char_in_list(all_characters, "Robin"),
                                                  find_char_in_list(all_characters, "Buggy")), ""),
        Character("Basil", Rank.SPECIAL, (find_char_in_list(all_characters, "Perona"),
                                          find_char_in_list(all_characters, "Blueno"),
                                          find_char_in_list(all_characters, "Usopp")), ""),
        Character("Kidd", Rank.SPECIAL, (find_char_in_list(all_characters, "Perona"),
                                         find_char_in_list(all_characters, "Bepo"),
                                         find_char_in_list(all_characters, "Buggy")), ""),
        Character("Enel", Rank.SPECIAL, (find_char_in_list(all_characters, "Sogeking"),
                                         find_char_in_list(all_characters, "Bepo"),
                                         find_char_in_list(all_characters, "Sanji")), ""),
        Character("Usopp 2", Rank.SPECIAL, find_char_in_list(all_characters, "Sogeking") * 2, ""),
        Character("Absalom", Rank.SPECIAL,
                  find_char_in_list(all_characters, "Zombie") * 3 + find_char_in_list(all_characters, "Nami"), ""),
    ]

    # all_characters = all_characters + [
    #     Character("wisp", Rank.RARE, (), "")
    # ]
    # all_characters = all_characters + [
    #     Character("wisp", Rank.HIDDEN, (), "")
    # ]
    # all_characters = all_characters + [
    #     Character("wisp", Rank.LIMITED, (), "")
    # ]
    #
    # all_characters = all_characters + [
    #     Character("wisp", Rank.ALTERNATE, (), "")
    # ]
    # all_characters = all_characters + [
    #     Character("wisp", Rank.IMMORTAL, (), "")
    # ]
    # all_characters = all_characters + [
    #     Character("wisp", Rank.LEGENDARY, (), "")
    # ]
    # all_characters = all_characters + [
    #     Character("wisp", Rank.TRANSCENDED, (), "")
    # ]
    # all_characters = all_characters + [
    #     Character("wisp", Rank.ETERNITY, (), "")
    # ]
    return all_characters
