# Shibboleth SELinux Policy

This repository contains the SELinux policy for the Shibboleth daemon (`shibd`). This policy is designed to enhance the security of the Shibboleth Identity Provider service by applying Mandatory Access Control (MAC) using SELinux.

## Installation

### From Source

To build and install the policy from source, follow these steps:

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/orrisroot/shibboleth-selinux.git
    cd shibboleth-selinux
    ```

2.  **Build the policy module:**
    ```sh
    make -f /usr/share/selinux/devel/Makefile
    ```

3.  **Install the policy module:**
    ```sh
    sudo semodule -i shibboleth.pp
    ```

4.  **Apply file contexts:**
    ```sh
    sudo restorecon -Rv /etc/shibboleth /var/cache/shibboleth /var/log/shibboleth /run/shibboleth /usr/sbin/shibd /usr/lib/systemd/system/shibd.service
    ```

### Using RPM

To create and install an RPM package, you must first ensure the source files are correctly structured.

1.  **Create the source directory structure:**
    The `shibboleth-selinux.spec` file expects the source tarball to contain a top-level directory named `shibboleth-selinux-1.0.0/`.

2.  **Create the source tarball:**
    ```sh
    # Create the source directory and copy all necessary source files into it
    mkdir -p shibboleth-selinux-1.0.1
    cp shibboleth.te shibboleth.fc shibboleth-selinux.8 shibboleth-selinux.spec LICENSE README.md shibboleth-selinux-1.0.1/
    
    # Create the tarball from the top-level directory
    tar -czvf shibboleth-selinux-1.0.1.tar.gz shibboleth-selinux-1.0.1/
    ```

3.  **Build the RPM package:**
    ```sh
    # You will need to move the tarball to your RPM build directory
    cp shibboleth-selinux-1.0.1.tar.gz ~/rpmbuild/SOURCES/
    
    # Build the RPM
    rpmbuild -ba shibboleth-selinux.spec
    ```

4.  **Install the RPM package:**
    The resulting RPM will be located in `~/rpmbuild/RPMS/noarch/`.
    ```sh
    sudo dnf localinstall ~/rpmbuild/RPMS/noarch/shibboleth-selinux-1.0.1-1.el10.noarch.rpm
    ```
    *(Note: Adjust the package name and path according to your system and build environment.)*

## Usage

Once the policy is installed, the `shibd` service will run in the `shibboleth_t` domain, providing enhanced security.

## Troubleshooting

If you encounter SELinux denials (AVC messages) in your system logs, you can use the `audit2allow` tool to generate a permissive rule.

1.  **Install the `setroubleshoot-server` and `policycoreutils-devel` packages:**
    ```sh
    sudo yum install setroubleshoot-server policycoreutils-devel
    ```

2.  **Generate a new policy module from audit logs:**
    ```sh
    grep "shibd" /var/log/audit/audit.log | audit2allow -M my-shibboleth-policy
    ```
    This will create `my-shibboleth-policy.te` and `my-shibboleth-policy.pp` files.

3.  **Review and install the new policy:**
    Review the `.te` file to ensure the rules are what you expect, then install it.
    ```sh
    sudo semodule -i my-shibboleth-policy.pp
    ```

## Contributing

We welcome contributions to this project. Please submit bug reports or pull requests via GitHub.

