/*
 * Derived from com.android.mms.MmsConfig
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms;

public class MmsConfig {
    // Email gateway alias support, including the master switch and different rules
    private static boolean mAliasEnabled = false;
    private static int mAliasRuleMinChars = 2;
    private static int mAliasRuleMaxChars = 48;
	
    public static boolean isAliasEnabled() {
        return mAliasEnabled;
    }

    public static int getAliasMinChars() {
        return mAliasRuleMinChars;
    }

    public static int getAliasMaxChars() {
        return mAliasRuleMaxChars;
    }
}
