include default-vars.mk

latest-version:
	$(tooldir)/github-latest-release.py $(REPO)

spec:
	mkdir -p $(outdir)
	cp -r $(SRCS) $(outdir)/
	sed -i 's#^Version:.*$$#Version: $(shell $(tooldir)/github-latest-release.py $(REPO))#' $(outdir)/$(pkg).spec
	cd $(outdir) && spectool --get-files --all $(pkg).spec

include latest-release-from-spec.mk

include srpm-from-spec.mk
