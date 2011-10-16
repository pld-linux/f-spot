#
%bcond_with	gnome2
#
%include	/usr/lib/rpm/macros.mono
Summary:	Personal photo manager
Summary(pl.UTF-8):	Menedżer prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.8.2
Release:	5
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/Public/GNOME/sources/f-spot/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	3f2286835c9cdf44e50bc564d8e6b892
Patch1:		%{name}-PixbufLoader.patch
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotnet-flickrnet
BuildRequires:	dotnet-gnome-keyring-sharp-devel
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-gtk-sharp2-devel >= 2.12.1
BuildRequires:	dotnet-ndesk-dbus-glib-sharp-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-icon-theme
BuildRequires:	intltool >= 0.40.0
BuildRequires:	lcms-devel >= 1.12
BuildRequires:	libgnome-keyring-devel
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libtool
BuildRequires:	libunique-devel
BuildRequires:	mono-addins-devel
BuildRequires:	mono-csharp >= 1.1.17
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	mono-addins
Suggests:	dcraw
Suggests:	udev-libgphoto2
Suggests:	dbus-x11
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
ExclusiveArch:	%{ix86} %{x8664} arm hppa ia64 ppc s390 s390x sparc sparcv9
ExcludeArch:	i386
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreq mono(Mono.*) mono(FlickrNet) mono(gnome-keyring-sharp)

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
%patch1 -p1

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I build/m4/f-spot -I build/m4/shamrock -I build/m4/shave
%{__autoconf}
%{__autoheader}
%{__automake}
CFLAGS="-pthread -I/usr/include/gtk-2.0 -I/usr/lib64/gtk-2.0/include -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/include/gio-unix-2.0/ -I/usr/include/glib-2.0 -I/usr/lib64/glib-2.0/include -I/usr/include/pixman-1 -I/usr/include/freetype2 -I/usr/include/libpng14"
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
%gconf_schema_install:

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor
%gconf_schema_uninstall

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_iconsdir}/hicolor/*/*/*.*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.exe
%{_libdir}/%{name}/*.addins
%dir %{_libdir}/%{name}/Extensions
%{_libdir}/%{name}/Extensions/*
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*
%{_libdir}/%{name}/*.dll
%{_libdir}/%{name}/*.mdb
%{_libdir}/%{name}/*.dll.config
%{_libdir}/%{name}/*.exe.config
%{_desktopdir}/*.desktop
%{_pkgconfigdir}/f-spot.pc
%{_sysconfdir}/gconf/schemas/f-spot.schemas

%if %{with gnome2}
%files screensaver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-screensaver/f-spot-screensaver
%{_desktopdir}/screensavers/f-spot-screensaver.desktop
%endif
