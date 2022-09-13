Summary:        Configuration-management, application deployment, cloud provisioning system
Name:           ansible
Version:        2.13.3
Release:        1%{?dist}
License:        GPLv3+
URL:            https://www.ansible.com
Group:          Development/Libraries
Vendor:         VMware, Inc.
Distribution:   Photon

Source0: http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz
%define sha512 %{name}=06d3e322980eb61b0f73b93b43d0bf3b5542feacbf11e8dc7862150f13bcc3c46d7f7a34ca1866cd6f4a09881e464a63714e9e645ca1367cee05dd192f375c4b

Source1: tdnf.py

BuildArch: noarch

BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-resolvelib

%if 0%{?with_check}
BuildRequires: python3-pip
BuildRequires: python3-jinja2 >= 3.1.2
BuildRequires: python3-PyYAML
BuildRequires: python3-pytest
BuildRequires: python3-cryptography
%endif

Requires: python3
Requires: python3-jinja2 >= 3.1.2
Requires: python3-PyYAML
Requires: python3-xml
Requires: python3-paramiko
Requires: python3-resolvelib

%description
Ansible is a radically simple IT automation system. It handles configuration-management, application deployment, cloud provisioning, ad-hoc task-execution, and multinode orchestration - including trivializing things like zero downtime rolling updates with load balancers.

%prep
%autosetup -p1
cp -vp %{SOURCE1} lib/%{name}/modules/

%build
%py3_build

%install
%py3_install

%if 0%{?with_check}
%check
# make check is unstable at the moment
#pip3 install pytest-forked
#make tests-py3 %%{?_smp_mflags}
%endif

%files
%defattr(-, root, root)
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Sat Sep 03 2022 Shreenidhi Shedi <sshedi@vmware.com> 2.13.3-1
- Upgrade to v2.13.3
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 2.9.27-1
- Automatic Version Bump
* Fri Dec 10 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.12.1-1
- Upgrade to v2.12.1 & fix tdnf module packaging
* Wed Jun 02 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.11.1-1
- Bump version to 2.11.1
* Mon Apr 12 2021 Gerrit Photon <photon-checkins@vmware.com> 2.9.20-1
- Automatic Version Bump
* Fri Jul 03 2020 Shreendihi Shedi <sshedi@vmware.com> 2.9.10-1
- Upgrade to version 2.9.10
- Removed python2 dependancy
* Mon Apr 20 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-2
- Fix CVE-2020-1733, CVE-2020-1739
* Fri Apr 03 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.10-1
- Upgrade version to 2.8.10 & various CVEs fixed
* Sun Feb 16 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-3
- Fix 'make check'
* Thu Feb 06 2020 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-2
- Fix for CVE-2019-14864
- Fix dependencies
- Patch to support tdnf operations
* Mon Aug 12 2019 Shreenidhi Shedi <sshedi@vmware.com> 2.8.3-1
- Upgraded to version 2.8.3
* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> 2.7.6-1
- Version update to 2.7.6, fix CVE-2018-16876
* Mon Sep 17 2018 Ankit Jain <ankitja@vmware.com> 2.6.4-1
- Version update to 2.6.4
* Thu Oct 12 2017 Anish Swaminathan <anishs@vmware.com> 2.4.0.0-1
- Version update to 2.4.0.0
* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.2.2.0-2
- Use python2 explicitly
* Thu Apr 6 2017 Alexey Makhalov <amakhalov@vmware.com> 2.2.2.0-1
- Version update
* Wed Sep 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.1.1.0-1
- Initial build. First version
