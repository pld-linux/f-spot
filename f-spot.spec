#
# TODO:
#	- update aflinta's delete.patch
#	- check if fs patch is still needed, propably causes weird effects on my box
#	- use system mono-addins
#
%include	/usr/lib/rpm/macros.mono
#
Summary:	Personal photo manager
Summary(pl.UTF-8):	Menedżer prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.4.2
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/Public/GNOME/sources/f-spot/0.4/%{name}-%{version}.tar.bz2
# Source0-md5:	970b8c9de9acf97c90e3d9608827606d
Patch0:		%{name}-exec.patch
Patch1:		%{name}-dir.patch
Patch2:		%{name}-fs.patch
Patch3:		%{name}-delete.patch
# http://bugzilla.gnome.org/show_bug.cgi?id=516620
Patch4:		%{name}-DESTDIR.patch
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	dotnet-ndesk-dbus-glib-sharp-devel
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	intltool >= 0.35
BuildRequires:	lcms-devel >= 1.12
BuildRequires:	libexif-devel >= 1:0.6.13
BuildRequires:	libgnomeui-devel >= 2.16.0
BuildRequires:	libgphoto2-devel >= 2.2.1
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.1.16.1
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
%patch0 -p1
%patch1 -p0
%patch2 -p1
#%patch3 -p0
%patch4 -p1

%build
%{__intltoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-static \
	--disable-scrollkeeper \
	--with-gnome-screensaver=%{_prefix}

# <make-jN-workaround>
%{__make} -C extensions/FlickrExport/FlickrNet \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers

%{__make} -C extensions/PicasaWebExport/google-sharp \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers

%{__make} -C extensions/SmugMugExport/SmugMugNet \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers
# </make-jN-workaround>

%{__make} \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_desktopdir}/screensavers

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
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
%{_libdir}/%{name}/*.dll.config
%{_libdir}/%{name}/*.exe.config
%{_desktopdir}/*.desktop
%{_pkgconfigdir}/f-spot.pc

%files screensaver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-screensaver/f-spot-screensaver
%{_desktopdir}/screensavers/f-spot-screensaver.desktop
