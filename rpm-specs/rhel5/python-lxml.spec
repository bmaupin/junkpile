# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-lxml
%define pkgname         lxml
%define version         2.2.6
%define release         1

Summary: lxml Python module
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://codespeak.net/lxml/%{pkgname}-%{version}.tgz
Vendor: The lxml Project
URL: http://codespeak.net/lxml
License: BSD
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: gcc, python, python-devel, libxml2, libxml2-devel, libxml2-python, libxslt, libxslt-devel, libxslt-python
Requires: python, libxml2, libxml2-python, libxslt, libxslt-python
Prefix: %{_prefix}

%description
lxml is a Pythonic binding for the libxml2 and libxslt libraries. It is unique in that it combines the speed and feature completeness of these libraries with the simplicity of a native Python API, mostly compatible but superior to the well-known ElementTree API.

lxml is the most feature-rich and easy-to-use library for working with XML and HTML in the Python language.

lxml %{version}

%prep
# Extract the lxml tar file
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
%doc CREDITS.txt doc README.txt TODO.txt
# Files to include in the RPM
%{_prefix}

%changelog
* Thu Mar 04 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 2.2.6-1
- initial RHEL packaging

