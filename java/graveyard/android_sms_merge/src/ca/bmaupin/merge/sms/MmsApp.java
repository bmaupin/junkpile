/*
 * Derived from com.android.mms.MmsApp
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms;

import android.app.Application;
import android.content.Context;
import android.location.Country;
import android.location.CountryDetector;
import android.location.CountryListener;
import android.os.StrictMode;
import android.util.Log;

import ca.bmaupin.merge.sms.data.Contact;
import ca.bmaupin.merge.sms.data.Conversation;

public class MmsApp extends Application {
    private CountryDetector mCountryDetector;
    private CountryListener mCountryListener;
	private String mCountryIso;
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
        
        // Figure out the country *before* loading contacts and formatting numbers
        mCountryDetector = (CountryDetector) getSystemService(Context.COUNTRY_DETECTOR);
        mCountryListener = new CountryListener() {
            @Override
            public synchronized void onCountryDetected(Country country) {
                mCountryIso = country.getCountryIso();
            }
        };
        mCountryDetector.addCountryListener(mCountryListener, getMainLooper());
        
        Contact.init(this);
        Conversation.init(this);
    }
	
    synchronized public static MmsApp getApplication() {
        return sMmsApp;
    }
    
    @Override
    public void onTerminate() {
        mCountryDetector.removeCountryListener(mCountryListener);
    }
    
    // This function CAN return null.
    public String getCurrentCountryIso() {
        if (mCountryIso == null) {
            Country country = mCountryDetector.detectCountry();
            if (country != null) {
                mCountryIso = country.getCountryIso();
            }
        }
        return mCountryIso;
    }
}
