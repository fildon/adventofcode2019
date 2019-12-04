#     It is a six-digit number.
#     The value is within the range given in your puzzle input.
#     Two adjacent digits are the same (like 22 in 122345).
#     Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).

# Other than the range rule, the following are true:

#     111111 meets these criteria (double 11, never decreases).
#     223450 does not meet these criteria (decreasing pair of digits 50).
#     123789 does not meet these criteria (no double).

# How many different passwords within the range given in your puzzle input meet these criteria?

# Your puzzle input is 197487-673251.

###

# By manual reasoning 222222 is smallest satisfier
# By manual reasoning 669999 is largest satisfier


def is_criteria_match(candidate):
    return not decreases(candidate) and has_pair(candidate)

def decreases(candidate):
    previous = -1
    for digit in list(map(lambda x: int(x), str(candidate))):
        if digit < previous:
            return True
        previous = digit
    return False

def has_pair(candidate):
    previous = -1
    for digit in list(map(lambda x: int(x), str(candidate))):
        if digit == previous:
            return True
        previous = digit
    return False

matches_found = 0
for candidate in range(197487, 673251):
    if is_criteria_match(candidate):
        matches_found = matches_found + 1

print(matches_found)
