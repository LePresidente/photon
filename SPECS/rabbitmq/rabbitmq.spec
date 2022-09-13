%global _rabbit_libdir %{_libdir}/rabbitmq
%global _rabbit_user rabbitmq

Name:          rabbitmq-server
Summary:       RabbitMQ messaging server
Version:       3.10.6
Release:       1%{?dist}
Group:         Applications
Vendor:        VMware, Inc.
Distribution:  Photon
License:       MPLv1.1
URL:           https://github.com/rabbitmq/rabbitmq-server

Source0:       https://github.com/rabbitmq/rabbitmq-server/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha512 rabbitmq=e43cebc07c3e58b9900e30425ea6a6c31d6f2b0ad38a920ccd249df599983126445fd2eb7084d6b38d014701e69475fa6261baa29b39579a063cded0336e109c

Source1:       rabbitmq.conf

Requires:      erlang
Requires:      erlang-sd_notify
Requires:      socat
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd
Requires:      /bin/sed
Requires(pre): /usr/sbin/useradd /usr/sbin/groupadd

BuildRequires: erlang
BuildRequires: rsync
BuildRequires: zip
BuildRequires: git
BuildRequires: libxslt
BuildRequires: xmlto
BuildRequires: python3-xml
BuildRequires: python3
BuildRequires: elixir
BuildRequires: systemd-rpm-macros

BuildArch:     noarch

%description
rabbitmq messaging server

%prep
%autosetup -p1

%build
LANG="en_US.UTF-8" LC_ALL="en_US.UTF-8"
%make_build

%install
export RMQ_ROOTDIR=%{_rabbit_libdir}
%make_install %{?_smp_mflags}

install -vdm755 %{buildroot}%{_sharedstatedir}/rabbitmq
install -vdm755 %{buildroot}%{_sysconfdir}/rabbitmq

mkdir -p %{buildroot}%{_localstatedir}/log \
         %{buildroot}%{_localstatedir}/opt/rabbitmq/log \
         %{buildroot}%{_unitdir}

ln -sfv %{_localstatedir}/opt/rabbitmq/log %{buildroot}%{_localstatedir}/log/rabbitmq

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/rabbitmq

cat << EOF >> %{buildroot}%{_unitdir}/%{name}.service
[Unit]
Description=RabbitMQ broker
After=network.target epmd@0.0.0.0.socket
Wants=network.target epmd@0.0.0.0.socket

[Service]
Type=notify
User=%{_rabbit_user}
Group=%{_rabbit_user}
NotifyAccess=all
TimeoutStartSec=3600
WorkingDirectory=%{_sharedstatedir}/rabbitmq
ExecStart=%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/sbin/%{name}
ExecStop=%{_rabbit_libdir}/lib/rabbitmq_server-%{version}/sbin/rabbitmqctl stop

[Install]
WantedBy=multi-user.target
EOF

%if 0%{?with_check}
%check
make %{?_smp_mflags} tests
%endif

%clean
rm -rf %{buildroot}

%pre
if ! getent group %{_rabbit_user} >/dev/null; then
  groupadd -r %{_rabbit_user}
fi

if ! getent passwd %{_rabbit_user} >/dev/null; then
  useradd -r -g %{_rabbit_user} -d %{_localstatedir}/lib/rabbitmq %{_rabbit_user} \
  -s /sbin/nologin -c "RabbitMQ messaging server"
fi

%post
chown -R %{_rabbit_user}:%{_rabbit_user} %{_sharedstatedir}/rabbitmq
chown -R %{_rabbit_user}:%{_rabbit_user} %{_sysconfdir}/rabbitmq
chmod g+s %{_sysconfdir}/rabbitmq
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%dir %attr(0750, %{_rabbit_user}, %{_rabbit_user}) %{_localstatedir}/opt/rabbitmq/log
%attr(0750, %{_rabbit_user}, %{_rabbit_user}) %{_localstatedir}/log/rabbitmq
%{_rabbit_libdir}/*
%{_unitdir}/*
%{_sharedstatedir}/*
%config(noreplace) %attr(0644, %{_rabbit_user}, %{_rabbit_user}) %{_sysconfdir}/rabbitmq/rabbitmq.conf

%changelog
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 3.10.6-1
- Automatic Version Bump
* Wed Jun 22 2022 Shreenidhi Shedi <sshedi@vmware.com> 3.9.15-3
- Fix binary path
* Thu Jun 16 2022 Ashwin Dayanand Kamat <kashwindayan@vmware.com> 3.9.15-2
- Bump version as a part of libxslt upgrade
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 3.9.15-1
- Automatic Version Bump
* Tue Jan 11 2022 Nitesh Kumar <kunitesh@vmware.com> 3.8.14-2
- Bump up version to use fips enable erlang.
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 3.8.14-1
- Automatic Version Bump
* Thu Sep 24 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.9-1
- Automatic Version Bump
* Wed Sep 09 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.8-1
- Automatic Version Bump
* Wed Aug 19 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.7-1
- Automatic Version Bump
* Wed Jul 29 2020 Gerrit Photon <photon-checkins@vmware.com> 3.8.6-1
- Automatic Version Bump
* Tue Jun 23 2020 Tapas Kundu <tkundu@vmware.com> 3.7.20-3
- Build with python3
- Mass removal python2
* Mon Apr 27 2020 Tapas Kundu <tkundu@vmware.com> 3.7.20-2
- Fix rabbitmq server issue when we enable rabbitmq plugin.
* Tue Oct 29 2019 Keerthana K <keerthanak@vmware.com> 3.7.20-1
- Update to version 3.7.20
* Mon Aug 19 2019 Keerthana K <keerthanak@vmware.com> 3.7.3-1
- Update to version 3.7.3
* Tue Feb 05 2019 Alexey Makhalov <amakhalov@vmware.com> 3.6.15-4
- Added BuildRequires python2.
* Thu Jan 31 2019 Siju Maliakkal <smaliakkal@vmware.com> 3.6.15-3
- Consuming erlang 19.3
* Mon Sep 24 2018 Dweep Advani <dadvani@vmware.com> 3.6.15-2
- Consuming updated erlang version of 21.0
* Wed Sep 12 2018 Keerthana K <keerthanak@vmware.com> 3.6.15-1
- Update to version 3.6.15
* Thu Dec 28 2017 Divya Thaluru <dthaluru@vmware.com>  3.6.10-3
- Fixed the log file directory structure
* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.6.10-2
- Remove shadow from requires and use explicit tools for post actions
* Wed May 31 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.10-1
- Updated to latest and fixed service start issue
* Wed Apr 26 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.9-2
- Fix arch
* Wed Apr 5 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.9-1
- Updating package to the latest
* Mon Dec 12 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.6.6-1
- Initial.
