Summary:       Modular initramfs image creation utility
Name:          mkinitcpio
Version:       31
Release:       1%{?dist}
License:       GPLv2
URL:           https://projects.archlinux.org/mkinitcpio.git/
Group:         System Environment/Development
Vendor:        VMware, Inc.
Distribution:  Photon
Source0:       https://projects.archlinux.org/mkinitcpio.git/snapshot/%{name}-%{version}.tar.gz
%define sha512 mkinitcpio=9b30fb02b6470b6e6b54fb611b4b62f89fdaf71cefd8ee74d22253f3d240b9c17b570be766c3ab627fc67bf8aa0e2ccec747d19fa29d6e4f9dadaced61259c8b
Patch0:        mkinitcpio-shutdown-ramfs.service.patch
BuildRequires: asciidoc3
BuildRequires: git
BuildRequires: python3
BuildRequires: python3-xml
BuildRequires: docbook-xsl
BuildRequires: libxml2-devel
BuildRequires: libxslt
BuildArch:     noarch

%description
Multi-format archive and compression library

%prep
%autosetup -p0

%build
for i in "hooks/*" ; do sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" $i; done
sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" init
sed -i "s/\#\!\/usr\/bin\/ash/\#\!\/bin\/bash/" shutdown
sed -i "s/a2x/a2x3 --verbose --no-xmllint/" Makefile

make %{?_smp_mflags}

%install
rm -rf %{buildroot}%{_infodir}
make  %{?_smp_mflags} DESTDIR=%{buildroot} install

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/lib/*
/usr/bin/*
/etc/*
/usr/share/*

%changelog
*   Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 31-1
-   Automatic Version Bump
*   Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 30-2
-   Bump version as a part of libxslt upgrade
*   Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 30-1
-   Automatic Version Bump
*   Mon Jul 27 2020 Gerrit Photon <photon-checkins@vmware.com> 28-1
-   Automatic Version Bump
*   Sun Jun 21 2020 Tapas Kundu <tkundu@vmware.com> 24-3
-   Build with python3
-   Mass removal python2
*   Fri Jan 18 2019 Alexey Makhalov <amakhalov@vmware.com> 24-2
-   Added buildRequires python2.
*   Mon Sep 10 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 24-1
-   Update to version 24
*   Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 23-3
-   fix directory create in shutdown service
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 23-2
-   Fix arch
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 23-1
-   Update package version
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 19-2
-   GA - Bump release of all rpms
*   Tue Feb 23 2016 Kumar Kaushik <kaushikk@vmware.com> 19-1
-   Updated to new version.
*   Sat Jul 11 2015 Touseef Liaqat <tliaqat@vmware.com> 18-2
-   Remove ash dependency
*   Fri Jun 5 2015 Touseef Liaqat <tliaqat@vmware.com> 18-1
-   Initial build.  First version
