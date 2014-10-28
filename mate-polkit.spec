Summary:	MATE dialogs for polkit
Name:		mate-polkit
Version:	1.8.0
Release:	2
License:	LGPL v2+ (polkit-mate library), GPL v2+ (D-Bus service)
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.8/%{name}-%{version}.tar.xz
# Source0-md5:	bd7dfb225e1ba6aac3c5752d496071d8
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	yelp-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/%{name}

%description
polkit-mate provides a D-BUS session bus service that is used to
bring up authentication dialogs used for obtaining privileges.

%prep
%setup -q

# kill mate-common deps
%{__sed} -i -e '/MATE_COMPILE_WARNINGS.*/d'	\
    -i -e '/MATE_MAINTAINER_MODE_DEFINES/d'	\
    -i -e '/MATE_COMMON_INIT/d'			\
    -i -e '/MATE_CXX_WARNINGS.*/d'		\
    -i -e '/MATE_DEBUG_CHECK/d' configure.ac

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-examples	\
	--disable-silent-rules	\
	--disable-static	\
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun	-p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS ChangeLog
%dir %{_libexecdir}
%attr(755,root,root) %ghost %{_libdir}/libpolkit-gtk-mate-1.so.0
%attr(755,root,root) %{_libdir}/libpolkit-gtk-mate-1.so.0.0.0
%attr(755,root,root) %{_libexecdir}/polkit-mate-authentication-agent-1
%{_libdir}/girepository-1.0/PolkitGtkMate-1.0.typelib
%{_sysconfdir}/xdg/autostart/polkit-mate-authentication-agent-1.desktop

