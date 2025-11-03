import requests
from contaminated_sessions import check_project_mismatch

"""
check_project_mismatch is designed to check a specific MR scan session for mismatching project information.
In other words, the meta data labeling the MR scan session does NOT match the project data attributed to at least one
MR scan within that scan session.

You can see this in the web interface by navigating to an MR scan session page and hitting the "View" --> "View XML"
button. This will show you the raw XML data for that session, including XNAT's intended project for this MR Scan session
and XNAT's intended project for each MR scan within this scan session.
"""

# connect to xnat2 using the RCS created qa account
XNAT_HOST = 'https://xnat2.bu.edu'
USERNAME = 'bucncqa'
PASSWORD = 'h1pp0campu$'

# See INC20666967 for more information.
#   250716_S0156_TWCF_SES1/BU_CNC_E00482 is known to be contamined by checking the XNAT2 user interface.
#   251008_QA/BU_CNC_E00732 is an arbitrary QA scan that should NOT be contaminated.
SESSION_ID_OF_KNOWN_CONTAMINATED_SCAN = 'BU_CNC_E00482' # MR Session label = 250716_S0156_TWCF_SES1
SESSION_ID_OF_KNOWN_UNCONTAMINATED_SCAN = 'BU_CNC_E00732' # MR Session label = 251008_QA

with requests.Session() as session:

    session.auth = (USERNAME, PASSWORD)

    assert check_project_mismatch(session, SESSION_ID_OF_KNOWN_CONTAMINATED_SCAN), "Known contaminated session not identified."
    assert not check_project_mismatch(session, SESSION_ID_OF_KNOWN_UNCONTAMINATED_SCAN), "Known clean session incorrectly identified as contaminated."

    print("Test passed: Contaminated session correctly identified.")