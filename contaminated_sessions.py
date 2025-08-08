import requests
import pandas as pd
from io import StringIO
from lxml import etree
import os
import configparser

ns = {'xnat': 'http://nrg.wustl.edu/xnat'}

def read_auth_file(filename=".xnat_auth"):
    import configparser
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Auth file '{filename}' not found.")
    config = configparser.ConfigParser()
    config.read(filename)
    if 'auth' not in config:
        raise KeyError("Auth section missing in config file.")
    username = config['auth'].get('username')
    password = config['auth'].get('password')
    if not username or not password:
        raise KeyError("Username or password missing in auth file.")
    return username, password

USERNAME, PASSWORD = read_auth_file()
XNAT_HOST = 'https://xnat2.bu.edu'


def get_mr_sessions(session, start_date=None, end_date=None):
    """
    Fetch all sessions from XNAT, optionally filtering by date range using XNAT REST API query parameters.
    Dates should be in 'YYYY-MM-DD' format.
    """
    base_url = f'{XNAT_HOST}/data/experiments?format=csv&xsiType=xnat:mrSessionData'
    date_param = None
    from datetime import datetime
    def to_mmddyyyy(date_str):
        return datetime.strptime(date_str, "%Y-%m-%d").strftime("%m/%d/%Y")

    if start_date and end_date:
        date_param = f"date={to_mmddyyyy(start_date)}-{to_mmddyyyy(end_date)}"
    elif start_date:
        date_param = f"date={to_mmddyyyy(start_date)}"
    elif end_date:
        date_param = f"date={to_mmddyyyy(end_date)}"

    if date_param:
        url = base_url + "&" + date_param
    else:
        url = base_url
    response = session.get(url)
    response.raise_for_status()
    csv_content = response.text
    df = pd.read_csv(StringIO(csv_content))
    return df

def check_project_mismatch(session, session_id):
    url = f'{XNAT_HOST}/data/experiments/{session_id}?format=xml'
    response = session.get(url)
    if response.status_code != 200:
        print(f"Warning: Could not fetch session XML for {session_id} (status: {response.status_code})")
        return False
    xml_root = etree.fromstring(response.content)

    session_project = xml_root.get('project')
    if session_project is None:
        session_project_list = xml_root.xpath('string(/xnat:MRSession/@project)', namespaces=ns)
        session_project = session_project_list if session_project_list else None

    if session_project is None:
        print(f"Warning: No project attribute found in session {session_id}")
        return False

    scan_elements = xml_root.xpath('//xnat:scan[@project and not(@project="{0}")]'.format(session_project), namespaces=ns)

    return bool(scan_elements)

def main():
    import argparse
    from datetime import datetime

    parser = argparse.ArgumentParser(description="Find sessions with scan/project mismatch, optionally filtering by date range.")
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)', required=False)
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)', required=False)
    args = parser.parse_args()

    with requests.Session() as session:
        session.auth = (USERNAME, PASSWORD)
        df_sessions = get_mr_sessions(session, start_date=args.start_date, end_date=args.end_date)
        print(f"Total sessions: {len(df_sessions)}")

        flagged_session_ids = []
        for idx, row in df_sessions.iterrows():
            session_id = row['ID']
            if check_project_mismatch(session, session_id):
                print(f"Flagged session with project mismatch: {session_id}")
                flagged_session_ids.append(session_id)

        df_flagged = df_sessions[df_sessions['ID'].isin(flagged_session_ids)]

        print("\nSummary:")
        print(f"Flagged {len(df_flagged)} sessions with scan/project mismatch.")

        if not df_flagged.empty:
            print("\nFlagged Sessions DataFrame:")
            print(df_flagged)
            output_file = "contaminated_sessions.csv"
            df_flagged.to_csv(output_file, index=False)
            print(f"\nFlagged sessions saved to '{output_file}'")

if __name__ == "__main__":
    main()