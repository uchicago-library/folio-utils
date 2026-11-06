#! /usr/local/bin/python3.7

# This script will pull in functions that I've put in other scripts to make a file of
# a list of permissions for any version of FOLIO and have it in a usable fashion.

import folioclient
import requests
import json
import logging
import argparse
import configparser

# Set up logfiles, based on which host we're using.
logging.basicConfig(filename='getpermsdebug.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

#  Download all permissions from the server and put in outputfile

def get_permissions(fc:folioclient.FolioClient, perms_get_url:str):
    url = perms_get_url
    r = fc.folio_get(url)
    d = json.dumps(r, indent=4)
    return(d)

config = configparser.ConfigParser()
config.read('config.ini')
parser = argparse.ArgumentParser()

parser.add_argument('-o', '--outputfile', metavar='', required=True, help='Name of output file')
parser.add_argument('-s', '--server', metavar='', required=True, help='Server and tenant settings from config.ini')

args = parser.parse_args()
server = args.server.upper()
okapi_base_url = config.get(server, 'okapi_base_url')
username = config.get(server, 'username')
password = config.get(server, 'password')
tenant = config.get(server, 'tenant')
login_path = config.get(server, 'login_path')
login_url = okapi_base_url + login_path
perms_path = config.get(server, 'perms_path')
perms_get_url = okapi_base_url + perms_path + '?length=10000'

with folioclient.FolioClient(okapi_base_url, tenant, username, password) as fc:
    perms = get_permissions(fc, perms_get_url)
    with open(args.outputfile, 'w', newline='') as out:
        out.write(perms)




