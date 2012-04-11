package ca.bmaupin.test.phonegap.enyo;

import org.apache.cordova.DroidGap;

import android.os.Bundle;

public class PhonegapEnyoTest extends DroidGap {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
//        setContentView(R.layout.main);
        super.loadUrl("file:///android_asset/www/index.html");
    }
}