include default-vars.mk

gitdir ?= ./gitrepo
gitdir := $(abspath $(gitdir))

latest-version: git-clone
	cd $(gitdir) && rpmspec -q --srpm --qf '%{version}\n' $(SPEC)

latest-release: git-clone
	cd $(gitdir) && rpmspec -q --srpm --qf '%{version}-%{release}\n' $(SPEC)

spec: git-clone
	mkdir -p $(outdir)
	cp -r $(gitdir)/* $(outdir)/
	cd $(outdir) && spectool -g -A $(SPEC)
	[ -e $(outdir)/sources ] && cd $(outdir) && $(tooldir)/verify_sources.py sources

git-clone:
	if [ -d $(gitdir)/.git ]; then \
		cd $(gitdir); \
		git clean -xdf; \
		git fetch --all; \
		git checkout $(BRANCH); \
	else \
		git clone \
			--recursive --depth=1 --branch=$(BRANCH) --single-branch \
			$(GIT_REPO) $(gitdir); \
	fi
