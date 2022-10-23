from cs50 import get_int


def main():
    # prompt the user for input
    height = get_height()
    # print pyramids. for each row
    for i in range(height):
        # conditional statement. printing inverse space_pyramid and hashsigns
        for j in range(1, height, 1):
            if i + j >= height:
                print("#", end="")
            else:
                print(" ", end="")
        # printing the unchanging part
        print("#", end="")
        print(" ", end="")
        print(" ", end="")
        print("#", end="")
        # printing normal pyramid
        for k in range(height):
            if i > k:
                print("#", end="")
        print()


def get_height():
    # repeat loop for getting input
    while True:
        n = get_int("How many steps should the pyramid have?: ")
        if n >= 1 and n <= 8:
            break
    return n


main()
