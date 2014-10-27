/*
 * Derived from com.android.mms.data.ContactList
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.data;

import java.util.ArrayList;

import android.text.TextUtils;

public class ContactList extends ArrayList<Contact> {
	private static final long serialVersionUID = 1L;
	
    public String formatNames(String separator) {
        String[] names = new String[size()];
        int i = 0;
        for (Contact c : this) {
            names[i++] = c.getName();
        }
        return TextUtils.join(separator, names);
    }
}
