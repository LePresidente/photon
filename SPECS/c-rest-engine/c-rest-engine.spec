Name:          c-rest-engine
Summary:       minimal http(s) server library
Version:       1.2
Release:       8%{?dist}
Group:         Applications/System
Vendor:        VMware, Inc.
Distribution:  Photon
License:       Apache 2.0
URL:           http://www.github.com/vmware/c-rest-engine

Source0:       %{name}-%{version}.tar.gz
%define sha1   c-rest-engine=25aa9d1f2680e26114dee18365c510692552f8e4

Patch0:        c-rest-engine-aarch64.patch
Patch1:        c-rest-engine-fix-log-file-len.patch
Patch2:        preprocess-timeout.patch
Patch3:        fd_leak.patch
Patch4:        include_time_header.patch
Patch5:        openssl-1.1.1-compatibility.patch

Requires:      openssl >= 1.0.1

BuildRequires: coreutils >= 8.22
BuildRequires: openssl-devel >= 1.0.1

%description
c-rest-engine is a minimal embedded http(s) server written in C.
Its primary intent is to enable REST(Representational State Transfer)
API support for C daemons.

%package devel
Summary: c-rest-engine dev files
Requires:  openssl-devel >= 1.0.1
Requires:  %{name} = %{version}-%{release}

%description devel
development libs and header files for c-rest-engine

%prep
%autosetup -p1

%build
cd build
autoreconf -mif ..
sh ../configure \
    --host=%{_host} --build=%{_build} \
    --prefix=%{_prefix} \
    --with-ssl=/usr \
    --enable-debug=%{_enable_debug} \
    --disable-static

make %{?_smp_mflags} CFLAGS="-O2 -fcommon -Wno-error=unused-result -Wno-error=stringop-truncation -Wno-error=stringop-overflow"

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
cd build && make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%post -p  /sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/*.so.*
%exclude %{_sbindir}/vmrestd

%files devel
%{_includedir}/vmrest.h
%{_libdir}/*.so

# %doc ChangeLog README COPYING

%changelog
* Wed Aug 04 2021 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2-8
- Bump up release for openssl
* Thu Jan 14 2021 Alexey Makhalov <amakhalov@vmware.com> 1.2-7
- GCC-10 support.
* Wed Nov 18 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2-6
- Remove make check as unit tests are not present in c-rest-engine
* Wed Jul 22 2020 Satya Naga Vasamsetty <svasamsetty@vmware.com> 1.2-5
- Fix openssl-1.1.1g compatibility
* Fri Jan 11 2019 Ankit Jain <ankitja@vmware.com> 1.2-4
- Added Makecheck
* Tue May 08 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-3
- Appying patch for fd leak issue.
* Fri Feb 23 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-2
- Appying patch for preprocess timeout.
* Wed Feb 14 2018 Kumar Kaushik <kaushikk@vmware.com> 1.2-1
- Upgrading to version 1.2. Removing all upstream patches.
* Thu Nov 23 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.1-1
- Update to v1.1-1
* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.5-2
- Aarch64 support
* Thu Nov 02 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.5-1
- Adding version, 1.0.5, get peer info API.
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.0.4-3
- Remove coreutils runtime dependency.
* Tue Sep 12 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.4-2
- Making default log level as ERROR.
* Mon Sep 11 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.4-1
- Updating to version 1.0.4.
* Tue Aug 22 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.3-2
- Upstream version 1.0.4 patch for 1.0.3.
* Fri Jul 21 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.3-1
- Updating version to 1.0.3, API for setting SSL info.
* Tue Jun 20 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.2-1
- Updating version to 1.0.2
* Thu May 18 2017 Kumar Kaushik <kaushikk@vmware.com> 1.0.1-1
- Updating version to 1.0.1
* Thu May 04 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.0.0-1
- Initial build.  First version
