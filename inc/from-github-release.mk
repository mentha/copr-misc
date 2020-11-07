latest-version:
	$(tooldir)/github-latest-release.py $(REPO)

spec:
	mkdir -p $(outdir)
	cp * $(outdir)/
	sed -i 's#^Version:.*$$#Version: $(shell $(tooldir)/github-latest-release.py $(REPO))#' $(outdir)/$(pkg).spec
	cd $(outdir) && spectool -g -A $(pkg).spec

include latest-release-from-spec.mk
