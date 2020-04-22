from cs50 import get_float


class main(object):
    while True:
        amt = get_float("enter amount ")
        if(amt > 0.0):
            break
    amt *= 100
    c = 0
    c += amt // 25
    amt %= 25
    c += amt // 10
    amt %= 10
    c += amt // 5
    amt %= 5
    c += amt
    print(c)


if __name__ == '__main__':
    main()