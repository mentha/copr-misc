Version:        1.5
Release:        1%{?dist}

Name:           i3blocks
Summary:        A feed generator for text based status bars
License:        GPLv3
URL:            https://github.com/vivien/i3blocks
Source0:        %{URL}/archive/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake

%description
A feed generator for text based status bars.

%prep
%autosetup

%build
./autogen.sh
%configure
%make_build

%install
%make_install INSTALL="install -p"
#install -Dpm0644 i3lock.1 %{buildroot}%{_mandir}/man1/i3lock.1

%files
%license COPYING
%{_bindir}/%{name}
%{_sysconfdir}/i3blocks.conf
%{_mandir}/man1/i3blocks.1.gz
%{_datarootdir}/bash-completion/completions/i3blocks
