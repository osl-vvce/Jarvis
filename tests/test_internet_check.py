import requests
from unittest.mock import patch

from internet_check import is_Online


@patch("internet_check.requests.get")
def test_internet_check_success(mock_get):
    mock_get.return_value.status_code = 200

    assert is_Online() is True


@patch("internet_check.requests.get")
def test_internet_check_failure_status(mock_get):
    mock_get.return_value.status_code = 500

    assert is_Online() is False


@patch("internet_check.requests.get")
def test_internet_check_connection_error(mock_get):
    mock_get.side_effect = requests.ConnectionError

    assert is_Online() is False


@patch("internet_check.requests.get")
def test_internet_check_timeout(mock_get):
    mock_get.side_effect = requests.Timeout

    assert is_Online() is False


@patch("internet_check.requests.get")
def test_internet_check_custom_url_and_timeout(mock_get):
    mock_get.return_value.status_code = 200

    result = is_Online("https://example.com", timeout=10)

    mock_get.assert_called_once_with(
        "https://example.com",
        timeout=10
    )

    assert result is True


@patch("internet_check.requests.get")
def test_internet_check_no_content(mock_get):
    mock_get.return_value.status_code = 204

    assert is_Online() is True


@patch("internet_check.requests.get")
def test_internet_check_not_found(mock_get):
    mock_get.return_value.status_code = 404

    assert is_Online() is False


@patch("internet_check.requests.get")
def test_internet_check_default_arguments(mock_get):
    mock_get.return_value.status_code = 200

    is_Online()

    mock_get.assert_called_once_with(
        "https://www.google.com",
        timeout=5
    )


@patch("internet_check.requests.get")
def test_internet_check_unexpected_exception(mock_get):
    mock_get.side_effect = ValueError("Unexpected error")

    assert is_Online() is False