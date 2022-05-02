import validators
import re

def normalize_text(line):
    if not line:
        return ""

    trimmed_line = " ".join(line.split())
    split_line = ""
    for word in trimmed_line.split(" "):
        if validators.url(word):
            continue

        split_line += word.lower() + " "

    if not split_line or split_line.isspace():
        return ""

    pattern = re.compile(r"[^A-Za-z ]+", re.UNICODE)
    normalized_line = pattern.sub("", split_line)

    return normalized_line

def main():

    with open('markovClean.txt', "w+", encoding="utf-8") as output_file:
        with open('markov.txt', encoding="utf-8") as input_file:
            for input_line in input_file:
                output_line = normalize_text(input_line.rstrip())
                if output_line: 
                    output_file.write(output_line)

    print("Finished processing.")
    
main()
