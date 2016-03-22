# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-kadm5
%define pkgname         pykadm5
%define version         20080122
%define release         1

Summary: kadm5 Python module
Name: %{name}
Version: %{version}
Release: %{release}
# Source file created by checking out SVN repository using instructions from 
#    http://code.google.com/p/pykadm5/source/checkout
#    (svn checkout http://pykadm5.googlecode.com/svn/trunk/ pykadm5-read-only)
#    and then removing all .svn folders (find . | grep \.svn | xargs -i -t rm -rf {}) 
#    because they were causing a setuptools error when compiling due to this bug:
#    https://bugzilla.redhat.com/show_bug.cgi?id=460631
Source: %{name}-%{version}.tar.gz
# Patch from http://code.google.com/p/pykadm5/issues/detail?id=1
Patch: pykadm5-pu-2008-11-11.patch
Vendor: Josef Boleininger
URL: http://code.google.com/p/pykadm5
License: GPL
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: python, python-devel, krb5-devel
Prefix: %{_prefix}

%description
Python module for MIT Kerberos kadmin.

%{name} %{version}

%prep
# Extract the source tar file
# Default name of source directory when checked out using instructions from
#    http://code.google.com/p/pykadm5/source/checkout
%setup -q -n pykadm5-read-only
# Apply the patch
%patch -p1 -b .0

%build
%{__python} setup.py build

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
%doc CHANGELOG COPYING README TODO
# Files to include in the RPM
%{_prefix}

%changelog
* Fri Jul  8 2011 Bryan Maupin <bmaupin@users.noreply.github.com> 20080122-1
- initial RHEL packaging

