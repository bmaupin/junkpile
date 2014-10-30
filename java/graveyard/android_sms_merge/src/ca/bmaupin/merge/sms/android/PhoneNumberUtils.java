/*
 * Derived from android.telephony.PhoneNumberUtils
 * (tag android-4.4.4_r2.0.1)
 * https://android.googlesource.com/platform/frameworks/base/+/android-4.4.4_r2.0.1/telephony/java/android/telephony/PhoneNumberUtils.java
 */

package ca.bmaupin.merge.sms.android;

public class PhoneNumberUtils {
    /*
     * Special characters
     *
     * (See "What is a phone number?" doc)
     * 'p' --- GSM pause character, same as comma
     * 'n' --- GSM wild character
     * 'w' --- GSM wait character
     */
    public static final char PAUSE = ',';
    public static final char WAIT = ';';
    public static final char WILD = 'N';
	
    /** True if c is ISO-LATIN characters 0-9, *, # , +, WILD, WAIT, PAUSE   */
    public final static boolean
    isNonSeparator(char c) {
        return (c >= '0' && c <= '9') || c == '*' || c == '#' || c == '+'
                || c == WILD || c == WAIT || c == PAUSE;
    }
	
	/**
     * Strips separators from a phone number string.
     * @param phoneNumber phone number to strip.
     * @return phone string stripped of separators.
     */
    public static String stripSeparators(String phoneNumber) {
        if (phoneNumber == null) {
            return null;
        }
        int len = phoneNumber.length();
        StringBuilder ret = new StringBuilder(len);
        for (int i = 0; i < len; i++) {
            char c = phoneNumber.charAt(i);
            // Character.digit() supports ASCII and Unicode digits (fullwidth, Arabic-Indic, etc.)
            int digit = Character.digit(c, 10);
            if (digit != -1) {
                ret.append(digit);
            } else if (isNonSeparator(c)) {
                ret.append(c);
            }
        }
        return ret.toString();
    }
}
