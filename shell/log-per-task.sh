#!/bin/bash

export LOG_FILE=log.txt


# Set up logging
# Log success/failure for each task
begin() {
    if [ "$next_task" == "" ]; then
        stdbuf -o0 echo "`basename \"$0\"`:" | tee -a $LOG_FILE
        error_count=0
        next_task=$@
        return
    fi
    task=$next_task
    next_task=$@
    if [ "$error_count" -eq 0 ]; then
        stdbuf -o0 echo "  [X] ${task}" | tee -a $LOG_FILE
    else
        stdbuf -o0 echo "  [ ] ERROR completing task: ${task}" | tee -a $LOG_FILE
    fi
    error_count=0
}
# Make sure the last task gets logged
trap begin EXIT
# Log specific commands that return errors
log_failure() {
    this_command="$(history 1 | sed -e "s/^[ ]*[0-9]*[ ]*//g")";
    stdbuf -o0 echo "      ERROR running command: ${this_command}" | tee -a $LOG_FILE
    error_count=$((error_count+1))
}
set -o history
trap log_failure ERR
# Send STDERR to log file
exec 2>> $LOG_FILE


begin "Install prerequisite packages"
# In the standard RHEL repos
yum -y install libselinux-python
# In the RHEL Supplementary repos
yum -y install java-1.7.0-oracle.x86_64 java-1.7.0-oracle-devel.x86_64


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
