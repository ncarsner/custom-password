import pytest
from main import generate_password
import string

# Import the main function from the main module
from main import main


# Test the generate_password function with various parameters
@pytest.mark.parametrize(
    "length, require_alpha, require_lower, require_upper, require_digits, allowed_punctuation, prohibited_punctuation, expected_length",
    [
        (16, 2, 1, 1, 2, "&<>\"'%~'`@{}/\\", None, 16),
        (20, 2, 1, 1, 2, string.punctuation, "", 20),
        (12, 2, 1, 1, 2, string.punctuation, "", 12),
    ],
)
def test_generate_password(
    length,
    require_alpha,
    require_lower,
    require_upper,
    require_digits,
    allowed_punctuation,
    prohibited_punctuation,
    expected_length,
):
    """
    Test the generate_password function to ensure it generates passwords
    that meet the specified criteria.
    """
    if allowed_punctuation is None:
        allowed_punctuation = ""
    if prohibited_punctuation is None:
        prohibited_punctuation = ""
    password = generate_password(
        length=length,
        require_alpha=require_alpha,
        require_lower=require_lower,
        require_upper=require_upper,
        require_digits=require_digits,
        allowed_punctuation=allowed_punctuation,
        prohibited_punctuation=prohibited_punctuation,
    )
    # Check if the password contains at least one lowercase letter
    assert any(c.islower() for c in password)
    # Check if the password contains at least one uppercase letter
    assert any(c.isupper() for c in password)
    # Check if the password contains at least one digit
    assert any(c.isdigit() for c in password)
    # Check if the password contains allowed punctuation and not prohibited punctuation
    if allowed_punctuation:
        assert any(
            c in allowed_punctuation
            for c in password
            if c not in prohibited_punctuation
        )
    # Ensure no prohibited punctuation is in the password
    assert all(c not in prohibited_punctuation for c in password)
    # Check if the password length matches the expected length
    assert len(password) == expected_length


# Test the main function with various command-line arguments
@pytest.mark.parametrize(
    "args, expected_length",
    [
        (["-e", "-d", "12"], 12),
        (["-sa", "-d", "16"], 16),
        (["-d", "20"], 20),
        (["-e"], 8),
        (["-sa"], 15),
    ],
)
def test_main_args(monkeypatch, capsys, args, expected_length):
    """
    Test the main function to ensure it correctly processes command-line arguments
    and generates passwords of the expected length.
    """
    monkeypatch.setattr("sys.argv", ["main.py"] + args)
    main()
    captured = capsys.readouterr()
    password = captured.out.split("\n")[0]
    # Check if the password length matches the expected length
    assert len(password) == expected_length
    # Check if the password contains at least one lowercase letter
    assert any(c.islower() for c in password)
    # Check if the password contains at least one uppercase letter
    assert any(c.isupper() for c in password)
    # Check if the password contains at least one digit
    assert any(c.isdigit() for c in password)


# Test the main function with invalid command-line arguments to ensure it raises SystemExit
@pytest.mark.parametrize(
    "args",
    [
        (["-e", "-d", "5"]),  # Legnth too short
        (["-sa", "-d", "7"]),  # Length too short
        (["-e", "-sa"]),  # Both -e and -sa flags provided
        (["-e", "-sa", "-d", "5"]),  # Both -e and -sa flags provided, with -d flag and invalid int
        (["-d", "abc"]),  # -d flag included but invalid int provided
        (["-d"]),  # -d flag included but no int provided
    ],
)
def test_main_args_fail(monkeypatch, args):
    """
    Test the main function to ensure it raises SystemExit with code 1 when provided with invalid arguments.
    """
    monkeypatch.setattr("sys.argv", ["main.py"] + args)
    with pytest.raises(SystemExit) as excinfo:
        main()
    if args in [["-d"], ["-d", "abc"]]:
        assert excinfo.value.code == 2
    else:
        assert excinfo.value.code == 1
