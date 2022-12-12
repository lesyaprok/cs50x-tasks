# print out a half-pyramid of a specified height
def main():
    height = get_height()
    print_pyramid(height)


# prompt the user for the half-pyramid’s height, a positive integer between 1 and 8, inclusive.
def get_height():
    while True:
        try:
            height = int(input("Enter the height: "))
            if (height < 1 or height > 8):
                continue
            return height
        except ValueError:
            continue


# generate half-pyramid of a specified height
def print_pyramid(height):
    spaces_count = height - 1
    hashes_count = 1

    while spaces_count >= 0:
        if spaces_count > 0:
            for i in range(spaces_count):
                print(" ", end="")
        for i in range(hashes_count):
            print("#", end="")
        print("")
        spaces_count -= 1
        hashes_count += 1


if __name__ == "__main__":
    main()
