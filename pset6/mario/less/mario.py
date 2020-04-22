from cs50 import get_int


class main(object):
    while True:
        # It will prompt for height
        h = get_int("enter height")
        # Check condition if user enter invalid height
        if(h >= 1 and h <= 8):
            break
    for i in range(h):
        for j in range(h - i - 1):
            print(f" ", end="")
        for k in range(i + 1):
            print(f"#", end="")
        print()


if __name__ == '__main__':
    main()