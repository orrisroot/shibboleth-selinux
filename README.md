# **Shibboleth SELinux Policy**

This project provides an SELinux policy for the Shibboleth daemon (shibd) to ensure it operates securely in an SELinux-enforced environment.

The policy restricts access for the Shibboleth process to its configuration files, PID files, cache, and logs, enforcing the principle of least privilege.

## **File Contents**

* **shibboleth.te**: The policy source file defining SELinux types and rules for the Shibboleth daemon.
* **shibboleth.fc**: The file defining SELinux file contexts for files and directories related to Shibboleth.
* **shibboleth\_selinux.8**: The man page for this SELinux policy.
* **shibboleth-selinux.spec**: The SPEC file used to build this policy as an RPM package.

## **Installation**

### **Prerequisites**

To build and install this policy, you need the following packages:

* selinux-policy-devel
* policycoreutils
* rpm-build

You can install these packages using the following command:

sudo dnf install selinux-policy-devel policycoreutils rpm-build

### **Build and Install**

1. Place all the files listed above in a single directory.
2. Create a tar.gz archive of the source files.
   tar \-czvf shibboleth-selinux-1.0.0.tar.gz shibboleth.te shibboleth.fc shibboleth\_selinux.8 shibboleth-selinux.spec

3. Create the SRPM (Source RPM).
   rpmbuild \-ts shibboleth-selinux-1.0.0.tar.gz

4. Build the RPM from the SRPM.
   rpmbuild \-bb \~/rpmbuild/SPECS/shibboleth-selinux.spec

5. Install the generated RPM.
   sudo rpm \-ivh \~/rpmbuild/RPMS/noarch/shibboleth-selinux-1.0.0-1.el8.noarch.rpm

### **Policy Auto-Loading**

When the RPM package is installed on a system with SELinux enabled, the policy is automatically loaded, and the file contexts for related files are updated.

## **License**

This project is distributed under the GPLv2+ license.

## **Copyright**

Copyright (C) 2025 Yoshihiro OKUMURA
