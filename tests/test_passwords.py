import pytest
from main import generate_password
import string

# import random
from main import main


@pytest.mark.parametrize(
    "length, require_alpha, require_lower, require_upper, require_digits, allowed_punctuation, prohibited_punctuation, expected_length",
    [
        (16, 2, 1, 1, 2, None, "&<>\"'%~'`@{}/\\", 16),
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
    password = generate_password(
        length=length,
        require_alpha=require_alpha,
        require_lower=require_lower,
        require_upper=require_upper,
        require_digits=require_digits,
        allowed_punctuation=allowed_punctuation,
        prohibited_punctuation=prohibited_punctuation,
    )
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    if allowed_punctuation:
        assert any(
            c in allowed_punctuation
            for c in password
            if c not in prohibited_punctuation
        )
    assert all(c not in prohibited_punctuation for c in password)
    assert len(password) == expected_length


@pytest.mark.parametrize(
    "args, expected_length",
    [
        (["-e", "-d", "12"], 12),
        (["-sa", "-d", "16"], 16),
        (["-d", "20"], 20),
        (["-e"], 8),  # Default length
        (["-sa"], 8),  # Default length
    ],
)
def test_main_args(monkeypatch, capsys, args, expected_length):
    monkeypatch.setattr("sys.argv", ["main.py"] + args)
    main()
    captured = capsys.readouterr()
    password = captured.out.split("\n")[0]
    assert len(password) == expected_length
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)


@pytest.mark.parametrize(
    "args",
    [
        (["-e", "-d", "5"]),  # Too short to meet requirements
        (["-sa", "-d", "5"]),  # Too short to meet requirements
        (["-d"]),  # -d flag included but no int provided
        (["-d", "abc"]),  # -d flag included but invalid int provided
        (["-e", "-sa", "-d", "5"]),  # Both -e and -sa flags provided
    ],
)
def test_main_args_fail(monkeypatch, capsys, args):
    monkeypatch.setattr("sys.argv", ["main.py"] + args)
    with pytest.raises(SystemExit):
        main()
