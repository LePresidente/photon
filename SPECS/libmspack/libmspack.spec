Summary:        A library that provides compression and decompression of file formats used by Microsoft
Name:           libmspack
Version:        0.10.1alpha
Release:        1%{?dist}
License:        LGPLv2+
URL:            http://www.cabextract.org.uk/libmspack/libmspack-0.5alpha.tar.gz
Group:          Applications/System
Vendor:         VMware, Inc.
Distribution:   Photon
Source0:        http://www.cabextract.org.uk/libmspack/%{name}-%{version}.tar.gz
%define sha1    libmspack=82a6a102a2422d4d61bdd00f059bd3978409ca5f
%description
A library that provides compression and decompression of file formats used by Microsoft

%package        devel
Summary:        Header and development files for libmspack
Requires:       %{name} = %{version}-%{release}
%description    devel
It contains the libraries and header files to create applications.

%prep
%setup -q

%build
%configure
#Package does not support parallel make
make

%install
make DESTDIR=%{buildroot} install

%check
cd test
./cabd_test

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*

%files  devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.la
%{_libdir}/*.so

%changelog
*   Mon Apr 13 2020 Sujay G <gsujay@vmware.com> 0.10.1alpha-1
-   Bump version to 0.10.1alpha, to fix CVE-2019-1010305
*   Mon Sep 10 2018 Bo Gan <ganb@vmware.com> 0.7.1alpha-1
-   Update to 0.7.1alpha
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5alpha-3
-   Add devel package.
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 0.5alpha-2
-   GA - Bump release of all rpms
*   Fri Jan 22 2016 Xiaolin Li <xiaolinl@vmware.com> 0.5-1
-   Updated to version 0.5
*   Thu Nov 06 2014 Sharath George <sharathg@vmware.com> 0.4-1
    Initial version
