from decouple import config

"""
    This file contains the configuration for the application.
    decouple is a tool that allows us to store sensitive data in a separate file.
    documentation: https://pypi.org/project/python-decouple/
"""

USER = config("USUARIO")
PASSWORD = config('PASS')
DB_NAME = config('DB_NAME')
