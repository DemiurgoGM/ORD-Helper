from all_characters import setup
from character import Rank, Character, find_char_in_list, find_best_char_opt, format_missing_char

all_characters = setup()


def see_all_chars() -> None:
    """
    Prints the representation of all characters along with their associated common materials.

    This function iterates over the global list of `all_characters` and prints each character's
    name and a summary of the common materials associated with that character.
    """
    for char in all_characters:
        # Print the character's name and a list of all common materials they require.
        print(f"{char.__repr__()} - {char.get_repr_all_commons()}\n")


def see_best_opt_chars(owned_: tuple) -> None:
    """
    Prints the top character options based on the materials currently owned by the player.

    This function finds the best character options that the player can work towards,
    given the materials they currently own. It then prints the top results, showing each character and the materials
    still needed to complete them.

    :param owned_: A tuple containing the characters (materials) the player currently owns.
    """
    # Find the best character options based on owned materials.
    results = find_best_char_opt(all_characters, list(owned_))

    # Iterate through the top results and print their details.
    for i, result in enumerate(results):
        print(f"{result[0].__repr__()} - {format_missing_char(result[1])}\n")
        if i > 3:
            break  # Limit output to the top 4 characters to avoid overwhelming the player.


if __name__ == '__main__':
    print()
    owned = find_char_in_list(all_characters, "Luffy") * 3 + find_char_in_list(all_characters, "Chopper") * 3 + find_char_in_list(all_characters,
                                                                                                                "Buggy") * 5
    see_best_opt_chars(owned)
    # see_all_chars()
