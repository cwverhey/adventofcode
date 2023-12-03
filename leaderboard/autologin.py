#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this script logs in to adventofcode.com using GitHub auth, retrieves the AoC cookie, and uploads it to an FTP server

from bs4 import BeautifulSoup as bs
import requests
import ftplib
import tempfile
import json

# get authentication data from JSON file
#
# to create this file:
# cat '{"gh_user": "foo", "gh_key": "bar", "ftp_host": "ftp.fbi.gov", "ftp_user": "baz", "ftp_key": "boaz"}' > auth.json
#
with open('auth.json', 'r') as f:
    auth = json.load(f)

# start session with adventofcode.com, get login tokens for login form
sess = requests.Session()

r = sess.get("https://adventofcode.com/auth/github")
soup = bs(r.content, features="html5lib") # if this gives an error, try without `features`-parameter
formhtml = soup.find("form")

inputs = {i.attrs['name']: i.attrs.get('value','') for i in formhtml.find_all('input')}
inputs['login'] = auth['gh_user']
inputs['password'] = auth['gh_key']

# action = formhtml.attrs.get("action", '') # hardcode instead; if AoC changes the action you'll be sending your pass to someone else
# method = formhtml.attrs.get("method", "get").lower() # GET/POST

# perform login at github.com in the same session
r = sess.post("https://github.com/session", data=inputs)

# save AoC session cookie (gives error if cookie not set in session)
for c in sess.cookies:
    if c.name == "session" and c.domain == ".adventofcode.com":
        cookie = c.name+"="+c.value

with tempfile.NamedTemporaryFile(mode='w') as f:
    f.write(cookie)

# upload to FTP server
ftpsession = ftplib.FTP_TLS(auth['ftp_server'], auth['ftp_user'], auth['ftp_key']) # require TLS with FTP_TLS()
with open(fp.name,'rb') as cookiefile:
    ftpsession.storbinary('STOR adventofcode-cookie.txt', cookiefile)
ftpsession.quit()
