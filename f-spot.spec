
%include	/usr/lib/rpm/macros.mono
Summary:	Personal photo manager
Summary(pl):	Mened¿er prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.1.11
Release:	6
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/gnome/sources/f-spot/0.1/%{name}-%{version}.tar.bz2
# Source0-md5:	d4d75f6a5272fa15b5658abdf708b050
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-exec.patch
Patch2:		%{name}-dir.patch
Patch3:		%{name}-utf8.patch
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dotnet-dbus-sharp-devel
BuildRequires:	dotnet-gtk-sharp2-gnome-devel >= 2.7
BuildRequires:	gettext-devel
BuildRequires:	intltool >= 0.21
BuildRequires:	lcms-devel >= 1.12
BuildRequires:	libexif-devel >= 1:0.6.12
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libgphoto2-devel >= 2.1.99
BuildRequires:	libjpeg-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	mono-csharp >= 1.1.7
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
%patch3 -p0

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
	themesdir=%{_datadir}/gnome-screensaver/themes

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	saverdir=%{_libdir}/gnome-screensaver \
	themesdir=%{_datadir}/gnome-screensaver/themes

rm -f $RPM_BUILD_ROOT%{_libdir}/%{name}/*.la
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

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

%files screensaver
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gnome-screensaver/f-spot-screensaver
%{_datadir}/gnome-screensaver/themes/f-spot-screensaver.desktop
