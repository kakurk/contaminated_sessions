# Contaimined Scans

This repository houses a tool for scanning an XNAT instance for "contaminated" scans sessions. Contaminated scans sessions are scan session (in XNAT's terminology, "experiment" sessions) that contain scans from a different scan session.

This tool is written as a python command line tool and assumes a python virtual enviroment is created locally.

Usage:

    contaminated_sessions.py --start-date YYYYMMDD --end-date YYYYMMDD

Outputs:
    1. An emailed report letting the user know how many contaminated sessions were identified
    2. If any contaminated sessions are found, writes report to /tmp/contaminated_sessions.csv