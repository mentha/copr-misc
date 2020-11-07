latest-release: spec
	cd $(outdir) && rpmspec -q --srpm --qf '%{version}-%{release}\n' $(pkg).spec
