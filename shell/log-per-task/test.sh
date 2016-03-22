#!/bin/bash

# Set up logging
source log-per-task.sh


begin "Install prerequisite packages"
# In the standard RHEL repos
yum -y install libselinux-python
# In the RHEL Supplementary repos
yum -y install java-1.7.0-oracle.x86_64
yum -y install java-1.7.0-oracle-devel.x86_64


begin "Configure Oracle Instant Client"
echo /usr/lib/oracle/11.2/client64/lib > /etc/ld.so.conf.d/oracle-client.conf
ldconfig


begin "Install UnlimitedJCEPolicyJDK7.zip"
wget \
    --quiet \
    --no-cookies \
    --no-check-certificate \
    --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" \
    -O UnlimitedJCEPolicyJDK7.zip \
    http://download.oracle.com/otn-pub/java/jce/7/UnlimitedJCEPolicyJDK7.zip
jar xvf UnlimitedJCEPolicyJDK7.zip
# Copy them to an alternate location and use update-alternatives so they don't
# get overwritten when Java is updated
mkdir -p /usr/lib/jvm-private/java-1.7.0-oracle.x86_64/jce/unrestricted
/bin/cp -f UnlimitedJCEPolicy/local_policy.jar /usr/lib/jvm-private/java-1.7.0-oracle.x86_64/jce/unrestricted
/bin/cp -f UnlimitedJCEPolicy/US_export_policy.jar /usr/lib/jvm-private/java-1.7.0-oracle.x86_64/jce/unrestricted
update-alternatives \
    --install \
    /usr/lib/jvm/jre-1.7.0-oracle.x86_64/lib/security/local_policy.jar \
    jce_1.7.0_oracle_local_policy.x86_64 \
    /usr/lib/jvm-private/java-1.7.0-oracle.x86_64/jce/unrestricted/local_policy.jar \
    900000 \
    --slave \
    /usr/lib/jvm/jre-1.7.0-oracle.x86_64/lib/security/US_export_policy.jar \
    jce_1.7.0_oracle_us_export_policy.x86_64 \
    /usr/lib/jvm-private/java-1.7.0-oracle.x86_64/jce/unrestricted/US_export_policy.jar
rm -rf UnlimitedJCEPolicy UnlimitedJCEPolicyJDK7.zip

