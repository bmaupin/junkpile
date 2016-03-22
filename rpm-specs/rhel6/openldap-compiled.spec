# This is where the package will be installed.  Change this next line as necessary.
%define _prefix         /usr/local
# This is where OpenSSL is located.  Change this next line as necessary.
%define openssldir      /usr/local
# This is where Heimdal Kerberos is located.  Change this next line as necessary.
%define heimdaldir      /usr/local
# This is where BDB is located.  Change this next line as necessary.
%define bdbdir          /usr/local
# This is where Cyrus-SASL is located.  Change this next line as necessary.
%define sasldir         /usr/local
# Where the perl headers are located.  Change this next line as necessary
%define perlheadersdir  /usr/lib64/perl5/CORE
# This is the name of the service.  Change this next line as necessary.
%define servicename     ldap-compiled
%define name            openldap-compiled
%define pkgname         openldap
%define version         2.4.38
%define release         1%{?dist}

Summary: OpenLDAP directory server
Name: %{name}
Version: %{version}
Release: %{release}
Source0: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{pkgname}-%{version}.tgz
Source1: %{servicename}.init
Source2: usr-local-bin.csh
Source3: usr-local-bin.sh
Vendor: The OpenLDAP Project
URL: http://www.openldap.org/
License: OpenLDAP
Group: System Environment/Daemons
BuildRequires: gcc, make, cyrus-sasl-compiled, openssl-compiled, heimdal-compiled, db4-compiled, libicu-devel, libtool-ltdl-devel, perl-devel, tcp_wrappers-devel
Requires: openssl-compiled, heimdal-compiled, db4-compiled, cyrus-sasl-compiled, libicu, libtool-ltdl, /usr/sbin/useradd, /sbin/chkconfig
Prefix: %{_prefix}

%description
OpenLDAP %{version}

%prep
# Extract the installation tar file
%setup -q -n %{pkgname}-%{version}

%build
# Descriptions of flags used:
# --enable-shared
#       build shared libraries [default=yes]
# --disable-static
#       don't build static libraries
#--disable-ipv6
#--with-cyrus-sasl
#	with Cyrus SASL support (default = auto)
#--with-tls
#	with TLS/SSL support auto (default = auto)
#--enable-dynamic
#	 enable linking built binaries with dynamic libs (default = no)
#--enable-slapd
#	enable building slapd (default = yes)
#--enable-mdb
#   enable mdb database backend (default = yes)
#--enable-modules
#	enable dynamic module support (default = no)
#--enable-spasswd
#	enable (Cyrus) SASL password verification (default = no)
#--enable-rlookups
#	enable reverse lookups of client hostnames (default = no)
#--enable-wrappers
#	enable tcp wrapper support (default = no)
#--enable-rewrite
#	enable DN rewriting in back-ldap and rwm overlay (default = auto)
#--enable-backends=mod
#	enable all available backends
#--disable-shell
#--disable-sql
#--enable-overlays=mod
#	enable all available overlays
#--disable-ndb
#	fixes "configure: error: could not locate mysql_config"
CFLAGS="$RPM_OPT_FLAGS -O2" LD_LIBRARY_PATH="%{bdbdir}/lib" CPPFLAGS="-I%{openssldir}/include -I%{heimdaldir}/include -I%{bdbdir}/include -I%{sasldir}/include -I%{perlheadersdir}" LDFLAGS="-L%{openssldir}/lib -L%{heimdaldir}/lib -L%{bdbdir}/lib -L%{sasldir}/lib -R%{openssldir}/lib -R%{heimdaldir}/lib -R%{bdbdir}/lib -R%{sasldir}/lib" ./configure --prefix=%{_prefix} --enable-shared --disable-static --disable-ipv6 --with-cyrus-sasl --with-tls --enable-dynamic --enable-slapd --enable-mdb --enable-modules --enable-spasswd --enable-rlookups --enable-wrappers --enable-rewrite --enable-backends=mod --disable-shell --disable-sql --enable-overlays=mod --disable-ndb

make depend
make
#make test

%install
# Install scripts to fix the PATH variable
mkdir -p %{buildroot}/etc/profile.d
install -pm 644 %{SOURCE2} %{buildroot}/etc/profile.d
install -pm 644 %{SOURCE3} %{buildroot}/etc/profile.d

# Installs the files in BuildRoot when building the RPM
make DESTDIR=%{buildroot} install

# Install an init script for the servers.
mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
install -m 755 %{SOURCE1} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{servicename}

# Create the data directory.
mkdir -p %{buildroot}/%{_prefix}/var/openldap-data
# Create the new run directory
mkdir -p %{buildroot}/var/run/%{name}

# Enable the Berkeley DB backend
sed -i 's/# moduleload	back_bdb.la/moduleload	back_bdb.la/' %{buildroot}/%{_prefix}/etc/openldap/slapd.conf

# Update the /var/run location
sed -i "s#/usr/local/var/run/slapd.args#/var/run/%{name}/slapd.args#" %{buildroot}/%{_prefix}/etc/openldap/slapd.conf
sed -i "s#/usr/local/var/run/slapd.pid#/var/run/%{name}/slapd.pid#" %{buildroot}/%{_prefix}/etc/openldap/slapd.conf

%pre
# Force exit status to 0 (success) even if user already exists.
/usr/sbin/useradd -c "LDAP User" -u 55 -s /bin/false -r -d %{_prefix}/var/openldap-data ldap 2> /dev/null || :

STARTAGAIN=0

# If the package is being upgraded
if [ $1 -gt 1 ] ; then
    OLD_SLAPD_VERSION=$( rpm -q --queryformat "%{VERSION}" %{name} )
    # If the version number changed
    if [ "$OLD_SLAPD_VERSION" != %{version} ] ; then
        /sbin/service %{servicename} status >/dev/null 2>/dev/null
        # If slapd is running
        if [ "$?" = "0" ] ; then
            # Stop it
            /sbin/service %{servicename} stop
            STARTAGAIN=1
        fi
    fi
fi

%post
/sbin/chkconfig --add %{servicename}

%preun
# If it's being uninstalled (and not upgraded)
if [ $1 -eq 0 ] ; then
        /sbin/service %{servicename} stop > /dev/null 2>&1 || :
        /sbin/chkconfig --del %{servicename}
fi

%postun
# If it's being upgraded
if [ $1 -ge 1 ] ; then
    if [ "$STARTAGAIN" = 1 ] ; then
        /sbin/service %{servicename} start > /dev/null 2>&1 || :
    fi
fi

%files
# Sets the owner and group of all files to root
%defattr(-,root,root)
# Install scripts to fix the PATH variable
%config(noreplace) /etc/profile.d/usr-local-bin.csh
%config(noreplace) /etc/profile.d/usr-local-bin.sh
# Labels certain files as documents to be put in /usr/share/doc
%doc ANNOUNCEMENT CHANGES COPYRIGHT doc INSTALL LICENSE README
# Files to include in the RPM
%{_prefix}
%attr(0755,root,root) %config(noreplace) %{_sysconfdir}/rc.d/init.d/%{servicename}
%config(noreplace) %{_prefix}/etc/openldap/slapd.conf
%attr(-,ldap,ldap) %{_prefix}/etc/openldap
%attr(0700,ldap,ldap) %{_prefix}/var/openldap-data
%attr(0755,ldap,ldap) /var/run/%{name}

%changelog
* Mon Nov 25 2013 bmaupin <bmaupin@users.noreply.github.com> 2.4.38-1
- upgrade to OpenLDAP 2.4.38

* Wed Jul 24 2013 bmaupin <bmaupin@users.noreply.github.com> 2.4.35-1
- upgrade to OpenLDAP 2.4.35

* Thu Oct 18 2012 bmaupin <bmaupin@users.noreply.github.com> 2.4.33-1
- upgrade to OpenLDAP 2.4.33
- explicitly enable building with mdb database backend enabled
- include dist in the release variable
- update spec file according to RHEL 6 guidelines
- make sure profile.d path scripts are included in sources
- make sure ldap.init is included in sources
- add tcp_wrappers-devel as a depencency
- removed --with-kerberos configure flag (unrecognized)
- manually include perl headers directory

* Wed Mar 30 2011 bmaupin <bmaupin@users.noreply.github.com> 2.4.23-1
- upgrade to OpenLDAP 2.4.23

* Mon May 17 2010 bmaupin <bmaupin@users.noreply.github.com> 2.4.22-1
- upgrade to OpenLDAP 2.4.22
- compile using optimizations (-O2)
- disable static libraries and explicitly enable shared libraries
- remove redundant enabling of specific backends and overlays (they're all enabled as modules)
- remove deprecated options

* Mon Jan 25 2010 bmaupin <bmaupin@users.noreply.github.com> 2.4.21-1
- upgrade to OpenLDAP 2.4.21
- remove dependency for google-perftools package
- use more basic init script; we'll keep our customized init script in Puppet
- don't replace existing init script

* Wed Oct  7 2009 bmaupin <bmaupin@users.noreply.github.com> 2.4.19-1
- upgrade to OpenLDAP 2.4.19
- add condition to make sure ldap service isn't removed from chkconfig during upgrade
- add condition to stop ldap service before upgrade if LDAP version is changing
- add condition to try to start ldap service after upgrade if it was running before upgrade
- don't replace existing slapd.conf file

