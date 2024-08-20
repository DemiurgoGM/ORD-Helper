
from all_characters import setup
from character import Rank, Character, find_char_in_list, find_best_char_opt

if __name__ == '__main__':
    chars = setup()
    # owned = find_char_in_list(chars, "Usopp") * 3 + find_char_in_list(chars, "Nami")*3 +find_char_in_list(chars, "Swordsman") * 5
    # print(find_best_char_opt(chars, list(owned)))
    for char in chars:
        # print(chars[-3].get_repr_all_commons())
        print(f"{char.__repr__()} - {char.get_repr_all_commons()}\n")
    # for rank in Rank:
    #     print(f"{rank}: {rank.name} - {rank.value}")
