outdir ?= ./output

override outdir := $(abspath $(outdir))
pkg       := $(patsubst %.spec,%,$(basename $(spec)))
pkgdir    := ${CURDIR}/pkgs/$(pkg)
incdir    := $(abspath ./inc)
MAKEFLAGS += -I $(incdir)
tooldir   := $(abspath ./tools)
export pkg
export tooldir

.PHONY: help latest-version latest-release spec srpm pkginstall

help:
	@echo 'usage: make <spec|srpm|latest-version|latest-release> spec=pkgname [outdir=path]'

latest-version: pkginstall
	cd $(pkgdir) && $(MAKE) --no-print-directory latest-version

latest-release: pkginstall
	cd $(pkgdir) && $(MAKE) --no-print-directory latest-release outdir=$(outdir)

spec: pkginstall
	cd $(pkgdir) && $(MAKE) spec outdir=$(outdir)

srpm: spec
	rpmbuild \
		--define '_sourcedir $(outdir)' \
		--define '_specdir $(outdir)' \
		--define '_builddir $(outdir)' \
		--define '_srcrpmdir $(outdir)' \
		--define '_rpmdir $(outdir)' \
		--nodeps \
		-bs $(outdir)/$(pkg).spec

ifeq ($(shell id -u),0)
pkginstall:
	dnf -y install \
		git \
		rpm-build \
		python3 \
		python3-requests \
		rpmdevtools
else
pkginstall:
	@true
endif
