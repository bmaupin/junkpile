Building OpenLDAP and dependencies (RHEL 6)
---

1. Set up build environment

        sudo yum -y install gcc git rpm-build
        echo "%_topdir        %{getenv:HOME}/rpm" > ~/.rpmmacros
        cd ~ && mkdir rpm rpm/BUILD rpm/RPMS rpm/SOURCES rpm/SPECS rpm/SRPMS

2. Download sources

        cd ~/rpm/SOURCES
        wget http://download.oracle.com/berkeley-db/db-4.7.25.tar.gz
        wget http://www.openssl.org/source/openssl-1.0.1e.tar.gz
        wget http://www.h5l.org/dist/src/heimdal-1.5.2.tar.gz
        wget ftp://ftp.andrew.cmu.edu/pub/cyrus-mail/cyrus-sasl-2.1.23.tar.gz
        wget ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/openldap-2.4.38.tgz

3. Download our sources and specs

        git clone https://github.com/bmaupin/rpm-specs.git
        mv rpm-specs/sources/* ~/rpm/SOURCES
        mv rpm-specs/rhel6/* ~/rpm/SPECS

4. Install build prerequisites

        sudo yum -y install byacc libicu-devel libtool-ltdl-devel ncurses-devel perl-devel tcp_wrappers-devel

5. Build and install

        rpmbuild -ba ~/rpm/SPECS/db4-compiled.spec
        sudo rpm -iv ~/rpm/RPMS/x86_64/db4-compiled-4.7.25-3.el6.x86_64.rpm
        rpmbuild -ba ~/rpm/SPECS/openssl-compiled.spec
        sudo rpm -iv ~/rpm/RPMS/x86_64/openssl-compiled-1.0.1e-1.el6.x86_64.rpm
        rpmbuild -ba ~/rpm/SPECS/heimdal-compiled.spec
        sudo rpm -iv ~/rpm/RPMS/x86_64/heimdal-compiled-1.5.2-2.el6.x86_64.rpm
        rpmbuild -ba ~/rpm/SPECS/cyrus-sasl-compiled.spec
        sudo rpm -iv ~/rpm/RPMS/x86_64/cyrus-sasl-compiled-2.1.23-4.el6.x86_64.rpm
        rpmbuild -ba ~/rpm/SPECS/openldap-compiled.spec
        sudo rpm -iv ~/rpm/RPMS/x86_64/openldap-compiled-2.4.38-1.el6.x86_64.rpm


6. Start the OpenLDAP service

				sudo service ldap-compiled start
