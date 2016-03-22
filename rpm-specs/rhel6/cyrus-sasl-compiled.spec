# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr/local
# This is where OpenSSL is located.  Change this next line as necessary.
%define openssldir      /usr/local
# This is where Heimdal Kerberos is located.  Change this next line as necessary.
%define heimdaldir      /usr/local
# This is the name of the service.  Change this next line as necessary.
%define servicename     saslauthd-compiled
%define name            cyrus-sasl-compiled
%define pkgname         cyrus-sasl
%define version         2.1.23
%define release         4%{?dist}

Summary: The Cyrus SASL library for OpenLDAP
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/%{pkgname}-%{version}.tar.gz
Source1: %{servicename}.init
Patch0: cyrus-sasl-2.1.23-gssapi.patch
Vendor: Carnegie Mellon University
URL: http://asg.web.cmu.edu/sasl/sasl-library.html
License: Freely Distributable
Group: System Environment/Libraries
BuildRequires: gcc, make, openssl-compiled, heimdal-compiled
Requires: openssl-compiled, heimdal-compiled, /sbin/chkconfig 
Prefix: %{_prefix}

%description
Cyrus-SASL %{version} for OpenLDAP

%prep
# Extract the installation tar file
%setup -q -n %{pkgname}-%{version}

# Apply the GSSAPI patch
# based on info from here: http://lists.freebsd.org/pipermail/freebsd-questions/2011-February/227044.html
%patch0 -p0 -b .0

%build
# Descriptions of flags used:
# --enable-shared
#       build shared libraries [default=yes]
# --disable-static
#       don't build static libraries
#--disable-sample \
#	disable sample code (default=enabled)
#--without-dblib \
#	do not use DB library package
#--without-pam \
#	do not use PAM
#--without-des \
#	do not use DES
#--disable-des \
#	disable DES
#--with-openssl= \
#	use OpenSSL from PATH
#--with-saslauthd=/var/run/saslauthd \
#	 enable use of the saslauth daemon using state dir DIR
#--disable-checkapop \
#	disable use of sasl_checkapop (default = enabled)
#--disable-cram \
#	disable CRAM-MD5 authentication (default=enabled)
#--disable-digest \
#	disable DIGEST-MD5 authentication (default=enabled)
#--disable-otp \
#	disable OTP authentication (default=enabled)
#--disable-anon \
#	disable ANONYMOUS authentication (default=enabled)
#--enable-plain \
#	enable PLAIN authentication (default=enabled)
#--enable-login \
#	enable unsupported LOGIN authentication (default=disabled)
#--enable-gssapi= \
#	enable GSSAPI authentication--this is provided by Heimdal, so should be pointed to the Heimdal installation directory (default=enabled)
#--with-plugindir=
#	set the directory where plugins will be found (default=/usr/lib/sasl2)
CFLAGS="$RPM_OPT_FLAGS -O2" CC="gcc -Wl,-rpath,%{_prefix}/lib -Wl,-rpath,%{heimdaldir}/lib -Wl,-rpath,%{openssldir}/lib" CPPFLAGS="-I%{heimdaldir}/include -I%{openssldir}/include" LDFLAGS="-L%{heimdaldir}/lib -L%{openssldir}/lib" ./configure --prefix=%{_prefix} --enable-shared --disable-static --disable-sample --without-dblib --without-pam --without-des --disable-des --with-openssl=%{openssldir} --with-saslauthd=/var/run/saslauthd-openldap --disable-checkapop --disable-cram --disable-digest --disable-otp --disable-anon --enable-plain --enable-login --enable-gssapi=%{heimdaldir} --with-plugindir=%{_prefix}/lib/sasl2
make

%install
# Installs the files in BuildRoot when building the RPM
make DESTDIR=%{buildroot} install

# Install an init script for the servers.
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{servicename}

# Create the new run directory
mkdir -p %{buildroot}/var/run/%{servicename}

%post 
/sbin/chkconfig --add %{servicename}

%preun
/sbin/chkconfig --del %{servicename}

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Labels certain files as documents to be put in /usr/share/doc
%doc AUTHORS ChangeLog COPYING doc INSTALL NEWS README
# Files to include in the RPM
%{_prefix}
%attr(0755,root,root) %config %{_sysconfdir}/rc.d/init.d/%{servicename}
%attr(0755,root,root) %dir /var/run/%{servicename}

%changelog
* Wed Jul 24 2013 bmaupin <bmaupin@users.noreply.github.com> 2.1.23-4
- build with latest version of OpenSSL (1.0.1e)

* Thu Oct 18 2012 bmaupin <bmaupin@users.noreply.github.com> 2.1.23-3
- include dist in the release variable
- update spec file according to RHEL 6 guidelines
- make sure %{servicename}.init is included in sources

* Tue Apr  5 2011 bmaupin <bmaupin@users.noreply.github.com> 2.1.23-2
- compile using optimizations (-O2)
- explicitly enable shared libraries and disable static libraries
- use compiler command to pass rpath flags because passing them using the linker flags wasn't working

