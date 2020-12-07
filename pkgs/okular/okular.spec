Version: 20.08.3
Release: 1%{?dist}

# based on fedora package okular
Name:    okular
Summary: A universal document viewer developed by KDE

License: GPLv2
URL:     https://www.kde.org/applications/graphics/okular/

Source0: https://download.kde.org/stable/release-service/%{version}/src/%{name}-%{version}.tar.xz

BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: extra-cmake-modules
BuildRequires: kf5-rpm-macros
BuildRequires: cmake(KDEExperimentalPurpose)
BuildRequires: cmake(KF5Activities)
BuildRequires: cmake(KF5Archive)
BuildRequires: cmake(KF5Bookmarks)
BuildRequires: cmake(KF5Completion)
BuildRequires: cmake(KF5Config)
BuildRequires: cmake(KF5ConfigWidgets)
BuildRequires: cmake(KF5CoreAddons)
BuildRequires: cmake(KF5Crash)
BuildRequires: cmake(KF5DBusAddons)
BuildRequires: cmake(KF5DocTools)
BuildRequires: cmake(KF5IconThemes)
BuildRequires: cmake(KF5JS)
BuildRequires: cmake(KF5KIO)
BuildRequires: cmake(KF5Kirigami2)
BuildRequires: cmake(KF5Parts)
BuildRequires: cmake(KF5Pty)
BuildRequires: cmake(KF5ThreadWeaver)
BuildRequires: cmake(KF5Wallet)
BuildRequires: cmake(KF5KHtml)
BuildRequires: cmake(KF5WindowSystem)
BuildRequires: cmake(Qt5DBus)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5PrintSupport)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(Qt5Quick)
BuildRequires: pkgconfig(phonon4qt5)
BuildRequires: cmake(Qca-qt5)
BuildRequires: cmake(KF5KExiv2)
BuildRequires: kdegraphics-mobipocket-devel
BuildRequires: chmlib-devel
BuildRequires: pkgconfig(libzip)
BuildRequires: ebook-tools-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(libmarkdown)
BuildRequires: pkgconfig(libspectre)
BuildRequires: pkgconfig(poppler-qt5)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(ddjvuapi)
BuildRequires:  cmake(Qt5TextToSpeech)

Requires: %{name}-part%{?_isa} = %{version}-%{release}

%description
Okular combines the excellent functionalities with the versatility of supporting different kind of documents, like PDF, Postscript, DjVu, CHM, XPS, ePub and others.

%package devel
Summary:  Development files for %{name}
Provides: okular5-devel = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package  libs
Summary:  Runtime files for %{name}
Recommends: cups-client
Recommends: ghostscript
%description libs
%{summary}.

%package part
Summary: Okular kpart plugin
Provides: okular5-part = %{version}-%{release}
Provides: okular5-part%{?_isa} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Conflicts: kde-l10n < 17.03
%description part
%{summary}.


%prep
%autosetup -p1
sed -i -e 's|^add_subdirectory( mobile )|#add_subdirectory( mobile )|' CMakeLists.txt

%build
%define __cmake_configure %__cmake -G'Unix Makefiles' .
%cmake_kf5
%make_build

%install
%make_install
%find_lang all --all-name --with-html --with-man
grep -v \
  -e %{_mandir} \
  -e %{_kf5_docdir} \
  all.lang > okular-part.lang
cat all.lang okular-part.lang | sort | uniq -u > okular.lang
rm %{buildroot}%{_kf5_datadir}/applications/org.kde.mobile.*

%check
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.okular.desktop
appstream-util validate-relax --nonet %{buildroot}%{_kf5_metainfodir}/org.kde.okular.appdata.xml

%files -f okular.lang
%license COPYING
%{_kf5_bindir}/okular
%{_kf5_datadir}/applications/org.kde.okular.desktop
%{_kf5_metainfodir}/org.kde.okular.appdata.xml
%{_kf5_datadir}/applications/okularApplication_*.desktop
%{_kf5_metainfodir}/org.kde.okular-*.metainfo.xml
%{_kf5_datadir}/okular/
%{_kf5_datadir}/icons/hicolor/*/*/*
%{_kf5_datadir}/kconf_update/okular.upd
%{_kf5_datadir}/qlogging-categories5/%{name}*
%{_mandir}/man1/okular.1*

%files devel
%{_includedir}/okular/
%{_libdir}/libOkular5Core.so
%{_libdir}/cmake/Okular5/

%ldconfig_scriptlets libs

%files libs
%{_libdir}/libOkular5Core.so.9*

%files part -f okular-part.lang
%{_qt5_plugindir}/kio_msits.so
%{_kf5_datadir}/kservices5/ms-its.protocol
%{_kf5_datadir}/config.kcfg/*.kcfg
%{_kf5_datadir}/kservices5/okular[A-Z]*.desktop
%{_kf5_datadir}/kservices5/okular_part.desktop
%{_kf5_datadir}/kservicetypes5/okularGenerator.desktop
%{_kf5_datadir}/kxmlgui5/okular/
%dir %{_qt5_plugindir}/okular/
%dir %{_qt5_plugindir}/okular/generators/
%{_qt5_plugindir}/okular/generators/okularGenerator_*.so
%{_qt5_plugindir}/okularpart.so
