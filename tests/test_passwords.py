import pytest
from main import generate_password
import string
# import random


@pytest.mark.parametrize(
    "length, require_alpha, require_lower, require_upper, require_digits, allowed_punctuation, prohibited_punctuation, expected_length",
    [
        (16, 2, 1, 1, 2, None, "&<>”‘%~'\"`@{}/\\", 16),
        (20, 2, 1, 1, 2, string.punctuation, '', 20),
        (12, 2, 1, 1, 2, string.punctuation, '', 12),
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
