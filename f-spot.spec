#
%include	/usr/lib/rpm/macros.mono
#
Summary:	Personal photo manager
Summary(pl):	Mened¿er prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.2.2
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/gnome/sources/f-spot/0.2/%{name}-%{version}.tar.bz2
# Source0-md5:	69b4e70546b4ab1d7dcc7095fcfa65cd
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-exec.patch
Patch2:		%{name}-dir.patch
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel >= 2.14.0
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotnet-dbus-sharp-devel >= 0.63
BuildRequires:	dotnet-gnome-sharp-devel >= 2.16.0
BuildRequires:	gettext-devel
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
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	sqlite-devel >= 2.8.6
Requires(post,postun):	desktop-file-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
F-Spot is an application designed to provide personal photo management
to the GNOME desktop.

%description -l pl
F-Spot jest prywatnym mened¿erem galerii fotograficznych dla
¶rodowiska GNOME.

%package screensaver
Summary:	Module for gnome-screensaver
Summary(pl):	Modu³ dla gnome-screensavera
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-screensaver

%description screensaver
F-Spot module for gnome-screensaver.

%description screensaver -l pl
Modu³ F-Spot dla gnome-screensavera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0

%build
%{__intltoolize}
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--disable-static \
	--with-gnome-screensaver=%{_prefix}

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

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.exe
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*
%{_libdir}/%{name}/*.dll
%{_libdir}/%{name}/*.dll.config
%{_libdir}/%{name}/*.exe.config
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_pkgconfigdir}/f-spot.pc

%files screensaver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-screensaver/f-spot-screensaver
%{_desktopdir}/screensavers/f-spot-screensaver.desktop
