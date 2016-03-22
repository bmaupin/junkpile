# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-cups
%define pkgname         pycups
%define version         1.9.49
%define release         1

Summary: cups Python module
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://cyberelk.net/tim/data/%{pkgname}/%{pkgname}-%{version}.tar.bz2
# Patch for systems running Python < 2.5
Patch0: pycups-1.9.49-python-2.4.patch
Patch1: pycups-1.9.49-version.patch
Vendor: Tim Waugh
URL: http://cyberelk.net/tim/software/pycups
License: GPL
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: gcc, python, python-devel, cups, cups-devel
Requires: python, cups
Prefix: %{_prefix}

%description
These Python bindings are intended to wrap the CUPS API.

%{name} %{version}

%prep
# Extract the source tar file
%setup -q -n %{pkgname}-%{version}

# Apply the patches
%patch0 -b .python-24
%patch1 -b .version

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
%doc ChangeLog COPYING examples NEWS README TODO
# Files to include in the RPM
%{_prefix}

%changelog
* Mon Apr 26 2010 bmaupin <bmaupin@users.noreply.github.com> 1.9.49-1
- initial RHEL packaging

