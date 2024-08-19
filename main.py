# This is a sample Python script.
from characters import setup, Rank

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    chars = setup()
    for char in chars:
        # print(chars[-3].get_repr_all_commons())
        print(f"{char.__repr__()} - {char.get_repr_all_commons()}\n")
    # for rank in Rank:
    #     print(f"{rank}: {rank.name} - {rank.value}")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
