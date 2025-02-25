import pytest
from unittest.mock import patch, Mock
from src.social_analyzer import analyze_social_activity

@patch("requests.get")
def test_analyze_social_activity_success(mock_get):
    """Test successful social activity analysis."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "mentions": [
            {"followers": 15000},
            {"followers": 5000},
            {"followers": 20000}
        ]
    }
    mock_get.return_value = mock_response

    influencer_count = analyze_social_activity("TEST123")
    assert influencer_count == 2  # Only 15000 and 20000 are >= 10000

@patch("requests.get")
def test_analyze_social_activity_failure(mock_get):
    """Test failed social activity analysis."""
    mock_get.return_value.status_code = 404
    influencer_count = analyze_social_activity("TEST123")
    assert influencer_count == 0
