import pytest
import requests
from unittest.mock import patch, MagicMock
import pandas as pd
from utils.extract import extract_data

@patch('utils.extract.requests.get')
def test_extract_data(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text   = """
    <div class='collection-card'>
        <h3 class='product-title'>Test Product</h3>
        <span class='price'>$20.00</span>
        <p>Rating: ⭐4.5 / 5</p>
        <p>Red</p>
        <p>M</p>
        <p>Men</p>
    </div>
    """
    mock_get.return_value = mock_response
    df = extract_data()
    assert not df.empty
    assert df.iloc[0]['Title'] == 'Test Product'
    assert df.iloc[0]['Price'] == '$20.00'
    assert df.iloc[0]['Rating'] == '4.5'

    # Simulate a failed request
    mock_get.side_effect = requests.exceptions.RequestException("Request failed")
    df = extract_data()
    assert df.empty, "Should return empty DataFrame on request failure"