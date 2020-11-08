#!/usr/bin/env python3

import re
import requests
import subprocess as sp
import sys

cmd = sys.argv[1]
pkg = sys.argv[2]

pkgid = requests.get('https://koji.fedoraproject.org/koji/search', params={
	'type': 'package',
	'match': 'exact',
	'terms': pkg}, allow_redirects=False)
if pkgid.status_code != 302:
	print('package {} not found on koji'.format(pkg))
	exit(1)
pkgid = pkgid.headers['location'].rsplit('=', 1)[-1]

builds = requests.get('https://koji.fedoraproject.org/koji/builds', params={
	'order': '-completion_time',
	'packageID': pkgid,
	'state': '1'})
releases = re.findall(r'<a\s+href="buildinfo\?buildID=\d+">{}-([^<]+\.fc\d+)</a>'.format(pkg), builds.text)

frel = max([int(x) for x in re.findall(r'<a\s+href="(\d+)/">', requests.get('https://mirrors.kernel.org/fedora/releases/').text)])

lastrel = None
for r in releases:
	fr = int(r.rsplit('c', 1)[-1])
	if fr > frel:
		continue
	lastrel = r
	break

if not lastrel:
	print('cannot find suitable build for {}'.format(pkg))
	exit(1)

m = re.match(r'^(.*)-(\d+\.fc\d+)$', lastrel)
ver = m[1]
rpmrel = m[2]

if cmd == 'version':
	print(ver)
	exit(0)

rpmname = '{}-{}-{}.src.rpm'.format(pkg, ver, rpmrel)
sp.run(['curl', '-C', '-', '-o', rpmname,
	'https://kojipkgs.fedoraproject.org/packages/{}/{}/{}/src/{}'.format(pkg, ver, rpmrel, rpmname)], stdin=sp.DEVNULL, check=True)

if cmd == 'download':
	pass
elif cmd == 'unpack':
	with sp.Popen(['rpm2cpio', rpmname], stdin=sp.DEVNULL, stdout=sp.PIPE) as r2c:
		with sp.Popen(['cpio', '-i'], stdin=r2c.stdout) as p:
			p.wait()
		r2c.wait()
else:
	print('unknown command')
	exit(1)
