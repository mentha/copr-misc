Name:    wine50
Version: 5.0.2
Release: 1%{?dist}
Summary: a compatibility layer capable of running Windows applications

License: LGPLv2+
URL:     https://www.winehq.org/
Source0: https://dl.winehq.org/wine/source/5.0/wine-%{version}.tar.xz

BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc
BuildRequires: mingw32-gcc
BuildRequires: mingw64-gcc

BuildRequires: SDL2-devel SDL2-devel(x86-32)
BuildRequires: cups-devel cups-devel(x86-32)
BuildRequires: dbus-devel dbus-devel(x86-32)
BuildRequires: fontconfig-devel fontconfig-devel(x86-32)
BuildRequires: freetype-devel freetype-devel(x86-32)
BuildRequires: glibc-devel glibc-devel(x86-32)
BuildRequires: gnutls-devel gnutls-devel(x86-32)
BuildRequires: gstreamer1-devel gstreamer1-devel(x86-32)
BuildRequires: gstreamer1-plugins-base-devel gstreamer1-plugins-base-devel(x86-32)
BuildRequires: krb5-devel krb5-devel(x86-32)
BuildRequires: libX11-devel libX11-devel(x86-32)
BuildRequires: libXcomposite-devel libXcomposite-devel(x86-32)
BuildRequires: libXcursor-devel libXcursor-devel(x86-32)
BuildRequires: libXext-devel libXext-devel(x86-32)
BuildRequires: libXfixes-devel libXfixes-devel(x86-32)
BuildRequires: libXinerama-devel libXinerama-devel(x86-32)
BuildRequires: libXrandr-devel libXrandr-devel(x86-32)
BuildRequires: libXrender-devel libXrender-devel(x86-32)
BuildRequires: libXxf86vm-devel libXxf86vm-devel(x86-32)
BuildRequires: libcom_err-devel libcom_err-devel(x86-32)
BuildRequires: libglvnd-devel libglvnd-devel(x86-32)
BuildRequires: libjpeg-devel libjpeg-devel(x86-32)
BuildRequires: libpng-devel libpng-devel(x86-32)
BuildRequires: libtiff-devel libtiff-devel(x86-32)
BuildRequires: libunwind-devel
BuildRequires: libusb-devel libusb-devel(x86-32)
BuildRequires: libv4l-devel libv4l-devel(x86-32)
BuildRequires: libvkd3d-devel
BuildRequires: libxml2-devel libxml2-devel(x86-32)
BuildRequires: libxslt-devel libxslt-devel(x86-32)
BuildRequires: mesa-libOSMesa-devel mesa-libOSMesa-devel(x86-32)
BuildRequires: mpg123-devel mpg123-devel(x86-32)
BuildRequires: ncurses-devel ncurses-devel(x86-32)
BuildRequires: openal-soft-devel openal-soft-devel(x86-32)
BuildRequires: pulseaudio-libs-devel pulseaudio-libs-devel(x86-32)
BuildRequires: systemd-devel systemd-devel(x86-32)
BuildRequires: vulkan-loader-devel vulkan-loader-devel(x86-32)
BuildRequires: zlib-devel zlib-devel(x86-32)

%description
Wine (originally an acronym for "Wine Is Not an Emulator") is a compatibility layer capable of running Windows applications on several POSIX-compliant operating systems, such as Linux, macOS, & BSD. Instead of simulating internal Windows logic like a virtual machine or emulator, Wine translates Windows API calls into POSIX calls on-the-fly, eliminating the performance and memory penalties of other methods and allowing you to cleanly integrate Windows applications into your desktop.

%prep
%autosetup -n wine-%{version}

%build

%define config_options --prefix=%{_prefix} --disable-tests --with-cups --with-curses --with-dbus --with-fontconfig --with-freetype --with-gnutls --with-gstreamer --with-jpeg --with-mingw --with-mpg123 --with-openal --with-opengl --with-osmesa --with-png --with-pthread --with-pulse --with-sdl --with-tiff --with-udev --with-v4l2 --with-vulkan --with-x --with-xcomposite --with-xcursor --with-xfixes --with-xinerama --with-xinput2 --with-xml --with-xrandr --with-xrender --with-xshape --with-xshm --with-xslt --with-xxf86vm --with-zlib --without-alsa --without-capi --without-cms --without-coreaudio --without-faudio --without-gettext --without-gettextpo --without-glu --without-gphoto --without-gsm --without-gssapi --without-hal --without-inotify --without-krb5 --without-ldap --without-netapi --without-opencl --without-oss --without-pcap --without-sane
# autodetect --with-unwind --with-vkd3d

mkdir build-w64 build-wow64

cd build-w64
../configure --enable-win64 %{config_options}
%make_build
cd ../build-wow64
env PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig \
		    ../configure --with-wine64=../build-w64 %{config_options}
%make_build

%install
cd build-w64
%make_install
cd ../build-wow64
%make_install

%files
%{_bindir}/function_grep.pl
%{_bindir}/msidb
%{_bindir}/msiexec
%{_bindir}/notepad
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/widl
%{_bindir}/wine
%{_bindir}/wine-preloader
%{_bindir}/wine64
%{_bindir}/wine64-preloader
%{_bindir}/wineboot
%{_bindir}/winebuild
%{_bindir}/winecfg
%{_bindir}/wineconsole
%{_bindir}/winecpp
%{_bindir}/winedbg
%{_bindir}/winedump
%{_bindir}/winefile
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/winemine
%{_bindir}/winepath
%{_bindir}/wineserver
%{_bindir}/wmc
%{_bindir}/wrc
%{_datadir}/applications/wine.desktop
%{_datadir}/wine/
%{_includedir}/wine/
%{_prefix}/lib/libwine.so
%{_prefix}/lib/libwine.so.1
%{_prefix}/lib/libwine.so.1.0
%{_prefix}/lib/wine/
%{_prefix}/lib64/libwine.so
%{_prefix}/lib64/libwine.so.1
%{_prefix}/lib64/libwine.so.1.0
%{_prefix}/lib64/wine/

%doc %{_mandir}/de.UTF-8/man1/wine.1.gz
%doc %{_mandir}/de.UTF-8/man1/winemaker.1.gz
%doc %{_mandir}/de.UTF-8/man1/wineserver.1.gz
%doc %{_mandir}/fr.UTF-8/man1/wine.1.gz
%doc %{_mandir}/fr.UTF-8/man1/winemaker.1.gz
%doc %{_mandir}/fr.UTF-8/man1/wineserver.1.gz
%doc %{_mandir}/man1/msiexec.1.gz
%doc %{_mandir}/man1/notepad.1.gz
%doc %{_mandir}/man1/regedit.1.gz
%doc %{_mandir}/man1/regsvr32.1.gz
%doc %{_mandir}/man1/widl.1.gz
%doc %{_mandir}/man1/wine.1.gz
%doc %{_mandir}/man1/wineboot.1.gz
%doc %{_mandir}/man1/winebuild.1.gz
%doc %{_mandir}/man1/winecfg.1.gz
%doc %{_mandir}/man1/wineconsole.1.gz
%doc %{_mandir}/man1/winecpp.1.gz
%doc %{_mandir}/man1/winedbg.1.gz
%doc %{_mandir}/man1/winedump.1.gz
%doc %{_mandir}/man1/winefile.1.gz
%doc %{_mandir}/man1/wineg++.1.gz
%doc %{_mandir}/man1/winegcc.1.gz
%doc %{_mandir}/man1/winemaker.1.gz
%doc %{_mandir}/man1/winemine.1.gz
%doc %{_mandir}/man1/winepath.1.gz
%doc %{_mandir}/man1/wineserver.1.gz
%doc %{_mandir}/man1/wmc.1.gz
%doc %{_mandir}/man1/wrc.1.gz
%doc %{_mandir}/pl.UTF-8/man1/wine.1.gz
