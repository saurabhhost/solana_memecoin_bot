import pytest
from unittest.mock import patch, Mock
from src.safety_checker import check_token_safety, is_safe_token

@pytest.fixture
def mock_config():
    return {"filters": {"min_safety_score": 85}}

@patch("requests.get")
def test_check_token_safety_success(mock_get, mock_config):
    """Test successful safety check."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = """
        <div id="safety-score">90</div>
        <div id="liquidity-status">Burned</div>
        <div id="token-flags">None</div>
    """
    mock_get.return_value = mock_response

    safety_data = check_token_safety("TEST123", mock_config)
    assert safety_data["safety_score"] == 90
    assert safety_data["liquidity_burned"] is True
    assert safety_data["mintable"] is False
    assert safety_data["pausable"] is False

@patch("requests.get")
def test_check_token_safety_failure(mock_get, mock_config):
    """Test failed safety check."""
    mock_get.return_value.status_code = 404
    safety_data = check_token_safety("TEST123", mock_config)
    assert safety_data is None

def test_is_safe_token(mock_config):
    """Test token safety determination."""
    with patch("src.safety_checker.check_token_safety") as mock_check:
        mock_check.return_value = {
            "safety_score": 90,
            "liquidity_burned": True,
            "mintable": False,
            "pausable": False
        }
        assert is_safe_token("TEST123", mock_config) is True

        mock_check.return_value = {"safety_score": 80}
        assert is_safe_token("TEST123", mock_config) is False
