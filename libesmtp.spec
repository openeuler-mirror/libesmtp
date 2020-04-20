%define plugindir %{_libdir}/esmtp-plugins

Name:           libesmtp
Version:        1.0.6
Release:        19
Summary:        A library for posting electronic mail
License:        LGPLv2+

URL:            https://www.stafford.uklinux.net/%{name}/
Source:         https://www.stafford.uklinux.net/%{name}/%{name}-%{version}.tar.bz2
Patch0:         libesmtp-1.0.6-openssl-1.1.patch
Patch1:         CVE-2019-19977.patch
BuildRequires:  gcc openssl-devel pkgconfig autoconf automake libtool

%description
%{name} is an SMTP client which manages posting (or submission of) electronic
mail via a preconfigured Mail Transport Agent (MTA). It may be used as part of
a Mail User Agent (MUA) or other program that must be able to post electronic
mail where mail functionality may not be that program's primary purpose.

%package 	devel
Summary:	Header and development files for %{name}
License:	LGPLv2+ and GPLv2+
Requires:	%{name} = %{version}-%{release}, openssl-devel

%description 	devel
%{name}-devel contains the header files for developing
applications that want to make use of %{name}.

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

autoreconf -fi

chmod a-x htable.c

%build

if pkg-config openssl ; then
  export CFLAGS="$CFLAGS $RPM_OPT_FLAGS `pkg-config --cflags openssl`"
  export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L openssl`"
fi
%configure --with-auth-plugin-dir=%{plugindir} --enable-pthreads \
  --enable-require-all-recipients --enable-debug \
  --enable-etrn --disable-isoc --disable-more-warnings
make %{?_smp_mflags}
cat << "EOF" > %{name}.pc
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name:		 libESMTP
Version: 	 %{version}
Description:	 SMTP client library.
Requires:	 openssl
Libs:		 -pthread -L${libdir} -lesmtp
Cflags:
EOF

cat << "EOF" > %{name}-config
#! /bin/sh
exec pkg-config "$@" libesmtp
EOF

%install
%make_install
install -p -m 644 -D %{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc

%delete_la

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYING COPYING.LIB
%doc AUTHORS
%{_libdir}/%{name}.so.*
%{plugindir}

%files devel
%defattr(-,root,root)
%doc examples
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}.a
%{_prefix}/include/*.h

%files help
%defattr(-,root,root)
%doc NEWS Notes README

%changelog
* Mon Apr 20 2020 openEuler Buildteam <buildteam@openeuler.org> - 1.0.6-19
- Type:cves
- ID:CVE-2019-19977
- SUG:NA
- DESC:remove ntlm_build_type_2() to fix CVE-2019-19977
 
* Mon Oct 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.6-18
- Type:enhancement
- Id:NA
- SUG:NA
- DESC:modify the location of COPYING

* Sun Sep 15 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.0.6-17
- Package init
