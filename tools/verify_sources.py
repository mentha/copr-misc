#!/usr/bin/env python3

import hashlib
import re
import sys

hashmap = {
		'SHA512': hashlib.sha512
		}

with open(sys.argv[1]) as hashfile:
	r = re.compile(r'^([^\s(]+)\s*\(([^)]+)\)\s*=\s*(.*)$')
	for l in hashfile.readlines():
		l = l.strip()
		m = r.match(l)
		h = hashmap[m[1]]()
		with open(m[2], 'rb') as f:
			h.update(f.read())
		if m[3].lower() != h.hexdigest().lower():
			print('{} verification fail!'.format(m[2]))
			exit(1)

print('all verification passed.')
