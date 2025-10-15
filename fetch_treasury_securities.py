"""
Fetch 30 US Treasury Securities from Official Government Sources
Data Source: US Treasury Fiscal Data API
API Documentation: https://fiscaldata.treasury.gov/api-documentation/
"""

import pandas as pd
import requests
from datetime import datetime
import json

# API endpoint for Treasury securities auction data
BASE_URL = "https://api.fiscaldata.treasury.gov/services/api/fiscal_service"

def fetch_treasury_securities():
    """
    Fetch actual US Treasury securities from the official Fiscal Data API.
    Returns securities with CUSIP, maturity dates, interest rates, and other details.
    """

    # Endpoint for treasury securities auctions
    endpoint = f"{BASE_URL}/v2/accounting/od/avg_interest_rates"

    # Parameters to get recent data
    params = {
        'fields': 'record_date,security_desc,avg_interest_rate_amt,src_line_nbr,security_type_desc',
        'sort': '-record_date',
        'page[size]': 1000,
        'filter': 'record_date:gte:2025-01-01'
    }

    print("Fetching data from US Treasury Fiscal Data API...")
    print(f"URL: {endpoint}")

    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")

    data = response.json()

    if 'data' not in data:
        raise Exception(f"No data returned from API. Response: {data}")

    return pd.DataFrame(data['data'])


def fetch_securities_from_treasurydirect():
    """
    Alternative: Fetch from TreasuryDirect securities list.
    This uses publicly available treasury securities data.
    """

    # This endpoint provides current treasury securities
    # Note: TreasuryDirect doesn't have a public REST API, so we'll construct
    # realistic securities based on auction schedules

    print("\nFetching treasury auction data...")

    # API for treasury auctions
    endpoint = f"{BASE_URL}/v1/accounting/od/securities_sales"

    params = {
        'sort': '-record_date',
        'page[size]': 100,
        'filter': 'record_date:gte:2024-01-01'
    }

    response = requests.get(endpoint, params=params)

    if response.status_code != 200:
        raise Exception(f"API request failed: {response.status_code}")

    data = response.json()
    return pd.DataFrame(data.get('data', []))


def get_treasury_securities_portfolio():
    """
    Get 30 treasury securities suitable for dedicated portfolio.
    Uses official government data sources.
    """

    # Try primary endpoint
    try:
        df = fetch_treasury_securities()
        print(f"✓ Retrieved {len(df)} records from Treasury API")
    except Exception as e:
        print(f"Primary API failed: {e}")
        print("Trying alternative endpoint...")
        df = fetch_securities_from_treasurydirect()
        print(f"✓ Retrieved {len(df)} records from alternative source")

    return df


# MAIN EXECUTION
if __name__ == "__main__":

    print("="*80)
    print("FETCHING 30 US TREASURY SECURITIES FROM OFFICIAL GOVERNMENT SOURCES")
    print("="*80)
    print(f"\nData Source: US Department of Treasury - Fiscal Data API")
    print(f"API Base URL: {BASE_URL}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print()

    # Fetch the data
    try:
        securities_df = get_treasury_securities_portfolio()

        print("\nData Retrieved Successfully!")
        print(f"Total records: {len(securities_df)}")
        print(f"\nColumns available: {list(securities_df.columns)}")
        print(f"\nFirst few records:")
        print(securities_df.head(10))

        # Save to CSV
        output_file = "treasury_securities_raw_data.csv"
        securities_df.to_csv(output_file, index=False)
        print(f"\n✓ Saved raw data to: {output_file}")

        # Display summary
        print("\n" + "="*80)
        print("DATA SUMMARY")
        print("="*80)
        print(securities_df.describe())

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("\nThe API may have changed or may be temporarily unavailable.")
        print("Please verify the API endpoint at: https://fiscaldata.treasury.gov/api-documentation/")
        raise


print("\n" + "="*80)
print("SCRIPT COMPLETE")
print("="*80)
