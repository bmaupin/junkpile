/*
 * Derived from com.android.mms.data.Contact
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.data;

import android.text.TextUtils;

public class Contact {
    private String mNumber;
    private String mName;
	
    public synchronized String getName() {
        if (TextUtils.isEmpty(mName)) {
            return mNumber;
        } else {
            return mName;
        }
    }
}
