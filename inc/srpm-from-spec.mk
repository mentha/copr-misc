srpm: spec
	rpmbuild \
		--define '_sourcedir $(outdir)' \
		--define '_specdir $(outdir)' \
		--define '_builddir $(outdir)' \
		--define '_srcrpmdir $(outdir)' \
		--define '_rpmdir $(outdir)' \
		--nodeps \
		-bs $(outdir)/$(pkg).spec
