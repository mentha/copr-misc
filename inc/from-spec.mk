include default-vars.mk

latest-version:
	awk '/^Version:/{ print $$2 }' $(SPEC)

spec:
	mkdir -p $(outdir)
	cp -r $(SRCS) $(outdir)/
	cd $(outdir) && spectool --get-files --all $(pkg).spec

include latest-release-from-spec.mk

include srpm-from-spec.mk
