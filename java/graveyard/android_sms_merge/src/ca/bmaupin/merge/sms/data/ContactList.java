/*
 * Derived from com.android.mms.data.ContactList
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.data;

import java.util.ArrayList;
import java.util.List;

import ca.bmaupin.merge.sms.ui.MessageUtils;
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
    
    public String serialize() {
        return TextUtils.join(";", getNumbers());
    }
    
    public String[] getNumbers() {
        return getNumbers(false /* don't scrub for MMS address */);
    }

    public String[] getNumbers(boolean scrubForMmsAddress) {
        List<String> numbers = new ArrayList<String>();
        String number;
        for (Contact c : this) {
            number = c.getNumber();

            if (scrubForMmsAddress) {
                // parse/scrub the address for valid MMS address. The returned number
                // could be null if it's not a valid MMS address. We don't want to send
                // a message to an invalid number, as the network may do its own stripping,
                // and end up sending the message to a different number!
                number = MessageUtils.parseMmsAddress(number);
            }

            // Don't add duplicate numbers. This can happen if a contact name has a comma.
            // Since we use a comma as a delimiter between contacts, the code will consider
            // the same recipient has been added twice. The recipients UI still works correctly.
            // It's easiest to just make sure we only send to the same recipient once.
            if (!TextUtils.isEmpty(number) && !numbers.contains(number)) {
                numbers.add(number);
            }
        }
        return numbers.toArray(new String[numbers.size()]);
    }
}
