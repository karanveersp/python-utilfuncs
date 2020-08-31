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
