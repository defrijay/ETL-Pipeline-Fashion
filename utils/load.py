from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
from googleapiclient.errors import HttpError

def load_to_csv(df, filename='products.csv'):
    df.to_csv(filename, index=False)