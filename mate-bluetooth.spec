Summary:	MATE Bluetooth Subsystem
Summary(pl.UTF-8):	Podsystem MATE Bluetooth
Name:		mate-bluetooth
Version:	1.6.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://pub.mate-desktop.org/releases/1.6/%{name}-%{version}.tar.xz
# Source0-md5:	3a080314d10e28918393047ea67b9177
URL:		http://wiki.mate-desktop.org/docs:mate-bluetooth
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake >= 1:1.9
BuildRequires:	dbus-glib-devel >= 0.74
BuildRequires:	docbook-dtd43-xml
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.26.0
BuildRequires:	gobject-introspection-devel >= 0.6.7
BuildRequires:	gtk+2-devel >= 2:2.20.0
BuildRequires:	gtk-doc >= 1.9
BuildRequires:	intltool >= 0.40.4
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libunique-devel >= 1.0
BuildRequires:	mate-common
BuildRequires:	mate-doc-utils >= 0.9.0
BuildRequires:	mate-file-manager-sendto-devel >= 1.1.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.592
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xz
Requires(post,postun):	glib2 >= 1:2.26.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	%{name}-libs = %{version}-%{release}
Requires:	bluez >= 4.36
Requires:	dbus(org.openobex.client)
Requires:	dconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mate-bluetooth is a fork of gnome-bluetooth (and it is a fork of
bluez-gnome) focused on integration with the MATE desktop environment.

%description -l pl.UTF-8
mate-bluetooth to odgałęzienie pakietu gnome-bluetooth (będącego z
kolei odgałęzieniem bluez-gnome), skupiające się na integracji ze
środowiskiem graficznym MATE.

%package libs
Summary:	MATE Bluetooth subsystem shared libraries
Summary(pl.UTF-8):	Współdzielone biblioteki dla podsystemu MATE Bluetooth
License:	LGPL v2+
Group:		X11/Libraries
Requires:	dbus-glib >= 0.74
Requires:	glib2 >= 1:2.26.0
Requires:	gtk+2 >= 2:2.20.0

%description libs
MATE Bluetooth subsystem shared libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki dla podsystemu MATE Bluetooth.

%package devel
Summary:	Header files for MATE Bluetooth subsystem
Summary(pl.UTF-8):	Pliki nagłówkowe dla podsystemu MATE Bluetooth
License:	LGPL v2+
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-glib-devel >= 0.74
Requires:	glib2-devel >= 1:2.26.0
Requires:	gtk+2-devel >= 2:2.20.0

%description devel
Header files for MATE Bluetooth subsystem.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla podsystemu MATE Bluetooth.

%package apidocs
Summary:	MATE Bluetooth library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki MATE Bluetooth
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
MATE Bluetooth library API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki MATE Bluetooth.

%package -n mate-file-manager-sendto-bluetooth
Summary:	caja-sendto MATE Bluetooth plugin
Summary(pl.UTF-8):	Wtyczka caja-sendto dla MATE Bluetooth
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	mate-file-manager-sendto >= 1.1.0

%description -n mate-file-manager-sendto-bluetooth
A caja-sendto plugin for sending files via MATE Bluetooth.

%description -n mate-file-manager-sendto-bluetooth -l pl.UTF-8
Wtyczka caja-sentdo do wysyłania plików poprzez MATE Bluetooth.

%prep
%setup -q

%build
mate-doc-prepare --copy --force
%{__gtkdocize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-gtk-doc \
	--disable-desktop-update \
	--disable-icon-update \
	--disable-schemas-install \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/caja-sendto/plugins/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/mate-bluetooth/plugins/*.la

# mate < 1.5 did not exist in PLD, avoid dependency on mate-conf
%{__rm} $RPM_BUILD_ROOT%{_datadir}/MateConf/gsettings/mate-bluetooth*

%find_lang %{name} --with-mate --with-omf --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache mate
%glib_compile_schemas

%postun
%update_icon_cache mate
%glib_compile_schemas

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	-n mate-file-manager-sendto-bluetooth
%glib_compile_schemas

%postun	-n mate-file-manager-sendto-bluetooth
%glib_compile_schemas

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/mate-bluetooth-applet
%attr(755,root,root) %{_bindir}/mate-bluetooth-properties
%attr(755,root,root) %{_bindir}/mate-bluetooth-sendto
%attr(755,root,root) %{_bindir}/mate-bluetooth-wizard
%dir %{_libdir}/mate-bluetooth
%dir %{_libdir}/mate-bluetooth/plugins
%attr(755,root,root) %{_libdir}/mate-bluetooth/plugins/libgbtgeoclue.so
%{_datadir}/glib-2.0/schemas/org.mate.Bluetooth.gschema.xml
%{_datadir}/mate-bluetooth
%{_sysconfdir}/xdg/autostart/mate-bluetooth-applet.desktop
%{_desktopdir}/mate-bluetooth-properties.desktop
%{_iconsdir}/mate/*/apps/bluetooth.*
%{_iconsdir}/mate/*/status/bluetooth-*.*
%{_mandir}/man1/mate-bluetooth-applet.1*
%{_mandir}/man1/mate-bluetooth-properties.1*
%{_mandir}/man1/mate-bluetooth-sendto.1*
%{_mandir}/man1/mate-bluetooth-wizard.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-bluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmate-bluetooth.so.8
%{_libdir}/girepository-1.0/MateBluetooth-1.0.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libmate-bluetooth.so
%{_datadir}/gir-1.0/MateBluetooth-1.0.gir
%{_includedir}/mate-bluetooth
%{_pkgconfigdir}/mate-bluetooth-1.0.pc

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/mate-bluetooth

%files -n mate-file-manager-sendto-bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/caja-sendto/plugins/libnstbluetooth.so
%{_datadir}/glib-2.0/schemas/org.mate.Bluetooth.nst.gschema.xml
