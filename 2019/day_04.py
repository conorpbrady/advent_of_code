# --- Day 4: Secure Container ---
#
# However, they do remember a few key facts about the password:
#
# It is a six-digit number.
# The value is within the range given in your puzzle input.
# Two adjacent digits are the same (like 22 in 122345).
# Going from left to right, the digits never decrease; they only ever increase
# or stay the same (like 111123 or 135679).
#
# How many different passwords within the range given in your puzzle input
# meet these criteria?

# Your puzzle input is 197487-673251.



start = 197487
finish = 673251


def is_valid_password(num):
    num_str = str(num)

    two_adjacent = False
    increasing = True
    counts = []

    for i in range(0,len(num_str)):

        if len(counts) == 0:
            counts.append([num_str[i],1])
        else:
            last_element = counts[-1]
            if last_element[0] == num_str[i]:
                counts[-1][1] += 1
            else:
                counts.append([num_str[i], 1])
        if i == len(num_str) - 1:
            break
        if int(num_str[i]) > int(num_str[i+1]):
            increasing = False
            break

    for count in counts:
        if count[1] == 2:
            two_adjacent = True

    return (two_adjacent and increasing)

possible_passwords = []
for i in range(start,finish):
    if is_valid_password(i):
        possible_passwords.append(i)

print(len(possible_passwords))

# print(is_valid_password(112222))
# print(is_valid_password(112233))
# print(is_valid_password(123444))
# print(is_valid_password(111122))
