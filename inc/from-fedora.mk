include default-vars.mk

latest-version:
	$(tooldir)/fedora-koji-latest.py version $(pkg)

srpm:
	mkdir -p $(outdir)
	cd $(outdir) && $(tooldir)/fedora-koji-latest.py download $(pkg)

spec:
	mkdir -p $(outdir)
	cd $(outdir) && $(tooldir)/fedora-koji-latest.py unpack $(pkg)

include latest-release-from-spec.mk
