Summary:	A portable, high level programming interface to various calling conventions
Name:		libffi
Version:	3.4.2
Release:	1%{?dist}
License:	BSD
URL:		http://sourceware.org/libffi/
Group:		System Environment/GeneralLibraries
Vendor:		VMware, Inc.
Distribution: 	Photon
Source0:	ftp://sourceware.org/pub/libffi/%{name}-%{version}.tar.gz
%define sha512  %{name}=31bad35251bf5c0adb998c88ff065085ca6105cf22071b9bd4b5d5d69db4fadf16cadeec9baca944c4bb97b619b035bb8279de8794b922531fddeb0779eb7fb1
Provides:	pkgconfig(libffi)

%if %{with_check}
BuildRequires:  dejagnu
%endif

%description
The libffi library provides a portable, high level programming interface
to various calling conventions. This allows a programmer to call any
function specified by a call interface description at run time.

%package        devel
Summary:        Header and development files for libffi
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup

%build
sed -e '/^includesdir/ s:$(libdir)/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:$(includedir):' \
    -i include/Makefile.in &&
sed -e '/^includedir/ s:${libdir}/@PACKAGE_NAME@-@PACKAGE_VERSION@/include:@includedir@:' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in        &&
%configure \
	--disable-static
make %{?_smp_mflags}

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install %{?_smp_mflags}
install -D -m644 LICENSE %{buildroot}/usr/share/licenses/%{name}/LICENSE
find %{buildroot}/%{_lib64dir} -name '*.la' -delete
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%ldconfig_scriptlets

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_lib64dir}/*.so*

%files devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datarootdir}/licenses/libffi/LICENSE
%{_mandir}/man3/*

%changelog
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 3.4.2-1
- Automatic Version Bump
* Wed Jul 08 2020 Gerrit Photon <photon-checkins@vmware.com> 3.3-1
- Automatic Version Bump
* Fri Nov 09 2018 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-7
- Cross compilation support
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-6
- Aarch64 support
* Wed Jul 12 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-5
- Get tcl, expect and dejagnu from packages
* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.2.1-4
- Added -devel subpackage
* Thu Oct 06 2016 ChangLee <changlee@vmware.com> 3.2.1-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.2.1-2
- GA - Bump release of all rpms
* Fri Jan 15 2016 Xiaolin Li <xiaolinl@vmware.com> 3.2.1-1
- Updated to version 3.2.1
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 3.1-1
- Initial build. First version.
