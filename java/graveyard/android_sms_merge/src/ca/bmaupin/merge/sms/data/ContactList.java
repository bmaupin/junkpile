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
    
    /**
     * Returns a ContactList for the corresponding recipient ids passed in. This method will
     * create the contact if it doesn't exist, and would inject the recipient id into the contact.
     */
    public static ContactList getByIds(String spaceSepIds, boolean canBlock) {
        ContactList list = new ContactList();
        for (RecipientIdCache.Entry entry : RecipientIdCache.getAddresses(spaceSepIds)) {
            if (entry != null && !TextUtils.isEmpty(entry.number)) {
                Contact contact = Contact.get(entry.number, canBlock);
                contact.setRecipientId(entry.id);
                list.add(contact);
            }
        }
        return list;
    }
}
