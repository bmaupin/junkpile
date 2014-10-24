/*
 * Derived from android.provider.Telephony
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.archive.android;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import android.provider.Telephony.BaseMmsColumns;
import android.text.TextUtils;
import android.util.Patterns;

public class Telephony {

    /**
     * Contains all MMS messages.
     */
    public static final class Mms implements BaseMmsColumns {
        /**
         * Regex pattern for names and email addresses.
         * <ul>
         *     <li><em>mailbox</em> = {@code name-addr}</li>
         *     <li><em>name-addr</em> = {@code [display-name] angle-addr}</li>
         *     <li><em>angle-addr</em> = {@code [CFWS] "<" addr-spec ">" [CFWS]}</li>
         * </ul>
         * @hide
         */
        public static final Pattern NAME_ADDR_EMAIL_PATTERN =
                Pattern.compile("\\s*(\"[^\"]*\"|[^<>\"]+)\\s*<([^<>]+)>\\s*");
    	
        /**
         * Helper method to extract email address from address string.
         * @hide
         */
        public static String extractAddrSpec(String address) {
            Matcher match = NAME_ADDR_EMAIL_PATTERN.matcher(address);
            if (match.matches()) {
                return match.group(2);
            }
            return address;
        }
    	
        /**
         * Is the specified address an email address?
         *
         * @param address the input address to test
         * @return true if address is an email address; false otherwise.
         * @hide
         */
        public static boolean isEmailAddress(String address) {
            if (TextUtils.isEmpty(address)) {
                return false;
            }
            String s = extractAddrSpec(address);
            Matcher match = Patterns.EMAIL_ADDRESS.matcher(s);
            return match.matches();
        }
    }
}
