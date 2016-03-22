# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr/local
# This is where OpenSSL is located.  Change this next line as necessary.
%define openssldir      /usr/local
# This is where OpenLDAP is located (for purposes of placing the keytab file).  Change this next line as necessary
%define openldapdir     /usr/local
%define name            heimdal-compiled
%define pkgname         heimdal
%define version         1.5.2
%define release         2%{?dist}

Summary: Heimdal Kerberos 5 implementation for OpenLDAP
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://www.h5l.org/dist/src/%{pkgname}-%{version}.tar.gz
Vendor: The Heimdal Project
URL: http://www.h5l.org/
License: BSD
Group: System Environment/Libraries
BuildRequires: gcc, byacc, ncurses-devel, openssl-compiled
Requires: openssl-compiled
Prefix: %{_prefix}

%description
Heimdal %{version} for OpenLDAP

%prep
# Extract the Heimdal tar file
%setup -q -n %{pkgname}-%{version}

%build
# Descriptions of flags used:
# --enable-shared \  
#	build shared libraries [default=yes]
# --disable-static
#       don't build static libraries
#--enable-pthread-support \
#	if you want thread safe libraries
#--with-openssl=/usr/local \
#	use openssl in dir
#--without-readline \
#	don't compile with support for the GNU Readline library, which will be used in some programs. If no readline library is found, the (simpler) editline library will be used instead. 
#--without-openldap \
#	don't Compile Heimdal with support for storing the database in LDAP. 
#--without-hesiod \
#--disable-berkeley-db \
#	if you don't want berkeley db
#--without-ipv6
#	do not enable IPv6 support
CFLAGS="$RPM_OPT_FLAGS -O2" CPPFLAGS="-I%{openssldir}/include/" LDFLAGS="-L%{openssldir}/lib -R%{openssldir}/lib" ./configure --prefix=%{_prefix} --sysconfdir=%{openldapdir}/etc --enable-shared --disable-static --enable-pthread-support --with-openssl=%{openssldir} --without-readline --without-openldap --without-hesiod --disable-berkeley-db --without-ipv6
make

%install
# Installs the files in BuildRoot when building the RPM
make DESTDIR=%{buildroot} install

# Heimdal 1.5.2 creates broken absolute symlinks; remove them
rm %{buildroot}/%{_prefix}/share/man/cat5/mech.5
rm %{buildroot}/%{_prefix}/share/man/cat5/qop.5

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc ChangeLog* doc LICENSE NEWS README TODO
# Files to include in the RPM
%{_prefix}

%changelog
* Wed Jul 24 2013 Bryan Maupin <bmaupin@users.noreply.github.com> 1.5.2-2
- build with latest version of OpenSSL (1.0.1e)

* Thu Oct 18 2012 Bryan Maupin <bmaupin@users.noreply.github.com> 1.5.2-1
- upgrade to version 1.5.2
- include dist in the release variable
- update spec file according to RHEL 6 guidelines
- fix broken absolute symlinks
- make sure profile.d path scripts are included in sources

* Mon Apr  4 2011 Bryan Maupin <bmaupin@users.noreply.github.com> 1.4-1
- explicitly set rpath to point to SSL libraries
- upgrade to version 1.4
- apply patch for missing lib/otp/version-script.map

* Mon May 17 2010 Bryan Maupin <bmaupin@users.noreply.github.com> 1.3.2-1
- upgrade to version 1.3.2
- compile using optimizations (-O2)
- disable static libraries and explicitly enable shared libraries

