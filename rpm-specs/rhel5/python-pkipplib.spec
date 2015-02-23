# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-pkipplib
%define pkgname         pkipplib
%define version         0.07
%define release         1

Summary: pkipplib Python module
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://pypi.python.org/packages/source/p/pkipplib/pkipplib-0.07.tar.gz
Vendor: Jerome Alet
URL: http://www.pykota.com/software/pkipplib
License: GNU GPL
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: python
Requires: python
Prefix: %{_prefix}

%description
pkipplib is a Python library which can prepare IPP requests with the help of a somewhat high level API.

%{name} %{version}

%prep
# Extract the source tar file
%setup -q -n %{pkgname}-%{version}

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
%doc COPYING PKG-INFO README
# Files to include in the RPM
%{_prefix}
# Files in the BuildRoot to exclude from the RPM
%exclude %{_prefix}/bin

%changelog
* Wed May 5 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 0.07-1
- initial RHEL packaging

