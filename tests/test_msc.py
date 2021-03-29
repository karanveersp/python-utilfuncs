from unittest.mock import patch

import utilfuncs as util


@patch("time.sleep")
def test_keep_trying_works_on_expected_error(mock_sleep):
    # arrange
    def raise_error_once(need_to_raise_flag=[True]):
        """Function with mutalble default"""
        if need_to_raise_flag[0]:
            need_to_raise_flag[0] = False
            raise Exception("Expected")
        print("clear")

    # act
    util.keep_retrying_on_specific_error(
        "Expected",
        2,
        raise_error_once,
        [True]
    )

    mock_sleep.assert_called_once()
    mock_sleep.assert_called_with(2)


def test_filter_by_glob_works():
    my_list = ["hulk_smash.txt", "hulk_smash.log", "hulk_sleep.txt"]

    pattern = "hulk_*.txt"

    expected = ["hulk_smash.txt", "hulk_sleep.txt"]

    result = util.filter_by_glob(my_list, pattern)

    assert expected == result


def test_filter_by_glob_works_v1():
    my_list = ["newyork_liberty", "newyork_empire", "newyork_liberty"]

    pattern = "*_liberty"

    expected = ["newyork_liberty", "newyork_liberty"]

    result = util.filter_by_glob(my_list, pattern)

    assert expected == result