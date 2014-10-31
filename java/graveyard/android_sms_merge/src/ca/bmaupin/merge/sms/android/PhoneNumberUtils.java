/*
 * Derived from android.telephony.PhoneNumberUtils
 * (tag android-4.4.4_r2.0.1)
 * https://android.googlesource.com/platform/frameworks/base/+/android-4.4.4_r2.0.1/telephony/java/android/telephony/PhoneNumberUtils.java
 */

package ca.bmaupin.merge.sms.android;

import android.text.TextUtils;
import android.util.SparseIntArray;

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
    /*
     * Calling Line Identification Restriction (CLIR)
     */
    private static final String CLIR_ON = "*31#";
    private static final String CLIR_OFF = "#31#";
	
    /** True if c is ISO-LATIN characters 0-9, *, # , +, WILD  */
    public final static boolean
    isDialable(char c) {
        return (c >= '0' && c <= '9') || c == '*' || c == '#' || c == '+' || c == WILD;
    }
    
    /** True if c is ISO-LATIN characters 0-9, *, # , +, WILD, WAIT, PAUSE   */
    public final static boolean
    isNonSeparator(char c) {
        return (c >= '0' && c <= '9') || c == '*' || c == '#' || c == '+'
                || c == WILD || c == WAIT || c == PAUSE;
    }
    
    /** This any anything to the right of this char is part of the
     *  post-dial string (eg this is PAUSE or WAIT)
     */
    public final static boolean
    isStartsPostDial (char c) {
        return c == PAUSE || c == WAIT;
    }
    
    
    /** Extracts the network address portion and canonicalizes
     *  (filters out separators.)
     *  Network address portion is everything up to DTMF control digit
     *  separators (pause or wait), but without non-dialable characters.
     *
     *  Please note that the GSM wild character is allowed in the result.
     *  This must be resolved before dialing.
     *
     *  Returns null if phoneNumber == null
     */
    public static String
    extractNetworkPortion(String phoneNumber) {
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
            } else if (c == '+') {
                // Allow '+' as first character or after CLIR MMI prefix
                String prefix = ret.toString();
                if (prefix.length() == 0 || prefix.equals(CLIR_ON) || prefix.equals(CLIR_OFF)) {
                    ret.append(c);
                }
            } else if (isDialable(c)) {
                ret.append(c);
            } else if (isStartsPostDial (c)) {
                break;
            }
        }
        return ret.toString();
    }
    
    /**
     * Extracts the network address portion and canonicalize.
     *
     * This function is equivalent to extractNetworkPortion(), except
     * for allowing the PLUS character to occur at arbitrary positions
     * in the address portion, not just the first position.
     *
     * @hide
     */
    public static String extractNetworkPortionAlt(String phoneNumber) {
        if (phoneNumber == null) {
            return null;
        }

        int len = phoneNumber.length();
        StringBuilder ret = new StringBuilder(len);
        boolean haveSeenPlus = false;

        for (int i = 0; i < len; i++) {
            char c = phoneNumber.charAt(i);
            if (c == '+') {
                if (haveSeenPlus) {
                    continue;
                }
                haveSeenPlus = true;
            }
            if (isDialable(c)) {
                ret.append(c);
            } else if (isStartsPostDial (c)) {
                break;
            }
        }

        return ret.toString();
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
    
    /** or -1 if both are negative */
    static private int
    minPositive (int a, int b) {
        if (a >= 0 && b >= 0) {
            return (a < b) ? a : b;
        } else if (a >= 0) { /* && b < 0 */
            return a;
        } else if (b >= 0) { /* && a < 0 */
            return b;
        } else { /* a < 0 && b < 0 */
            return -1;
        }
    }
    
    /** index of the last character of the network portion
     *  (eg anything after is a post-dial string)
     */
    static private int
    indexOfLastNetworkChar(String a) {
        int pIndex, wIndex;
        int origLength;
        int trimIndex;

        origLength = a.length();

        pIndex = a.indexOf(PAUSE);
        wIndex = a.indexOf(WAIT);

        trimIndex = minPositive(pIndex, wIndex);

        if (trimIndex < 0) {
            return origLength - 1;
        } else {
            return trimIndex - 1;
        }
    }
    
    /**
     * Compare phone numbers a and b, return true if they're identical enough for caller ID purposes.
     */
    public static boolean compare(String a, String b) {
        // We've used loose comparation at least Eclair, which may change in the future.

        return compare(a, b, false);
    }
    
    /**
     * @hide only for testing.
     */
    public static boolean compare(String a, String b, boolean useStrictComparation) {
        return (useStrictComparation ? compareStrictly(a, b) : compareLoosely(a, b));
    }
    
    /**
     * Compare phone numbers a and b, return true if they're identical
     * enough for caller ID purposes.
     *
     * - Compares from right to left
     * - requires MIN_MATCH (7) characters to match
     * - handles common trunk prefixes and international prefixes
     *   (basically, everything except the Russian trunk prefix)
     *
     * Note that this method does not return false even when the two phone numbers
     * are not exactly same; rather; we can call this method "similar()", not "equals()".
     *
     * @hide
     */
    public static boolean
    compareLoosely(String a, String b) {
        int ia, ib;
        int matched;
        int numNonDialableCharsInA = 0;
        int numNonDialableCharsInB = 0;

        if (a == null || b == null) return a == b;

        if (a.length() == 0 || b.length() == 0) {
            return false;
        }

        ia = indexOfLastNetworkChar (a);
        ib = indexOfLastNetworkChar (b);
        matched = 0;

        while (ia >= 0 && ib >=0) {
            char ca, cb;
            boolean skipCmp = false;

            ca = a.charAt(ia);

            if (!isDialable(ca)) {
                ia--;
                skipCmp = true;
                numNonDialableCharsInA++;
            }

            cb = b.charAt(ib);

            if (!isDialable(cb)) {
                ib--;
                skipCmp = true;
                numNonDialableCharsInB++;
            }

            if (!skipCmp) {
                if (cb != ca && ca != WILD && cb != WILD) {
                    break;
                }
                ia--; ib--; matched++;
            }
        }

        if (matched < MIN_MATCH) {
            int effectiveALen = a.length() - numNonDialableCharsInA;
            int effectiveBLen = b.length() - numNonDialableCharsInB;


            // if the number of dialable chars in a and b match, but the matched chars < MIN_MATCH,
            // treat them as equal (i.e. 404-04 and 40404)
            if (effectiveALen == effectiveBLen && effectiveALen == matched) {
                return true;
            }

            return false;
        }

        // At least one string has matched completely;
        if (matched >= MIN_MATCH && (ia < 0 || ib < 0)) {
            return true;
        }

        /*
         * Now, what remains must be one of the following for a
         * match:
         *
         *  - a '+' on one and a '00' or a '011' on the other
         *  - a '0' on one and a (+,00)<country code> on the other
         *     (for this, a '0' and a '00' prefix would have succeeded above)
         */

        if (matchIntlPrefix(a, ia + 1)
            && matchIntlPrefix (b, ib +1)
        ) {
            return true;
        }

        if (matchTrunkPrefix(a, ia + 1)
            && matchIntlPrefixAndCC(b, ib +1)
        ) {
            return true;
        }

        if (matchTrunkPrefix(b, ib + 1)
            && matchIntlPrefixAndCC(a, ia +1)
        ) {
            return true;
        }

        return false;
    }

    /**
     * @hide
     */
    public static boolean
    compareStrictly(String a, String b) {
        return compareStrictly(a, b, true);
    }

    /**
     * @hide
     */
    public static boolean
    compareStrictly(String a, String b, boolean acceptInvalidCCCPrefix) {
        if (a == null || b == null) {
            return a == b;
        } else if (a.length() == 0 && b.length() == 0) {
            return false;
        }

        int forwardIndexA = 0;
        int forwardIndexB = 0;

        CountryCallingCodeAndNewIndex cccA =
            tryGetCountryCallingCodeAndNewIndex(a, acceptInvalidCCCPrefix);
        CountryCallingCodeAndNewIndex cccB =
            tryGetCountryCallingCodeAndNewIndex(b, acceptInvalidCCCPrefix);
        boolean bothHasCountryCallingCode = false;
        boolean okToIgnorePrefix = true;
        boolean trunkPrefixIsOmittedA = false;
        boolean trunkPrefixIsOmittedB = false;
        if (cccA != null && cccB != null) {
            if (cccA.countryCallingCode != cccB.countryCallingCode) {
                // Different Country Calling Code. Must be different phone number.
                return false;
            }
            // When both have ccc, do not ignore trunk prefix. Without this,
            // "+81123123" becomes same as "+810123123" (+81 == Japan)
            okToIgnorePrefix = false;
            bothHasCountryCallingCode = true;
            forwardIndexA = cccA.newIndex;
            forwardIndexB = cccB.newIndex;
        } else if (cccA == null && cccB == null) {
            // When both do not have ccc, do not ignore trunk prefix. Without this,
            // "123123" becomes same as "0123123"
            okToIgnorePrefix = false;
        } else {
            if (cccA != null) {
                forwardIndexA = cccA.newIndex;
            } else {
                int tmp = tryGetTrunkPrefixOmittedIndex(b, 0);
                if (tmp >= 0) {
                    forwardIndexA = tmp;
                    trunkPrefixIsOmittedA = true;
                }
            }
            if (cccB != null) {
                forwardIndexB = cccB.newIndex;
            } else {
                int tmp = tryGetTrunkPrefixOmittedIndex(b, 0);
                if (tmp >= 0) {
                    forwardIndexB = tmp;
                    trunkPrefixIsOmittedB = true;
                }
            }
        }

        int backwardIndexA = a.length() - 1;
        int backwardIndexB = b.length() - 1;
        while (backwardIndexA >= forwardIndexA && backwardIndexB >= forwardIndexB) {
            boolean skip_compare = false;
            final char chA = a.charAt(backwardIndexA);
            final char chB = b.charAt(backwardIndexB);
            if (isSeparator(chA)) {
                backwardIndexA--;
                skip_compare = true;
            }
            if (isSeparator(chB)) {
                backwardIndexB--;
                skip_compare = true;
            }

            if (!skip_compare) {
                if (chA != chB) {
                    return false;
                }
                backwardIndexA--;
                backwardIndexB--;
            }
        }

        if (okToIgnorePrefix) {
            if ((trunkPrefixIsOmittedA && forwardIndexA <= backwardIndexA) ||
                !checkPrefixIsIgnorable(a, forwardIndexA, backwardIndexA)) {
                if (acceptInvalidCCCPrefix) {
                    // Maybe the code handling the special case for Thailand makes the
                    // result garbled, so disable the code and try again.
                    // e.g. "16610001234" must equal to "6610001234", but with
                    //      Thailand-case handling code, they become equal to each other.
                    //
                    // Note: we select simplicity rather than adding some complicated
                    //       logic here for performance(like "checking whether remaining
                    //       numbers are just 66 or not"), assuming inputs are small
                    //       enough.
                    return compare(a, b, false);
                } else {
                    return false;
                }
            }
            if ((trunkPrefixIsOmittedB && forwardIndexB <= backwardIndexB) ||
                !checkPrefixIsIgnorable(b, forwardIndexA, backwardIndexB)) {
                if (acceptInvalidCCCPrefix) {
                    return compare(a, b, false);
                } else {
                    return false;
                }
            }
        } else {
            // In the US, 1-650-555-1234 must be equal to 650-555-1234,
            // while 090-1234-1234 must not be equal to 90-1234-1234 in Japan.
            // This request exists just in US (with 1 trunk (NDD) prefix).
            // In addition, "011 11 7005554141" must not equal to "+17005554141",
            // while "011 1 7005554141" must equal to "+17005554141"
            //
            // In this comparison, we ignore the prefix '1' just once, when
            // - at least either does not have CCC, or
            // - the remaining non-separator number is 1
            boolean maybeNamp = !bothHasCountryCallingCode;
            while (backwardIndexA >= forwardIndexA) {
                final char chA = a.charAt(backwardIndexA);
                if (isDialable(chA)) {
                    if (maybeNamp && tryGetISODigit(chA) == 1) {
                        maybeNamp = false;
                    } else {
                        return false;
                    }
                }
                backwardIndexA--;
            }
            while (backwardIndexB >= forwardIndexB) {
                final char chB = b.charAt(backwardIndexB);
                if (isDialable(chB)) {
                    if (maybeNamp && tryGetISODigit(chB) == 1) {
                        maybeNamp = false;
                    } else {
                        return false;
                    }
                }
                backwardIndexB--;
            }
        }

        return true;
    }
    
    /**
     * Returns the rightmost MIN_MATCH (5) characters in the network portion
     * in *reversed* order
     *
     * This can be used to do a database lookup against the column
     * that stores getStrippedReversed()
     *
     * Returns null if phoneNumber == null
     */
    public static String
    toCallerIDMinMatch(String phoneNumber) {
        String np = extractNetworkPortionAlt(phoneNumber);
        return internalGetStrippedReversed(np, MIN_MATCH);
    }
    
    /**
     * Returns the last numDigits of the reversed phone number
     * Returns null if np == null
     */
    private static String
    internalGetStrippedReversed(String np, int numDigits) {
        if (np == null) return null;

        StringBuilder ret = new StringBuilder(numDigits);
        int length = np.length();

        for (int i = length - 1, s = length
            ; i >= 0 && (s - i) <= numDigits ; i--
        ) {
            char c = np.charAt(i);

            ret.append(c);
        }

        return ret.toString();
    }
    
    /**
     * Return true iff the network portion of <code>address</code> is,
     * as far as we can tell on the device, suitable for use as an SMS
     * destination address.
     */
    public static boolean isWellFormedSmsAddress(String address) {
        String networkPortion =
                PhoneNumberUtils.extractNetworkPortion(address);
        return (!(networkPortion.equals("+")
                  || TextUtils.isEmpty(networkPortion)))
               && isDialable(networkPortion);
    }
    
    private static boolean isDialable(String address) {
        for (int i = 0, count = address.length(); i < count; i++) {
            if (!isDialable(address.charAt(i))) {
                return false;
            }
        }
        return true;
    }
    
    /**
     * Normalize a phone number by removing the characters other than digits. If
     * the given number has keypad letters, the letters will be converted to
     * digits first.
     *
     * @param phoneNumber
     *            the number to be normalized.
     * @return the normalized number.
     *
     * @hide
     */
    public static String normalizeNumber(String phoneNumber) {
        StringBuilder sb = new StringBuilder();
        int len = phoneNumber.length();
        for (int i = 0; i < len; i++) {
            char c = phoneNumber.charAt(i);
            // Character.digit() supports ASCII and Unicode digits (fullwidth, Arabic-Indic, etc.)
            int digit = Character.digit(c, 10);
            if (digit != -1) {
                sb.append(digit);
            } else if (i == 0 && c == '+') {
                sb.append(c);
            } else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z')) {
                return normalizeNumber(PhoneNumberUtils.convertKeypadLettersToDigits(phoneNumber));
            }
        }
        return sb.toString();
    }
    
    // Three and four digit phone numbers for either special services,
    // or 3-6 digit addresses from the network (eg carrier-originated SMS messages) should
    // not match.
    //
    // This constant used to be 5, but SMS short codes has increased in length and
    // can be easily 6 digits now days. Most countries have SMS short code length between
    // 3 to 6 digits. The exceptions are
    //
    // Australia: Short codes are six or eight digits in length, starting with the prefix "19"
    //            followed by an additional four or six digits and two.
    // Czech Republic: Codes are seven digits in length for MO and five (not billed) or
    //            eight (billed) for MT direction
    //
    // see http://en.wikipedia.org/wiki/Short_code#Regional_differences for reference
    //
    // However, in order to loose match 650-555-1212 and 555-1212, we need to set the min match
    // to 7.
    static final int MIN_MATCH = 7;
    
    /**
     * Translates any alphabetic letters (i.e. [A-Za-z]) in the
     * specified phone number into the equivalent numeric digits,
     * according to the phone keypad letter mapping described in
     * ITU E.161 and ISO/IEC 9995-8.
     *
     * @return the input string, with alpha letters converted to numeric
     *         digits using the phone keypad letter mapping.  For example,
     *         an input of "1-800-GOOG-411" will return "1-800-4664-411".
     */
    public static String convertKeypadLettersToDigits(String input) {
        if (input == null) {
            return input;
        }
        int len = input.length();
        if (len == 0) {
            return input;
        }

        char[] out = input.toCharArray();

        for (int i = 0; i < len; i++) {
            char c = out[i];
            // If this char isn't in KEYPAD_MAP at all, just leave it alone.
            out[i] = (char) KEYPAD_MAP.get(c, c);
        }

        return new String(out);
    }
    
    /**
     * The phone keypad letter mapping (see ITU E.161 or ISO/IEC 9995-8.)
     * TODO: This should come from a resource.
     */
    private static final SparseIntArray KEYPAD_MAP = new SparseIntArray();
    static {
        KEYPAD_MAP.put('a', '2'); KEYPAD_MAP.put('b', '2'); KEYPAD_MAP.put('c', '2');
        KEYPAD_MAP.put('A', '2'); KEYPAD_MAP.put('B', '2'); KEYPAD_MAP.put('C', '2');

        KEYPAD_MAP.put('d', '3'); KEYPAD_MAP.put('e', '3'); KEYPAD_MAP.put('f', '3');
        KEYPAD_MAP.put('D', '3'); KEYPAD_MAP.put('E', '3'); KEYPAD_MAP.put('F', '3');

        KEYPAD_MAP.put('g', '4'); KEYPAD_MAP.put('h', '4'); KEYPAD_MAP.put('i', '4');
        KEYPAD_MAP.put('G', '4'); KEYPAD_MAP.put('H', '4'); KEYPAD_MAP.put('I', '4');

        KEYPAD_MAP.put('j', '5'); KEYPAD_MAP.put('k', '5'); KEYPAD_MAP.put('l', '5');
        KEYPAD_MAP.put('J', '5'); KEYPAD_MAP.put('K', '5'); KEYPAD_MAP.put('L', '5');

        KEYPAD_MAP.put('m', '6'); KEYPAD_MAP.put('n', '6'); KEYPAD_MAP.put('o', '6');
        KEYPAD_MAP.put('M', '6'); KEYPAD_MAP.put('N', '6'); KEYPAD_MAP.put('O', '6');

        KEYPAD_MAP.put('p', '7'); KEYPAD_MAP.put('q', '7'); KEYPAD_MAP.put('r', '7'); KEYPAD_MAP.put('s', '7');
        KEYPAD_MAP.put('P', '7'); KEYPAD_MAP.put('Q', '7'); KEYPAD_MAP.put('R', '7'); KEYPAD_MAP.put('S', '7');

        KEYPAD_MAP.put('t', '8'); KEYPAD_MAP.put('u', '8'); KEYPAD_MAP.put('v', '8');
        KEYPAD_MAP.put('T', '8'); KEYPAD_MAP.put('U', '8'); KEYPAD_MAP.put('V', '8');

        KEYPAD_MAP.put('w', '9'); KEYPAD_MAP.put('x', '9'); KEYPAD_MAP.put('y', '9'); KEYPAD_MAP.put('z', '9');
        KEYPAD_MAP.put('W', '9'); KEYPAD_MAP.put('X', '9'); KEYPAD_MAP.put('Y', '9'); KEYPAD_MAP.put('Z', '9');
    }
    
    //===== Beginning of utility methods used in compareLoosely() =====

    /**
     * Phone numbers are stored in "lookup" form in the database
     * as reversed strings to allow for caller ID lookup
     *
     * This method takes a phone number and makes a valid SQL "LIKE"
     * string that will match the lookup form
     *
     */
    /** all of a up to len must be an international prefix or
     *  separators/non-dialing digits
     */
    private static boolean
    matchIntlPrefix(String a, int len) {
        /* '([^0-9*#+pwn]\+[^0-9*#+pwn] | [^0-9*#+pwn]0(0|11)[^0-9*#+pwn] )$' */
        /*        0       1                           2 3 45               */

        int state = 0;
        for (int i = 0 ; i < len ; i++) {
            char c = a.charAt(i);

            switch (state) {
                case 0:
                    if      (c == '+') state = 1;
                    else if (c == '0') state = 2;
                    else if (isNonSeparator(c)) return false;
                break;

                case 2:
                    if      (c == '0') state = 3;
                    else if (c == '1') state = 4;
                    else if (isNonSeparator(c)) return false;
                break;

                case 4:
                    if      (c == '1') state = 5;
                    else if (isNonSeparator(c)) return false;
                break;

                default:
                    if (isNonSeparator(c)) return false;
                break;

            }
        }

        return state == 1 || state == 3 || state == 5;
    }

    /** all of 'a' up to len must be a (+|00|011)country code)
     *  We're fast and loose with the country code. Any \d{1,3} matches */
    private static boolean
    matchIntlPrefixAndCC(String a, int len) {
        /*  [^0-9*#+pwn]*(\+|0(0|11)\d\d?\d? [^0-9*#+pwn] $ */
        /*      0          1 2 3 45  6 7  8                 */

        int state = 0;
        for (int i = 0 ; i < len ; i++ ) {
            char c = a.charAt(i);

            switch (state) {
                case 0:
                    if      (c == '+') state = 1;
                    else if (c == '0') state = 2;
                    else if (isNonSeparator(c)) return false;
                break;

                case 2:
                    if      (c == '0') state = 3;
                    else if (c == '1') state = 4;
                    else if (isNonSeparator(c)) return false;
                break;

                case 4:
                    if      (c == '1') state = 5;
                    else if (isNonSeparator(c)) return false;
                break;

                case 1:
                case 3:
                case 5:
                    if      (isISODigit(c)) state = 6;
                    else if (isNonSeparator(c)) return false;
                break;

                case 6:
                case 7:
                    if      (isISODigit(c)) state++;
                    else if (isNonSeparator(c)) return false;
                break;

                default:
                    if (isNonSeparator(c)) return false;
            }
        }

        return state == 6 || state == 7 || state == 8;
    }

    /** all of 'a' up to len must match non-US trunk prefix ('0') */
    private static boolean
    matchTrunkPrefix(String a, int len) {
        boolean found;

        found = false;

        for (int i = 0 ; i < len ; i++) {
            char c = a.charAt(i);

            if (c == '0' && !found) {
                found = true;
            } else if (isNonSeparator(c)) {
                return false;
            }
        }

        return found;
    }
    
    /*
     * Note that this function does not strictly care the country calling code with
     * 3 length (like Morocco: +212), assuming it is enough to use the first two
     * digit to compare two phone numbers.
     */
    private static CountryCallingCodeAndNewIndex tryGetCountryCallingCodeAndNewIndex(
        String str, boolean acceptThailandCase) {
        // Rough regexp:
        //  ^[^0-9*#+]*((\+|0(0|11)\d\d?|166) [^0-9*#+] $
        //         0        1 2 3 45  6 7  89
        //
        // In all the states, this function ignores separator characters.
        // "166" is the special case for the call from Thailand to the US. Uguu!
        int state = 0;
        int ccc = 0;
        final int length = str.length();
        for (int i = 0 ; i < length ; i++ ) {
            char ch = str.charAt(i);
            switch (state) {
                case 0:
                    if      (ch == '+') state = 1;
                    else if (ch == '0') state = 2;
                    else if (ch == '1') {
                        if (acceptThailandCase) {
                            state = 8;
                        } else {
                            return null;
                        }
                    } else if (isDialable(ch)) {
                        return null;
                    }
                break;

                case 2:
                    if      (ch == '0') state = 3;
                    else if (ch == '1') state = 4;
                    else if (isDialable(ch)) {
                        return null;
                    }
                break;

                case 4:
                    if      (ch == '1') state = 5;
                    else if (isDialable(ch)) {
                        return null;
                    }
                break;

                case 1:
                case 3:
                case 5:
                case 6:
                case 7:
                    {
                        int ret = tryGetISODigit(ch);
                        if (ret > 0) {
                            ccc = ccc * 10 + ret;
                            if (ccc >= 100 || isCountryCallingCode(ccc)) {
                                return new CountryCallingCodeAndNewIndex(ccc, i + 1);
                            }
                            if (state == 1 || state == 3 || state == 5) {
                                state = 6;
                            } else {
                                state++;
                            }
                        } else if (isDialable(ch)) {
                            return null;
                        }
                    }
                    break;
                case 8:
                    if (ch == '6') state = 9;
                    else if (isDialable(ch)) {
                        return null;
                    }
                    break;
                case 9:
                    if (ch == '6') {
                        return new CountryCallingCodeAndNewIndex(66, i + 1);
                    } else {
                        return null;
                    }
                default:
                    return null;
            }
        }

        return null;
    }
}
