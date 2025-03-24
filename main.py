import random
import string
import argparse


def generate_password(
    length,
    require_alpha=2,
    require_lower=1,
    require_upper=1,
    require_digits=2,
    allowed_punctuation=None,
    prohibited_punctuation=None,
):
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation

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
        password.extend(
            random.choices(
                string.ascii_letters + string.digits + allowed_punctuation,
                k=length - sum([require_lower, require_upper, require_digits]),
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
    parser = argparse.ArgumentParser(description="Custom Password Generator")
    parser.add_argument(
        "-sa",
        action="store_true",
        help="Generate password for system type 2 (with all punctuation allowed)",
    )
    parser.add_argument(
        "-s",
        action="store_true",
        help="Generate password for system type 2 (with some punctuation allowed)",
    )
    parser.add_argument(
        "-e", action="store_true", help="Generate password for system type 1"
    )
    args = parser.parse_args()

    prohibited_punctuation = "',{}"  # Define prohibited punctuation characters

    if args.e:
        # System 1 (punctuation limited to !, $, #, and ;)
        password = generate_password(
            random.randint(8, 32),
            require_alpha=2,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            allowed_punctuation="!$#;",
            prohibited_punctuation=prohibited_punctuation,
        )
    elif args.sa:
        # System 2 (all punctuation allowed)
        password = generate_password(
            random.randint(15, 32),
            require_alpha=2,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            allowed_punctuation=string.punctuation,
            prohibited_punctuation=prohibited_punctuation,
        )
    elif args.s:
        # System 2 (limited punctuation allowed, with some characters removed)
        password = generate_password(
            random.randint(15, 32),
            require_alpha=2,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            allowed_punctuation=string.punctuation,
            prohibited_punctuation=prohibited_punctuation,
        )
    else:
        # Default system (no flag, limited punctuation, 12-20 characters)
        password = generate_password(
            random.randint(12, 20),
            require_alpha=2,
            require_lower=1,
            require_upper=1,
            require_digits=2,
            allowed_punctuation=string.punctuation,
            prohibited_punctuation=prohibited_punctuation,
        )

    print(password)


if __name__ == "__main__":
    main()
