"""
Stolen from: https://github.com/akshaynagpal/w2n and modified a bit
Copied into here for handiness sake



The MIT License (MIT)

Copyright (c) 2016 Akshay Nagpal (https://github.com/akshaynagpal)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from __future__ import print_function


american_number_system = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
    "hundred": 100,
    "thousand": 1000,
    "million": 1000000,
    "billion": 1000000000,
    "trillion": 1000000000,
    "point": ".",
}

decimal_words = {
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
}

three_digit_postfixes = {
    "trillion": 10**12,
    "billion": 10**9,
    "million": 10**6,
    "thousand": 10**3,
}


def number_formation(number_words: list) -> int:
    """
    Form numeric multipliers for million, billion, thousand etc.
    """
    numbers = []
    for number_word in number_words:
        numbers.append(american_number_system[number_word])
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] * numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 100 in numbers:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]


def get_decimal_sum(decimal_digit_words: list) -> float:
    """
    Convert post decimal digit words to numerial digits
    """
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if dec_word not in decimal_words:
            return 0
        else:
            decimal_number_str.append(american_number_system[dec_word])
    final_decimal_string = "0." + "".join(map(str, decimal_number_str))
    return float(final_decimal_string)


def get_subgroup(i):
    g = []
    for mag in {10**1, 10**2, 10**3, 10**6, 10**9, 10**12}:
        if float(i) / mag < 1:
            g.append(mag)
    return min(g)


def word_to_num(number_sentence: str) -> int:
    """
    Function to return integer for an input `number_sentence` string
    """
    if type(number_sentence) is not str:
        raise ValueError("Type of input is not string!")

    number_sentence = number_sentence.replace("-", " ")
    number_sentence = number_sentence.lower()  # converting input to lowercase

    # return the number if user enters a number string
    if number_sentence.isdigit():
        return int(number_sentence)

    # strip extra spaces and split sentence into words
    split_words = number_sentence.strip().split()

    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        if word in american_number_system:
            clean_numbers.append(word)

    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        raise ValueError("No valid number words found!")

    # Error if user enters million,billion, thousand or decimal point twice
    if any(
        [
            clean_numbers.count("thousand") > 1,
            clean_numbers.count("million") > 1,
            clean_numbers.count("billion") > 1,
            clean_numbers.count("trillion") > 1,
            clean_numbers.count("point") > 1,
        ]
    ):
        raise ValueError("Redundant number word!")

    # separate decimal part of number (if exists)
    if clean_numbers.count("point") == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index("point") + 1 :]
        clean_numbers = clean_numbers[: clean_numbers.index("point")]

    trillion_index = (
        clean_numbers.index("trillion") if "trillion" in clean_numbers else -1
    )
    billion_index = clean_numbers.index("billion") if "billion" in clean_numbers else -1
    million_index = clean_numbers.index("million") if "million" in clean_numbers else -1
    thousand_index = (
        clean_numbers.index("thousand") if "thousand" in clean_numbers else -1
    )
    if any(
        [
            all(
                [
                    thousand_index > -1,
                    (
                        thousand_index < million_index
                        or thousand_index < billion_index
                        or thousand_index < trillion_index
                    ),
                ]
            ),
            all(
                [
                    million_index > -1,
                    (million_index < billion_index or million_index < trillion_index),
                ]
            ),
            all([billion_index > -1, billion_index < trillion_index]),
        ]
    ):
        raise ValueError("Malformed number!")

    # groups represents clean_numbers, split into three digit groupings.
    # e.g. ['two', 'million', 'twenty', 'three', 'thousand', 'forty', 'nine'] =>
    # [['two', 'million'], ['twenty', 'three', 'thousand'], ['forty', 'nine']]
    groups = []
    group = []
    for word in clean_numbers:
        group.append(word)
        if word in three_digit_postfixes:
            groups.append(group[:])
            group = []
    if group:
        groups.append(group)

    try:
        equal_subs = (
            len(set([get_subgroup(american_number_system[i]) for i in groups[0]])) == 1
        )
    except:
        equal_subs = False

    if len(groups) == 1 and equal_subs:  # e.g. nine one one = 911
        return int("".join([str(american_number_system[i]) for i in groups[0]]))
    else:
        total_sum = 0  # storing the number to be returned
        for group in groups:
            if group[-1] in three_digit_postfixes:
                three_digit_number_word, postfix = group[:-1], group[-1]
            else:  # the last three digits...
                three_digit_number_word, postfix = group, "unit"
            if three_digit_number_word:
                three_digit_number = number_formation(three_digit_number_word)
            # else if there is no three_digit_number_word, a bare postfix like
            # 'thousand' should be interpreted as 1,000
            else:
                three_digit_number = 1
            postfix_value = three_digit_postfixes.get(postfix, 1)
            total_sum += three_digit_number * postfix_value

        # adding decimal part to total_sum (if exists)
        if len(clean_decimal_numbers) > 0:
            decimal_sum = get_decimal_sum(clean_decimal_numbers)
            total_sum += decimal_sum

        return total_sum
