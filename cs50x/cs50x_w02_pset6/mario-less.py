from cs50 import get_int


def main():
    # prompt the user for input
    height = get_height()
    # print pyramid
    for i in range(1, height + 1):
        for j in range(height, i, -1):
            print(" ", end="")
        for k in range(i):
            print("#", end="")
        print()


def get_height():
    while True:
        n = get_int("How many steps should the pyramid have?: ")
        if n >= 1 and n <= 8:
            break
    return n


main()
