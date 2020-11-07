latest-release: spec
	cd $(outdir) && rpmspec -q --srpm --qf '%|epoch?{%{epoch}:}:{}|%{version}-%{release}\n' $(pkg).spec
