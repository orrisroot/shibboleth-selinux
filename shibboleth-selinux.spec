%global shibboleth_policy_version 1.0.0
%global package_name shibboleth

Name:           %{package_name}-selinux
Version:        %{shibboleth_policy_version}
Release:        1%{?dist}
Summary:        SELinux policy for the Shibboleth daemon
Group:          System Environment/Base
License:        GPLv2+
BuildArch:      noarch
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  selinux-policy-devel
Requires:       policycoreutils
Requires:       shibboleth

%description
This package contains the SELinux policy module for the Shibboleth daemon (shibd).
It grants the necessary permissions for the shibd process to operate securely
while adhering to the principle of least privilege. The policy covers the
daemon itself, its configuration, runtime files, caches, and logs.

%prep
%setup -q

%build
# Compile the SELinux policy module
make -f %{_datadir}/selinux/devel/Makefile

%install
# Create the SELinux module package file
mkdir -p %{buildroot}%{_datadir}/selinux/packages
install -m 644 %{package_name}.pp %{buildroot}%{_datadir}/selinux/packages/

# Install the man page
mkdir -p %{buildroot}%{_mandir}/man8
install -m 644 %{name}.8 %{buildroot}%{_mandir}/man8/

%clean
rm -rf %{buildroot} %{pakage_prefix}.pp

%files
%doc shibboleth.te shibboleth.fc README.md LICENSE
%{_datadir}/selinux/packages/%{package_name}.pp
%{_mandir}/man8/%{name}.8.gz

%post
# Load the SELinux policy module and restore contexts if SELinux is enabled
/usr/sbin/semodule -n -i %{_datadir}/selinux/packages/%{package_name}.pp
if /usr/sbin/selinuxenabled; then
    /usr/sbin/load_policy || :
    /sbin/restorecon -R /usr/sbin/shibd || :
    /sbin/restorecon -R /usr/lib/systemd/system/shibd.service || :
    /sbin/restorecon -R /etc/shibboleth || :
    /sbin/restorecon -R /run/shibboleth || :
    /sbin/restorecon -R /var/cache/shibboleth || :
    /sbin/restorecon -R /var/log/shibboleth || :
fi
exit 0

%postun
# Remove the SELinux policy module and restore contexts if SELinux is enabled
if [ $1 -eq 0 ]; then
    /usr/sbin/semodule -n -r %{package_name}
    if /usr/sbin/selinuxenabled; then
        /usr/sbin/load_policy || :
        /sbin/restorecon -R /usr/sbin/shibd || :
        /sbin/restorecon -R /usr/lib/systemd/system/shibd.service || :
        /sbin/restorecon -R /etc/shibboleth || :
        /sbin/restorecon -R /run/shibboleth || :
        /sbin/restorecon -R /var/cache/shibboleth || :
        /sbin/restorecon -R /var/log/shibboleth || :
    fi
fi
exit 0

%changelog
* Tue Aug 26 2025 Yoshihiro OKUMURA <orrisroot@gmail.com> - 1.0.0-1
- Initial RPM package for Shibboleth SELinux policy
