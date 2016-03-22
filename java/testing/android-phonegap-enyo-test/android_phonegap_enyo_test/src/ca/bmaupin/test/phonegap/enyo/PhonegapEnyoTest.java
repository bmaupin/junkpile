package ca.bmaupin.test.phonegap.enyo;

import org.apache.cordova.DroidGap;

import android.os.Bundle;

public class PhonegapEnyoTest extends DroidGap {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        setContentView(R.layout.main);
        // settings sample using onyx
        super.loadUrl("file:///android_asset/www/enyo/lib/onyx/examples/Settings/index.html");
        // flickr sample app
//        super.loadUrl("file:///android_asset/www/enyo/support/apps/flickr/index.html");
        // fittable layout examples
//        super.loadUrl("file:///android_asset/www/enyo/lib/layout/fittable/examples/app-layouts.html");
        // reminder example using onyx
//        super.loadUrl("file:///android_asset/www/enyo/lib/onyx/examples/Reminders/index.html");
        // onyx examples
//        super.loadUrl("file:///android_asset/www/enyo/lib/onyx/examples/OnyxSampler/index.html");
    }
}