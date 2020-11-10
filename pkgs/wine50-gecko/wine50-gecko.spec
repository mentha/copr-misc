Name:      wine50-gecko
Version:   2.47.1
Release:   1%{?dist}
Summary:   Wine's own version of Internet Explorer

License: MPLv2
URL:     https://www.winehq.org/
Source0: http://dl.winehq.org/wine/wine-gecko/%{version}/wine-gecko-%{version}-x86.tar.bz2
Source1: http://dl.winehq.org/wine/wine-gecko/%{version}/wine-gecko-%{version}-x86_64.tar.bz2

BuildRequires: tar
BuildRequires: bzip2

Requires: wine50

%description
Wine implements its own version of Internet Explorer. The implementation is based on a custom version of Mozilla's Gecko Layout Engine. When your application tries to display a site, Wine loads and uses its custom implementation of Gecko.

%prep
%setup -T -a 0 -q -c
%setup -T -a 1 -q -c -D

%install
%define dest %{buildroot}/%{_datadir}/wine/gecko
mkdir -p %{dest}
cp -r wine-gecko-%{version}-x86 %{dest}/
cp -r wine-gecko-%{version}-x86_64 %{dest}/

%files
%{_datadir}/wine/gecko/
