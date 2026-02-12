import pytest

from shopee_affiliate.validators import validate_sub_ids


def test_validate_sub_ids_accepts_none_and_empty():
    validate_sub_ids(None)
    validate_sub_ids([])


def test_validate_sub_ids_rejects_more_than_5():
    with pytest.raises(ValueError):
        validate_sub_ids(["a", "b", "c", "d", "e", "f"])


@pytest.mark.parametrize(
    "value",
    [
        ["campanhaA", "bannerB"],
        ["s1"],
        ["A1", "B2", "C3"],
    ],
)
def test_validate_sub_ids_accepts_alnum(value):
    validate_sub_ids(value)


@pytest.mark.parametrize(
    "value",
    [
        ["canal_email"],
        ["campanha-A"],
        ["banner#1"],
        [""],
    ],
)
def test_validate_sub_ids_rejects_non_alnum(value):
    with pytest.raises(ValueError):
        validate_sub_ids(value)
