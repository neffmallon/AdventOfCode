import click
from pathlib import Path
import os


def make_day(project_dir, template, year, day):

    if not os.path.exists(os.path.join(project_dir, year)):
        os.mkdir(os.path.join(project_dir, year))

    file = os.path.join(project_dir, year, f"day_{day}.py")
    if not os.path.exists(file):
        with open(file, "w") as f:
            f.write(template.format(year=year, day=day))

        file = os.path.join(project_dir, year, f"day_{day}_in.txt")
        if not os.path.exists(file):
            with open(file, "w") as f:
                pass


@click.command()
@click.argument("year")
@click.option("--day", default=None)
@click.option("--whole_year/--one_day", default=False)
def main(year, day, whole_year):
    project_dir = Path(__file__).resolve().parents[0]
    script_template = """from pathlib import Path
import os

# solution goes here

if __name__ == "__main__":
    project_dir = Path(__file__).resolve().parents[1]
    file = os.path.join(project_dir, "{year}", "day_{day}_in.txt")
    with open(file, "r") as f:
        puzzle_input = [s.strip() for s in f]
"""
    if whole_year or day is None:
        for day in range(1, 26):
            if day < 10:
                day = f"0{day}"
            make_day(project_dir, script_template, year, day)

    else:
        if len(day) == 1:
            day = f"0{day}"
        make_day(project_dir, script_template, year, day)


if __name__ == "__main__":
    main()
