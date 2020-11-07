FEDORA_RELEASE ?= 33

GIT_REPO = https://src.fedoraproject.org/rpms/$(pkg).git
BRANCH   = f$(FEDORA_RELEASE)
SPEC     = $(pkg).spec

include from-git.mk
