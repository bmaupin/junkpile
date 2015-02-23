# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-hashlib
%define pkgname         hashlib
%define version         20081119
%define release         1

Summary: hashlib Python module
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://code.krypto.org/python/hashlib/%{pkgname}-%{version}.tar.gz
Vendor: Gregory P. Smith <greg@krypto.org>
URL: http://code.krypto.org/python/hashlib/
License: Python Software Foundation License Version 2
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: gcc, python, python-devel, openssl-devel
Requires: python < 2.5
Prefix: %{_prefix}

%description
Provides the SHA-224, SHA-256, SHA-384, SHA-512 hash algorithms in addition to
platform optimized versions of MD5 and SHA1. If OpenSSL is present all of its 
hash algorithms are provided.

This is a stand alone packaging of the hashlib library included with Python 2.5
so that it can be used on older versions of Python (tested on 2.3 and 2.4).

%{name} %{version}

%prep
# Extract the source tar file
%setup -q -n %{pkgname}-%{version}

%build
# Build with optional OpenSSL to provide more algorithms
%{__python} setup.py --openssl-prefix=%{_prefix} --openssl-incdir=%{_includedir} --openssl-libdir=%{_libdir} build

%install
# Cleanup from previous builds
rm -rf $RPM_BUILD_ROOT

# Installs the files in BuildRoot when building the RPM
%{__python} setup.py install --prefix=$RPM_BUILD_ROOT/%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc ChangeLog LICENSE PKG-INFO README.txt test
# Files to include in the RPM
%{_prefix}

%changelog
* Mon Apr 26 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 1.9.49-1
- initial RHEL packaging

