Summary:	Personal photo manager
Summary(pl):	Mened¿er prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.0.2
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.0/%{name}-%{version}.tar.bz2
# Source0-md5:	8edd68204233b75579fad0bb64f841f8
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel
BuildRequires:	dotnet-gtk-sharp-devel >= 1.0
BuildRequires:	intltool >= 0.21
BuildRequires:	libexif-devel >= 1:0.5.7
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libjpeg-devel
BuildRequires:	mono-csharp >= 1.0
BuildRequires:	sqlite2-devel >= 2.8.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
F-Spot is an application designed to provide personal photo management
to the GNOME desktop.

%description -l pl
F-Spot jest prywatnym mened¿erem galerii fotograficznych dla
¶rodowiska GNOME.

%prep
%setup -q

%build
%configure \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.exe
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*
%{_libdir}/%{name}/lib*.la
%{_libdir}/%{name}/*.exe.config
