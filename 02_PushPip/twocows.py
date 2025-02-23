import argparse
import cowsay


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-e', default='oo')
    parser.add_argument('-f', default='default')

    parser.add_argument('-E', default='oo')
    parser.add_argument('-F', default='default')
    parser.add_argument('-N', default='  ',)

    parser.add_argument('message1')
    parser.add_argument('message2')

    args = parser.parse_args()

    cow1 = cowsay.cowsay(message=args.message1, cow=args.f, eyes=args.e)
    cow2 = cowsay.cowsay(message=args.message2, cow=args.F, eyes=args.E,
                         tongue=args.N)

    cow1_lines = cow1.split('\n')
    cow2_lines = cow2.split('\n')

    cow1_height = len(cow1_lines)
    cow2_height = len(cow2_lines)

    if cow1_height > cow2_height:
        for i in range(max(cow1_height, cow2_height) - min(cow1_height, cow2_height)):
            cow2_lines.insert(0, " " * len(max(cow2_lines, key=len)))
    else:
        for i in range(max(cow1_height, cow2_height) - min(cow1_height, cow2_height)):
            cow1_lines.insert(0, " " * len(max(cow1_lines, key=len)))


    for i in range(len(cow1_lines)):
        cow1_lines[i] += " " * (len(max(cow1_lines, key=len)) - len(cow1_lines[i]))

    for i in range(len(cow1_lines)):
        line1 = cow1_lines[i]
        line2 = cow2_lines[i]
        print(f"{line1} {line2}")


if __name__ == '__main__':
    main()