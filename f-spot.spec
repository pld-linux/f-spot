#
# TODO:
#	- use system libgphoto2-sharp.dll, NDesk.Glitz.dll, gnome-keyring-sharp.dll
#	  Tao (http://www.taoframework.com/), semweb (http://taubz.for.net/code/semweb)
#
%include	/usr/lib/rpm/macros.mono
%define		_noautoreq 'mono(Mono.*)' 'mono(FlickrNet)' 'mono(gnome-keyring-sharp)'
#
Summary:	Personal photo manager
Summary(pl.UTF-8):	Menedżer prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.6.1.5
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/Public/GNOME/sources/f-spot/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	411bac8266a60d9a728218d19dd5e735
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	beagle-devel >= 0.3.0
BuildRequires:	dotnet-gnome-desktop-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.12.1
BuildRequires:	dotnet-libgphoto2-sharp-devel >= 2.1.4
BuildRequires:	dotnet-ndesk-dbus-glib-sharp-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-icon-theme
BuildRequires:	gtk+2-devel >= 2:2.12.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	lcms-devel >= 1.12
BuildRequires:	libexif-devel >= 1:0.6.13
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libgphoto2-devel >= 2.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	mono-addins-devel
BuildRequires:	mono-csharp >= 1.1.17
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite-devel >= 2.8.6
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	dotnet-libgphoto2-sharp
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
ExclusiveArch:	%{ix86} %{x8664} arm hppa ia64 ppc s390 s390x sparc sparcv9
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
F-Spot is an application designed to provide personal photo management
to the GNOME desktop.

%description -l pl.UTF-8
F-Spot jest prywatnym menedżerem galerii fotograficznych dla
środowiska GNOME.

%package screensaver
Summary:	Module for gnome-screensaver
Summary(pl.UTF-8):	Moduł dla gnome-screensavera
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-screensaver

%description screensaver
F-Spot module for gnome-screensaver.

%description screensaver -l pl.UTF-8
Moduł F-Spot dla gnome-screensavera.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-static \
	--disable-scrollkeeper \
	--with-gnome-screensaver=%{_prefix}

%{__make} -j1 \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.exe
%{_libdir}/%{name}/*.addins
%dir %{_libdir}/%{name}/extensions
%{_libdir}/%{name}/extensions/*
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*
%{_libdir}/%{name}/*.dll
%{_libdir}/%{name}/*.mdb
%{_libdir}/%{name}/*.dll.config
%{_libdir}/%{name}/*.exe.config
%{_desktopdir}/*.desktop
%{_pkgconfigdir}/f-spot.pc

%files screensaver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-screensaver/f-spot-screensaver
%{_desktopdir}/screensavers/f-spot-screensaver.desktop
