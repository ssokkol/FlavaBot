import re


def remove_special_characters(input_string):
    clean_string = re.sub(r"[^\w\s]", "", input_string)
    return clean_string
