from pathlib import Path
import os


def alphebetize_string(s: str):
    l = [c for c in s]
    l.sort()
    return "".join(l)


def decode_numbers(num_list: list):
    """Figure out which number corresponds to which code.

    strategy:
    # ID 1, 4, 7, 8
    # ID 6 by comparing sixes vs 1
    # ID 0 by comparing sixes vs 4
    # ID 9 by elimination

    # ID 3 by comparing vs 1
    # ID 5 vs 2 by comparing to 8-9 or 8-6
    """
    num_list = [alphebetize_string(s) for s in num_list]
    lengths = [len(s) for s in num_list]

    # ID 1, 4, 7, 8
    decoded_dict = {
        num_list[lengths.index(2)]: 1,
        num_list[lengths.index(3)]: 7,
        num_list[lengths.index(7)]: 8,
        num_list[lengths.index(4)]: 4,
    }
    encode_dict = {
        1: {c for c in num_list[lengths.index(2)]},
        7: {c for c in num_list[lengths.index(3)]},
        4: {c for c in num_list[lengths.index(4)]},
        8: {c for c in num_list[lengths.index(7)]},
    }
    sixes = [i for i in range(10) if lengths[i] == 6]
    fives = [i for i in range(10) if lengths[i] == 5]
    # do the 6s
    for idx in sixes:
        n_set = {c for c in num_list[idx]}
        if n_set.issuperset(encode_dict[1]):
            if n_set.issuperset(encode_dict[4]):
                decoded_dict[num_list[idx]] = 9
                encode_dict[9] = n_set
            else:
                decoded_dict[num_list[idx]] = 0
                encode_dict[0] = n_set
        else:
            decoded_dict[num_list[idx]] = 6
            encode_dict[6] = n_set

    # do the 5s
    for idx in fives:
        n_set = {c for c in num_list[idx]}
        if n_set.issuperset(encode_dict[1]):
            decoded_dict[num_list[idx]] = 3
            encode_dict[3] = n_set
        else:
            if not n_set.issuperset(encode_dict[8] - encode_dict[9]):
                decoded_dict[num_list[idx]] = 5
                encode_dict[5] = n_set
            else:
                decoded_dict[num_list[idx]] = 2
                encode_dict[2] = n_set

    return decoded_dict


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2021", "day_08_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    output_digits = [s.split(" | ")[1].split(" ") for s in puzzle_input]
    count_1478 = sum(
        [sum([1 for c in s if len(c) in (2, 3, 4, 7)]) for s in output_digits]
    )
    print(f"Part 1: {count_1478}")

    # Part 2: decode the values, then add them all up!
    digit_sum = 0
    input_digits = [s.split(" | ")[0].split(" ") for s in puzzle_input]
    for p_input, p_output in zip(input_digits, output_digits):
        out_dict = decode_numbers(p_input)
        po = [alphebetize_string(s) for s in p_output]
        out = sum([out_dict[s] * 10 ** (3 - idx) for idx, s in enumerate(po)])
        # print(out)
        digit_sum += out

    print(f"Part 2: {digit_sum}")
