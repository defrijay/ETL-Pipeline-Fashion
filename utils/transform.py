import re

def transform_data(df):
    df = df[(df['Price'] != 'Price Unavailable') & (df['Rating'] != 'Invalid Rating')].copy()
    
    df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').str.strip()
    df['Rating'] = df['Rating'].str.replace(' / 5', '').str.strip()
    
    df['Price'] = df['Price'].astype(float) * 16000
    df['Rating'] = df['Rating'].astype(float)

    df['Size'] = df['Size'].apply(lambda x: re.sub(r'Size:\s*', '', x) if isinstance(x, str) else x)
    df['Gender'] = df['Gender'].apply(lambda x: re.sub(r'Gender:\s*', '', x) if isinstance(x, str) else x)
    
    df['Colors'] = df['Colors'].apply(lambda x: re.sub(r'\s*Colors$', '', x) if isinstance(x, str) else x)
    
    df.drop_duplicates(subset=['Title'], inplace=True)
    df.dropna(inplace=True)
    
    df = df[df['Title'] != 'Unknown Product']
    
    return df
