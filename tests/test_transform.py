import pytest
import pandas as pd
from utils.transform import transform_data

def test_transform_data():
    data = pd.DataFrame({
        'Title': ['Product 1', 'Unknown Product'],
        'Price': ['$10.00', 'Price Unavailable'],
        'Rating': ['4.5 / 5', 'Invalid Rating'],
        'Colors': ['Red', 'Blue'],
        'Size': ['M', 'L'],
        'Gender': ['Men', 'Women'],
        'Timestamp': ['2023-01-01 00:00:00', '2023-01-01 00:00:00']
    })
    transformed_data = transform_data(data)
    assert 'Unknown Product' not in transformed_data['Title'].values
    assert transformed_data['Price'].dtype == float
    assert transformed_data['Rating'].dtype == float