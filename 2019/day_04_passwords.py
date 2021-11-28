def is_valid(password: int):
    password_str = str(password)
    for i in range(len(str(password)) - 1):
        if int(password_str[i]) > int(password_str[i + 1]):
            return False
    for i in range(len(str(password)) - 1):
        if int(password_str[i]) == int(password_str[i + 1]):
            if i < len(str(password)) - 2:
                if int(password_str[i + 1]) == int(password_str[i + 2]):
                    continue
            if i > 0:
                if int(password_str[i]) == int(password_str[i - 1]):
                    continue
            return True
    return False


if False:
    password_count = 0
    passwords = []
    for i in range(256310, 732736):
        if is_valid(i):
            password_count += 1
            passwords.append(i)
