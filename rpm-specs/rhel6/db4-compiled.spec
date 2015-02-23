# This is where the package will be installed.  Change this next line as necessary.
%define _prefix 	/usr/local
%define name 		  db4-compiled
%define pkgname		db4
%define version 	4.7.25
%define release 	3%{?dist}

Summary: Berkeley DB 4 for OpenLDAP
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
Patch1: http://www.oracle.com/technology/products/berkeley-db/db/update/%{version}/patch.%{version}.1
Patch2: http://www.oracle.com/technology/products/berkeley-db/db/update/%{version}/patch.%{version}.2
Patch3: http://www.oracle.com/technology/products/berkeley-db/db/update/%{version}/patch.%{version}.3
Patch4: http://www.oracle.com/technology/products/berkeley-db/db/update/%{version}/patch.%{version}.4
Vendor: Oracle
URL: http://www.oracle.com/
License: Open Source License for Oracle Berkeley DB
Group: System Environment/Libraries
BuildRequires: gcc, make
Prefix: %{_prefix}

%description
Berkeley DB %{version} for OpenLDAP

%prep
# Extract the installation tar file
%setup -q -n db-%{version}

# Install the patches
%patch1 -p0 -b .1
%patch2 -p0 -b .2
%patch3 -p0 -b .3
%patch4 -p1 -b .4

%build
cd build_unix
# --enable-shared
#   build shared libraries [default=yes]
# --disable-static
#   don't build static libraries
# --enable-posixmutexes --with-mutex=POSIX/pthreads flags used due to 
#   recommendation by Howard Chu (http://www.openldap.org/lists/openldap-software/200708/msg00344.html)
CFLAGS="$RPM_OPT_FLAGS -O2" ../dist/configure --prefix=%{_prefix} --enable-shared --disable-static --enable-posixmutexes --with-mutex=POSIX/pthreads
make

%install
# Installs the files in BuildRoot when building the RPM
cd build_unix
make DESTDIR=%{buildroot} install

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc LICENSE README docs
# Files to include in the RPM
%{_prefix}

%changelog
* Thu Oct 18 2012 Bryan Maupin <bmaupin@users.noreply.github.com> 4.7.25-3
- downgrade to version 4.7.25 (http://www.openldap.org/its/index.cgi/Incoming?id=7378)
- include dist in the release variable
- update spec file according to RHEL 6 guidelines
- make sure profile.d path scripts are included in sources

* Wed Mar 30 2011 Bryan Maupin <bmaupin@users.noreply.github.com> 4.8.30-1
- upgrade to version 4.8.30

* Mon May 17 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 4.8.26-1
- upgrade to version 4.8.26
- compile using optimizations (-O2)
- compile using --enable-posixmutexes --with-mutex=POSIX/pthreads flags
- disable static libraries and explicitly enable shared libraries
