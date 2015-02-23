# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr/local
%define name            openssl-compiled
%define pkgname         openssl
%define version         1.0.1e
%define release         1%{?dist}

Summary: The OpenSSL toolkit for OpenLDAP
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://www.openssl.org/source/%{pkgname}-%{version}.tar.gz
Vendor: The OpenSSL Project
URL: http://www.openssl.org/
License: BSDish
Group: System Environment/Libraries
BuildRequires: gcc, perl, make
Prefix: %{_prefix}

%description
OpenSSL %{version} for OpenLDAP

%prep
# Extract the openssl tar file
%setup -q -n %{pkgname}-%{version}

%build
# shared: In addition to the usual static libraries, create shared libraries on platforms where it's supported.
# --libdir=lib
#    Install libs to %{_prefix}/lib instead of %{_prefix}/lib64 on 64-bit systems
CFLAGS="$RPM_OPT_FLAGS -O2" ./config --prefix=%{_prefix} --libdir=lib --openssldir=%{_prefix} shared
make

%install
# Installs the files in BuildRoot when building the RPM
# OpenSSL uses "INSTALL_PREFIX" instead of "DESTDIR"
make INSTALL_PREFIX=%{buildroot} install

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc CHANGES doc FAQ INSTALL LICENSE NEWS PROBLEMS README
# Files to include in the RPM
%{_prefix}
# Files in the BuildRoot to exclude from the RPM
%exclude %{_prefix}/misc/tsget

%changelog
* Wed Jul 24 2013 Bryan Maupin <bmaupin@users.noreply.github.com> 1.0.1e-1
- upgrade to version 1.0.1e

* Thu Oct 18 2012 Bryan Maupin <bmaupin@users.noreply.github.com> 1.0.1c-1
- upgrade to version 1.0.1c
- include dist in the release variable
- update spec file according to RHEL 6 guidelines

* Wed Mar 30 2011 Bryan Maupin <bmaupin@users.noreply.github.com> 1.0.0d-1
- upgrade to version 1.0.0d

* Thu May 13 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 1.0.0-2
- exclude tsget tool (requires WWW::Curl::Easy Perl module, not provided in RHEL repositories)
- compile using optimizations (-O2)

* Tue May 11 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 1.0.0-1
- upgrade to version 1.0.0
- add to system libraries

