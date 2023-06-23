use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

const DATA_DIR : str = "/home/nathan/PycharmProjects/AdventOfCode/2022/inputs/";

fn main() {
    let input_file = DATA_DIR + "day_01_in.txt";

    let mut big_elf_calories = 0;
    // File hosts must exist in current path before this produces output
    if let Ok(lines) = read_lines(input_file) {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            let this_elf = 0;
            if let Ok(ip) = line {
                if ip = "\n" {
                    match big_elf_calories.cmp(&this_elf){
                        Ordering::Greater =>
                    }
                }
            }
        }
    }
}

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}