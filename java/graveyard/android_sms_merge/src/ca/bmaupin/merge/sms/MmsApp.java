/*
 * Derived from com.android.mms.MmsApp
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms;

import android.app.Application;
import android.content.Context;
import android.os.StrictMode;
import android.preference.PreferenceManager;
import android.util.Log;

public class MmsApp extends Application {
	private static MmsApp sMmsApp = null;
	
    @Override
    public void onCreate() {
        super.onCreate();

        if (Log.isLoggable(LogTag.STRICT_MODE_TAG, Log.DEBUG)) {
            // Log tag for enabling/disabling StrictMode violation log. This will dump a stack
            // in the log that shows the StrictMode violator.
            // To enable: adb shell setprop log.tag.Mms:strictmode DEBUG
            StrictMode.setThreadPolicy(
                    new StrictMode.ThreadPolicy.Builder().detectAll().penaltyLog().build());
        }

        sMmsApp = this;
    }
	
    synchronized public static MmsApp getApplication() {
        return sMmsApp;
    }
}
