log_file=log.txt


# Script that logs per task
# - Console sees stdout, stderr, and task success/failure
# - Log file only sees stderr and task success/failure. Ex:
#
# $ cat log.txt
# log-per-task.sh:
# This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
# This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
#  [X] Install prerequisite packages
#      ERROR running command: test
#  [ ] ERROR completing task: Configure Oracle Instant Client
#  [X] Install UnlimitedJCEPolicyJDK7.zip


# Log success/failure for each task
begin() {
    if [ "$next_task" == "" ]; then
        stdbuf -o0 echo "`basename \"$0\"`:" | tee -a $log_file
        error_count=0
        next_task=$@
        return
    fi
    task=$next_task
    next_task=$@
    if [ "$error_count" -eq 0 ]; then
        stdbuf -o0 echo "  [X] ${task}" | tee -a $log_file
    else
        stdbuf -o0 echo "  [ ] ERROR completing task: ${task}" | tee -a $log_file
    fi
    error_count=0
}


# Make sure the last task gets logged
trap begin EXIT


# Log specific commands that return errors
log_failure() {
    this_command="$(history 1 | sed -e "s/^[ ]*[0-9]*[ ]*//g")";
    stdbuf -o0 echo "      ERROR running command: ${this_command}" | tee -a $log_file
    error_count=$((error_count+1))
}
set -o history
trap log_failure ERR


# Send STDERR to log file
exec 2>> $log_file
