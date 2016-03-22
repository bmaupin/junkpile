# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr/local
%define name            gperftools
%define version         2.1
%define release         1%{?dist}

Summary: Performance tools for C++
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://gperftools.googlecode.com/files/%{name}-%{version}.tar.gz
Vendor: Google Inc. and others
URL: http://code.google.com/p/gperftools
License: BSD
Group: Development/Libraries
BuildRequires: gcc, make, gcc-c++
Prefix: %{_prefix}

%description
The gperftools packages contains some utilities to improve and analyze the performance of C++ programs.  This includes an optimized thread-caching malloc() and cpu and heap profiling utilities.

%prep
# Extract the installation tar file
%setup -q -n %{name}-%{version}

%build
# Descriptions of flags used:
#--enable-minimal        build only tcmalloc-minimal
CFLAGS="$RPM_OPT_FLAGS -O2" CXXFLAGS="$RPM_OPT_FLAGS -O2" ./configure --enable-minimal --prefix=%{_prefix}
make
#make check

%install
# Installs the files in BuildRoot when building the RPM
make DESTDIR=%{buildroot} install

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc AUTHORS COPYING doc INSTALL NEWS README TODO
# Files to include in the RPM
%{_prefix}

%changelog
* Mon Nov 25 2013 bmaupin <bmaupin@users.noreply.github.com> 2.1-1
- upgrade to gperftools 2.1

* Mon Nov 12 2012 bmaupin <bmaupin@users.noreply.github.com> 2.0-2
- include dist in the release variable
- update spec file according to RHEL 6 guidelines

* Mon Oct 15 2012 bmaupin <bmaupin@users.noreply.github.com> 2.0-1
- upgrade to gperftools 2.0

* Thu Mar 31 2011 bmaupin <bmaupin@users.noreply.github.com> 1.6-1
- upgrade to Google Performance Tools 1.6
- compile using optimizations (-O2)

* Thu Jan 21 2010 bmaupin <bmaupin@users.noreply.github.com> 1.5-1
- upgrade to Google Performance Tools 1.5
- no longer build with libunwind
- use --enable-minimal flag, to only build tcmalloc-minimal

