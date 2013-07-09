<?php 
/*
 * Miscellaneous functions
 */

/**
 * Convert provided variable in Microsoft's horrendous FILETIME format
 * (http://support.microsoft.com/kb/188768) and return as epoch time
 *
 * @param unknown $filetime
 * @return number
 */
function convert_filetime_to_epoch($filetime) {
    return ($filetime / 10000000) - 11644473600;
}

/**
 * Convert provided variable in ASN.1 GeneralizedTime format and return as epoch
 * time.  Compatible with old versions of PHP (less than 5.2) that don't have 
 * the DateTime class.
 *
 * @param unknown $gt
 * @return unknown
 */
function convert_generalizedtime_to_epoch($gt) {
    // if the generalizedtime is in UTC
    if (strcmp(substr($gt, -1), "Z") == 0) {
        if (strcmp(date_default_timezone_get(), "") != 0) {
            $timezone = date_default_timezone_get();
        } else {
            // change your local timezone here as necessary
            $timezone = 'Canada/Eastern';
        }
        date_default_timezone_set('UTC');
        $gt_epoch = strtotime(substr($gt, 0, -3));
        date_default_timezone_set($timezone);
        return $gt_epoch;
    } else {
        return strtotime(intval($gt));
    }
}

?>
