/*
 * Derived from com.android.mms.data.Contact
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.data;

import java.io.IOException;
import java.io.InputStream;
import java.nio.CharBuffer;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.HashSet;

import android.content.ContentUris;
import android.content.Context;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.net.Uri;
import android.provider.ContactsContract.Contacts;
import android.provider.ContactsContract.Data;
import android.provider.ContactsContract.Presence;
import android.provider.ContactsContract.CommonDataKinds.Email;
import android.provider.ContactsContract.CommonDataKinds.Phone;
import android.provider.ContactsContract.Profile;
import android.telephony.PhoneNumberUtils;
import android.text.TextUtils;
import android.util.Log;
import ca.bmaupin.merge.sms.LogTag;
import ca.bmaupin.merge.sms.R;
import ca.bmaupin.merge.sms.android.SqliteWrapper;
import ca.bmaupin.merge.sms.android.Telephony.Mms;

public class Contact {
	public static final int CONTACT_METHOD_TYPE_PHONE = 1;
    public static final int CONTACT_METHOD_TYPE_EMAIL = 2;
    public static final int CONTACT_METHOD_TYPE_SELF = 3;       // the "Me" or profile contact
	private static final int CONTACT_METHOD_ID_UNKNOWN = -1;
	private static final String TAG = "Contact";
	private static ContactsCache sContactCache;
    private static final String SELF_ITEM_KEY = "Self_Item_Key";
	
	private final static HashSet<UpdateListener> mListeners = new HashSet<UpdateListener>();
	
    private long mContactMethodId;   // Id in phone or email Uri returned by provider of current
                                     // Contact, -1 is invalid. e.g. contact method id is 20 when
                                     // current contact has phone content://.../phones/20.
    private int mContactMethodType;
    private String mNumber;
    private String mNumberE164;
    private String mName;
    private String mNameAndNumber;   // for display, e.g. Fred Flintstone <670-782-1123>
    private boolean mNumberIsModified; // true if the number is modified
    
    private long mRecipientId;       // used to find the Recipient cache entry
    private String mLabel;
    private long mPersonId;
    private int mPresenceResId;      // TODO: make this a state instead of a res ID
    private String mPresenceText;
    private BitmapDrawable mAvatar;
    private byte [] mAvatarData;
    private boolean mIsStale;
    private boolean mQueryPending;
    private boolean mIsMe;          // true if this contact is me!
    private boolean mSendToVoicemail;   // true if this contact should not put up notification
    
    public interface UpdateListener {
        public void onUpdate(Contact updated);
    }
    
    /*
     * Make a basic contact object with a phone number.
     */
    private Contact(String number) {
        init(number, "");
    }

    private Contact(boolean isMe) {
        init(SELF_ITEM_KEY, "");
        mIsMe = isMe;
    }
    
    private void init(String number, String name) {
        mContactMethodId = CONTACT_METHOD_ID_UNKNOWN;
        mName = name;
        setNumber(number);
        mNumberIsModified = false;
        mLabel = "";
        mPersonId = 0;
        mPresenceResId = 0;
        mIsStale = true;
        mSendToVoicemail = false;
    }
	
    public static void logWithTrace(String tag, String msg, Object... format) {
        Thread current = Thread.currentThread();
        StackTraceElement[] stack = current.getStackTrace();

        StringBuilder sb = new StringBuilder();
        sb.append("[");
        sb.append(current.getId());
        sb.append("] ");
        sb.append(String.format(msg, format));

        sb.append(" <- ");
        int stop = stack.length > 7 ? 7 : stack.length;
        for (int i = 3; i < stop; i++) {
            String methodName = stack[i].getMethodName();
            sb.append(methodName);
            if ((i+1) != stop) {
                sb.append(" <- ");
            }
        }

        Log.d(tag, sb.toString());
    }
    
    public static Contact get(String number, boolean canBlock) {
        return sContactCache.get(number, canBlock);
    }
    
    public synchronized boolean existsInDatabase() {
        return (mPersonId > 0);
    }
    
    private static String emptyIfNull(String s) {
        return (s != null ? s : "");
    }
    
    /**
     * Fomat the name and number.
     *
     * @param name
     * @param number
     * @param numberE164 the number's E.164 representation, is used to get the
     *        country the number belongs to.
     * @return the formatted name and number
     */
    public static String formatNameAndNumber(String name, String number, String numberE164) {
        // Format like this: Mike Cleron <(650) 555-1234>
        //                   Erick Tseng <(650) 555-1212>
        //                   Tutankhamun <tutank1341@gmail.com>
        //                   (408) 555-1289
        String formattedNumber = number;
        if (!Mms.isEmailAddress(number)) {
            formattedNumber = PhoneNumberUtils.formatNumber(number, numberE164,
                    MmsApp.getApplication().getCurrentCountryIso());
        }

        if (!TextUtils.isEmpty(name) && !name.equals(number)) {
            return name + " <" + formattedNumber + ">";
        } else {
            return formattedNumber;
        }
    }
    
    public synchronized String getNumber() {
        return mNumber;
    }
    
    public synchronized void setNumber(String number) {
        if (!Mms.isEmailAddress(number)) {
            mNumber = PhoneNumberUtils.formatNumber(number, mNumberE164,
                    MmsApp.getApplication().getCurrentCountryIso());
        } else {
            mNumber = number;
        }
        notSynchronizedUpdateNameAndNumber();
        mNumberIsModified = true;
    }
    
    public synchronized String getName() {
        if (TextUtils.isEmpty(mName)) {
            return mNumber;
        } else {
            return mName;
        }
    }
    
    private void notSynchronizedUpdateNameAndNumber() {
        mNameAndNumber = formatNameAndNumber(mName, mNumber, mNumberE164);
    }
    
    public synchronized void setRecipientId(long id) {
        mRecipientId = id;
    }
    
    public synchronized Uri getUri() {
        return ContentUris.withAppendedId(Contacts.CONTENT_URI, mPersonId);
    }
    
    public synchronized Drawable getAvatar(Context context, Drawable defaultValue) {
        if (mAvatar == null) {
            if (mAvatarData != null) {
                Bitmap b = BitmapFactory.decodeByteArray(mAvatarData, 0, mAvatarData.length);
                mAvatar = new BitmapDrawable(context.getResources(), b);
            }
        }
        return mAvatar != null ? mAvatar : defaultValue;
    }
    
    private static class ContactsCache {
    	private final TaskStack mTaskQueue = new TaskStack();
    	
        /**
         * For a specified phone number, 2 rows were inserted into phone_lookup
         * table. One is the phone number's E164 representation, and another is
         * one's normalized format. If the phone number's normalized format in
         * the lookup table is the suffix of the given number's one, it is
         * treated as matched CallerId. E164 format number must fully equal.
         *
         * For example: Both 650-123-4567 and +1 (650) 123-4567 will match the
         * normalized number 6501234567 in the phone lookup.
         *
         *  The min_match is used to narrow down the candidates for the final
         * comparison.
         */
        // query params for caller id lookup
        private static final String CALLER_ID_SELECTION = " Data._ID IN "
                + " (SELECT DISTINCT lookup.data_id "
                + " FROM "
                    + " (SELECT data_id, normalized_number, length(normalized_number) as len "
                    + " FROM phone_lookup "
                    + " WHERE min_match = ?) AS lookup "
                + " WHERE lookup.normalized_number = ? OR"
                    + " (lookup.len <= ? AND "
                        + " substr(?, ? - lookup.len + 1) = lookup.normalized_number))";

        // query params for caller id lookup without E164 number as param
        private static final String CALLER_ID_SELECTION_WITHOUT_E164 =  " Data._ID IN "
            + " (SELECT DISTINCT lookup.data_id "
            + " FROM "
                + " (SELECT data_id, normalized_number, length(normalized_number) as len "
                + " FROM phone_lookup "
                + " WHERE min_match = ?) AS lookup "
            + " WHERE "
                + " (lookup.len <= ? AND "
                    + " substr(?, ? - lookup.len + 1) = lookup.normalized_number))";

        // Utilizing private API
        private static final Uri PHONES_WITH_PRESENCE_URI = Data.CONTENT_URI;

        private static final String[] CALLER_ID_PROJECTION = new String[] {
                Phone._ID,                      // 0
                Phone.NUMBER,                   // 1
                Phone.LABEL,                    // 2
                Phone.DISPLAY_NAME,             // 3
                Phone.CONTACT_ID,               // 4
                Phone.CONTACT_PRESENCE,         // 5
                Phone.CONTACT_STATUS,           // 6
                Phone.NORMALIZED_NUMBER,        // 7
                Contacts.SEND_TO_VOICEMAIL      // 8
        };
        
        private static final int PHONE_ID_COLUMN = 0;
        private static final int PHONE_LABEL_COLUMN = 2;
        private static final int CONTACT_NAME_COLUMN = 3;
        private static final int CONTACT_ID_COLUMN = 4;
        private static final int CONTACT_PRESENCE_COLUMN = 5;
        private static final int CONTACT_STATUS_COLUMN = 6;
        private static final int PHONE_NORMALIZED_NUMBER = 7;
        private static final int SEND_TO_VOICEMAIL = 8;
        
        private static final String[] SELF_PROJECTION = new String[] {
            Phone._ID,                      // 0
            Phone.DISPLAY_NAME,             // 1
        };
        
        private static final int SELF_NAME_COLUMN = 1;
        
        // query params for contact lookup by email
        private static final Uri EMAIL_WITH_PRESENCE_URI = Data.CONTENT_URI;

        private static final String EMAIL_SELECTION = "UPPER(" + Email.DATA + ")=UPPER(?) AND "
                + Data.MIMETYPE + "='" + Email.CONTENT_ITEM_TYPE + "'";

        private static final String[] EMAIL_PROJECTION = new String[] {
                Email._ID,                    // 0
                Email.DISPLAY_NAME,           // 1
                Email.CONTACT_PRESENCE,       // 2
                Email.CONTACT_ID,             // 3
                Phone.DISPLAY_NAME,           // 4
                Contacts.SEND_TO_VOICEMAIL    // 5
        };
        private static final int EMAIL_ID_COLUMN = 0;
        private static final int EMAIL_NAME_COLUMN = 1;
        private static final int EMAIL_STATUS_COLUMN = 2;
        private static final int EMAIL_CONTACT_ID_COLUMN = 3;
        private static final int EMAIL_CONTACT_NAME_COLUMN = 4;
        private static final int EMAIL_SEND_TO_VOICEMAIL_COLUMN = 5;
    	
        private final Context mContext;
        
        private final HashMap<String, ArrayList<Contact>> mContactsHash =
                new HashMap<String, ArrayList<Contact>>();
        
        private ContactsCache(Context context) {
            mContext = context;
        }
        
        private static class TaskStack {
            Thread mWorkerThread;
            private final ArrayList<Runnable> mThingsToLoad;

            public TaskStack() {
                mThingsToLoad = new ArrayList<Runnable>();
                mWorkerThread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                        while (true) {
                            Runnable r = null;
                            synchronized (mThingsToLoad) {
                                if (mThingsToLoad.size() == 0) {
                                    try {
                                        mThingsToLoad.wait();
                                    } catch (InterruptedException ex) {
                                        break;  // Exception sent by Contact.init() to stop Runnable
                                    }
                                }
                                if (mThingsToLoad.size() > 0) {
                                    r = mThingsToLoad.remove(0);
                                }
                            }
                            if (r != null) {
                                r.run();
                            }
                        }
                    }
                }, "Contact.ContactsCache.TaskStack worker thread");
                mWorkerThread.setPriority(Thread.MIN_PRIORITY);
                mWorkerThread.start();
            }

            public void push(Runnable r) {
                synchronized (mThingsToLoad) {
                    mThingsToLoad.add(r);
                    mThingsToLoad.notify();
                }
            }
        }
    	
        public void pushTask(Runnable r) {
            mTaskQueue.push(r);
        }
    	
        public Contact get(String number, boolean canBlock) {
            return get(number, false, canBlock);
        }

        private Contact get(String number, boolean isMe, boolean canBlock) {
            if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                logWithTrace(TAG, "get(%s, %s, %s)", number, isMe, canBlock);
            }

            if (TextUtils.isEmpty(number)) {
                number = "";        // In some places (such as Korea), it's possible to receive
                                    // a message without the sender's address. In this case,
                                    // all such anonymous messages will get added to the same
                                    // thread.
            }

            // Always return a Contact object, if if we don't have an actual contact
            // in the contacts db.
            Contact contact = internalGet(number, isMe);
            Runnable r = null;

            synchronized (contact) {
                // If there's a query pending and we're willing to block then
                // wait here until the query completes.
                while (canBlock && contact.mQueryPending) {
                    try {
                        contact.wait();
                    } catch (InterruptedException ex) {
                        // try again by virtue of the loop unless mQueryPending is false
                    }
                }

                // If we're stale and we haven't already kicked off a query then kick
                // it off here.
                if (contact.mIsStale && !contact.mQueryPending) {
                    contact.mIsStale = false;

                    if (Log.isLoggable(LogTag.APP, Log.VERBOSE)) {
                        log("async update for " + contact.toString() + " canBlock: " + canBlock +
                                " isStale: " + contact.mIsStale);
                    }

                    final Contact c = contact;
                    r = new Runnable() {
                        @Override
                        public void run() {
                            updateContact(c);
                        }
                    };

                    // set this to true while we have the lock on contact since we will
                    // either run the query directly (canBlock case) or push the query
                    // onto the queue.  In either case the mQueryPending will get set
                    // to false via updateContact.
                    contact.mQueryPending = true;
                }
            }
            // do this outside of the synchronized so we don't hold up any
            // subsequent calls to "get" on other threads
            if (r != null) {
                if (canBlock) {
                    r.run();
                } else {
                    pushTask(r);
                }
            }
            return contact;
        }
        
        private boolean contactChanged(Contact orig, Contact newContactData) {
            // The phone number should never change, so don't bother checking.
            // TODO: Maybe update it if it has gotten longer, i.e. 650-234-5678 -> +16502345678?

            // Do the quick check first.
            if (orig.mContactMethodType != newContactData.mContactMethodType) {
                return true;
            }

            if (orig.mContactMethodId != newContactData.mContactMethodId) {
                return true;
            }

            if (orig.mPersonId != newContactData.mPersonId) {
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    Log.d(TAG, "person id changed");
                }
                return true;
            }

            if (orig.mPresenceResId != newContactData.mPresenceResId) {
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    Log.d(TAG, "presence changed");
                }
                return true;
            }

            if (orig.mSendToVoicemail != newContactData.mSendToVoicemail) {
                return true;
            }

            String oldName = emptyIfNull(orig.mName);
            String newName = emptyIfNull(newContactData.mName);
            if (!oldName.equals(newName)) {
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    Log.d(TAG, String.format("name changed: %s -> %s", oldName, newName));
                }
                return true;
            }

            String oldLabel = emptyIfNull(orig.mLabel);
            String newLabel = emptyIfNull(newContactData.mLabel);
            if (!oldLabel.equals(newLabel)) {
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    Log.d(TAG, String.format("label changed: %s -> %s", oldLabel, newLabel));
                }
                return true;
            }

            if (!Arrays.equals(orig.mAvatarData, newContactData.mAvatarData)) {
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    Log.d(TAG, "avatar changed");
                }
                return true;
            }

            return false;
        }
        
        private void updateContact(final Contact c) {
            if (c == null) {
                return;
            }

            Contact entry = getContactInfo(c);
            synchronized (c) {
                if (contactChanged(c, entry)) {
                    if (Log.isLoggable(LogTag.APP, Log.VERBOSE)) {
                        log("updateContact: contact changed for " + entry.mName);
                    }

                    c.mNumber = entry.mNumber;
                    c.mLabel = entry.mLabel;
                    c.mPersonId = entry.mPersonId;
                    c.mPresenceResId = entry.mPresenceResId;
                    c.mPresenceText = entry.mPresenceText;
                    c.mAvatarData = entry.mAvatarData;
                    c.mAvatar = entry.mAvatar;
                    c.mContactMethodId = entry.mContactMethodId;
                    c.mContactMethodType = entry.mContactMethodType;
                    c.mNumberE164 = entry.mNumberE164;
                    c.mName = entry.mName;
                    c.mSendToVoicemail = entry.mSendToVoicemail;

                    c.notSynchronizedUpdateNameAndNumber();

                    // We saw a bug where we were updating an empty contact. That would trigger
                    // l.onUpdate() below, which would call ComposeMessageActivity.onUpdate,
                    // which would call the adapter's notifyDataSetChanged, which would throw
                    // away the message items and rebuild, eventually calling updateContact()
                    // again -- all in a vicious and unending loop. Break the cycle and don't
                    // notify if the number (the most important piece of information) is empty.
                    if (!TextUtils.isEmpty(c.mNumber)) {
                        // clone the list of listeners in case the onUpdate call turns around and
                        // modifies the list of listeners
                        // access to mListeners is synchronized on ContactsCache
                        HashSet<UpdateListener> iterator;
                        synchronized (mListeners) {
                            iterator = (HashSet<UpdateListener>)Contact.mListeners.clone();
                        }
                        for (UpdateListener l : iterator) {
                            if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                                Log.d(TAG, "updating " + l);
                            }
                            l.onUpdate(c);
                        }
                    }
                }
                synchronized (c) {
                    c.mQueryPending = false;
                    c.notifyAll();
                }
            }
        }
        
        /**
         * Returns the caller info in Contact.
         */
        private Contact getContactInfo(Contact c) {
            if (c.mIsMe) {
                return getContactInfoForSelf();
            } else if (Mms.isEmailAddress(c.mNumber)) {
                return getContactInfoForEmailAddress(c.mNumber);
            } else if (isAlphaNumber(c.mNumber)) {
                // first try to look it up in the email field
                Contact contact = getContactInfoForEmailAddress(c.mNumber);
                if (contact.existsInDatabase()) {
                    return contact;
                }
                // then look it up in the phone field
                return getContactInfoForPhoneNumber(c.mNumber);
            } else {
                // it's a real phone number, so strip out non-digits and look it up
                final String strippedNumber = PhoneNumberUtils.stripSeparators(c.mNumber);
                return getContactInfoForPhoneNumber(strippedNumber);
            }
        }
        
        // Some received sms's have addresses such as "OakfieldCPS" or "T-Mobile". This
        // function will attempt to identify these and return true. If the number contains
        // 3 or more digits, such as "jello123", this function will return false.
        // Some countries have 3 digits shortcodes and we have to identify them as numbers.
        //    http://en.wikipedia.org/wiki/Short_code
        // Examples of input/output for this function:
        //    "Jello123" -> false  [3 digits, it is considered to be the phone number "123"]
        //    "T-Mobile" -> true   [it is considered to be the address "T-Mobile"]
        //    "Mobile1"  -> true   [1 digit, it is considered to be the address "Mobile1"]
        //    "Dogs77"   -> true   [2 digits, it is considered to be the address "Dogs77"]
        //    "****1"    -> true   [1 digits, it is considered to be the address "****1"]
        //    "#4#5#6#"  -> true   [it is considered to be the address "#4#5#6#"]
        //    "AB12"     -> true   [2 digits, it is considered to be the address "AB12"]
        //    "12"       -> true   [2 digits, it is considered to be the address "12"]
        private boolean isAlphaNumber(String number) {
            // TODO: PhoneNumberUtils.isWellFormedSmsAddress() only check if the number is a valid
            // GSM SMS address. If the address contains a dialable char, it considers it a well
            // formed SMS addr. CDMA doesn't work that way and has a different parser for SMS
            // address (see CdmaSmsAddress.parse(String address)). We should definitely fix this!!!
            if (!PhoneNumberUtils.isWellFormedSmsAddress(number)) {
                // The example "T-Mobile" will exit here because there are no numbers.
                return true;        // we're not an sms address, consider it an alpha number
            }
            if (MessageUtils.isAlias(number)) {
                return true;
            }
            number = PhoneNumberUtils.extractNetworkPortion(number);
            if (TextUtils.isEmpty(number)) {
                return true;    // there are no digits whatsoever in the number
            }
            // At this point, anything like "Mobile1" or "Dogs77" will be stripped down to
            // "1" and "77". "#4#5#6#" remains as "#4#5#6#" at this point.
            return number.length() < 3;
        }
        
        /**
         * Queries the caller id info with the phone number.
         * @return a Contact containing the caller id info corresponding to the number.
         */
        private Contact getContactInfoForPhoneNumber(String number) {
            Contact entry = new Contact(number);
            entry.mContactMethodType = CONTACT_METHOD_TYPE_PHONE;

            if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                log("queryContactInfoByNumber: number=" + number);
            }

            String normalizedNumber = PhoneNumberUtils.normalizeNumber(number);
            String minMatch = PhoneNumberUtils.toCallerIDMinMatch(normalizedNumber);
            if (!TextUtils.isEmpty(normalizedNumber) && !TextUtils.isEmpty(minMatch)) {
                String numberLen = String.valueOf(normalizedNumber.length());
                String numberE164 = PhoneNumberUtils.formatNumberToE164(
                        number, MmsApp.getApplication().getCurrentCountryIso());
                String selection;
                String[] args;
                if (TextUtils.isEmpty(numberE164)) {
                    selection = CALLER_ID_SELECTION_WITHOUT_E164;
                    args = new String[] {minMatch, numberLen, normalizedNumber, numberLen};
                } else {
                    selection = CALLER_ID_SELECTION;
                    args = new String[] {
                            minMatch, numberE164, numberLen, normalizedNumber, numberLen};
                }

                Cursor cursor = mContext.getContentResolver().query(
                        PHONES_WITH_PRESENCE_URI, CALLER_ID_PROJECTION, selection, args, null);
                if (cursor == null) {
                    Log.w(TAG, "queryContactInfoByNumber(" + number + ") returned NULL cursor!"
                            + " contact uri used " + PHONES_WITH_PRESENCE_URI);
                    return entry;
                }

                try {
                    if (cursor.moveToFirst()) {
                        fillPhoneTypeContact(entry, cursor);
                    }
                } finally {
                    cursor.close();
                }
            }
            return entry;
        }
        
        /**
         * @return a Contact containing the info for the profile.
         */
        private Contact getContactInfoForSelf() {
            Contact entry = new Contact(true);
            entry.mContactMethodType = CONTACT_METHOD_TYPE_SELF;

            if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                log("getContactInfoForSelf");
            }
            Cursor cursor = mContext.getContentResolver().query(
                    Profile.CONTENT_URI, SELF_PROJECTION, null, null, null);
            if (cursor == null) {
                Log.w(TAG, "getContactInfoForSelf() returned NULL cursor!"
                        + " contact uri used " + Profile.CONTENT_URI);
                return entry;
            }

            try {
                if (cursor.moveToFirst()) {
                    fillSelfContact(entry, cursor);
                }
            } finally {
                cursor.close();
            }
            return entry;
        }
        
        private void fillPhoneTypeContact(final Contact contact, final Cursor cursor) {
            synchronized (contact) {
                contact.mContactMethodType = CONTACT_METHOD_TYPE_PHONE;
                contact.mContactMethodId = cursor.getLong(PHONE_ID_COLUMN);
                contact.mLabel = cursor.getString(PHONE_LABEL_COLUMN);
                contact.mName = cursor.getString(CONTACT_NAME_COLUMN);
                contact.mPersonId = cursor.getLong(CONTACT_ID_COLUMN);
                contact.mPresenceResId = getPresenceIconResourceId(
                        cursor.getInt(CONTACT_PRESENCE_COLUMN));
                contact.mPresenceText = cursor.getString(CONTACT_STATUS_COLUMN);
                contact.mNumberE164 = cursor.getString(PHONE_NORMALIZED_NUMBER);
                contact.mSendToVoicemail = cursor.getInt(SEND_TO_VOICEMAIL) == 1;
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    log("fillPhoneTypeContact: name=" + contact.mName + ", number="
                            + contact.mNumber + ", presence=" + contact.mPresenceResId
                            + " SendToVoicemail: " + contact.mSendToVoicemail);
                }
            }
            byte[] data = loadAvatarData(contact);

            synchronized (contact) {
                contact.mAvatarData = data;
            }
        }
        
        private void fillSelfContact(final Contact contact, final Cursor cursor) {
            synchronized (contact) {
                contact.mName = cursor.getString(SELF_NAME_COLUMN);
                if (TextUtils.isEmpty(contact.mName)) {
                    contact.mName = mContext.getString(R.string.messagelist_sender_self);
                }
                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                    log("fillSelfContact: name=" + contact.mName + ", number="
                            + contact.mNumber);
                }
            }
            byte[] data = loadAvatarData(contact);

            synchronized (contact) {
                contact.mAvatarData = data;
            }
        }
        /*
         * Load the avatar data from the cursor into memory.  Don't decode the data
         * until someone calls for it (see getAvatar).  Hang onto the raw data so that
         * we can compare it when the data is reloaded.
         * TODO: consider comparing a checksum so that we don't have to hang onto
         * the raw bytes after the image is decoded.
         */
        private byte[] loadAvatarData(Contact entry) {
            byte [] data = null;

            if ((!entry.mIsMe && entry.mPersonId == 0) || entry.mAvatar != null) {
                return null;
            }

            if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                log("loadAvatarData: name=" + entry.mName + ", number=" + entry.mNumber);
            }

            // If the contact is "me", then use my local profile photo. Otherwise, build a
            // uri to get the avatar of the contact.
            Uri contactUri = entry.mIsMe ?
                    Profile.CONTENT_URI :
                    ContentUris.withAppendedId(Contacts.CONTENT_URI, entry.mPersonId);

            InputStream avatarDataStream = Contacts.openContactPhotoInputStream(
                        mContext.getContentResolver(),
                        contactUri);
            try {
                if (avatarDataStream != null) {
                    data = new byte[avatarDataStream.available()];
                    avatarDataStream.read(data, 0, data.length);
                }
            } catch (IOException ex) {
                //
            } finally {
                try {
                    if (avatarDataStream != null) {
                        avatarDataStream.close();
                    }
                } catch (IOException e) {
                }
            }

            return data;
        }
        
        private int getPresenceIconResourceId(int presence) {
            // TODO: must fix for SDK
            if (presence != Presence.OFFLINE) {
                return Presence.getPresenceIconResourceId(presence);
            }

            return 0;
        }
        
        /**
         * Query the contact email table to get the name of an email address.
         */
        private Contact getContactInfoForEmailAddress(String email) {
            Contact entry = new Contact(email);
            entry.mContactMethodType = CONTACT_METHOD_TYPE_EMAIL;

            Cursor cursor = SqliteWrapper.query(mContext, mContext.getContentResolver(),
                    EMAIL_WITH_PRESENCE_URI,
                    EMAIL_PROJECTION,
                    EMAIL_SELECTION,
                    new String[] { email },
                    null);

            if (cursor != null) {
                try {
                    while (cursor.moveToNext()) {
                        boolean found = false;
                        synchronized (entry) {
                            entry.mContactMethodId = cursor.getLong(EMAIL_ID_COLUMN);
                            entry.mPresenceResId = getPresenceIconResourceId(
                                    cursor.getInt(EMAIL_STATUS_COLUMN));
                            entry.mPersonId = cursor.getLong(EMAIL_CONTACT_ID_COLUMN);
                            entry.mSendToVoicemail =
                                    cursor.getInt(EMAIL_SEND_TO_VOICEMAIL_COLUMN) == 1;

                            String name = cursor.getString(EMAIL_NAME_COLUMN);
                            if (TextUtils.isEmpty(name)) {
                                name = cursor.getString(EMAIL_CONTACT_NAME_COLUMN);
                            }
                            if (!TextUtils.isEmpty(name)) {
                                entry.mName = name;
                                if (Log.isLoggable(LogTag.CONTACT, Log.DEBUG)) {
                                    log("getContactInfoForEmailAddress: name=" + entry.mName +
                                            ", email=" + email + ", presence=" +
                                            entry.mPresenceResId);
                                }
                                found = true;
                            }
                        }

                        if (found) {
                            byte[] data = loadAvatarData(entry);
                            synchronized (entry) {
                                entry.mAvatarData = data;
                            }

                            break;
                        }
                    }
                } finally {
                    cursor.close();
                }
            }
            return entry;
        }
        
        // Invert and truncate to five characters the phoneNumber so that we
        // can use it as the key in a hashtable.  We keep a mapping of this
        // key to a list of all contacts which have the same key.
        private String key(String phoneNumber, CharBuffer keyBuffer) {
            keyBuffer.clear();
            keyBuffer.mark();

            int position = phoneNumber.length();
            int resultCount = 0;
            while (--position >= 0) {
                char c = phoneNumber.charAt(position);
                if (Character.isDigit(c)) {
                    keyBuffer.put(c);
                    if (++resultCount == STATIC_KEY_BUFFER_MAXIMUM_LENGTH) {
                        break;
                    }
                }
            }
            keyBuffer.reset();
            if (resultCount > 0) {
                return keyBuffer.toString();
            } else {
                // there were no usable digits in the input phoneNumber
                return phoneNumber;
            }
        }
        
        // Reuse this so we don't have to allocate each time we go through this
        // "get" function.
        static final int STATIC_KEY_BUFFER_MAXIMUM_LENGTH = 5;
        static CharBuffer sStaticKeyBuffer = CharBuffer.allocate(STATIC_KEY_BUFFER_MAXIMUM_LENGTH);
        
        private Contact internalGet(String numberOrEmail, boolean isMe) {
            synchronized (ContactsCache.this) {
                // See if we can find "number" in the hashtable.
                // If so, just return the result.
                final boolean isNotRegularPhoneNumber = isMe || Mms.isEmailAddress(numberOrEmail) ||
                        MessageUtils.isAlias(numberOrEmail);
                final String key = isNotRegularPhoneNumber ?
                        numberOrEmail : key(numberOrEmail, sStaticKeyBuffer);

                ArrayList<Contact> candidates = mContactsHash.get(key);
                if (candidates != null) {
                    int length = candidates.size();
                    for (int i = 0; i < length; i++) {
                        Contact c= candidates.get(i);
                        if (isNotRegularPhoneNumber) {
                            if (numberOrEmail.equals(c.mNumber)) {
                                return c;
                            }
                        } else {
                            if (PhoneNumberUtils.compare(numberOrEmail, c.mNumber)) {
                                return c;
                            }
                        }
                    }
                } else {
                    candidates = new ArrayList<Contact>();
                    // call toString() since it may be the static CharBuffer
                    mContactsHash.put(key, candidates);
                }
                Contact c = isMe ?
                        new Contact(true) :
                        new Contact(numberOrEmail);
                candidates.add(c);
                return c;
            }
        }
    }
    
    private static void log(String msg) {
        Log.d(TAG, msg);
    }
}
