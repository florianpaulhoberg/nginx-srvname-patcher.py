#!/usr/bin/env python3

# 2017-08-11 nginx-srvname-patcher.py
# Florian Paul Hoberg <florian@hoberg.ch>
# This will patch your nginx binary file
# from Server: nginx to Server: B00B
# You can change B00B to anything else
# but limited to max. 5 chars
# 
# License: BSD 3-Clause License
# Python Version: 3
# usage: nginx-srvname-patcher.py nginx-bin-file

import sys
import re

SERVER_NAME_ORIG = "Server: nginx"
ENCODED_SERVER_NAME_ORIG = SERVER_NAME_ORIG.encode()
SERVER_NAME = "Server: B00B"
ENCODED_SERVER_NAME = SERVER_NAME.encode()
NGINX_BIN = "nginx_new"

def binary_nginx_patch(path):
    """ Read binary to buffer"""   
    with open(path, 'rb') as f:
        buffer = f.read()
    return buffer

def check_nginx_string(data):
    """ Check for original  'Server: nginx' content in raw data"""
    if ENCODED_SERVER_NAME_ORIG in data:
        print("OK: Found expected original string:\n", SERVER_NAME_ORIG)
        patch_true = input("MSG: Proceed with patching? [y/N] ")
        if patch_true == "y":
            print("OK: Start patching nginx binary.", file=sys.stderr)
        else:
            print("WARN: Patching stopped.", file=sys.stderr)
            exit(2)

def write_new_nginx_binary(data_out):
    """ Write patched binary file """
    with open(NGINX_BIN, 'wb') as new_nginx_binary:
        data_out = data_out.replace(ENCODED_SERVER_NAME_ORIG, ENCODED_SERVER_NAME)
        new_nginx_binary.write(data_out)
    print("OK: Patching done. New binary:", NGINX_BIN)

def main():
    if len(sys.argv) > 0:
        data = binary_nginx_patch(sys.argv[1])
    check_nginx_string(data)
    write_new_nginx_binary(data)

try:
    main()
except FileNotFoundError:
    print("CRIT: Please define path to nginx binary.")
