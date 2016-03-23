<?php

$ad_servers = array(
        "dc-1.example.org",
        "dc-2.example.org",
        "dc-3.example.org",
        "dc-4.example.org",
        "dc-5.example.org",
        );

$ad_bind_dn = "";
$ad_bind_password = "";

$ad_base = "dc=example,dc=org";
$ad_users_base = "ou=allusers,dc=example,dc=org";

// domain attributes
$ad_lockoutduration_attr_name = "lockoutDuration";
$ad_maxpwdage_attr_name = "maxPwdAge";

// account attributes
$ad_account_attr_name = "sAMAccountName";
$ad_dn_attr_name = "dn";
$ad_lockouttime_attr_name = "lockoutTime";
$ad_password_attr_name = "unicodePwd";
$ad_pwdlastset_attr_name = "pwdLastSet";
$ad_useraccountcontrol_attr_name = "UserAccountControl";
$ad_whencreated_attr_name = "whenCreated";

$krb5_realm = 'EXAMPLE.ORG';

$krb5_error_auth_failure = "Cannot get ticket (Preauthentication failed)";
$krb5_error_client_not_found = "Cannot get ticket (Client not found in Kerberos database)";
$krb5_error_credentials_revoked = "Cannot get ticket (Clients credentials have been revoked)";
$krb5_error_encryption_type = "Cannot get ticket (KDC has no support for encryption type)";
$krb5_error_password_expired = "Cannot get ticket (Password has expired)";


/**
 * Connects to AD, returning the connection object, or null if connection
 * failed.
 *
 * @return void|unknown
 */
function ad_connect() {
    global $ad_servers;
    global $ad_bind_dn;
    global $ad_bind_password;
    global $debug;
    
    // randomize the order of the AD servers so we're not hitting the same one 
    // every time in lieu of a load balancer
    shuffle($ad_servers);
    
    foreach ($ad_servers as $ad_server) {
        if ($debug) {
            error_log('DEBUG: $ad_server=' . $ad_server);
        }

        // initial connection to AD
        $a = ldap_connect(sprintf("ldaps://%s", $ad_server));
        if (!$a) {
            error_log("ERROR: AD connection failed");
            return;

        // make sure the connection object is valid
        } else {
            // bind to AD
            $result = ldap_bind($a, $ad_bind_dn, $ad_bind_password);

            // if the bind succeeded
            if ($result) {
                // move on
                break;

            // if the bind failed
            } else {
                error_log("ERROR: Error binding to {$ad_server}");
                // if the last AD server fails (otherwise go to the next one)
                if ($ad_server == end(array_values($ad_servers))) {
                    error_log("ERROR: Last AD server bind filed");
                    error_log('ERROR: $ad_bind_dn=' . $ad_bind_dn);
                    error_log('ERROR: $ad_server=' . $ad_server);
                    return;
                }
            }
        }
    }

    return $a;
}

/**
 * Searches AD for one entry provided an AD connection object, base, filter, and
 * list of attributes to search for.  Returns the search data or null if no
 * results are found or more than one entry is found.
 *
 * @param unknown $a
 * @param unknown $base
 * @param unknown $filter
 * @param unknown $attrs
 * @return void|unknown
 */
function ad_search_one($a, $base, $filter, $attrs) {
    global $ad_dn_attr_name;
    global $debug;

    // add the DN attribute to the list of attributes if it's not already there
    if (!in_array($ad_dn_attr_name, $attrs)) {
        $attrs[] = $ad_dn_attr_name;
    }

    // search AD to make sure the account exists
    $result = ldap_search(
            $a,
            $base,
            $filter,
            $attrs);
    // get the entries from the search results
    $data = ldap_get_entries($a, $result);

    // data is a list of entries.  there should only be one entry since we're
    // only searching one person
    if ($data["count"] == 1) {
        if ($debug) {
            error_log("DEBUG: {$ad_dn_attr_name}={$data[0][$ad_dn_attr_name]}");
        }
        return $data;

    } elseif ($data["count"] == 0) {
        error_log("ERROR: Entry not found in AD");
        error_log('ERROR: $data["count"]=' . $data["count"]);
        error_log('ERROR: $data=' . var_export($data, true));
        return;

    } else {
        error_log("ERROR: More than one entry found in AD");
        error_log('ERROR: $data=' . var_export($data, true));
        error_log('ERROR: $data["count"]=' . $data["count"]);
        return;
    }
}

/**
 * Change password in AD.  Requires UID of account, new password, and boolean
 * indicating whether or not this is an admin password reset (ignores password
 * requirements).  Returns message indicating whether password change succeeded 
 * or not and why.
 * 
 * @param unknown $uid
 * @param unknown $newpassword
 * @return void|string
 */
function changepw_ad($uid, $newpassword, $admin = false) {
    // required in case changepw_ad is called more than once
    if (!function_exists('encode_password')) {
        function encode_password($pw) {
            $encodedpass = "";
            $pw = "\"" . $pw . "\"";
            $len = strlen($pw);
            for ($i = 0; $i < $len; $i++) $encodedpass .= "{$pw{$i}}\000";
            return $encodedpass;
        }
    }
    
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_dn_attr_name;
    global $ad_password_attr_name;
    global $ad_pwdlastset_attr_name;

    $a = ad_connect();
    // search AD to make sure the account exists and to get the DN
    $data = ad_search_one(
            $a,
            $ad_users_base,
            sprintf("(%s=%s)", $ad_account_attr_name, $uid),
            array($ad_dn_attr_name, $ad_pwdlastset_attr_name));
    
    // don't enforce password history policy if this is an admin password reset
    if ($admin === false) {
        // this chunk of code tells AD to enforce password history policy
        $ctrl1 = array(
                // LDAP_SERVER_POLICY_HINTS_OID for Windows 2012 and above
                "oid" => "1.2.840.113556.1.4.2239",
                "value" => sprintf("%c%c%c%c%c", 48, 3, 2, 1, 1));
        $ctrl2 = array(
                // LDAP_SERVER_POLICY_HINTS_DEPRECATED_OID for Windows 2008 R2 SP1 and above
                "oid" => "1.2.840.113556.1.4.2066",
                "value" => sprintf("%c%c%c%c%c", 48, 3, 2, 1, 1));
        if (!ldap_set_option($a, LDAP_OPT_SERVER_CONTROLS, array($ctrl1, $ctrl2))) {
            error_log("ERROR: Failed to set server controls");
        }
    }
    
    $dn = $data[0][$ad_dn_attr_name];
    $entry[$ad_password_attr_name] = encode_password($newpassword);
    $result = ldap_mod_replace($a, $dn, $entry);
    
    if ($result == false) {
        error_log("ERROR: Error changing password");
        error_log('ERROR: $uid=' . $uid);
        error_log('ERROR: $dn=' . $dn);
        return;
    }
    
    // if this is an admin reset, set the account to "User must change password at next logon"
    if ($admin === true) {
        $entry[$ad_pwdlastset_attr_name] = 0;
        $result = ldap_mod_replace($a, $dn, $entry);
        
        if ($result == false) {
            error_log("ERROR: Error modifying attribute");
            error_log('ERROR: $uid=' . $uid);
            error_log('ERROR: $dn=' . $dn);
            return;
        }
    }
    
    // close connection to AD
    ldap_unbind($a);

    return "accept";
}

/**
 * If the account exists in AD, returns true.  Otherwise, returns false.
 *
 * @param unknown $uid
 * @return boolean
 */
function does_ad_account_exist($uid) {
    global $ad_users_base;
    global $ad_account_attr_name;

    $a = ad_connect();
    $data = ad_search_one(
            $a,
            $ad_users_base,
            sprintf("(%s=%s)", $ad_account_attr_name, $uid),
            array()
    );

    // close connection to AD
    ldap_unbind($a);

    if ($data === null) {
        return false;
    } else {
        return true;
    }
}

/**
 * Get the timestamp of when the account was created and return it as a 
 * formatted string.
 * 
 * @param unknown $uid
 */
function get_ad_account_creation_date($uid) {
    global $ad_base;
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_whencreated_attr_name;
    
    if (isset($_SESSION["ad_{$ad_whencreated_attr_name}"])) {
        $whencreated_gt = $_SESSION["ad_{$ad_whencreated_attr_name}"];
        
    } else {
        $a = ad_connect();
        $data = ad_search_one(
                $a,
                $ad_users_base,
                sprintf("(%s=%s)", $ad_account_attr_name, $uid),
                array($ad_whencreated_attr_name));
        $whencreated_gt = $data[0][strtolower($ad_whencreated_attr_name)][0];
        // close connection to AD
        ldap_unbind($a);
    }
    
    $whencreated_epoch = convert_generalizedtime_to_epoch($whencreated_gt);
    return date('Y-m-d H:i:s', $whencreated_epoch);
}

/**
 * Get the account status of the provided uid.  Returns an array of account 
 * statuses (Enabled/Disabled, Unlocked/Locked).
 * 
 * @param unknown $uid
 * @return multitype:string
 */
function get_ad_account_status($uid) {
    $account_status = array();
    
    $account_status[] = "Created on " . get_ad_account_creation_date($uid);
    
    if (is_ad_account_disabled($uid)) {
        $account_status[] = "<span style=\"color: red;\">Disabled</span>";
    } else {
        $account_status[] = "Enabled";
    }
    
    $result = is_ad_account_locked($uid);
    
    if ($result) {
        $account_status[] = "<span style=\"color: red;\">{$result}</span>";
    } else {
        $account_status[] = "Unlocked";
    }
    
    return $account_status;
}

function get_ad_account_password_status($uid) {
    global $ad_base;
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_maxpwdage_attr_name;
    global $ad_pwdlastset_attr_name;
    global $ad_useraccountcontrol_attr_name;
    
    $password_status = array();
    
    if (isset($_SESSION["ad_{$ad_pwdlastset_attr_name}"]) && 
            isset($_SESSION["ad_{$ad_useraccountcontrol_attr_name}"])) {
        $pwdlastset = $_SESSION["ad_{$ad_pwdlastset_attr_name}"];
        $uac = $_SESSION["ad_{$ad_useraccountcontrol_attr_name}"];
    
    } else {
        $a = ad_connect();
        $data = ad_search_one(
                $a,
                $ad_users_base,
                sprintf("(%s=%s)", $ad_account_attr_name, $uid),
                array($ad_pwdlastset_attr_name,
                        $ad_useraccountcontrol_attr_name));
        $pwdlastset = $data[0][strtolower($ad_pwdlastset_attr_name)][0];
        $uac = $data[0][strtolower($ad_useraccountcontrol_attr_name)][0];
        // close connection to AD
        ldap_unbind($a);
    }
    
    // http://support.microsoft.com/kb/305144
    if (($uac & 65536) == 65536) {
        $password_status[] = "Password never expires";
    } elseif ($pwdlastset == '0') {
        $password_status[] = "<span style=\"color: red;\">User must change password at next logon</span>";
    } else {
        if (isset($_SESSION["ad_{$ad_maxpwdage_attr_name}"])) {
            $maxpwdage = $_SESSION["ad_{$ad_maxpwdage_attr_name}"];
        
        } else {
            // get maxpwdage
            $a = ad_connect();
            $result = ldap_read(
                    $a,
                    $ad_base,
                    '(objectClass=*)',
                    array($ad_maxpwdage_attr_name));
            $data = ldap_get_entries($a, $result);
            $maxpwdage = $data[0][strtolower($ad_maxpwdage_attr_name)][0];
            // close connection to AD
            ldap_unbind($a);
        }
        
        if (function_exists('bcmod') && bcmod($maxpwdage, 4294967296) === '0') {
            $password_status[] = "Domain does not expire passwords";
            
        } else {
            // value is in Microsoft's terrible FileTime format
            $pwdexpire_ft = $pwdlastset - $maxpwdage;
            
            $pwdexpire_epoch = convert_filetime_to_epoch($pwdexpire_ft);
            
            if ($pwdexpire_epoch > time()) {
                $password_status[] = "Password expires on " . date('Y-m-d H:i:s', $pwdexpire_epoch);
            } else {
                $password_status[] = "<span style=\"color: red;\">Password expired on " . date('Y-m-d H:i:s', $pwdexpire_epoch) . "</span>";
            }
            
            $pwdlastset_epoch = convert_filetime_to_epoch($pwdlastset);
            $password_status[] = "Password last set on " . date('Y-m-d H:i:s', $pwdlastset_epoch);
        }
    }
    
    // http://support.microsoft.com/kb/305144
    // this doesn't seem to be reliable, but we'll leave it for now
    if (($uac & 64) == 64) {
        $password_status[] = "<span style=\"color: red;\">User cannot change password</span>";
    }
    // http://support.microsoft.com/kb/305144
    // apparently this bit is meaningless since new accounts have it by default
    // http://www.systemtools.com/toolboard/showthread.php?718-Question-about-useraccountcontrol-flags-specifically-PASSWD_NOTREQD
    /*
    if (($uac & 32) == 32) {
        $password_status[] = "<span style=\"color: red;\">No password is required</span>";
    }
    */
    
    return $password_status;
}

/**
 * Determine whether the provided account is disabled in AD or not, and return
 * true if it is disabled, false if it is enabled
 * 
 * @param unknown $uid
 * @return boolean
 */
function is_ad_account_disabled($uid) {
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_useraccountcontrol_attr_name;
    
    if (isset($_SESSION["ad_{$ad_useraccountcontrol_attr_name}"])) {
        $uac = $_SESSION["ad_{$ad_useraccountcontrol_attr_name}"];
    
    } else {
        $a = ad_connect();
        $data = ad_search_one(
                $a,
                $ad_users_base,
                sprintf("(%s=%s)", $ad_account_attr_name, $uid),
                array($ad_useraccountcontrol_attr_name));
        $uac = $data[0][strtolower($ad_useraccountcontrol_attr_name)][0];
        // close connection to AD
        ldap_unbind($a);
    }
    
    // the account is disabled
    // http://support.microsoft.com/kb/305144
    if (($uac & 2) == 2) {
        return true;
    } else {
        return false;
    }
}

/**
 * Determine whether the provided account is locked in AD or not, and return
 * false if it is unlocked, or if it is locked a message indicating when it will
 * unlock.
 *
 * @param unknown $uid
 * @return boolean
 */
function is_ad_account_locked($uid) {
    global $ad_base;
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_lockoutduration_attr_name;
    global $ad_lockouttime_attr_name;
    
    if (isset($_SESSION["ad_{$ad_lockouttime_attr_name}"])) {
        $lockouttime = $_SESSION["ad_{$ad_lockouttime_attr_name}"];
    
    } else {
        $a = ad_connect();
        $data = ad_search_one(
                $a,
                $ad_users_base,
                sprintf("(%s=%s)", $ad_account_attr_name, $uid),
                array($ad_lockouttime_attr_name));
        // close connection to AD
        ldap_unbind($a);
        
        if (in_array(strtolower($ad_lockouttime_attr_name), $data[0], true)) {
            $lockouttime = $data[0][strtolower($ad_lockouttime_attr_name)][0];
        } else {
            return false;
        }
    }
    
    // if account's never been locked, our job's easy
    if ($lockouttime == 0) {
        return false;
    }
    
    if (isset($_SESSION["ad_{$ad_lockoutduration_attr_name}"])) {
        $lockoutduration = $_SESSION["ad_{$ad_lockoutduration_attr_name}"];
    
    } else {
        // get lockoutDuration from the domain
        $a = ad_connect();
        $result = ldap_read(
                $a,
                $ad_base,
                '(objectClass=*)',
                array($ad_lockoutduration_attr_name));
        $data = ldap_get_entries($a, $result);
        $lockoutduration = $data[0][strtolower($ad_lockoutduration_attr_name)][0];
        
        // close connection to AD
        ldap_unbind($a);
    }
    
    $unlocktime_ft = $lockouttime - $lockoutduration;
    $unlocktime_epoch = convert_filetime_to_epoch($unlocktime_ft);
    
    // if unlock time is in the future
    if ($unlocktime_epoch > time()) {
        // account is locked
        return "Locked until " . date('Y-m-d H:i:s', $unlocktime_epoch);
    } else {
        // otherwise it's unlocked
        return false;
    }
}

/**
 * Determine whether the password for the provided account in AD is expired or
 * not, and return true if it is expired, false if it is not expired
 *
 * @param unknown $uid
 * @return boolean
 */
function is_ad_account_password_expired($uid) {
    global $ad_base;
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_maxpwdage_attr_name;
    global $ad_pwdlastset_attr_name;
    global $ad_useraccountcontrol_attr_name;
    
    if (isset($_SESSION["ad_{$ad_pwdlastset_attr_name}"]) && 
            isset($_SESSION["ad_{$ad_useraccountcontrol_attr_name}"])) {
        $pwdlastset = $_SESSION["ad_{$ad_pwdlastset_attr_name}"];
        $uac = $_SESSION["ad_{$ad_useraccountcontrol_attr_name}"];
    
    } else {
        $a = ad_connect();
        $data = ad_search_one(
                $a,
                $ad_users_base,
                sprintf("(%s=%s)", $ad_account_attr_name, $uid),
                array($ad_pwdlastset_attr_name,
                        $ad_useraccountcontrol_attr_name));
        $pwdlastset = $data[0][strtolower($ad_pwdlastset_attr_name)][0];
        $uac = $data[0][strtolower($ad_useraccountcontrol_attr_name)][0];
        // close connection to AD
        ldap_unbind($a);
    }
    
    // account set to password never expires
    // http://support.microsoft.com/kb/305144
    if (($uac & 65536) == 65536) {
        // close connection to AD
        ldap_unbind($a);
        return false;
        
    } else {
        if (isset($_SESSION["ad_{$ad_maxpwdage_attr_name}"])) {
            $maxpwdage = $_SESSION["ad_{$ad_maxpwdage_attr_name}"];
        
        } else {
            // get maxpwdage from the domain
            $a = ad_connect();
            $result = ldap_read(
                    $a,
                    $ad_base,
                    '(objectClass=*)',
                    array($ad_maxpwdage_attr_name));
            $data = ldap_get_entries($a, $result);
            $maxpwdage = $data[0][strtolower($ad_maxpwdage_attr_name)][0];
            // close connection to AD
            ldap_unbind($a);
        }
        
        // domain does not expire passwords
        if (function_exists('bcmod') && bcmod($maxpwdage, 4294967296) === '0') {
            return false;
        
        } else {
            // value is in Microsoft's terrible FILETIME format
            $pwdexpire_ft = $pwdlastset - $maxpwdage;
            $pwdexpire_epoch = convert_filetime_to_epoch($pwdexpire_ft);
            
            // if password expires in the future
            if ($pwdexpire_epoch > time()) {
                // it's not expired
                return false;
            } else {
                // otherwise it's expired
                return true;
            }
        }
    }
}

/**
 * Determine whether the "User must change password at next logon" flag on the 
 * provided account in AD is set or not, and return true if it is set and false
 * if it isn't
 *
 * @param unknown $uid
 * @return boolean
 */
function is_ad_must_change_password_set($uid) {
    global $ad_base;
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_pwdlastset_attr_name;
    
    if (isset($_SESSION["ad_{$ad_pwdlastset_attr_name}"])) {
        $pwdlastset = $_SESSION["ad_{$ad_pwdlastset_attr_name}"];
    
    } else {
        $a = ad_connect();
        $data = ad_search_one(
                $a,
                $ad_users_base,
                sprintf("(%s=%s)", $ad_account_attr_name, $uid),
                array($ad_pwdlastset_attr_name));
        $pwdlastset = $data[0][strtolower($ad_pwdlastset_attr_name)][0];
        // close connection to AD
        ldap_unbind($a);
    }
    
    // if pwdLastSet is 0, the user must change their password at next logon
    // http://technet.microsoft.com/en-us/library/ee198797.aspx
    if ($pwdlastset == '0') {
        return true;
    } else {
        return false;
    }
}

/**
 * Function for authenticating to the provided kerberos realm with the provided
 * principal and password.  Retries on encryption type error, since this seems 
 * to be randomly thrown by AD.  Returns true on successful auth, error message
 * otherwise.
 * 
 * @param unknown $realm
 * @param unknown $principal
 * @param unknown $password
 * @return boolean
 */
function krb5_init($principal, $password, $realm = null) {
    global $debug;
    global $krb5_realm;
    global $krb5_error_encryption_type;
    
    // set the realm if none provided
    if ($realm === null) {
        $realm = $krb5_realm;
    }
    
    $ccache = new KRB5CCache();
    
    while (true) {
        try {
            $ccache->initPassword($principal . "@" . $realm, $password);
            // auth succeeded
            return true;
        } catch (Exception $e) {
            if (strcmp($e->getMessage(), $krb5_error_encryption_type) == 0) {
                if ($debug) {
                    error_log('DEBUG: '. $e->getMessage());
                    error_log('DEBUG: $principal=' . $principal);
                    error_log('DEBUG: $realm=' . $realm);
                }
                // retry auth if we get encryption type error, randomly thrown by AD
                continue;
            } else {
                if ($debug) {
                    error_log('DEBUG: '. $e->getMessage());
                    error_log('DEBUG: $principal=' . $principal);
                    error_log('DEBUG: $realm=' . $realm);
                }
                // for all other errors, auth failed
                return $e->getMessage();
            }
        }
    }
}

/**
 * Retrieve attributes from AD for a given user and set them as session 
 * variables.  Return true on success, false if the user doesn't exist in AD. 
 * 
 * @return boolean
 */
function set_ad_session_attributes() {
    global $ad_base;
    global $ad_users_base;
    global $ad_account_attr_name;
    global $ad_lockoutduration_attr_name;
    global $ad_lockouttime_attr_name;
    global $ad_maxpwdage_attr_name;
    global $ad_pwdlastset_attr_name;
    global $ad_useraccountcontrol_attr_name;
    global $ad_whencreated_attr_name;

    $a = ad_connect();
    $data = ad_search_one(
            $a,
            $ad_users_base,
            sprintf("(%s=%s)", $ad_account_attr_name, $_SESSION['netid']),
            array(
                    $ad_lockouttime_attr_name,
                    $ad_pwdlastset_attr_name,
                    $ad_useraccountcontrol_attr_name,
                    $ad_whencreated_attr_name,
            )
    );

    // if the user wasn't found in AD
    if ($data === null) {
        // close connection to AD
        ldap_unbind($a);
        return false;
    }

    // otherwise, set user session attributes
    if (in_array(strtolower($ad_lockouttime_attr_name), $data[0], true)) {
        $_SESSION["ad_{$ad_lockouttime_attr_name}"] = $data[0][strtolower($ad_lockouttime_attr_name)][0];
    }
    $_SESSION["ad_{$ad_pwdlastset_attr_name}"] = $data[0][strtolower($ad_pwdlastset_attr_name)][0];
    $_SESSION["ad_{$ad_useraccountcontrol_attr_name}"] = $data[0][strtolower($ad_useraccountcontrol_attr_name)][0];
    $_SESSION["ad_{$ad_whencreated_attr_name}"] = $data[0][strtolower($ad_whencreated_attr_name)][0];
    
    // set AD domain session attributes
    $result = ldap_read(
            $a,
            $ad_base,
            '(objectClass=*)',
            array(
                    $ad_lockoutduration_attr_name,
                    $ad_maxpwdage_attr_name,
                    )
            );
    $data = ldap_get_entries($a, $result);
    $_SESSION["ad_{$ad_lockoutduration_attr_name}"] = $data[0][strtolower($ad_lockoutduration_attr_name)][0];
    $_SESSION["ad_{$ad_maxpwdage_attr_name}"] = $data[0][strtolower($ad_maxpwdage_attr_name)][0];

    // close connection to AD
    ldap_unbind($a);
    return true;
}

/**
 * Unset session attributes retrieved from AD
 */
function unset_ad_session_attributes() {
    global $ad_lockoutduration_attr_name;
    global $ad_lockouttime_attr_name;
    global $ad_maxpwdage_attr_name;
    global $ad_pwdlastset_attr_name;
    global $ad_useraccountcontrol_attr_name;
    global $ad_whencreated_attr_name;

    unset($_SESSION["ad_{$ad_lockoutduration_attr_name}"]);
    unset($_SESSION["ad_{$ad_lockouttime_attr_name}"]);
    unset($_SESSION["ad_{$ad_maxpwdage_attr_name}"]);
    unset($_SESSION["ad_{$ad_pwdlastset_attr_name}"]);
    unset($_SESSION["ad_{$ad_useraccountcontrol_attr_name}"]);
    unset($_SESSION["ad_{$ad_whencreated_attr_name}"]);
}

?>