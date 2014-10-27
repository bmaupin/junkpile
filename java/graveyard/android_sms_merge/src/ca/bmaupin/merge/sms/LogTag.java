/*
 * Derived from com.android.mms.LogTag
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms;

import android.util.Log;

public class LogTag {
    public static final String TAG = "Mms";
	
    public static final String THREAD_CACHE = "Mms:threadcache";
    
    public static final boolean VERBOSE = false;
    
    private static String prettyArray(String[] array) {
        if (array.length == 0) {
            return "[]";
        }

        StringBuilder sb = new StringBuilder("[");
        int len = array.length-1;
        for (int i = 0; i < len; i++) {
            sb.append(array[i]);
            sb.append(", ");
        }
        sb.append(array[len]);
        sb.append("]");

        return sb.toString();
    }

    private static String logFormat(String format, Object... args) {
        for (int i = 0; i < args.length; i++) {
            if (args[i] instanceof String[]) {
                args[i] = prettyArray((String[])args[i]);
            }
        }
        String s = String.format(format, args);
        s = "[" + Thread.currentThread().getId() + "] " + s;
        return s;
    }

    public static void debug(String format, Object... args) {
        Log.d(TAG, logFormat(format, args));
    }
}
