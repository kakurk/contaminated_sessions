import requests
from contaminated_sessions import get_mr_sessions

"""
get_mr_sessions is designed to extract all MR scan sessions from an XNAT instance within a specified date range.

Picking an arbitrary date range for testing.
There should be 6 sessions in this date range.
"""

# connect to xnat2 using the RCS created qa account
XNAT_HOST = 'https://xnat2.bu.edu'
USERNAME = 'bucncqa'
PASSWORD = 'h1pp0campu$'

# picking an arbitrary date range for testing.
# There should be 6 sessions in this date range.
START_DATE = '2025-05-01'
END_DATE = '2025-05-07'

with requests.Session() as session:

    session.auth = (USERNAME, PASSWORD)

    df_sessions = get_mr_sessions(session, start_date=START_DATE, end_date=END_DATE)

    assert len(df_sessions) == 6, f"Expected 6 sessions, got {len(df_sessions)}"

    print("Test passed: Correct number of sessions fetched.")