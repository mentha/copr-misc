Name:      wine50-mono
Version:   4.9.4
Release:   1%{?dist}
Summary:   an open-source and cross-platform implementation of the .NET Framework
BuildArch: x86_64

License: LGPLv2
URL:     https://github.com/madewokherd/wine-mono
Source0: http://dl.winehq.org/wine/wine-mono/%{version}/wine-mono-bin-%{version}.tar.gz

BuildRequires: tar
BuildRequires: gzip

Requires: wine50

%description
Wine Mono is a package containing Mono and other projects, intended as a replacement for the .NET runtime and class libraries in Wine. It works in conjunction with Wine's builtin mscoree.dll, and it is not intended to be useful for any other purpose.

%prep
%setup -q -c

%install
%define dest %{buildroot}/%{_datadir}/wine/mono
mkdir -p %{dest}
cp -r wine-mono-%{version} %{dest}/

%files
%{_datadir}/wine/mono/
