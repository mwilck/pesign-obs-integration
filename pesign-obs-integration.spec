#
# spec file for package pesign-obs-integration
#
# Copyright (c) 2018 SUSE LINUX GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#
# needssslcertforbuild


Name:           pesign-obs-integration
Summary:        Macros and scripts to sign the kernel and bootloader
License:        GPL-2.0-only
Group:          Development/Tools/Other
Version:        10.1
Release:        0
Requires:       fipscheck
Requires:       mozilla-nss-tools
Requires:       openssl
%ifarch %ix86 x86_64 ia64 aarch64
Requires:       pesign
%endif
BuildRequires:  openssl
Url:            http://en.opensuse.org/openSUSE:UEFI_Image_File_Sign_Tools
# OBS tar_scm.service supports only "-" as separator between name and version.
# We must use "_" here for Debian compatibility.
# The service-created tarball must be renamed manually from %{name}.tar.xz
Source:         %{name}_%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-build
# suse-module-tools <= 15.0.10 contains modsign-verify
Conflicts:	suse-module-tools <= 15.0.10

%description
This package provides scripts and rpm macros to automate signing of the
boot loader, kernel and kernel modules in the openSUSE Buildservice.

%prep
%setup -D -n %{name}

%build

%install

mkdir -p %buildroot/usr/lib/rpm/brp-suse.d %buildroot/usr/lib/rpm/pesign
install pesign-gen-repackage-spec kernel-sign-file gen-hmac %buildroot/usr/lib/rpm/pesign
install brp-99-pesign %buildroot/usr/lib/rpm/brp-suse.d
# brp-99-compress-vmlinux has nothing to do with signing. It is packaged in
# pesign-obs-integration because this package is already used by the kernel
# build
install brp-99-compress-vmlinux %buildroot/usr/lib/rpm/brp-suse.d
install -m644 pesign-repackage.spec.in %buildroot/usr/lib/rpm/pesign
mkdir -p %buildroot/usr/bin
install modsign-repackage %buildroot/usr/bin/
install -pm 755 modsign-verify %buildroot/usr/bin/
if test -e _projectcert.crt; then
	openssl x509 -inform PEM -in _projectcert.crt \
		-outform DER -out %buildroot/usr/lib/rpm/pesign/pesign-cert.x509
else
	echo "No buildservice project certificate available"
fi

%files
%defattr(-,root,root)
%license COPYING
%doc README
/usr/bin/modsign-repackage
/usr/bin/modsign-verify
/usr/lib/rpm/*

%changelog
