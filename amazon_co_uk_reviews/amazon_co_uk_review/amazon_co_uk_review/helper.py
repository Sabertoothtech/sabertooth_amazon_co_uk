import re

def extract_number(input_string, thousand_separator=',', scale_separator='.'):

    input_string = str(input_string).replace(thousand_separator, "")
    input_string = input_string.replace(scale_separator, ".")

    numbers = re.findall(r'\d+', input_string)
    if numbers:
        return float(numbers[0])
    else:
        return 0

