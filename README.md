# Contaimined Scans

This repository houses a tool for scanning an XNAT instance for "contaminated" scans sessions. 

An "XNAT instance" is an XNAT database running on a specific machine. As of this writing, at Boston University's Cognitive Neuroimaging Center, there are currently two XNAT instances: xnat.bu.edu AND xnat2.bu.edu.

Contaminated scans sessions are scan sessions (in XNAT's terminology, "[experiments](https://wiki.xnat.org/documentation/understanding-the-xnat-data-model#UnderstandingtheXNATDataModel-Experiments(xnat:experimentData))") that contain scans that should be in a different scan session.

This tool is written as a python command line tool and assumes a python virtual enviroment is created locally. This virtual enviroment can be recreated using the requirements.txt file in this repostiory. I (the author, Kyle Kurkela) have the virutal enviroment installed in the same directory as this repository in a hidden directory called ".venv".

Before running, you need to make sure that the virtual enviorment is activated. For example:

    # python version
    > python --version
    Python 3.9.21

    # create a new virtual enviroment
    > python -m venv .venv/contaminated

    # activate it
    > source .venv/contaminated/bin/activate

    # install all of the requirements
    > pip install -r requirements.txt

Usage:

    contaminated_sessions.py --start-date YYYYMMDD --end-date YYYYMMDD

Outputs:  
1. An emailed report letting the user know how many contaminated sessions were identified. 
2. If any contaminated sessions are found, writes report to /tmp/contaminated_sessions.csv.