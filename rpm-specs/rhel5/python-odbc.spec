# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-odbc
%define pkgname         pyodbc
%define version         2.1.7
%define release         1

Summary: Python ODBC module
Name: %{name}
Version: %{version}
Release: %{release}
Source: http://%{pkgname}.googlecode.com/files/%{pkgname}-%{version}.zip
# Patch from http://code.google.com/p/pyodbc/issues/detail?id=1
Vendor: Michael Kleehammer
URL: http://code.google.com/p/pyodbc/
License: MIT
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: python, python-devel, gcc, gcc-c++
Prefix: %{_prefix}

%description
pyodbc is a Python module that allows you to use ODBC to connect to almost any database from Windows, Linux, OS/X, and more.

%{name} %{version}

%prep
# Extract the source zip file
%setup -q -n %{pkgname}-%{version}

#%setup -q -n pyodbc-read-only

%build
%{__python} setup.py build

%install
# Cleanup from previous builds
rm -rf $RPM_BUILD_ROOT

# Installs the files in BuildRoot when building the RPM
# this package complains when we use just --prefix=$RPM_BUILD_ROOT/%{_prefix}
# so using --root and --prefix is the workaround
%{__python} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc LICENSE.txt README.rst
# Files to include in the RPM
%{_prefix}

%changelog
* Fri Jul  8 2011 bmaupin <bmaupin@users.noreply.github.com> 2.1.7
- initial RHEL packaging

