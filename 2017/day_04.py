from pathlib import Path
import os


def alphebetize_string(s: str):
    l = [c for c in s]
    l.sort()
    return "".join(l)


def judge_passphrase(line):
    phrase = line.split(" ")
    phrase_set = {word for word in phrase}
    return len(phrase) == len(phrase_set)


def judge_anagram_passphrase(line):
    phrase = [alphebetize_string(s) for s in line.split(" ")]
    phrase_set = {word for word in phrase}
    return len(phrase) == len(phrase_set)


if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "2017", "day_04_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]

    print(f"Part 1: {sum([judge_passphrase(line) for line in puzzle_input])}")
    print(f"Part 2: {sum([judge_anagram_passphrase(line) for line in puzzle_input])}")
