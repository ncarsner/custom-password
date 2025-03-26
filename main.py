#!../custom-password/.venv/Scripts/python

import random
import string
import argparse
import pyperclip


def generate_password(
    length,
    require_alpha=2,
    require_lower=1,
    require_upper=1,
    require_digits=2,
    require_punctuation=1,
    allowed_punctuation=None,
    prohibited_punctuation=None,
):
    """
    Generate a random password with specified requirements.

    Args:
        length (int): Length of the password.
        require_alpha (int): Minimum number of alphabetic characters.
        require_lower (int): Minimum number of lowercase characters.
        require_upper (int): Minimum number of uppercase characters.
        require_digits (int): Minimum number of digits.
        allowed_punctuation (str, optional): String of allowed punctuation characters.
        prohibited_punctuation (str, optional): String of prohibited punctuation.

    Returns:
        str: Generated password.
    """
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation
    all_chars = string.ascii_letters + string.digits + string.punctuation

    # Remove prohibited punctuation from the allowed punctuation set
    if prohibited_punctuation:
        allowed_punctuation = "".join(
            [char for char in punctuation if char not in prohibited_punctuation]
        )

    # Ensure the password meets requirements
    while True:
        password = []
        password.extend(random.choices(lowercase, k=require_lower))
        password.extend(random.choices(uppercase, k=require_upper))
        password.extend(random.choices(digits, k=require_digits))
        password.extend(random.choices(allowed_punctuation, k=require_punctuation))
        password.extend(random.choices(all_chars,
                k=length
                - sum(
                    [
                        require_lower,
                        require_upper,
                        require_digits,
                        require_punctuation,
                    ]
                ),
            )
        )

        # Shuffle the password to randomize character positions
        random.shuffle(password)

        # Convert list to string
        password = "".join(password)

        # Check if the password meets criteria
        if (
            sum(c.isalpha() for c in password) >= require_alpha
            and sum(c.isdigit() for c in password) >= require_digits
        ):
            return password


def main():
    """
    Main function to parse arguments and generate a password.

    Usage:
        python main.py [-sa] [-e] [-d <length>]

    Options:
        -sa  Generate password for system type 1 (all punctuation allowed, length between 15 and 28)
        -e   Generate password for system type 2 (length between 8 and 32)
        -d   Specify the length of the password

    If no options are provided, password with length 8-28 characters is generated.
    """
    parser = argparse.ArgumentParser(description="Custom Password Generator")
    parser.add_argument(
        "-sa",
        action="store_true",
        help="Generate password for system type 1 (all punctuation allowed, length between 15 and 28)",
    )
    parser.add_argument(
        "-e",
        action="store_true",
        help="Generate password for system type 2 (length between 8 and 32)",
    )
    parser.add_argument(
        "-d",
        type=int,
        help="Specify the length of the password",
    )
    args = parser.parse_args()

    if args.e and args.sa:
        print("Error: Cannot use both -e and -sa flags together.")
        raise SystemExit(1)
    if args.sa:
        if args.d is None:
            args.d = 15
        elif not (15 <= args.d <= 28):
            print("Error: For -sa flag, length must be between 15 and 28.")
            raise SystemExit(1)
    elif args.e:
        if args.d is None:
            args.d = 8
        elif not (8 <= args.d <= 32):
            print("Error: For -e flag, length must be between 8 and 32.")
            raise SystemExit(1)
    else:
        if args.d is None:
            args.d = 8
        elif not (8 <= args.d <= 28):
            print("Error: Password length must be between 8 and 28 characters.")
            raise SystemExit(1)

    if args.e:
        password = generate_password(
            args.d,
            require_alpha=2,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            require_punctuation=1,
            allowed_punctuation=".!#$*()+=",
            prohibited_punctuation="&<>”‘%~'\"`@{}/\\",
        )
    elif args.sa:
        password = generate_password(
            args.d,
            require_alpha=1,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            require_punctuation=1,
            allowed_punctuation="`~!@#$%^&*()_+-={}|\\:\";'<>?,./",
            prohibited_punctuation=None,
        )
    else:
        password = generate_password(
            args.d,
            require_alpha=1,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            require_punctuation=1,
            allowed_punctuation="`~!@#$%^&*()_+-={}|\\:\";'<>?,./",
            prohibited_punctuation=None,
        )

    print(password)
    pyperclip.copy(password)
    print("Password copied to clipboard.")


if __name__ == "__main__":
    main()
