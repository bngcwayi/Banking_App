import random
import string


def generate_password(length=12):
    # Define the character sets for each type of character
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine all character sets
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters

    # Ensure at least one character from each set in the password
    password = random.choice(lowercase_letters) + random.choice(uppercase_letters) + random.choice(
        digits) + random.choice(special_characters)

    # Generate the remaining part of the password
    password += ''.join(random.choice(all_characters) for _ in range(length - 4))

    # Shuffle the password to make the characters random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password


# Generate a password of default length (12 characters)
generated_password = generate_password()
print("Generated Password:", generated_password)