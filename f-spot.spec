Summary:	Personal photo manager
Summary(pl):	Mened¿er prywatnych galerii fotograficznych
Name:		f-spot
Version:	0.0.1
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.0/%{name}-%{version}.tar.bz2
# Source0-md5:	5fa94700b0c071eb0afd8336526dd4a1
URL:		http://www.gnome.org/projects/f-spot/
BuildRequires:	GConf2-devel
BuildRequires:	gtk-sharp-devel >= 0.17
BuildRequires:	libexif-devel >= 0.5.7
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libjpeg-devel
BuildRequires:	mono-csharp >= 0.28
BuildRequires:	sqlite-devel >= 2.8.6
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
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README TODO
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/*.exe
%attr(755,root,root) %{_libdir}/%{name}/lib*.so*
%{_libdir}/%{name}/lib*.la
