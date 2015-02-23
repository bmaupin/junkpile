# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr
%define name            python-ntlm
%define pkgname         pyntlm
%define version         20100505
%define release         1
#%define python_version %(%{__python} -c "import sys; print sys.version[:3]")%{nil}
%define _with_python25 %(%{__python} -c "import sys; 
if sys.version[:3] >= '2.5': print '1'
else: print '0'")%{nil}

Summary: ntlm Python module
Name: %{name}
Version: %{version}
Release: %{release}
# Source file created by checking out SVN repository using instructions from 
#    http://code.google.com/p/python-ntlm/source/checkout
#    (svn checkout http://python-ntlm.googlecode.com/svn/trunk/ python-ntlm-read-only)
#    and then removing all .svn folders (find . | grep \.svn | xargs -i -t rm -rf {}) 
#    because they were causing a setuptools error when compiling due to this bug:
#    https://bugzilla.redhat.com/show_bug.cgi?id=460631
Source: %{name}-%{version}.tar.gz
Vendor: Matthijs Mullender
URL: http://code.google.com/p/python-ntlm
License: LGPL
Group: System Environment/Libraries
BuildRoot: %{_builddir}/%{name}-root
BuildRequires: python, python-setuptools
%if %{_with_python25}
Requires: python >= 2.5
%else
Requires: python < 2.5, python-hashlib >= 20060408a
%endif
Prefix: %{_prefix}

%description
Python library that provides NTLM support, including an authentication handler for urllib2.

%{name} %{version}

%prep
# Extract the source tar file
# Default name of source directory when checked out using instructions from
# http://code.google.com/p/python-ntlm/source/checkout
%setup -q -n python-ntlm-read-only

%build
cd python26
%{__python} setup.py build

%install
# Cleanup from previous builds
rm -rf $RPM_BUILD_ROOT

# Installs the files in BuildRoot when building the RPM
cd python26
%{__python} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc python26/ntlm_examples
# Files to include in the RPM
%{_prefix}
# Files in the BuildRoot to exclude from the RPM
%exclude %{_prefix}/bin

%changelog
* Mon Apr 26 2010 bmaupin <bmaupin@users.noreply.github.com> 1.9.49-1
- initial RHEL packaging

