#!/usr/bin/env python3

import json
import os
import tempfile
import re
import rpm
import subprocess as sp
import sys

def outputof(args, **kargs):
	ka = {
			'stdin': sp.DEVNULL,
			'stdout': sp.PIPE,
			'universal_newlines': True,
			'check': True
			}
	ka.update(kargs)
	return sp.run(args, **ka).stdout

re_ver = re.compile(r'^(?:(\d+):)?(.*)-(\d+)\.((?:el|fc)[.\d]+)$')
def verparse(t, dist=None):
	m = re_ver.match(t)
	epoch = m[1]
	if not epoch:
		epoch = '0'
	ver = m[2]
	rel = m[3]
	if dist:
		rel = '.'.join([rel.split('.', 1)[0], dist])
	return (epoch, ver, rel)

repo = sys.argv[1]
gitrepo = sys.argv[2]
dist = outputof(['rpm', '--eval', '%dist']).strip()[1:]

print('checking copr build state')

state = set([x.split()[2] for x in outputof(['copr-cli', 'list-builds', repo]).splitlines()] + ['succeeded', 'failed'])
state.remove('succeeded')
state.remove('failed')
if len(state) != 0:
	print('there are currently packages in state {}'.format(state))
	exit(1)

print('loading copr packages')
repopkgs = json.loads(outputof(['copr-cli', 'list-packages', '--with-latest-succeeded-build', repo]))
managed_pkgs = os.listdir('pkgs')
updates = []
newpkgs = managed_pkgs.copy()

for p in repopkgs:
	if p['name'] not in managed_pkgs:
		print('package {} is not managed'.format(p['name']))
		continue
	newpkgs.remove(p['name'])
	buildlabel = p['latest_succeeded_build']['source_package']['version']
	buildver = verparse(buildlabel, dist)
	latestlabel = None
	outdir = 'pkgs/{}/output'.format(p['name'])
	latestlabel = outputof([
		'make',
		'latest-release',
		'spec={}.spec'.format(p['name']),
		'outdir=' + outdir
		], stderr=sp.DEVNULL).splitlines()[-1]
	latestver = verparse(latestlabel, dist)
	if rpm.labelCompare(buildver, latestver) < 0:
		updates.append(p['name'])
		print('package {} needs to update from {} to {}'.format(p['name'], buildlabel, latestlabel))
	elif buildver != latestver:
		print('package {} of version {} is newer than the latest version {}'.format(p['name'], buildlabel, latestlabel))
	else:
		print('package {} is up to date on version {}'.format(p['name'], buildlabel))

updates.extend(newpkgs)

def deplist(p):
	dd = 'pkgs/{}/deps'.format(p)
	if os.path.isdir(dd):
		return os.listdir(dd)
	return []

ignore = set()
for p in updates:
	for d in deplist(p):
		if d in updates:
			print('package {} depends on another package {} to be updated, ignoring'.format(p, d))
			ignore.add(p)
for p in ignore:
	updates.remove(p)

repodict = {}
for p in repopkgs:
	repodict[p['name']] = p

for p in updates:
	print('submitting update to package {}'.format(p))
	cmd = 'edit-package-scm'
	if p not in repodict:
		print('creating new package')
		cmd = 'add-package-scm'
	sp.run(['copr-cli', cmd,
		'--clone-url', gitrepo,
		'--spec', '{}.spec'.format(p),
		'--type', 'git',
		'--method', 'make_srpm',
		'--name', p,
		'--webhook-rebuild', 'off',
		repo], check=True)
	sp.run(['copr-cli', 'build-package',
		'--nowait',
		'--name', p,
		repo], check=True)
