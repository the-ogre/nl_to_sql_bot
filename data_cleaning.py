import re
import pandas as pd
from typing import Any

def remove_special_characters(text):
    pattern = r'[^\w\s]'
    return re.sub(pattern, '', text)


def clean_column_names(column_name: str) -> str:
    cleaned_name = column_name.replace(' ', '_')
    cleaned_name = re.sub(r'[^\w_]', '', cleaned_name)
    return cleaned_name


def clean_price_column(value: str) -> str:
    pattern = r"\b(\d+)\.00\b"
    match = re.search(pattern, value)
    if match:
        digits_before_decimal = match.group(1)
        return digits_before_decimal
    return value


def is_valid_date(col: list) -> bool:
    date_string = str(col[0])
    patterns = [
        r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$',  # YYYY-MM-DD
        # DD-MMM-YYYY
        r'^(0[1-9]|[12][0-9]|3[01])-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4}$',
        # MMM DD YYYY
        r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (0[1-9]|[12][0-9]|3[01]) \d{4}$',
        # YYYY-MMM-DD
        r'^\d{4}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(0[1-9]|[12][0-9]|3[01])$',
        # YYYY-MM-DD HH:MM:SS
        r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]) (\d{2}):(\d{2}):(\d{2})$',
        # DD-MMM-YYYY HH:MM:SS
        r'^(0[1-9]|[12][0-9]|3[01])-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-\d{4} (\d{2}):(\d{2}):(\d{2})$',
        # MMM DD YYYY HH:MM:SS
        r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (0[1-9]|[12][0-9]|3[01]) \d{4} (\d{2}):(\d{2}):(\d{2})$',
        # YYYY-MMM-DD HH:MM:SS
        r'^\d{4}-(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)-(0[1-9]|[12][0-9]|3[01]) (\d{2}):(\d{2}):(\d{2})$',
        # DD-MM-YYYY HH:MM:SS
        r'^(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-\d{4} (\d{2}):(\d{2}):(\d{2})$',
    ]
    for pattern in patterns:
        if re.match(pattern, date_string):
            return True
    return False


def convert_to_datetime(col: str) -> Any:
    try:
        if is_valid_date(col):
            return pd.to_datetime(col)
        return col
    except ValueError:
        return col