#!/usr/bin/env python3

import requests
import sys

v = requests.get('https://api.github.com/repos/{}/releases/latest'.format(sys.argv[1])).json()['tag_name']
if len(v) >= 2 and v[0].lower() == 'v' and v[1].isdigit():
	v = v[1:]
print(v)
