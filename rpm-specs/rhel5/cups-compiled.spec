%define name cups-compiled
%define pkgname cups

%define php_extdir %(php-config --extension-dir 2>/dev/null || echo %{_libdir}/php4)
%global php_apiver %((echo 0; php -i 2>/dev/null | sed -n 's/^PHP API => //p') | tail -1)

%define initdir /etc/rc.d/init.d
%define use_alternatives 1
%define lspp 1
%define cups_serverbin %{_exec_prefix}/lib/cups

Summary: Common Unix Printing System
Name: %{name}
Version: 1.4.2
Release: 50%{?dist}.4
License: GPLv2
Group: System Environment/Daemons
Source: http://ftp.easysw.com/pub/cups/%{version}/cups-%{version}-source.tar.bz2
# Our initscript
Source1: cups.init
# Pixmap for desktop file
Source2: cupsprinter.png
# udev rules for libusb devices
Source3: cups-libusb.rules
# LSPP-required ps->pdf filter
Source4: pstopdf
# xinetd config file for cups-lpd service
Source5: cups-lpd
# Filter for converting to CUPS raster format
Source6: pstoraster
Source7: pstoraster.convs
# Logrotate configuration
Source8: cups.logrotate
# Backend for NCP protocol
Source9: ncp.backend
# Cron-based tmpwatch for /var/spool/cups/tmp
Source10: cups.cron
# Filter and PPD for textonly printing
Source11: textonly.filter
Source12: textonly.ppd

Patch1: cups-no-gzip-man.patch
Patch2: cups-1.1.16-system-auth.patch
Patch3: cups-multilib.patch
Patch4: cups-serial.patch
Patch5: cups-banners.patch
Patch6: cups-serverbin-compat.patch
Patch7: cups-no-export-ssllibs.patch
Patch8: cups-str3448.patch
Patch9: cups-direct-usb.patch
Patch10: cups-lpr-help.patch
Patch11: cups-peercred.patch
Patch12: cups-pid.patch
Patch13: cups-page-label.patch
Patch14: cups-eggcups.patch
Patch15: cups-getpass.patch
Patch16: cups-driverd-timeout.patch
Patch17: cups-strict-ppd-line-length.patch
Patch18: cups-logrotate.patch
Patch19: cups-usb-paperout.patch
Patch20: cups-build.patch
Patch21: cups-res_init.patch
Patch22: cups-filter-debug.patch
Patch23: cups-uri-compat.patch
Patch24: cups-cups-get-classes.patch
Patch25: cups-avahi.patch
Patch26: cups-str3382.patch
Patch27: cups-str3285_v2-str3503.patch
Patch28: cups-str3390.patch
Patch29: cups-str3391.patch
Patch30: cups-str3381.patch
Patch31: cups-str3399.patch
Patch32: cups-str3403.patch
Patch33: cups-str3407.patch
Patch34: cups-str3418.patch
Patch35: cups-CVE-2009-3553.patch
Patch36: cups-str3422.patch
Patch37: cups-str3413.patch
Patch38: cups-str3439.patch
Patch39: cups-str3440.patch
Patch40: cups-str3442.patch
Patch41: cups-negative-snmp-string-length.patch
Patch42: cups-sidechannel-intrs.patch
Patch43: cups-media-empty-warning.patch
Patch44: cups-str3435.patch
Patch45: cups-str3436.patch
Patch46: cups-str3425.patch
Patch47: cups-str3428.patch
Patch48: cups-str3431.patch
Patch49: cups-snmp-quirks.patch
Patch50: cups-str3458.patch
Patch51: cups-str3460.patch
Patch52: cups-str3495.patch
Patch54: cups-str3505.patch
Patch55: cups-CVE-2010-0302.patch
Patch56: cups-str3541.patch
Patch57: cups-large-snmp-lengths.patch
Patch58: cups-hp-deviceid-oid.patch
Patch59: cups-texttops-rotate-page.patch
Patch60: cups-cgi-vars.patch
Patch61: cups-hostnamelookups.patch
Patch62: cups-CVE-2010-0540.patch
Patch63: cups-CVE-2010-0542.patch
Patch64: cups-CVE-2010-1748.patch
Patch65: cups-CVE-2010-2432.patch
Patch66: cups-CVE-2010-2431.patch
Patch67: cups-CVE-2010-2941.patch
Patch68: cups-str3627.patch
Patch69: cups-str3535.patch
Patch70: cups-str3679.patch
Patch71: cups-0755.patch
Patch72: cups-undo-str2537.patch
Patch73: cups-dns-failure-tolerance.patch
Patch74: cups-snmp-conf-typo.patch
Patch75: cups-str3832.patch
Patch76: cups-str3861.patch
Patch77: cups-str3809.patch
Patch78: cups-str3867.patch
Patch79: cups-str3795-str3880.patch
Patch80: cups-handle-empty-files.patch
Patch81: cups-str4015.patch
Patch82: cups-str3449.patch
Patch83: cups-str3635.patch
Patch84: cups-auth-return-unauthorized.patch
Patch85: cups-str3392.patch

## SECURITY PATCHES:
Patch100: cups-CVE-2012-5519.patch

## Optional LSPP patch:
Patch200: cups-lspp.patch

Epoch: 1
Url: http://www.cups.org/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts: cups
Requires: /sbin/chkconfig /sbin/service
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%if %use_alternatives
Provides: /usr/bin/lpq /usr/bin/lpr /usr/bin/lp /usr/bin/cancel /usr/bin/lprm /usr/bin/lpstat
Requires: /usr/sbin/alternatives
%endif

# Unconditionally obsolete LPRng so that upgrades work properly.
Obsoletes: lpd <= 3.8.15-3, lpr <= 3.8.15-3, LPRng <= 3.8.15-3
Provides: lpd = 3.8.15-4, lpr = 3.8.15-4, LPRng = 3.8.15-4

Obsoletes: cupsddk < 1.2.3-7
Provides: cupsddk = 1.2.3-7
Obsoletes: cupsddk-drivers < 1.2.3-7
Provides: cupsddk-drivers = 1.2.3-7

# kdelibs conflict for bug #192585.
Conflicts: kdelibs < 6:3.5.2-6

BuildRequires: pam-devel pkgconfig
BuildRequires: gnutls-devel libacl-devel
BuildRequires: openldap-devel
BuildRequires: make >= 1:3.80
BuildRequires: php-devel, pcre-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: krb5-devel
BuildRequires: avahi-devel
BuildRequires: poppler-utils

%if %lspp
BuildRequires: libselinux-devel >= 1.23
BuildRequires: audit-libs-devel >= 1.1
%endif

# -fstack-protector-all requires GCC 4.0.1
BuildRequires: gcc >= 4.0.1

BuildRequires: dbus-devel >= 0.90
Requires: dbus >= 0.90

# Requires tmpwatch for the cron.daily script (bug #218901).
Requires: tmpwatch

# We use portreserve to prevent our TCP port being stolen.
# Require the package here so that we know /etc/portreserve/ exists.
Requires: portreserve

Requires: poppler-utils

# We ship udev rules which use setfacl.
Requires: udev
Requires: acl

%package devel
Summary: Common Unix Printing System - development environment
Group: Development/Libraries
License: LGPLv2
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: gnutls-devel
Requires: krb5-devel
Requires: zlib-devel
Obsoletes: cupsddk-devel < 1.2.3-7
Provides: cupsddk-devel = 1.2.3-7
Conflicts: cups-devel

%package libs
Summary: Common Unix Printing System - libraries
Group: System Environment/Libraries
License: LGPLv2
Conflicts: cups-libs

%package lpd
Summary: Common Unix Printing System - lpd emulation
Group: System Environment/Daemons
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: xinetd
Conflicts: cups-lpd

%package php
Summary: Common Unix Printing System - php module
Group: Development/Languages
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
%if 0%{?php_zend_api}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}
%else
Requires: php-api = %{php_apiver}
%endif
Conflicts: cups-php


%description
The Common UNIX Printing System provides a portable printing layer for 
UNIX® operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 

%description devel
The Common UNIX Printing System provides a portable printing layer for 
UNIX® operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.

%description libs
The Common UNIX Printing System provides a portable printing layer for 
UNIX® operating systems. It has been developed by Easy Software Products 
to promote a standard printing solution for all UNIX vendors and users. 
CUPS provides the System V and Berkeley command-line interfaces. 
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lp/lpr commands.

%description lpd
The Common UNIX Printing System provides a portable printing layer for 
UNIX® operating systems. This is the package that provides standard 
lpd emulation.

%description php
The Common UNIX Printing System provides a portable printing layer for
UNIX® operating systems. This is the package that provides a PHP
module. 

%prep
#%setup -q
%setup -q -n %{pkgname}-%{version}
# Don't gzip man pages in the Makefile, let rpmbuild do it.
%patch1 -p1 -b .no-gzip-man
# Use the system pam configuration.
%patch2 -p1 -b .system-auth
# Prevent multilib conflict in cups-config script.
%patch3 -p1 -b .multilib
# Fix compilation of serial backend.
%patch4 -p1 -b .serial
# Ignore rpm save/new files in the banners directory.
%patch5 -p1 -b .banners
# Use compatibility fallback path for ServerBin.
%patch6 -p1 -b .serverbin-compat
# Don't export SSLLIBS to cups-config.
%patch7 -p1 -b .no-export-ssllibsd
# Avoid use-after-free in cupsAddDest.
%patch8 -p1 -b .str3448
# Allow file-based usb device URIs.
%patch9 -p1 -b .direct-usb
# Add --help option to lpr.
%patch10 -p1 -b .lpr-help
# Fix compilation of peer credentials support.
%patch11 -p1 -b .peercred
# Maintain a cupsd.pid file.
%patch12 -p1 -b .pid
# Fix orientation of page labels.
%patch13 -p1 -b .page-label
# Fix implementation of com.redhat.PrinterSpooler D-Bus object.
%patch14 -p1 -b .eggcups
# More sophisticated implementation of cupsGetPassword than getpass.
%patch15 -p1 -b .getpass
# Increase driverd timeout to 70s to accommodate foomatic.
%patch16 -p1 -b .driverd-timeout
# Only enforce maximum PPD line length when in strict mode.
%patch17 -p1 -b .strict-ppd-line-length
# Re-open the log if it has been logrotated under us.
%patch18 -p1 -b .logrotate
# Support for errno==ENOSPACE-based USB paper-out reporting.
%patch19 -p1 -b .usb-paperout
# Simplify the DNSSD parts so they can build using the compat library.
%patch20 -p1 -b .build
# Re-initialise the resolver on failure in httpAddrGetList().
%patch21 -p1 -b .res_init
# Log extra debugging information if no filters are available.
%patch22 -p1 -b .filter-debug
# Allow the usb backend to understand old-style URI formats.
%patch23 -p1 -b .uri-compat
# Fix support for older CUPS servers in cupsGetDests.
%patch24 -p1 -b .cups-get-classes
# Avahi support in the dnssd backend.
%patch25 -p1 -b .avahi
# Fix temporary filename creation.
%patch26 -p1 -b .str3382
# Fix cupsGetNamedDest() when a name is specified.
%patch27 -p1 -b .str3285_v2-str3503
# Set the PRINTER_IS_SHARED CGI variable.
%patch28 -p1 -b .str3390
# Set the CGI variables required by the serial backend.
%patch29 -p1 -b .str3391
# Fix signal handling when using gnutls.
%patch30 -p1 -b .str3381
# Reset SIGPIPE handler before starting child processes.
%patch31 -p1 -b .str3399
# Fixed typo in Russian translation of admin CGI page.
%patch32 -p1 -b .str3403
# Handle out-of-memory more gracefully when loading jobs.
%patch33 -p1 -b .str3407
# Set PPD_MAKE CGI variable.
%patch34 -p1 -b .str3418
# Fix use-after-free in select.c.
%patch35 -p1 -b .CVE-2009-3553
# Fix Russian translations of CGI pages.
%patch36 -p1 -b .str3422
# Fix SNMP handling.
%patch37 -p1 -b .str3413
# Fix adjustment of conflicting options in web interface.
%patch38 -p1 -b .str3439
# Show which option conflicts in web interface.
%patch39 -p1 -b .str3440
# Provide filter path for text/css.
%patch40 -p1 -b .str3442
# Fix SNMP handling with negative string lengths.
%patch41 -p1 -b .negative-snmp-string-length
# Fix signal handling in the sidechannel API.
%patch42 -p1 -b .sidechannel-intrs
# Stop network backends incorrectly clearing media-empty-warning.
%patch43 -p1 -b .media-empty-warning
# Fixed authentication bug in cupsPrintFiles2.
%patch44 -p1 -b .str3435
# Set PRINTER_NAME and PRINTER_URI_SUPPORTED CGI variables.
%patch45 -p1 -b .str3436
# Clean out completed jobs when PreserveJobHistory is off.
%patch46 -p1 -b .str3425
# Don't add two job-name attributes to each job object.
%patch47 -p1 -b .str3428
# Use the Get-Job-Attributes policy for a printer.
%patch48 -p1 -b .str3431
# Handle SNMP supply level quirks (bug #580604).
%patch49 -p1 -b .snmp-quirks
# Fix IPP authentication for servers requiring auth for
# IPP-Get-Printer-Attributes.
%patch50 -p1 -b .str3458
# Clear printer status after successful IPP job.
%patch51 -p1 -b .str3460
# Avoid needless delay in socket backend.
%patch52 -p1 -b .str3495
# Update classes.conf when a class member printer is deleted
# (bug #569903, STR #3505).
%patch54 -p1 -b .str3505
# Applied patch for CVE-2010-0302 (incomplete fix for CVE-2009-3553,
# bug #557775).
%patch55 -p1 -b .CVE-2010-0302
# The lpstat command did not limit the job list to the specified printers.
%patch56 -p1 -b .str3541
# Fixed handling of large SNMP value lengths from upstream commit 8941.
%patch57 -p1 -b .large-snmp-lengths
# Add an SNMP query for HP's device ID OID (STR #3552).
%patch58 -p1 -b .hp-deviceid-oid
# Adjust texttops output to be in natural orientation (STR #3563).
# This fixes page-label orientation when texttops is used in the
# filter chain (bug #593368).
%patch59 -p1 -b .texttops-rotate-page
# Set PATH_INFO and AUTH_TYPE CGI variables (STR #3599, STR #3600,
# bug #520849).
%patch60 -p1 -b .cgi-vars
# Use numeric addresses for interfaces unless HostNameLookups are
# turned on (bug #590632).
%patch61 -p1 -b .hostnamelookups
# Applied patch for CVE-2010-0540 (web interface CSRF), including
# cancel-RSS fix (bug #588805).
%patch62 -p1 -b .CVE-2010-0540
# Applied patch for CVE-2010-0542 (texttops unchecked memory
# allocation failure leading to NULL pointer dereference, STR #3516,
# bug #587746).
%patch63 -p1 -b .CVE-2010-0542
# Applied patch for CVE-2010-1748 (web interface memory disclosure,
# STR #3577, bug #591983).
%patch64 -p1 -b .CVE-2010-0542
# Prevent infinite loop via HTTP_UNAUTHORIZED responses (STR #3518,
# bug #607211, CVE-2010-2432).
%patch65 -p1 -b .CVE-2010-2432
# Fix latent privilege escalation vulnerability (STR #3510,
# bug #604728, CVE-2010-2431).
%patch66 -p1 -b .CVE-2010-2431
# Applied patch to fix cupsd memory corruption vulnerability
# (CVE-2010-2941, STR #3648, bug #624438).
%patch67 -p1 -b .CVE-2010-2941
# lpstat -p reported current job as job id zero (STR #3627, bug #614908).
%patch68 -p1 -b .str3627
# Set the default RIPCache to 128m (STR #3535, bug #616864).
%patch69 -p1 -b .str3535
# Scheduler tracks whether we are shutting down and doesn't start
# new jobs if so (STR #3679, bug #624441).
%patch70 -p1 -b .str3679
# Use mode 0755 for binaries and libraries where appropriate.
%patch71 -p1 -b .0755
# Revert STR #2537 so that non-UTF-8 clients continue to be accepted (bug #642448).
%patch72 -p1 -b .undo-str2537
# Add tolerance for DNS failures (bug #654667).
%patch73 -p1 -b .dns-failure-tolerance
# Typo in sample snmp.conf file (bug #672614).
%patch74 -p1 -b .snmp-conf-typo
# Map ASCII to ISO-8859-1 in the transcoding code (STR #3832, bug #681836).
%patch75 -p1 -b .str3832
# Check for empty values for some configuration directives (STR #3861, bug #706673).
%patch76 -p1 -b .str3861
# The network backends no longer try to collect SNMP supply and status
# information for raw queues (STR #3809, bug #709896).
%patch77 -p1 -b .str3809
# The imageto* filters could crash with bad GIF files (STR #3867,
# STR #3914, bug #714118).
%patch78 -p1 -b .str3867
# The scheduler might leave old job data files in the spool directory
# (STR #3795, STR #3880, bug #735505).
%patch79 -p1 -b .str3795-str3880
# Don't create zero-length request files (bug #740093).
%patch80 -p1 -b .handle-empty-files
# The lp and lpr commands did not cancel jobs queued from stdin on an error
# (STR #4015, bug #738914).
%patch81 -p1 -b .str4015
# cupsPrintFiles() did not report all errors (STR #3449, bug #740093)
%patch82 -p1 -b .str3449
# Fix German translation of web interface search template (STR #3635,
# bug #806818).
%patch83 -p1 -b .str3635
# Avoid "forbidden" error when moving job between queues via web UI
# (bug #834445).
%patch84 -p1 -b .auth-return-unauthorized
# Fixed LDAP browsing issues (bug #870386).
%patch85 -p1 -b .str3392

# SECURITY PATCHES:
%patch100 -p1 -b .CVE-2012-5519

%if %lspp
# LSPP support.
%patch200 -p1 -b .lspp
%endif


sed -i -e '1iMaxLogSize 0' conf/cupsd.conf.in

cp %{SOURCE5} cups-lpd.real
perl -pi -e "s,\@LIBDIR\@,%{_libdir},g" cups-lpd.real

# Let's look at the compilation command lines.
perl -pi -e "s,^.SILENT:,," Makedefs.in

# Fix locale code for Norwegian (bug #520379).
mv locale/cups_no.po locale/cups_nb.po

f=CREDITS.txt
mv "$f" "$f"~
iconv -f MACINTOSH -t UTF-8 "$f"~ > "$f"
rm "$f"~

# Rebuild configure script for --enable-avahi.
aclocal -I config-scripts
autoconf -I config-scripts

%build
export CFLAGS="$RPM_OPT_FLAGS -fstack-protector-all -DLDAP_DEPRECATED=1"
# --enable-debug to avoid stripping binaries
%configure --with-docdir=%{_datadir}/%{name}/www --enable-debug \
%if %lspp
	--enable-lspp \
%endif
	--with-log-file-perm=0600 --enable-pie --enable-relro \
	--enable-pdftops --with-pdftops=pdftops \
	--with-dbusdir=%{_sysconfdir}/dbus-1 \
	--with-php=/usr/bin/php-cgi --enable-avahi \
	localedir=%{_datadir}/locale

# If we got this far, all prerequisite libraries must be here.
make

%install
rm -rf $RPM_BUILD_ROOT

make BUILDROOT=$RPM_BUILD_ROOT install 

# Serial backend needs to run as root (bug #212577).
chmod 700 $RPM_BUILD_ROOT%{cups_serverbin}/backend/serial

rm -rf	$RPM_BUILD_ROOT%{initdir} \
	$RPM_BUILD_ROOT%{_sysconfdir}/init.d \
	$RPM_BUILD_ROOT%{_sysconfdir}/rc?.d
mkdir -p $RPM_BUILD_ROOT%{initdir}
install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{initdir}/cups

find $RPM_BUILD_ROOT/usr/share/cups/model -name "*.ppd" |xargs gzip -n9f

%if %use_alternatives
pushd $RPM_BUILD_ROOT%{_bindir}
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i $i.cups
done
cd $RPM_BUILD_ROOT%{_sbindir}
mv lpc lpc.cups
cd $RPM_BUILD_ROOT%{_mandir}/man1
for i in cancel lp lpq lpr lprm lpstat; do
	mv $i.1 $i-cups.1
done
cd $RPM_BUILD_ROOT%{_mandir}/man8
mv lpc.8 lpc-cups.8
popd
%endif

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps $RPM_BUILD_ROOT%{_sysconfdir}/X11/sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/X11/applnk/System $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -c -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/pixmaps
install -c -m 644 cups-lpd.real $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/cups-lpd
install -c -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/cups
install -c -m 755 %{SOURCE9} $RPM_BUILD_ROOT%{cups_serverbin}/backend/ncp
install -c -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/cups
install -c -m 755 %{SOURCE11} $RPM_BUILD_ROOT%{cups_serverbin}/filter/textonly
install -c -m 644 %{SOURCE12} $RPM_BUILD_ROOT%{_datadir}/cups/model/textonly.ppd

# Ship pstopdf for LSPP systems to deal with malicious postscript
%if %lspp
install -c -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{cups_serverbin}/filter
%endif

# Ship pstoraster (bug #69573).
install -c -m 755 %{SOURCE6} $RPM_BUILD_ROOT%{cups_serverbin}/filter
install -c -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/cups/mime

# Ship a printers.conf file, and a client.conf file.  That way, they get
# their SELinux file contexts set correctly.
touch $RPM_BUILD_ROOT%{_sysconfdir}/cups/printers.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/cups/classes.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/cups/client.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/cups/subscriptions.conf

# This is %%ghost'ed, but needs to be created in %%install anyway.
touch $RPM_BUILD_ROOT%{_sysconfdir}/cups/lpoptions

# Tell portreserve which port we want it to protect.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/portreserve

# LSB 3.2 printer driver directory
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ppd

echo ipp > $RPM_BUILD_ROOT%{_sysconfdir}/portreserve/%{name}

# Handle https:// device URIs (bug #478677, STR #3122).
ln -s ipp $RPM_BUILD_ROOT%{cups_serverbin}/backend/https

# Remove unshipped files.
rm -rf $RPM_BUILD_ROOT%{_mandir}/cat? $RPM_BUILD_ROOT%{_mandir}/*/cat?
rm -f $RPM_BUILD_ROOT%{_datadir}/applications/cups.desktop
rm -rf $RPM_BUILD_ROOT%{_datadir}/icons

# Put the php config bit into place
%{__mkdir_p} %{buildroot}%{_sysconfdir}/php.d
%{__cat} << __EOF__ > %{buildroot}%{_sysconfdir}/php.d/%{name}.ini
; Enable %{name} extension module
extension=phpcups.so
__EOF__

# Install the udev rules.
%{__mkdir_p} %{buildroot}/lib/udev/rules.d
install -m644 %{SOURCE3} \
	%{buildroot}/lib/udev/rules.d/70-cups-libusb.rules

%post
/sbin/chkconfig --del cupsd 2>/dev/null || true # Make sure old versions aren't there anymore
/sbin/chkconfig --add cups || true
# Remove old-style certs directory; new-style is /var/run
# (see bug #194581 for why this is necessary).
/bin/rm -rf /etc/cups/certs
%if %use_alternatives
/usr/sbin/alternatives --install %{_bindir}/lpr print %{_bindir}/lpr.cups 40 \
	 --slave %{_bindir}/lp print-lp %{_bindir}/lp.cups \
	 --slave %{_bindir}/lpq print-lpq %{_bindir}/lpq.cups \
	 --slave %{_bindir}/lprm print-lprm %{_bindir}/lprm.cups \
	 --slave %{_bindir}/lpstat print-lpstat %{_bindir}/lpstat.cups \
	 --slave %{_bindir}/cancel print-cancel %{_bindir}/cancel.cups \
	 --slave %{_sbindir}/lpc print-lpc %{_sbindir}/lpc.cups \
	 --slave %{_mandir}/man1/cancel.1.gz print-cancelman %{_mandir}/man1/cancel-cups.1.gz \
	 --slave %{_mandir}/man1/lp.1.gz print-lpman %{_mandir}/man1/lp-cups.1.gz \
	 --slave %{_mandir}/man8/lpc.8.gz print-lpcman %{_mandir}/man8/lpc-cups.8.gz \
	 --slave %{_mandir}/man1/lpq.1.gz print-lpqman %{_mandir}/man1/lpq-cups.1.gz \
	 --slave %{_mandir}/man1/lpr.1.gz print-lprman %{_mandir}/man1/lpr-cups.1.gz \
	 --slave %{_mandir}/man1/lprm.1.gz print-lprmman %{_mandir}/man1/lprm-cups.1.gz \
	 --slave %{_mandir}/man1/lpstat.1.gz print-lpstatman %{_mandir}/man1/lpstat-cups.1.gz \
	 --initscript cups
%endif
rm -f %{_localstatedir}/cache/cups/*.ipp %{_localstatedir}/cache/cups/*.cache
exit 0

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%preun
if [ "$1" = "0" ]; then
	/sbin/service cups stop > /dev/null 2>&1
	/sbin/chkconfig --del cups
%if %use_alternatives
	/usr/sbin/alternatives --remove print %{_bindir}/lpr.cups
%endif
fi
exit 0

%postun
if [ "$1" -ge "1" ]; then
	/sbin/service cups condrestart > /dev/null 2>&1
fi
exit 0

%triggerin -- samba-client
ln -sf ../../../bin/smbspool %{cups_serverbin}/backend/smb || :
exit 0

%triggerun -- samba-client
[ $2 = 0 ] || exit 0
rm -f %{cups_serverbin}/backend/smb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc LICENSE.txt README.txt CREDITS.txt CHANGES.txt
/lib/udev/rules.d/70-cups-libusb.rules
%dir %attr(0755,root,lp) /etc/cups
%dir %attr(0755,root,lp) /var/run/cups
%dir %attr(0511,lp,sys) /var/run/cups/certs
%verify(not md5 size mtime) %config(noreplace) %attr(0640,root,lp) /etc/cups/cupsd.conf
%attr(0640,root,lp) /etc/cups/cupsd.conf.default
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/cups/client.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) /etc/cups/classes.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0600,root,lp) /etc/cups/printers.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/cups/snmp.conf
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/cups/subscriptions.conf
/etc/cups/interfaces
%verify(not md5 size mtime) %config(noreplace) %attr(0644,root,lp) /etc/cups/lpoptions
%dir %attr(0755,root,lp) /etc/cups/ppd
%dir %attr(0700,root,lp) /etc/cups/ssl
%{_datadir}/cups/mime/pstoraster.convs
%config(noreplace) /etc/pam.d/cups
%config(noreplace) %{_sysconfdir}/logrotate.d/cups
%config(noreplace) %{_sysconfdir}/portreserve/%{name}
%dir %{_datadir}/%{name}/www
%dir %{_datadir}/%{name}/www/es
%dir %{_datadir}/%{name}/www/eu
%dir %{_datadir}/%{name}/www/ja
%dir %{_datadir}/%{name}/www/pl
%dir %{_datadir}/%{name}/www/ru
%{_datadir}/%{name}/www/images
%{_datadir}/%{name}/www/*.css
%doc %{_datadir}/%{name}/www/index.html
%doc %{_datadir}/%{name}/www/help
%doc %{_datadir}/%{name}/www/robots.txt
%doc %{_datadir}/%{name}/www/de/index.html
%doc %{_datadir}/%{name}/www/es/index.html
%doc %{_datadir}/%{name}/www/eu/index.html
%doc %{_datadir}/%{name}/www/ja/index.html
%doc %{_datadir}/%{name}/www/pl/index.html
%doc %{_datadir}/%{name}/www/ru/index.html
%{initdir}/cups
%{_bindir}/cupstestppd
%{_bindir}/cupstestdsc
%{_bindir}/cancel*
%{_bindir}/lp*
%{_bindir}/ppd*
%dir %{cups_serverbin}
%{cups_serverbin}/backend
%{cups_serverbin}/cgi-bin
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-polld
%{cups_serverbin}/daemon/cups-deviced
%{cups_serverbin}/daemon/cups-driverd
%{cups_serverbin}/notifier
%{cups_serverbin}/filter
%{cups_serverbin}/monitor
%{cups_serverbin}/driver
%{_mandir}/man1/cancel*
%{_mandir}/man1/cupstest*
%{_mandir}/man1/lp*
%{_mandir}/man1/ppd*
%{_mandir}/man[578]/*
%{_sbindir}/*
%dir %{_datadir}/cups
%dir %{_datadir}/cups/banners
%{_datadir}/cups/banners/*
%{_datadir}/cups/charsets
%{_datadir}/cups/charmaps
%{_datadir}/cups/data
%{_datadir}/cups/fonts
%{_datadir}/cups/model
%dir %{_datadir}/cups/templates
%{_datadir}/cups/templates/*.tmpl
%{_datadir}/cups/templates/de/*.tmpl
%{_datadir}/cups/templates/es/*.tmpl
%{_datadir}/cups/templates/eu/*.tmpl
%{_datadir}/cups/templates/ja/*.tmpl
%{_datadir}/cups/templates/pl/*.tmpl
%{_datadir}/cups/templates/ru/*.tmpl
%{_datadir}/locale/*
%{_datadir}/ppd
%dir %attr(1770,root,lp) /var/spool/cups/tmp
%dir %attr(0710,root,lp) /var/spool/cups
%dir %attr(0755,lp,sys) /var/log/cups
%{_datadir}/pixmaps/cupsprinter.png
%{_sysconfdir}/cron.daily/cups
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/cups.conf
%{_datadir}/cups/drv
%{_datadir}/cups/examples
%dir %{_datadir}/cups/mime
%{_datadir}/cups/mime/mime.types
%{_datadir}/cups/mime/mime.convs
%dir %{_datadir}/cups/ppdc
%{_datadir}/cups/ppdc/*.defs
%{_datadir}/cups/ppdc/*.h

%files libs
%defattr(-,root,root)
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_bindir}/cups-config
%{_mandir}/man1/cups-config.1.gz
%{_libdir}/*.so
%{_includedir}/cups

%files lpd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/xinetd.d/cups-lpd
%dir %{cups_serverbin}
%dir %{cups_serverbin}/daemon
%{cups_serverbin}/daemon/cups-lpd

%files php
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/php.d/%{name}.ini
%{php_extdir}/phpcups.so

%changelog
* Tue May 21 2013 bmaupin <bmaupin@users.noreply.github.com> cups-compiled-1:1.4.2-50:.4
- Build RHEL 5 package based on RHEL 6 SPEC file
- Rename package to cups-compiled
- Add conflicts so -compiled versions of packages don't get installed at the same time

* Tue Feb 26 2013 Tim Waugh <twaugh@redhat.com> 1:1.4.2-50:.4
- Added BrowseLDAPCACertFile and PrintcapGUI to restricted options
  list.

* Mon Feb 25 2013 Tim Waugh <twaugh@redhat.com> 1:1.4.2-50:.3
- Fix for CVE-2012-5519 patch: handle blacklisted lines that have no
  value part gracefully.

* Fri Feb 15 2013 Tim Waugh <twaugh@redhat.com> 1:1.4.2-50:.2
- Added documentation for new CVE-2012-5519 option.

* Thu Dec 13 2012 Tim Waugh <twaugh@redhat.com> 1:1.4.2-50:.1
- Applied patch to fix CVE-2012-5519 (privilege escalation for users
  in SystemGroup or with equivalent polkit permission).  This prevents
  HTTP PUT requests with paths under /admin/conf/ other than that for
  cupsd.conf, and also prevents such requests altering certain
  configuration directives such as PageLog and FileDevice (bug #875898).

* Fri Oct 26 2012 Tim Waugh <twaugh@redhat.com> 1:1.4.2-50
- Fixed LDAP browsing issues (bug #870386).

* Tue Aug 21 2012 Tim Waugh <twaugh@redhat.com> 1:1.4.2-49
- Avoid "forbidden" error when moving job between queues via web UI
  (bug #834445).

* Mon May 21 2012 Tim Waugh <twaugh@redhat.com> 1:1.4.2-48
- Fix German translation of web interface search template (STR #3635,
  bug #806818).

* Mon Mar 19 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-47
- cupsPrintFiles() did not report all errors (STR #3449, bug #740093)

* Mon Mar 19 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-46
- Fix lp and lpr return string (bug #740093).

* Tue Feb 14 2012 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-45
- Don't create zero-length request files (bug #740093).
- The lp and lpr commands did not cancel jobs queued from stdin on an error
  (STR #4015, bug #738914).
- Fixed condition in textonly filter to create temporary file
  regardless of the number of copies specified. (bug #738410)

* Tue Oct 18 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-44
- Init script should source /etc/sysconfig/cups (bug #744791)

* Wed Sep 07 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-43
- The scheduler might leave old job data files in the spool directory
  (STR #3795, STR #3880, bug #735505).

* Mon Aug 28 2011 Tim Waugh <twaugh@redhat.com> 1:1.4.2-42
- A further fix for imageto* filters crashing with bad GIF files
  (STR #3914, bug #714118).

* Wed Jul 27 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-41
- The imageto* filters could crash with bad GIF files (STR #3867, bug #714118).

* Thu Jun 16 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-40
- Map ASCII to ISO-8859-1 in the transcoding code (STR #3832, bug #681836).
- Check for empty values for some configuration directives (STR #3861, bug #706673).
- The network backends no longer try to collect SNMP supply and status
  information for raw queues (STR #3809, bug #709896).
- Handle EAI_NONAME when resolving hostnames (bug #712430).

* Tue Feb 01 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-39
- Fixed typo in sample snmp.conf file (bug #672614).

* Thu Jan 20 2011 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-38
- Call avc_init() only once to not leak file descriptors (bug #668010).

* Thu Dec 09 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-37
- Fixed cupsSNMPQuirks parsing code in cups-snmp-quirks.patch (bug #580604).
- lpstat -p reported current job as job id zero (STR #3627, bug #614908).
- Set the default RIPCache to 128m (STR #3535, bug #616864).
- Scheduler tracks whether we are shutting down and doesn't start
  new jobs if so (STR #3679, bug #624441).
- Added 'restartlog' action to initscript usage output (bug #632180).
- Fixed following rpmlint errors and warnings (bug #634931):
  - Fix character encoding in CREDITS.txt.
  - Mark D-Bus configuration file as config file.
  - Don't mark MIME types and convs files as config files.  Overrides
    can be placed as new *.types/*.convs files in /etc/cups.
  - Don't mark banners as config files.  Better is to provide new banners.
  - Don't mark initscript as config file.
  - Don't mark templates and www files as config files.  A better way to
    provide local overrides is to use a different ServerRoot setting.
    Note that a recent security fix required changed to template files.
  - Provide versioned LPRng symbol for rpmlint.
  - Use mode 0755 for binaries and libraries where appropriate.
  - Move /etc/cups/pstoraster.convs to /usr/share/cups/mime/.
  - Move cups-config man page to the devel sub-package.
- Revert STR #2537 so non-UTF-8 clients continue to be accepted (bug #642448).
- The php sub-package now explicitly requires the libs package with
  the same version and release (bug #646814).
- Added tolerance for DNS failures (bug #654667).
- Fixed initscript to stop service on reboot/halt (bug #659692).

* Thu Oct 28 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-36
- Applied patch to fix cupsd memory corruption vulnerability
  (CVE-2010-2941, STR #3648, bug #624438).

* Fri Jul 16 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-35
- Set org.cups.sid form variable in choose-device template (bug #615269).

* Wed Jul 14 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-34
- Don't set domain= for cookies (bug #613618).

* Thu Jun 24 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-33
- Fix latent privilege escalation vulnerability (STR #3510,
  bug #604728, CVE-2010-2431).

* Wed Jun 23 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-32
- Prevent infinite loop via HTTP_UNAUTHORIZED responses (STR #3518,
  bug #607211, CVE-2010-2432).

* Wed Jun 16 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-31
- Applied patch for CVE-2010-1748 (web interface memory disclosure,
  STR #3577, bug #591983).
- Applied patch for CVE-2010-0542 (texttops unchecked memory
  allocation failure leading to NULL pointer dereference, STR #3516,
  bug #587746).
- Applied patch for CVE-2010-0540 (web interface CSRF, STR #2398),
  including cancel-RSS fix (bug #588805).

* Thu Jun 10 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-30
- Use numeric addresses for interfaces unless HostNameLookups are
  turned on (bug #590632).

* Wed Jun  9 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-29
- Use upstream method of handling SNMP quirks in PPDs (STR #3551,
  bug #580604).

* Wed Jun  9 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-28
- Set PATH_INFO and AUTH_TYPE CGI variables (STR #3599, STR #3600,
  bug #520849).

* Tue Jun  8 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-27
- Adjust texttops output to be in natural orientation (STR #3563).
  This fixes page-label orientation when texttops is used in the
  filter chain (bug #593368).

* Mon Apr 19 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-26
- Fixed str3541.patch (bug #578424, STR #3541).

* Tue Apr 13 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-25
- Fixed handling of large SNMP value lengths from upstream commit 8941
  (bug #581931).
- Add an SNMP query for HP's device ID OID (STR #3552).

* Tue Apr 13 2010 Tim Waugh <twaugh@redhat.com> 1:1.4.2-24
- Handle SNMP supply level quirks (bug #580604).

* Mon Apr 12 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-23
- The lpstat command did not limit the job list
  to the specified printers (bug #578424, STR #3541).

* Wed Mar 31 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-22
- Another BrowsePoll fix: handle EAI_NODATA as well (bug #567589).

* Wed Mar 10 2010 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-21
- Fixed patch for STR #3425 again to correctly
  remove job info files in /var/spool/cups (bug #571860).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-20
- Applied patch for CVE-2010-0302 (incomplete fix for CVE-2009-3553,
  bug #557775).

* Wed Mar  3 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-19
- Update classes.conf when a class member printer is deleted
  (bug #569903, STR #3505).

* Tue Mar  2 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-18
- Don't apply gcrypt threading patch (bug #569802).
- Don't treat SIGPIPE as an error (bug #569777).
- Fixed cupsGetNamedDest() so it falls back to the real default
  printer when a default from configuration file does not exist
  (bug #569500, STR #3503).
- Added comments for all patches and sources.
- Removed use of prereq and buildprereq.
- Fixed use of '%%' in changelog.
- Versioned explicit obsoletes/provides.
- Use tabs throughout.

* Thu Feb 25 2010 Jiri Popelka <jpopelka@redhat.com> - 1:1.4.2-17
- Reset status after successful ipp job (bug #555732, STR #3460).
- Remove wait_bc call on most platforms (bug #562782, STR #3495).
- Re-initialize the resolver if getnameinfo() returns EAI_AGAIN (bug #567589).

* Wed Jan 13 2010 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-16
- Rebuild against new libaudit.

* Thu Dec 24 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-15
- Fixed ipp authentication for servers requiring authentication for
  IPP-Get-Printer-Attributes (bug #549785, STR #3458).
- Fixed invalid read in cupsAddDest (bug #550301, STR #3448).
- Ensure proper thread-safety in gnutls's use of libgcrypt
  (bug #550302).
- Fixed patch for STR #3425 by adding in back-ported change from svn
  revisions 8929 and 8936 (bug #548906, bug #550037).

* Tue Dec  8 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-14
- The scheduler did not use the Get-Job-Attributes policy for a
  printer (STR #3431).
- The scheduler added two job-name attributes to each job object
  (STR #3428).
- The scheduler did not clean out completed jobs when
  PreserveJobHistory was turned off (STR #3425).
- The web interface did not show completed jobs (STR #3436).
- Authenticated printing did not always work when printing directly to
  a remote server (STR #3435).
- Use upstream patch to stop the network backends incorrectly clearing
  the media-empty-warning state (rev 8896).
- Use upstream patch to fix interrupt handling in the side-channel
  APIs (rev 8896).
- Use upstream patch to handle negative SNMP string lengths (rev 8896).
- Use upstream fix for SNMP detection (bug #542857, STR #3413).
- Use the text filter for text/css files (bug #545026, STR #3442).
- Show conflicting option values in web UI (bug #544326, STR #3440).
- Use upstream fix for adjustment of conflicting options
  (bug #533426, STR #3439).
- No longer requires paps.  The texttopaps filter MIME conversion file
  is now provided by the paps package (bug #545036).

* Tue Dec  8 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-13
- Moved %%{_datadir}/cups/ppdc/*.h to the main package (bug #545348).

* Fri Dec  4 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-12
- The web interface prevented conflicting options from being adjusted
  (bug #533426, STR #3439).

* Thu Dec  3 2009 Tim Waugh <twaugh@redhat.com> - 1:1.4.2-11
- Fixes for SNMP scanning with Lexmark printers (bug #542857, STR #3413).

* Mon Nov 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-10
- Undo last change as it was incorrect.

* Mon Nov 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-9
- Fixed small typos introduced in fix for bug #536741.

* Fri Nov 20 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-8
- Do not translate russian links showing completed jobs
  (bug #539354, STR #3422).

* Thu Nov 19 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-7
- Applied patch to fix CVE-2009-3553 (bug #530111, STR #3200).

* Tue Nov 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-6
- Fixed display of current driver (bug #537182, STR #3418).
- Fixed out-of-memory handling when loading jobs (bug #538054,
  STR #3407).

* Mon Nov 16 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-5
- Fixed typo in admin web template (bug #537884, STR #3403).
- Reset SIGPIPE handler for child processes (bug #537886, STR #3399).

* Mon Nov 16 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-4
- Upstream fix for GNU TLS error handling bug (bug #537883, STR #3381).

* Wed Nov 11 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.2-3
- Fixed lspp-patch to avoid memory leak (bug #536741).

* Tue Nov 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-2
- Added explicit version dependency on cups-libs to cups-lpd
  (bug #502205).

* Tue Nov 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.2-1
- 1.4.2.  No longer need str3380, str3332, str3356, str3396 patches.
- Removed postscript.ppd.gz (bug #533371).
- Renumbered patches and sources.

* Tue Nov  3 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-13
- Removed stale patch from STR #2831 which was causing problems with
  number-up (bug #532516).

* Tue Oct 27 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-12
- Fix incorrectly applied patch from #STR3285 (bug #531108).
- Set the PRINTER_IS_SHARED variable for admin.cgi (bug #529634, #STR3390).
- Pass through serial parameters correctly in web interface (bug #529635, #STR3391).
- Fixed German translation (bug #531144, #STR3396).

* Tue Oct 20 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-11
- Fix cups-lpd to create unique temporary data files (bug #529838).

* Mon Oct 19 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-10
- Fixed German translation (bug #529575, STR #3380).

* Thu Oct  8 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-9
- Fixed naming of 'Generic PostScript Printer' entry.

* Wed Oct  7 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-8
- Use upstream patch for STR #3356 (bug #526405).

* Fri Oct  2 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-7
- Fixed orientation of page labels when printing text in landscape
  mode (bug #520141, STR #3334).

* Wed Sep 30 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-6
- Don't use cached PPD for raw queue (bug #526405, STR #3356).

* Wed Sep 23 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-5
- Fixed cups.init to be LSB compliant (bug #521641)

* Mon Sep 21 2009 Jiri Popelka <jpopelka@redhat.com> 1:1.4.1-4
- Changed cups.init to be LSB compliant (bug #521641), i.e.
  return code "2" (instead of "3") if invalid arguments
  return code "4" if restarting service under nonprivileged user
  return code "5" if cupsd not exist or is not executable
  return code "6" if cupsd.conf not exist

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> 1:1.4.1-3
- Use password-auth common PAM configuration instead of system-auth
  when available.

* Tue Sep 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-2
- Fixed 'service cups status' to check for correct subsys name
  (bug #521641).

* Mon Sep 14 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.1-1
- 1.4.1.

* Fri Sep  4 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.0-2
- Fixed the dnssd backend so that it only reports devices once avahi
  resolution has completed.  This makes it report Device IDs
  (bug #520858).
- Fix locale code for Norwegian (bug #520379).

* Fri Aug 28 2009 Tim Waugh <twaugh@redhat.com> 1:1.4.0-1
- 1.4.0.

* Thu Aug 27 2009 Warren Togami <wtogami@redhat.com> 1:1.4-0.rc1.21
- rebuild

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.20
- Fixed admin.cgi crash when modifying a class (bug #519724,
  STR #3312, patch from Jiri Popelka).

* Wed Aug 26 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.19
- Prevent infinite loop in cupsDoIORequest when processing HTTP
  errors (bug #518065, bug #519663, STR #3311).
- Fixed document-format-supported attribute when
  application/octet-stream is enabled (bug #516507, STR #3308, patch
  from Jiri Popelka).
- Fixed buggy JobKillDelay handling fix (STR #3292).
- Prevent infinite loop in ppdc (STR #3293).

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1:1.4-0.rc1.17.1
- rebuilt with new audit

* Fri Aug 21 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.17
- Removed 3-distribution symlink (bug #514244).

* Tue Aug 18 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.16
- Fixed JobKillDelay handling for cancelled jobs (bug #518026, STR
  #3292).
- Use 'exec' to invoke ghostscript in the pstoraster filter.  This
  allows the SIGTERM signal to reach the correct process, as well as
  conserving memory (part of bug #518026).

* Tue Aug 11 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.15
- Avoid empty BrowseLocalProtocols setting (bug #516460, STR #3287).

* Mon Aug 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.14
- Fixed ppds.dat handling of drv files (bug #515027, STR #3279).
- Fixed udev rules file to avoid DEVTYPE warning messages.
- Fixed cupsGetNamedDest() so it does not fall back to the default
  printer when a destination has been named (bug #516439, STR #3285).
- Fixed MIME type rules for image/jpeg and image/x-bitmap
  (bug #516438, STR #3284).
- Clear out cache files on upgrade.
- Require acl.

* Thu Aug  6 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.13
- Ship udev rules to allow libusb to access printer devices.
- Fixed duplex test pages (bug #514898, STR #3277).

* Wed Jul 29 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.12
- Fixed Avahi support in the dnssd backend (bug #513888).
- Fixed incorrect arguments to sigaction() in dnssd backend (STR #3272).
- Cheaply restore compatibility with 1.1.x by having cups_get_sdests()
  perform a CUPS_GET_CLASSES request if it is not sure it is talking
  to CUPS 1.2 or later (bug #512866).
- Prevent ipp backend looping with bad IPP devices (bug #476424,
  STR #3262).
- Fixed Device ID reporting in the usb backend (STR #3266).

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4-0.rc1.11.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.11
- Tell udevd to replay printer add events in the initscript.

* Wed Jul 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.10
- Applied patch to prevent bad job control files crashing cupsd on
  start-up (STR #3253, bug #509741).
- Correctly handle CUPS-Get-PPDs requests for models with '+' in their
  names (STR #3254, bug #509586).
- Accept incorrect device URIs in the (non-libusb) usb backend for
  compatibility with Fedora 11 before bug #507244 was fixed.
- Applied patch to fix incorrect device URIs (STR #3259, bug #507244).
- Applied patch to fix job-hold-until for remote queues (STR #3258,
  bug #497376).

* Mon Jul 13 2009 Remi Collet <Fedora@FamilleCollet.com> 1:1.4-0.rc1.9
- add PHP ABI check
- use php_extdir
- add php configuration file (/etc/php.d/cups.ini)

* Fri Jul 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.8
- Build does not require aspell-devel (bug #510405).

* Wed Jul  1 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.7
- Fixed template problem preventing current printer option defaults
  from being shown in the web interface (bug #506794, STR #3244).

* Wed Jul  1 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.6
- Fixed lpadmin for remote 1.3.x servers (bug #506977, STR #3231).

* Tue Jun 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.5
- Added more debugging output when constructing filter chain.

* Thu Jun 18 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.4
- More complete fix for STR #3229 (bug #506461).

* Wed Jun 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.3
- Don't use RPM_SOURCE_DIR macro.
- Fixed add/modify-printer templates which had extra double-quote
  characters, preventing the Continue button from appearing in certain
  browsers (bug #506461, STR #3229).

* Wed Jun 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.rc1.1
- 1.4rc1.  No longer need str3124, CVE-2009-0163, CVE-2009-0164,
  str3197, missing-devices patches.
- Disabled avahi patch for the time being.  More work is needed to
  port this to rc1.
- Removed wbuffer patch as it is not needed (see STR #1968).

* Fri May 15 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.18
- More complete fix for STR #3197 (bug #500859).

* Thu May 14 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.17
- Prevent cupsd crash when handling IPP_TAG_DELETEATTR requests
  (STR #3197, bug #500859).

* Thu May  7 2009 Ville Skyttä <ville.skytta at iki.fi> - 1:1.4-0.b2.16
- Avoid stripping binaries before rpmbuild creates the -debuginfo subpackage.

* Sun Apr 26 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.15
- Accept "Host: ::1" (bug #497393).
- Accept Host: fields set to the ServerName value (bug #497301).
- Specify that we want poppler's pdftops (not ghostscript) for the
  pdftops wrapper when calling configure.

* Fri Apr 17 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.14
- Applied patch to fix CVE-2009-0163 (bug #490596).
- Applied patch to fix CVE-2009-0164 (bug #490597).

* Thu Apr  2 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.13
- Don't verify MD5 sum, file size, or mtime for several config files:
  cupsd.conf, client.conf, classes.conf, printers.conf, snmp.conf,
  subscriptions.conf, lpoptions (bug #486287).

* Mon Mar 23 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.12
- If cups-polld gets EAI_AGAIN when looking up a hostname,
  re-initialise the resolver (bug #490943).

* Wed Mar 11 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.11
- Bumped cupsddk n-v-r for obsoletes/provides, as cupsddk was rebuilt.

* Tue Mar 10 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.10
- Applied patch to fix ppd-natural-language attribute in PPD list
  (STR #3124).

* Mon Mar  9 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.9
- Handle https:// device URIs (bug #478677, STR #3122).

* Thu Mar  5 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.8
- Updated to svn8404.

* Wed Feb 25 2009 Tim Waugh <twaugh@redhat.com>
- Added 'Should-Start: portreserve' to the initscript (part of bug #487250).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.4-0.b2.7.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.7
- Prevent cups-deviced missing devices (STR #3108).
- Actually drop the perl implementation of the dnssd backend and use
  the avahi-aware one.

* Thu Feb 12 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.6
- Beginnings of avahi support.  The dnssd backend should now work, but
  the scheduler will not yet advertise DNS-SD services.
- No longer require avahi-tools as the dnssd backend does not use the
  command line tools any longer.
- Load MIME type rules correctly (bug #426089, STR #3059).

* Wed Jan 28 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.4
- Fixed quotas (STR #3077, STR #3078).

* Tue Jan 27 2009 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.3
- Fixed default BrowseLocalProtocols (bug #481505).

* Tue Dec 16 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b2.2
- 1.4b2.
- No longer need CVE-2008-5183 patch.

* Sat Dec 13 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.6
- Start cupsd at priority 25: after avahi-daemon but before haldaemon
  (bug #468709).

* Tue Dec  9 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.5
- Applied patch to fix RSS subscription limiting (bug #473901,
  CVE-2008-5183).
- Attempt to unbreak the fix for STR #2831 (bug #474742).

* Sun Nov 30 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.4
- Own more directories (bug #473581).

* Tue Nov 11 2008 Tim Waugh <twaugh@redhat.com> 1:1.4-0.b1.3
- 1.4b1.
- No longer need ext, includeifexists, foomatic-recommended,
  getnameddest, str2101, str2536 patches.
- Require poppler-utils at runtime and for build.  No longer need
  pdftops.conf.
- Obsolete cupsddk.

* Thu Oct 30 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.9-3
- Fixed LSPP labels (bug #468442).

* Tue Oct 21 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.9-2
- Fixed textonly filter to send FF correctly.

* Fri Oct 10 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.9-1
- 1.3.9, including fixes for CVE-2008-3639 (STR #2918, bug #464710),
  CVE-2008-3640 (STR #2919, bug #464713) and CVE-2008-3641 (STR #2911,
  bug #464716).
- No longer need str2892 or res_init patches.

* Wed Sep 10 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-6
- Backported patch for FatalErrors configuration directive
  (bug #314941, STR #2536).

* Thu Sep  4 2008 Tim Waugh <twaugh@redhat.com>
- Use php-cgi for executing PHP scripts (bug #460898).

* Wed Sep  3 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-5
- The dnssd backend uses avahi-browse so require it (bug #458565).
- New php sub-package (bug #428235).
- cups-polld: reinit the resolver if we haven't yet resolved the
  hostname (bug #354071).

* Mon Aug 11 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-4
- Better password prompting behaviour (bug #215133, STR #2101).

* Tue Aug  5 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-3
- Mark template files config(noreplace) for site-local modifications
  (bug #441719).

* Sun Aug  3 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-2
- Applied patch to fix STR #2892 (bug #453610).

* Mon Jul 28 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.8-1
- 1.3.8.

* Fri Jul 18 2008 Tim Waugh <twaugh@redhat.com>
- Removed autoconf requirement by applying autoconf-generated changes
  to patches that caused them.  Affected patches: cups-lspp.

* Tue Jul 15 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-13
- CVE-2008-1373 patch is no longer needed (applied upstream).
- Mark HTML files and templates config(noreplace) for site-local
  modifications (bug #441719).
- The cups-devel package requires zlib-devel (bug #455192).

* Tue Jul  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-12
- Fixed bug #447200 again.

* Tue Jul  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-11
- Use portreserve.

* Tue Jun 24 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-10
- Rebuilt for new gnutls.

* Tue Jun 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-9
- Don't overwrite the upstream snmp.conf file.

* Tue Jun 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-8
- Fixed bug #447200 again.

* Tue Jun 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-7
- Backported cupsGetNamedDest from 1.4 (bug #428086).

* Tue Jun  3 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-6
- Applied patch to fix STR #2750 (IPP authentication).

* Fri May 30 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-5
- Better fix for cupsdTimeoutJob LSPP configuration suggested by
  Matt Anderson (bug #447200).

* Thu May 29 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-4
- Fix last fix (bug #447200).

* Wed May 28 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-3
- If cupsdTimeoutJob is called when the originating connection is still
  known, pass that to the function so that copy_banner can get at it if
  necessary (bug #447200).

* Fri May  9 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-2
- Applied patch to fix CVE-2008-1722 (integer overflow in image filter,
  bug #441692, STR #2790).

* Thu Apr  3 2008 Tim Waugh <twaugh@redhat.com>
- Main package requires exactly-matching libs package.

* Wed Apr  2 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.7-1
- 1.3.7.  No longer need str2715, str2727, or CVE-2008-0047 patches.

* Thu Apr  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-9
- Applied patch to fix CVE-2008-1373 (GIF overflow, bug #438303).
- Applied patch to prevent heap-based buffer overflow in CUPS helper
  program (bug #436153, CVE-2008-0047, STR #2729).

* Thu Apr  1 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-8
- Ship a few doc files (bug #438598).

* Thu Mar 27 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-7
- Don't ship broken symlink %%{_datadir}/cups/doc (bug #438598).

* Mon Mar 17 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-6
- Own %%{_datadir}/cups/www (bug #437742).

* Thu Feb 28 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-5
- Apply upstream fix for Adobe JPEG files (bug #166460, STR #2727).

* Tue Feb 26 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-4
- LSB header for initscript (bug #246897).
- Move HTML-related files to main application directory so that the CUPS
  web interface still works even with --excludedocs (bug #375631).

* Tue Feb 26 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-3
- Set MaxLogSize to 0 to prevent log rotation.  Upstream default is 1Mb, but
  we want logrotate to be in charge.

* Sat Feb 23 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-2
- Fix encoding of job-sheets option (bug #433753, STR #2715).

* Wed Feb 20 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.6-1
- 1.3.6.

* Thu Feb 14 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-6
- Include fixes from svn up to revision 7304.  No longer need str2703 patch.
  Build with --with-dbusdir.
- Try out logrotate again (bug #432730).

* Tue Feb 12 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-5
- Fixed admin.cgi handling of DefaultAuthType (bug #432478, STR #2703).

* Tue Feb  5 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-4
- Fix compilation of SO_PEERCRED support.
- Include fixes from svn up to revision 7287.  No longer need str2650 or
  str2664 patches.

* Fri Feb  1 2008 Tim Waugh <twaugh@redhat.com>
- Updated initscript for LSB exit codes and actions (bug #246897).

* Thu Jan 24 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-3
- Build requires autoconf.

* Mon Jan 21 2008 Tim Waugh <twaugh@redhat.com> 1:1.3.5-2
- Main package requires libs sub-package of the same release.

* Thu Jan 10 2008 Tim Waugh <twaugh@redhat.com>
- Apply patch to fix busy looping in the backends (bug #426653, STR #2664).

* Wed Jan  9 2008 Tim Waugh <twaugh@redhat.com>
- Apply patch to prevent overlong PPD lines from causing failures except
  in strict mode (bug #405061).  Needed for compatibility with older
  versions of foomatic (e.g. Red Hat Enterprise Linux 3/4).
- Applied upstream patch to fix cupsctl --remote-any (bug #421411, STR #2650).

* Thu Jan  3 2008 Tim Waugh <twaugh@redhat.com>
- Efficiency fix for pstoraster (bug #416871).

* Tue Dec 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.5-1
- 1.3.5.

* Mon Dec 10 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.4-5
- Rebuilt with higher release number.

* Tue Dec 4 2007 Warren Togami <wtogami@redhat.com> 1:1.3.4-3
- rebuild

* Fri Nov 30 2007 Tim Waugh <twaugh@redhat.com>
- CVE-2007-4045 patch is not necessarily because cupsd_client_t objects are
  not moved in array operations, only pointers to them.

* Tue Nov 27 2007 Tim Waugh <twaugh@redhat.com>
- Updated to improved dnssd backend from Till Kamppeter.

* Tue Nov 13 2007 Tim Waugh <twaugh@redhat.com>
- Fixed CVE-2007-4045 patch; has no effect with shipped packages since they
  are linked with gnutls.
- LSPP cupsdSetString/ClearString fixes (bug #378451).

* Wed Nov  7 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.4-2
- Applied patch to fix CVE-2007-4045 (bug #250161).
- Applied patch to fix CVE-2007-4352, CVE-2007-5392 and
  CVE-2007-5393 (bug #345101).

* Thu Nov  1 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.4-1
- 1.3.4 (bug #361681).

* Wed Oct 10 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.3-3
- Use ppdev instead of libieee1284 for parallel port Device ID
  retrieval (bug #311671).  This avoids SELinux audit messages.

* Tue Oct  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.3-2
- Use libieee1284 for parallel port Device ID retrieval (bug #311671).

* Fri Sep 28 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.3-1
- 1.3.3.

* Tue Sep 25 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.2-3
- Don't strip foomatic recommended strings from make/model names.

* Fri Sep 21 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.2-2
- Write printcap when remote printers have timed out (bug #290831).

* Wed Sep 19 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.2-1
- Include Till Kamppeter's dnssd backend.
- 1.3.2.
- No longer need str2512 patches.

* Tue Sep 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.1-3
- Write printcap when a remote queue is deleted (bug #290831).

* Tue Sep 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.1-2
- Avoid writing printcap unnecessarily (bug #290831).

* Mon Sep 17 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.1-1
- 1.3.1.

* Wed Aug 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.0-2
- More specific license tag.

* Mon Aug 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.3.0-1
- 1.3.0.

* Tue Jul 31 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.rc2.2
- Make cancel man page work properly with alternatives system (bug #249768).
- Don't call aclocal even when we modify m4 files -- CUPS does not use
  automake (bug #250251).

* Tue Jul 31 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.rc2.1
- Better buildroot tag.
- Moved LSPP access check in add_job() to before allocation of the job
  structure (bug #231522).
- 1.3rc2.  No longer need avahi patch.

* Mon Jul 23 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.5
- Use kernel support for USB paper-out detection, when available
  (bug #249213).

* Fri Jul 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.4
- Better error checking in the LSPP patch (bug #231522).

* Fri Jul 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.3
- Change initscript start level to 98, to start after avahi but before
  haldaemon.
- The devel sub-package requires krb5-devel.

* Thu Jul 19 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.2
- Build requires avahi-compat-libdns_sd-devel.  Applied patch to fix
  build against avahi (bug #245824).
- Build requires krb5-devel.

* Wed Jul 18 2007 Tim Waugh <twaugh@redhat.com> 1:1.3-0.b1.1
- 1.3b1.  No longer need relro, directed-broadcast, af_unix-auth, or
  str2109 patches.

* Fri Jul 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.12-1
- 1.2.12.  No longer need adminutil or str2408 patches.

* Mon Jul  9 2007 Tim Waugh <twaugh@redhat.com>
- Another small improvement for the textonly filter (bug #244979).

* Thu Jul  5 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-5
- Support for page-ranges and accounting in the textonly filter (bug #244979).

* Wed Jul  4 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-4
- Better paper-out detection patch still (bug #246222).

* Fri Jun 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-3
- Applied patch to fix group handling in PPDs (bug #186231, STR #2408).

* Wed Jun 27 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-2
- Fixed _cupsAdminSetServerSettings() sharing/shared handling (bug #238057).

* Mon Jun 25 2007 Tim Waugh <twaugh@redhat.com>
- Fixed permissions on classes.conf in the file manifest (bug #245748).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.11-1
- 1.2.11.

* Tue Jun 12 2007 Tim Waugh <twaugh@redhat.com>
- Make the initscript use start priority 56 (bug #213828).
- Better paper-out detection patch (bug #241589).

* Wed May  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-10
* Revert paper-out detection for the moment.

* Wed May  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-9
- Applied fix for rotated PDFs (bug #236753, STR #2348).

* Thu Apr 26 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-8
- Initscript fixes (bug #237955).

* Wed Apr 25 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-7
- Until bug #236736 is fixed, work around the kernel usblp driver's
  quirks so that we can detect paper-out conditions.

* Tue Apr 10 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-6
- Fixed 'cancel' man page (bug #234088).
- Added empty subscriptions.conf file to make sure it gets the right
  SELinux file context.

* Wed Apr  4 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-5
- Send D-BUS QueueChanged signal on printer state changes.

* Tue Apr  3 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-4
- Relay printer-state-message values in the IPP backend (STR #2109).

* Mon Apr  2 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-3
- Don't clear printer-state-reasons after job completion (STR #2323).

* Thu Mar 29 2007 Tim Waugh <twaugh@redhat.com>
- Small improvement for AF_UNIX auth patch.

* Thu Mar 29 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-2
- LSPP: Updated patch for line-wrapped labels (bug #228107).

* Tue Mar 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.10-1
- 1.2.10.

* Tue Mar 20 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.9-2
- Added %%{_datadir}/ppd for LSB (bug #232893).

* Fri Mar 16 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.9-1
- 1.2.9.

* Fri Mar  9 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-5
- Better UNIX domain sockets authentication patch after feedback from
  Uli (bug #230613).

* Thu Mar  8 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-4
- Implemented SCM_CREDENTIALS authentication for UNIX domain sockets
  (bug #230613).

* Fri Mar  2 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-3
- Updated LSPP patch (bug #229673).

* Mon Feb 26 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-2
- Applied fix for STR #2264 (bug #230116).

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.8-1
- 1.2.8.

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.7-8
- Removed logrotate config file and maxlogsize patch (bug #227369).  Now
  CUPS is in charge of rotating its own logs, and defaults to doing so once
  they get to 1Mb in size.

* Fri Jan 12 2007 Tim Waugh <twaugh@redhat.com> 1:1.2.7-7
- Don't even reload CUPS when rotating logs (bug #215024).

* Fri Dec  8 2006 Tim Waugh <twaugh@redhat.com>
- Requires tmpwatch for the cron.daily script (bug #218901).

* Thu Dec  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-6
- Fixed If-Modified-Since: handling in libcups (bug #217556, STR #2133).
- Fixed extra EOF in pstops output (bug #216154, STR #2111).
- Use upstream patch for STR #2121.

* Mon Nov 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-5
- Better LSPP fix for bug #216855.

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com>
- Use translated string for password prompt (STR #2121).

* Wed Nov 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-4
- Another LSPP fix (bug #216669).
- Fixed LSPP SELinux check (bug #216855).
- Increased PPD timeout in copy_model() (bug #216065).

* Tue Nov 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-3
- Run the serial backend as root (bug #212577).

* Thu Nov 16 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.7-2
- 1.2.7.

* Tue Nov 14 2006 Tim Waugh <twaugh@redhat.com>
- Fixed LogFilePerm.

* Mon Nov 13 2006 Tim Waugh <twaugh@redhat.com>
- Don't use getpass() (bug #215133).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.6-5
- Reload, don't restart, when logrotating (bug #215023).

* Wed Nov  8 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.6-4
- Fixed pdftops.conf (bug #214611).

* Mon Nov  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.6-3
- 1.2.6.

* Mon Nov  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-7
- One more D-Bus signal fix (bug #212763).

* Fri Nov  3 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-6
- Restore missed JobQueuedRemote D-Bus signal in ipp backend (part of
  bug #212763).

* Thu Nov  2 2006 Tim Waugh <twaugh@redhat.com>
- LSPP patch fix (bug #213498).

* Wed Nov  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-5
- Send QueueChanged D-Bus signal on all job state changes.

* Tue Oct 31 2006 Tim Waugh <twaugh@redhat.com>
- Added filter and PPD for text-only printer (bug #213030).

* Mon Oct 30 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-4
- Fixed support for /dev/ttyUSB devices (bug #212577, STR #2061).
- Fixed parallel backend (bug #213021, STR #2056).

* Tue Oct 26 2006 Tim Waugh <twaugh@redhat.com>
- Ship a real lpoptions file to make sure it is world-readable (bug #203510).

* Mon Oct 23 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.5-3
- 1.2.5.

* Tue Oct 17 2006 Tim Waugh <twaugh@redhat.com>
- Feature-complete LSPP patch from Matt Anderson (bug #210542).

* Thu Oct  5 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-9
- adminutil.c: when writing 'BrowseAllow @LOCAL', add a comment about what
  to change it to when using directed broadcasts from another subnet
  (bug #204373).

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-8
- LSPP patch didn't get updated properly in 1:1.2.4-6.  Use the right
  patch this time (bug #208676).  LSPP re-enabled.

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-7
- LSPP patch disabled, since it still causes cupsd to crash.

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-6
- Updated LSPP patch from Matt Anderson (bug #208676).

* Tue Oct  3 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-5
- Updated LSPP patch from Matt Anderson (bug #208676).

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.4-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-3
- Add '--help' option to lpr command (bug #206380, STR #1989).

* Fri Sep 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.4-2
- 1.2.4 (bug #206763).  No longer need str1968 patch.

* Wed Sep 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-5
- Fixed STR #1968 properly (bug #205619).

* Tue Sep 12 2006 Tim Waugh <twaugh@redhat.com>
- No longer need language patch.

* Mon Sep 11 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-4
- Applied upstream patch to fix STR #1968 (bug #205619).

* Thu Sep  7 2006 Tim Waugh <twaugh@redhat.com>
- %%ghost %%config(noreplace) /etc/cups/lpoptions (bug #59022).

* Wed Aug 30 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-3
- Don't overwrite snmp.c.
- No longer need str1893 patch.

* Wed Aug 30 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.3-2
- 1.2.3.  No longer need str1880 or str1881 patches.

* Tue Aug 29 2006 Tim Waugh <twaugh@redhat.com>
- Removed dest-cache patch.

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-17
- Fixed another LSPP patch problem (bug #203784).
- Updated fix for STR #1881 from upstream.

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-16
- Fixed another LSPP patch problem noted by Erwin Rol.

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-15
- Fixed LSPP patch passing NULL to strcmp (bug #203784).

* Mon Aug 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-14
- Updated LSPP patch (bug #203376).

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.2-13
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Fri Aug 18 2006 Tim Waugh <twaugh@redhat.com>
- Own notifier directory (bug #203085).

* Thu Aug 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-12
- Apply patch to fix STR #1880 (bug #200205).

* Wed Aug 16 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-11
- Use upstream patch to fix STR #1881.

* Fri Aug 11 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-10
- Remove 'Provides: LPRng = 3.8.15-3' (bug #148757).
- Applied patch to fix STR #1893 (bug #201800).

* Thu Aug 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-9
- Try different fix for STR #1795/STR #1881 (bug #201167).

* Sun Aug  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-8
- Apply patch from STR #1881 for remote IPP printing (bug #201167).

* Wed Aug  2 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-7
- Updated LSPP patch from Matt Anderson.
- Ship pstopdf filter for LSPP.

* Fri Jul 28 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-6
- Use replacement snmp.c from STR #1737 (bug #193093).
- Re-enable LSPP; doesn't harm browsing after all.

* Fri Jul 28 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-5
- Disable LSPP for now, since it seems to break browsing somehow.

* Mon Jul 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-4
- Fixed package requirements (bug #199903).

* Fri Jul 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-3
- Apply Matt Anderson's LSPP patch.
- Renumbered patches.

* Thu Jul 20 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.2-2
- 1.2.2.

* Wed Jul 19 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-21
- Sync with svn5754.  Fixes bug #198987, bug #195532, bug #130118.

* Tue Jul 18 2006 John (J5) Palmieri <johnp@redhat.com> - 1:1.2.1-20
- Require a new version of D-Bus and rebuild

* Fri Jul 14 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-19
- Sync with svn5737.  Fixes bug #192015.

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:1.2.1-18.1
- rebuild

* Fri Jul  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-18
- Ship with an empty classes.conf file.

* Tue Jul  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-17
- Sync with svn5706.
- No longer need localhost, str1740, str1758, str1736, str1776 patches.

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-16
- Bumped paps requirement.
- Don't use texttopaps for application/* MIME types (bug #197214).

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-15
- Require paps and use it for printing text (bug #197214).

* Thu Jun 15 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-14
- Don't export in SSLLIBS to cups-config.

* Thu Jun 15 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-13
- Fixed cupsd network default printer crash (STR #1776).

* Wed Jun 14 2006 Tomas Mraz <tmraz@redhat.com> - 1:1.2.1-12
- rebuilt with new gnutls

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-11
- Remove certs directory in %%post, not %%postun.

* Tue Jun 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-10
- Remove old-style certs directory after upgrade (bug #194581).

* Wed Jun  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-9
- Prevent 'too many open files' error (STR #1736, bug #194368).

* Wed Jun  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-8
- Fix 'Allow from @IF(...)' (STR #1758, bug #187703).

* Wed Jun  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-7
- ServerBin compatibility patch (bug #194005).

* Fri Jun  2 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-6
- Applied upstream patch to fix STR #1740 (bug #192809).

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-5
- Fixed group ownerships again (bug #192880).

* Thu Jun  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-4
- Fixed 'service cups reload' not to give an error message.

* Thu May 25 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-3
- Fix 'localhost' fallback in httpAddrGetList() (bug #192628, STR #1723).

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.1-2
- 1.2.1.
- Another STR #1705 fix (bug #192034).
- Fixed devel package multilib conflict (bug #192664).

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-7
- Sync to svn5568.  No longer need rpath patch.
- Added a 'conflicts:' for kdelibs to prevent bug #192548.

* Sat May 20 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-6
- Sync to svn5555.  No longer need str1670 or str1705 patches.

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-5
- Sync to svn5545.
- Ship a driver directory.

* Thu May 18 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-4
- Disable back-channel data in the usb backend (STR #1705, bug #192034).
- Fix for 'browsing stops on reload', STR #1670 (bug #191217).

* Wed May 16 2006 Tim Waugh <twaugh@redhat.com>
- Sync to svn5538.
- Added 'restartlog' to initscript, for clearing out error_log.  Useful
  for problem diagnosis.
- Initscript no longer needs to check for printconf-backend.

* Tue May 16 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-3
- Added image library build requirements.
- The devel package requires gnutls-devel (bug #191908).

* Mon May  8 2006 Tim Waugh <twaugh@redhat.com> 1:1.2.0-2
- 1.2.0.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.4
- Sync to svn5493.

* Fri May  5 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.3
- Sync to svn5491.

* Fri Apr 28 2006 Tim Waugh <twaugh@redhat.com>
- Sync to svn5470.
- No longer need link, CAN-2005-0064, or no-propagate-ipp-port patches.
- Switch to upstream PIE implementation (every single binary is PIE).
- Extend relro to all binaries.
- Better rpath patch.

* Wed Apr 26 2006 Tim Waugh <twaugh@redhat.com>
- No longer need backend, rcp, or ppdsdat patches.
- Use configure switch for LogFilePerm default instead of patch.

* Tue Apr 25 2006 Tim Waugh <twaugh@redhat.com>
- Own /var/run/cups (bug #189561).
- Sync from svn5460 to svn5462.

* Tue Apr 25 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.2
- Patch pdftops to understand 'includeifexists', and use that in the
  pdftops.conf file (bug #189809).

* Mon Apr 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.5.rc3.1
- 1.2rc3.
- Ship an snmp.conf.

* Fri Apr 21 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.4.rc2.2
- Updated to svn 5446.

* Wed Apr 19 2006 Tim Waugh <twaugh@redhat.com>
- Ignore .rpmnew and .rpmsave banner files.

* Tue Apr 11 2006 Tim Waugh <twaugh@redhat.com>
- Ship a /etc/cups/pdftops.conf file (bug #188583).

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com>
- Build requires libacl-devel.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.4.rc2.1
- 1.2rc2.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.9
- Sync scheduler/* with svn 5383.

* Fri Apr  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.8
- No longer need openssl-devel.
- Build with LDAP_DEPRECATED=1, to pick up declarations of ldap_init() etc.
- Only warn about ACLs once (STR #1532).
- Fix imagetops filter (STR #1533).
- Sync pstops.c with svn 5382.

* Thu Apr  6 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.7
- Build requires openldap-devel.
- Sync pstops.c with svn 5372.

* Tue Apr  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.6
- Tweak to allow 'usb:/dev/usb/lp0'-style URIs again.

* Sun Apr  2 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.5
- Backported svn 5365:5366 change for mutex-protected stringpool (STR #1530).

* Sat Apr  1 2006 Tim Waugh <twaugh@redhat.com>
- Fixed _cupsStrFree() (STR #1529).

* Fri Mar 31 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.4
- Fixed interaction with CUPS 1.1 servers (STR #1528).

* Wed Mar 29 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.3
- Fix group list of non-root backends (STR #1521, bug #186954).

* Tue Mar 28 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.2
- Fix lpq -h (STR#1515, bug #186686).

* Mon Mar 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.1
- Ship a printers.conf file, and a client.conf file.  That way, they get
  their SELinux file contexts set correctly.

* Mon Mar 27 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.2.rc1.0
- 1.2rc1.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.6
- Add KDE compatibility symbols _ipp_add_attr/_ipp_free_attr to ipp.h, with
  a comment saying why they shouldn't be used.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.5
- Fix KDE compatibility symbols _ipp_add_attr/_ipp_free_attr.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.4
- Update to svn snapshot.

* Thu Mar 23 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.3
- Update to svn snapshot.  No longer need users or policy patches.

* Fri Mar 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.2
- Rebuilt.

* Tue Mar 14 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.1
- Build requires gnutls-devel.
- Fixed default policy name.
- Fixed 'set-allowed-users' in web UI.

* Mon Mar 13 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b2.0
- 1.2b2.
- Use new CUPS_SERVERBIN location (/usr/lib/cups even on 64-bit hosts).

* Fri Mar 10 2006 Tim Waugh <twaugh@redhat.com>
- Fixed some permissions.

* Fri Mar 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b1.1
- Ship /etc/cups/ssl directory.

* Thu Mar  9 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.1.b1.0
- 1.2b1.  No longer need devid patch.

* Wed Mar  8 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5238.2
- Fixed 'device-id' attribute in GET_DEVICES requests (STR #1467).

* Tue Mar  7 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5238.1
- New svn snapshot.
- No longer need browse or raw patches.

* Wed Mar  1 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5137.1
- Fixed raw printing.
- Removed (unapplied) session printing patch.
- Fixed browse info.

* Thu Feb 23 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5137.0
- New svn snapshot.

* Fri Feb 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5102.0
- New svn snapshot.
- No longer need enabledisable patch.
- Fixed double-free in scheduler/policy.c (STR #1428).

* Fri Feb 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn5083.0
- New svn snapshot.

* Wed Jan 25 2006 Tim Waugh <twaugh@redhat.com> 1:1.2-0.0.svn4964.0
- Use -fPIE not -fpie in PIE patch.
- Fix link patch.
- Patch in PIE instead of using --enable-pie, since that doesn't work.

* Fri Jan 20 2006 Tim Waugh <twaugh@redhat.com>
- 1.2 svn snapshot.
- No longer need doclink, str1023, pdftops, sanity, lpstat, str1068,
  sigchld, gcc34, gcc4, slow, CAN-2004-0888, CAN-2005-2097, finddest,
  str1249, str1284, str1290, str1301, CVE-2005-3625,6,7 patches.
- Removed autodetect-tag patch.

* Tue Jan 17 2006 Tim Waugh <twaugh@redhat.com> 1:1.1.23-30
- Include 'Autodetected' tag for better integration with autodetection tools.

* Tue Jan 10 2006 Tim Waugh <twaugh@redhat.com> 1:1.1.23-29
- Apply dest-cache-v2 patch (bug #175847).

* Wed Jan  4 2006 Tim Waugh <twaugh@redhat.com> 1:1.1.23-28
- Apply patch to fix CVE-2005-3625, CVE-2005-3626, CVE-2005-3627
  (bug #176868).

* Mon Dec 19 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-27
- Link pdftops with -z relro.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 John (J5) Palmieri <johnp@redhat.com> - 1:1.1.23-26
- rebuild for new dbus

* Tue Nov  8 2005 Tomas Mraz <tmraz@redhat.com> 1:1.1.23-25
- rebuilt with new openssl

* Thu Oct 20 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-24
- Build with -fstack-protector-all.

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com> 1:1.1.23-23
- link libcupsimage.so against libcups

* Tue Oct 11 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-22
- Apply patch to fix STR #1301 (bug #169979).

* Thu Oct  6 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-21
- Apply patch to fix STR #1290.

* Wed Oct  5 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-20
- Apply upstream patch for STR #1249.

* Fri Sep 30 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-19
- Use upstream patch for STR #1284.

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Thu Sep 29 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-18
- Raise IPP_MAX_VALUES to 100 (bug #164232).  STR #1284.
- Made FindDest better behaved in some instances (bug #164232).  STR #1283.

* Fri Sep  2 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-17
- Fixed CAN-2005-2097 (bug #164510).

* Thu Jun 16 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-16
- Make DeletePrinterFromClass faster (bug #160620).

* Thu Mar 31 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-15
- Don't require exact dbus version, just minimum.

* Thu Mar 10 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-14
- Fixed up dbus patch so that it compiles.

* Wed Mar  9 2005 John (J5) Palmieri <johnp@redhat.com>
- Fix up dbus patch 

* Mon Mar  7 2005 John (J5) Palmieri <johnp@redhat.com> 1:1.1.23-13
- Fixed up dbus patch to work with dbus 0.31

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 1:1.1.23-12
- rebuild for openssl-0.9.7e

* Tue Feb 22 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-11
- UTF-8-ify spec file (bug #149293).

* Fri Feb 18 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-10
- Fixed build with GCC 4.

* Thu Feb 10 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-9
- Back to old DBUS API since new DBUS isn't built yet.

* Mon Feb  7 2005 Tim Waugh <twaugh@redhat.com>
- Use upstream patch for STR #1068.
- Apply patch to fix remainder of CAN-2004-0888 (bug #135378).

* Wed Feb  2 2005 Tim Waugh <twaugh@redhat.com>
- Applied patch to prevent occasional cupsd crash on reload (bug #146850).

* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-8
- New DBUS API.

* Tue Feb  1 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-7
- Applied patch to prevent file descriptor confusion (STR #1068).

* Fri Jan 28 2005 Tim Waugh <twaugh@redhat.com>
- Build does not require XFree86-devel (bug #146397).

* Thu Jan 27 2005 Tim Waugh <twaugh@redhat.com>
- Corrected directory modes so that they reflect what cupsd sets them to.

* Mon Jan 24 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-6
- Build against new dbus.

* Fri Jan 21 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-5
- Use tmpwatch to remove unused files in the spool temporary directory
  (bug #110026).

* Thu Jan 20 2005 Tim Waugh <twaugh@redhat.com>
- Use gzip's -n flag for the PPDs.

* Thu Jan 20 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-4
- Mark the initscript noreplace (bug #145629).

* Wed Jan 19 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-3
- Applied patch to fix CAN-2005-0064.

* Thu Jan  6 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-2
- Fixed patch from STR #1023.

* Tue Jan  4 2005 Tim Waugh <twaugh@redhat.com> 1:1.1.23-1
- 1.1.23.

* Mon Dec 20 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.23-0.rc1.1
- 1.1.23rc1.
- No longer need ioctl, ref-before-use, str1023 or str1024 patches.

* Fri Dec 17 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-6
- Use upstream patches for bug #143086.

* Thu Dec 16 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-5
- Fixed STR #1023 (part of bug #143086).
- Fixed STR #1024 (rest of bug #143086).

* Thu Dec  9 2004 Tim Waugh <twaugh@redhat.com>
- Not all files in the doc directory are pure documentation (bug #67337).

* Thu Dec  9 2004 Tim Waugh <twaugh@redhat.com>
- Fixed ioctl parameter size in usb backend.  Spotted by David A. Marlin.

* Fri Dec  3 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-4
- Convert de and fr .tmpl files into UTF-8 (bug #136177).

* Thu Dec  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-3
- Fix ref-before-use bug in debug output (bug #141585).

* Mon Nov 29 2004 Tim Waugh <twaugh@redhat.com>
- Copied "ext" patch over from xpdf RPM package.

* Mon Nov 22 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-2
- Fixed cups-lpd file mode (bug #137325).
- Convert all man pages to UTF-8 (bug #107118).  Patch from Miloslav Trmac.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com>
- New lpd subpackage, from patch by Matthew Galgoci (bug #137325).

* Tue Nov  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-1
- 1.1.22.
- No longer need ippfail, overread or str970 patches.

* Tue Oct 26 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc2.1
- Make cancel-cups(1) man page point to lp-cups(1) not lp(1) (bug #136973).
- Use upstream patch for STR #953.
- 1.1.22rc2.

* Wed Oct 20 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.7
- Prevent filters generating incorrect PS in locales where "," is the
  decimal separator (bug #136102).  Patch from STR #970.

* Thu Oct 14 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.5
- Fixed another typo in last patch!

* Thu Oct 14 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.4
- Fixed typo in last patch.

* Thu Oct 14 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.3
- Another attempt at fixing bug #135502.

* Wed Oct 13 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.2
- Fail better when receiving corrupt IPP responses (bug #135502).

* Mon Oct 11 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.22-0.rc1.1
- 1.1.22rc1.

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-7
- Set LogFilePerm 0600 in default config file.

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-6
- Apply patch to fix CAN-2004-0923 (bug #134601).

* Mon Oct  4 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-5
- Fixed reload logic (bug #134080).

* Wed Sep 29 2004 Warren Togami <wtogami@redhat.com> 1:1.1.21-4
- Remove .pdf from docs, fix links

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-3
- Write a pid file (bug #132987).

* Thu Sep 23 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-2
- 1.1.21.

* Thu Sep  9 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc2.2
- Updated DBUS patch (from Colin Walters).

* Tue Aug 24 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc2.1
- 1.1.21rc2.
- No longer need state, reload-timeout or str743 patches.
- httpnBase64 patch no longer applies; alternate method implemented
  upstream.
- Fix single byte overread in usersys.c (spotted by Colin Walters).

* Wed Aug 18 2004 Tim Waugh <twaugh@redhat.com>
- Applied httpnEncode64 patch from Colin Walters.

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com>
- Session printing patch (Colin Walters).  Disabled for now.

* Sun Aug 15 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.9
- Shorter reload timeout (Colin Walters).
- Updated DBUS patch from Colin Walters.

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com>
- Updated IPP backend IPP_PORT patch from Colin Walters.

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.8
- Preserve DBUS_SESSION_BUS_ADDRESS in environment (Colin Walters).
- Fixed enabledisable patch.

* Fri Aug 13 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.7
- Bumped DBUS version to 0.22.

* Fri Aug  6 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.6
- Patch from Colin Walters to prevent IPP backend using non-standard
  IPP port.

* Sun Aug  1 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.5
- Really bumped DBUS version.

* Fri Jul 30 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.4
- Bumped DBUS version.

* Fri Jul 16 2004 Tim Waugh <twaugh@redhat.com>
- Added version to LPRng obsoletes: tag (bug #128024).

* Thu Jul  8 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.3
- Updated DBUS patch.

* Tue Jun 29 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.2
- Apply patch from STR #743 (bug #114999).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-1.rc1.1
- Fix permissions on logrotate script (bug #126426).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-0.rc1.2
- Build for dbus-0.21.
- Fix SetPrinterState().

* Thu Jun  3 2004 Tim Waugh <twaugh@redhat.com>
- Use configure's --with-optim parameter instead of setting OPTIM at
  make time (bug #125228).

* Thu Jun  3 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.21-0.rc1.1
- 1.1.21rc1.
- No longer need str716, str718, authtype or encryption patches.

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-15
- Build on ppc and ppc64 again.

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-14
- ExcludeArch ppc, ppc64.
- More D-BUS changes.

* Tue Jun  1 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-13
- Enable optimizations on ia64 again.

* Thu May 27 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-12
- D-BUS changes.

* Wed May 26 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-11
- Build requires make >= 3.80 (bug #124472).

* Wed May 26 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-10
- Finish fix for cupsenable/cupsdisable (bug #102490).
- Fix MaxLogSize setting (bug #123003).

* Tue May 25 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-9
- Apply patches from CVS (authtype) to fix STR #434, STR #611, and as a
  result STR #719.  This fixes several problems including those noted in
  bug #114999.

* Mon May 24 2004 Tim Waugh <twaugh@redhat.com>
- Use upstream patch for exit code fix for bug #110135 [STR 718].

* Wed May 19 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-8
- If cupsd fails to start, make it exit with an appropriate code so that
  initlog notifies the user (bug #110135).

* Thu May 13 2004 Tim Waugh <twaugh@redhat.com>
- Fix cups/util.c:get_num_sdests() to use encryption when it is necessary
  or requested (bug #118982).
- Use upstream patch for the HTTP/1.1 Continue bug (from STR716).

* Tue May 11 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-7
- Fix non-conformance with HTTP/1.1, which caused failures when printing
  to a Xerox Phaser 8200 via IPP (bug #122352).
- Make lppasswd(1) PIE.
- Rotate logs within cupsd (instead of relying on logrotate) if we start
  to approach the filesystem file size limit (bug #123003).

* Tue Apr  6 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-6
- Fix pie patch (bug #120078).

* Fri Apr  2 2004 Tim Waugh <twaugh@redhat.com>
- Fix rcp patch for new system-config-printer name.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb  6 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-4
- Tracked D-BUS API changes.
- Updated D-BUS configuration file.
- Symlinks to avoid conflicting with bash builtins (bug #102490).

* Thu Feb  5 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-3
- Improved PIE patch.
- Fixed compilation with GCC 3.4.

* Thu Jan 29 2004 Tim Waugh <twaugh@redhat.com>
- Don't ship cupsconfig now that nothing uses it.

* Wed Jan  7 2004 Tim Waugh <twaugh@redhat.com> 1:1.1.20-2
- Try harder to find a translated page for the web interface (bug #107619).
- Added build_as_pie conditional to spec file to facilitate debugging.

* Mon Dec  1 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.20-1
- 1.1.20.
- No longer need idefense, str226 patches.
- Updated sanity patch.
- The devel sub-package requires openssl-devel (bug #110772).

* Wed Nov 26 2003 Thomas Woerner <twoerner@redhat.com> 1:1.1.19-16
- removed -Wl,-rpath from cups-sharedlibs.m4 (replaced old no_rpath patch)

* Tue Nov 25 2003 Thomas Woerner <twoerner@redhat.com> 1:1.1.19-15
- no rpath in cups-config anymore

* Thu Nov 20 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-14
- Enable PIE for cupsd.

* Fri Nov 14 2003 Tim Waugh <twaugh@redhat.com>
- Don't ignore the file descriptor when ShutdownClient is called: it
  might get closed before we next try to read it (bug #107787).

* Tue Oct 14 2003 Tim Waugh <twaugh@redhat.com>
- Removed busy-loop patch; 1.1.19 has its own fix for this.

* Thu Oct  2 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-13
- Apply patch from STR 226 to make CUPS reload better behaved (bug #101507).

* Wed Sep 10 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-12
- Prevent a libcups busy loop (bug #97958).

* Thu Aug 14 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-11
- Another attempt to fix bug #100984.

* Wed Aug 13 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-10
- Pass correct attributes-natural-language through even in the absence
  of translations for that language (bug #100984).
- Show compilation command lines.

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-9
- Prevent lpstat displaying garbage.

* Mon Jul 21 2003 Tim Waugh <twaugh@redhat.com>
- Mark mime.convs and mime.types as config files (bug #99461).

* Mon Jun 23 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-8
- Start cupsd before nfs server processes (bug #97767).

* Tue Jun 17 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-7
- Add some %%if %%use_dbus / %%endif's to make it compile without dbus
  (bug #97397).  Patch from Jos Vos.

* Mon Jun 16 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-6
- Don't busy loop in the client if the IPP port is in use by another
  app (bug #97468).

* Tue Jun 10 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-5
- Mark pam.d/cups as config file not to be replaced (bug #92236).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-3
- Provide a version for LPRng (bug #92145).

* Thu May 29 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-2
- Obsolete LPRng now.

* Tue May 27 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-1
- 1.1.19.  No longer need optparse patch.

* Sat May 17 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.4
- Ship configuration file for D-BUS.

* Fri May 16 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.3
- Rebuild for dbus-0.11 API changes.
- Fix ownership in file manifest (bug #90840).

* Wed May 14 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.2
- Fix option parsing in lpq (bug #90823).

* Tue May 13 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc5.1
- 1.1.19rc5.

* Thu May  8 2003 Tim Waugh <twaugh@redhat.com> 1:1.1.19-0.rc4.1
- 1.1.19rc4.  Ported initscript, idefense, ppdsdat, dbus patches.
- No longer need error, sigchld patches.
- Ship cupstestppd.

* Thu Apr 24 2003 Tim Waugh <twaugh@redhat.com>
- Mark banners as config files (bug #89069).

* Sat Apr 12 2003 Havoc Pennington <hp@redhat.com> 1:1.1.18-4
- adjust dbus patch - dbus_bus_get() sends the hello for you, 
  and there were a couple of memleaks
- buildprereq dbus 0.9
- rebuild for new dbus
- hope it works, I'm ssh'd in with no way to test. ;-)

* Thu Apr 10 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-3
- Get on D-BUS.

* Fri Mar 28 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-2
- Fix translation in the init script (bug #87551).

* Wed Mar 26 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-1.1
- Turn off optimization on ia64 until bug #87383 is fixed.

* Wed Mar 26 2003 Tim Waugh <twaugh@redhat.com> 1.1.18-1
- 1.1.18.
- No longer need uninit patch.
- Some parts of the iDefense and pdftops patches seem to have been
  picked up, but not others.

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-13
- Don't set SIGCHLD to SIG_IGN when using wait4 (via pclose) (bug #84101).

* Tue Feb  4 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-12
- Fix cups-lpd (bug #83452).

* Fri Jan 31 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-11
- Build ppds.dat on first install.

* Fri Jan 24 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-10
- Add support for rebuilding ppds.dat without running the scheduler
  proper (for bug #82500).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 1.1.17-9
- rebuilt

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-8
- Warn against editing queues managed by redhat-config-printer
  (bug #82267).

* Wed Jan 22 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-7
- Fix up error reporting in lpd backend.

* Thu Jan  9 2003 Tim Waugh <twaugh@redhat.com> 1.1.17-6
- Add epoch to internal requirements.
- Make 'condrestart' return success exit code when daemon isn't running.

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 1.1.17-5
- Use pkg-config information to find SSL libraries.

* Thu Dec 19 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-4
- Security fixes.
- Make 'service cups reload' update the configuration first (bug #79953).

* Tue Dec 10 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-3
- Fix cupsd startup hang (bug #79346).

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-2
- Fix parallel backend behaviour when cancelling jobs.

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 1.1.17-1
- 1.1.17.
- No longer need libdir patch.
- Fix logrotate script (bug #76791).

* Wed Nov 20 2002 Tim Waugh <twaugh@redhat.com>
- Build requires XFree86-devel (bug #78362).

* Wed Nov 20 2002 Tim Waugh <twaugh@redhat.com>
- 1.1.16.
- Updated system-auth patch.
- Add ncp backend script.

* Wed Nov 13 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-15
- Set alternatives priority to 40.

* Mon Nov 11 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.15-14
- Buildrequire pam-devel.
- Patch default PAM config file to remove directory names from module paths,
  allowing the configuration files to work equally well on multilib systems.
- Patch default PAM config file to use system-auth, require the file at build-
  time because that's what data/Makefile checks for.

* Fri Nov  8 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-13
- Use logrotate for log rotation (bug #76791).
- No longer need cups.desktop, since redhat-config-printer handles it.

* Thu Oct 17 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-12
- Revert to libdir for CUPS_SERVERBIN.

* Thu Oct 17 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-11
- Use %%configure for multilib correctness.
- Use libexec instead of lib for CUPS_SERVERBIN.
- Ship translated man pages.
- Remove unshipped files.
- Fix file list permissions (bug #59021, bug #74738).
- Fix messy initscript output (bug #65857).
- Add 'reload' to initscript (bug #76114).

* Fri Aug 30 2002 Bernhard Rosenkraenzer <bero@redhat.de> 1.1.15-10
- Add generic postscript PPD file (#73061)

* Mon Aug 19 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-9
- Fix prefix in pstoraster (bug #69573).

* Mon Aug 19 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-8
- Disable cups-lpd by default (bug #71712).
- No need for fread patch now that glibc is fixed.

* Thu Aug 15 2002 Tim Waugh <twaugh@redhat.com> 1.1.15-7
- Really add cups-lpd xinetd file (bug #63919).
- Ship pstoraster (bug #69573).
- Prevent fread from trying to read from beyond EOF (fixes a segfault
  with new glibc).

* Sat Aug 10 2002 Elliot Lee <sopwith@redhat.com> 1.1.15-6
- rebuilt with gcc-3.2 (we hope)

* Mon Aug  5 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.15-5
- Add cups-lpd xinetd file (#63919)

* Tue Jul 23 2002 Florian La Roche <Florian.LaRoche@redhat.de> 1.1.15-4
- add a "exit 0" to postun script

* Tue Jul  2 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.15-3
- Add a symlink /usr/share/cups/doc -> /usr/share/doc/cups-devel-1.1.15
  because some applications expect to find the cups docs in
  /usr/share/cups/doc

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun 21 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.15-1
- 1.1.15-1
- Fix up smb printing trigger (samba-client, not samba-clients)
- Start cupsd earlier, apparently it needs to be running before samba
  starts up for smb printing to work.

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May  7 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-17
- Rebuild in current environment
- [-16 never existed because of build system breakage]

* Wed Apr 17 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-15
- Fix bug #63387

* Mon Apr 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-14
- Fix dangling symlink created by samba-clients trigger

* Wed Apr 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-13
- Add desktop file and icon for CUPS configuration

* Wed Apr  3 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-12
- Support SMB printing (#62407)
- Add HTML redirections to doc files to work around users mistaking
  /usr/share/doc/cups-1.1.14 for the web frontend (#62405)

* Tue Apr  2 2002 Bill Nottingham <notting@redhat.com> 1.1.14-11
- fix subsys in initscript (#59206)
- don't strip binaries

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-10
- Make initscript use killproc instead of killall

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com> 1.1.14-9
- use alternatives --initscript support

* Mon Mar  4 2002 Bill Nottingham <notting@redhat.com> 1.1.14-8
- use the right path for the lpc man page, duh

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 1.1.14-7
- lpc man page is alternative too
- run ldconfig in -libs %%post/%%postun, not main
- remove alternatives in %%preun

* Wed Feb 27 2002 Bill Nottingham <notting@redhat.com> 1.1.14-6
- don't source /etc/sysconfig/network in cups.init, we don't use any
  values from it

* Tue Feb 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-4
- Fix bugs #60220 and #60352

* Thu Feb 21 2002 Tim Powers <timp@redhat.com>
- rebuild against correct version of openssl (0.9.6b)

* Wed Feb 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-2
- Add all man pages to alternatives (#59943)
- Update to real 1.1.14

* Tue Feb 12 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.14-1
- Update to almost-1.1.14

* Mon Feb 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-5
- Move cups-config to cups-devel subpackage
- Make alternatives usage a %%define to simplify builds for earlier
  releases
- Explicitly provide things we're supplying through alternatives
  to shut up kdeutils dependencies

* Tue Feb  5 2002 Tim Powers <timp@redhat.com>
- shut the alternatives stuff up for good

* Fri Feb  1 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-3
- Fix alternatives stuff
- Don't display error messages in %%post

* Wed Jan 30 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-2
- alternatives stuff

* Tue Jan 29 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.13-1
- 1.1.13
- Add patch for koi8-{r,u} and iso8859-8 encodings (#59018)
- Rename init scripts so we can safely "killall cupsd" from there

* Sat Jan 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.12-1
- Initial (conflicting, since alternatives isn't there yet) packaging for
  Red Hat Linux

* Sat Jan 19 2002 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.12

* Mon Nov  5 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.10-3
- Compress PPD files
- Fix build with gcc 3.1
- Fix init script

* Tue Sep  4 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.10-2
- Fix URL
- Generate printcap
- s/Copyright/License/g

* Tue Sep  4 2001 Than Ngo <than@redhat.com> 1.1.10-1
- update to 1.1.10-1 for ExtraBinge 7.2

* Tue May 29 2001 Michael Stefaniuc <mstefani@redhat.com>
- update to 1.1.8
- changed cupsd.conf to generate /etc/printcap

* Tue May 15 2001 Than Ngo <than@redhat.com>
- update to 1.1.7, bugfixes

* Thu Dec 14 2000 Than Ngo <than@redhat.com>
- fixed package dependency with lpr and LPRng

* Wed Oct 25 2000 Than Ngo <than@redhat.com>
- remove man/cat

* Tue Oct 24 2000 Than Ngo <than@redhat.com>
- don't start cupsd service in level 0, fixed

* Thu Oct 19 2000 Than Ngo <than@redhat.com>
- update to 1.1.4
- fix CUPS_DOCROOT (Bug #18717)

* Fri Aug 11 2000 Than Ngo <than@redhat.de>
- update to 1.1.2 (Bugfix release)

* Fri Aug 4 2000 Than Ngo <than@redhat.de>
- fix, cupsd read config file under /etc/cups (Bug #15432)
- add missing cups filters

* Wed Aug 2 2000 Tim Powers <timp@redhat.com>
- rebuilt against libpng-1.0.8

* Tue Aug 01 2000 Than Ngo <than@redhat.de>
- fix permission, add missing ldconfig in %%post and %%postun (Bug #14963)

* Sat Jul 29 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.1.1 (this has some major bugfixes)
- Fix a typo in initscript (it's $?, not ?$)
- Fix /usr/etc vs. /etc trouble, don't insist on /usr/var (YUCK!)
- Create the spool dir

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- fix unclean code for building against gcc-2.96
- add missing restart function in startup script

* Fri Jul 28 2000 Tim Powers <timp@redhat.com>
- fixed initscript so that conrestart doesn't return 1 if the test fails

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Wed Jul 19 2000 Than Ngo <than@redhat.de>
- using service to fire them up
- fix Prereq section

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- added defattr to the devel package

* Sun Jul 16 2000 Than Ngo <than@redhat.de>
- add cups config files

* Sat Jul 15 2000 Than Ngo <than@redhat.de>
- update to 1.1 release
- move back to /etc/rc.d/init.d
- fix cupsd.init to work with /etc/init.d and /etc/rc.d/init.d
- split cups

* Wed Jul 12 2000 Than Ngo <than@redhat.de>
- rebuilt

* Thu Jul 06 2000 Tim Powers <timp@redhat.com>
- fixed broken PreReq to now require /etc/init.d

* Tue Jun 27 2000 Tim Powers <timp@redhat.com>
- PreReq initscripts >= 5.20

* Mon Jun 26 2000 Tim Powers <timp@redhat.com>
- started changelog 
- fixed init.d script location
- changed script in init.d quite a bit and made more like the rest of our
  startup scripts 
