import os
import configparser
from contaminated_sessions import read_auth_file
import tempfile

"""
read_auth_file is designed to read a configuration file (default name: .xnat_auth_alt) that contains authentication details for accessing an XNAT server.
The file is expected to have a section named 'auth' with 'username' and 'password' entries:

[auth]
username = username
password = password
"""

fake_auth_file = """
[auth]
username = username
password = password
"""

with tempfile.NamedTemporaryFile(mode = 'w+', delete = True) as temp_auth_file:
    
    # write the temporary file
    temp_auth_file.write(fake_auth_file)

    # rewind it back to the beginning
    temp_auth_file.seek(0)

    # test it
    username, password = read_auth_file(temp_auth_file.name)
    
    assert username == "username", "Username does not match expected value."
    assert password == "password", "Password does not match expected value."

    print("Test passed: read_auth_file correctly reads username and password.")