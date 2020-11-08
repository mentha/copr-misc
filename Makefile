outdir ?= ./output

override outdir := $(abspath $(outdir))
pkg       := $(basename $(notdir $(spec)))
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

srpm: pkginstall
	cd $(pkgdir) && $(MAKE) srpm outdir=$(outdir)

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
