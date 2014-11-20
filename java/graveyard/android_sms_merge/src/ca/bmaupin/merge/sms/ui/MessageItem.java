/*
 * Derived from com.android.mms.ui.MessageItem
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import java.util.regex.Pattern;

import com.google.android.mms.MmsException;
import com.google.android.mms.pdu.EncodedStringValue;
import com.google.android.mms.pdu.PduPersister;

import android.content.ContentUris;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.Telephony.Mms;
import android.provider.Telephony.Sms;
import android.text.TextUtils;
import android.util.Log;
import ca.bmaupin.merge.sms.R;
import ca.bmaupin.merge.sms.data.Contact;
import ca.bmaupin.merge.sms.data.WorkingMessage;
import ca.bmaupin.merge.sms.ui.MessageListAdapter.ColumnsMap;

public class MessageItem {
    public static int ATTACHMENT_TYPE_NOT_LOADED = -1;
	
    final Context mContext;
    final String mType;
    final long mMsgId;
    final int mBoxId;
    
    String mTimestamp;
    String mAddress;
    String mContact;
    String mBody; // Body of SMS, first text of MMS.
    String mTextContentType; // ContentType of text of MMS.
    Pattern mHighlight; // portion of message to highlight (from search)
    
    // The only non-immutable field.  Not synchronized, as access will
    // only be from the main GUI thread.  Worst case if accessed from
    // another thread is it'll return null and be set again from that
    // thread.
    CharSequence mCachedFormattedMessage;
    
    Cursor mCursor;
    ColumnsMap mColumnsMap;
    private PduLoadedCallback mPduLoadedCallback;
    
    // Fields for MMS only.
    Uri mMessageUri;
    int mMessageType;
    int mAttachmentType;
    String mSubject;
	
    MessageItem(Context context, String type, final Cursor cursor,
            final ColumnsMap columnsMap, Pattern highlight) throws MmsException {
        mContext = context;
        mMsgId = cursor.getLong(columnsMap.mColumnMsgId);
        mHighlight = highlight;
        mType = type;
        mCursor = cursor;
        mColumnsMap = columnsMap;

        if ("sms".equals(type)) {
            mMessageUri = ContentUris.withAppendedId(Sms.CONTENT_URI, mMsgId);
            // Set contact and message body
            mBoxId = cursor.getInt(columnsMap.mColumnSmsType);
            mAddress = cursor.getString(columnsMap.mColumnSmsAddress);
            if (Sms.isOutgoingFolder(mBoxId)) {
                String meString = context.getString(
                        R.string.messagelist_sender_self);

                mContact = meString;
            } else {
                // For incoming messages, the ADDRESS field contains the sender.
                mContact = Contact.get(mAddress, false).getName();
            }
            mBody = cursor.getString(columnsMap.mColumnSmsBody);

            // Unless the message is currently in the progress of being sent, it gets a time stamp.
            if (!isOutgoingMessage()) {
                // Set "received" or "sent" time stamp
                long date = cursor.getLong(columnsMap.mColumnSmsDate);
                mTimestamp = MessageUtils.formatTimeStampString(context, date);
            }

        } else if ("mms".equals(type)) {
            mMessageUri = ContentUris.withAppendedId(Mms.CONTENT_URI, mMsgId);
            mBoxId = cursor.getInt(columnsMap.mColumnMmsMessageBox);
            mMessageType = cursor.getInt(columnsMap.mColumnMmsMessageType);
            String subject = cursor.getString(columnsMap.mColumnMmsSubject);
            if (!TextUtils.isEmpty(subject)) {
                EncodedStringValue v = new EncodedStringValue(
                        cursor.getInt(columnsMap.mColumnMmsSubjectCharset),
                        PduPersister.getBytes(subject));
                mSubject = v.getString();
            }
            mBody = null;
            mTextContentType = null;
            // Initialize the time stamp to "" instead of null
            mTimestamp = "";
            mAttachmentType = cursor.getInt(columnsMap.mColumnMmsTextOnly) != 0 ?
                    WorkingMessage.TEXT : ATTACHMENT_TYPE_NOT_LOADED;

        } else {
            throw new MmsException("Unknown type of the message: " + type);
        }
    }
    
    public boolean isMms() {
        return mType.equals("mms");
    }

    public boolean isSms() {
        return mType.equals("sms");
    }
    
    public boolean isOutgoingMessage() {
        boolean isOutgoingMms = isMms() && (mBoxId == Mms.MESSAGE_BOX_OUTBOX);
        boolean isOutgoingSms = isSms()
                                    && ((mBoxId == Sms.MESSAGE_TYPE_FAILED)
                                            || (mBoxId == Sms.MESSAGE_TYPE_OUTBOX)
                                            || (mBoxId == Sms.MESSAGE_TYPE_QUEUED));
        return isOutgoingMms || isOutgoingSms;
    }
    
    // Note: This is the only mutable field in this class.  Think of
    // mCachedFormattedMessage as a C++ 'mutable' field on a const
    // object, with this being a lazy accessor whose logic to set it
    // is outside the class for model/view separation reasons.  In any
    // case, please keep this class conceptually immutable.
    public void setCachedFormattedMessage(CharSequence formattedMessage) {
        mCachedFormattedMessage = formattedMessage;
    }
    
    public CharSequence getCachedFormattedMessage() {
        return mCachedFormattedMessage;
    }
    
    public void setOnPduLoaded(PduLoadedCallback pduLoadedCallback) {
        mPduLoadedCallback = pduLoadedCallback;
    }
    
    public void cancelPduLoading() {
/* TODO MMS    	
        if (mItemLoadedFuture != null && !mItemLoadedFuture.isDone()) {
            if (Log.isLoggable(LogTag.APP, Log.DEBUG)) {
                Log.v(TAG, "cancelPduLoading for: " + this);
            }
            mItemLoadedFuture.cancel(mMessageUri);
            mItemLoadedFuture = null;
        }
*/
    }

    public interface PduLoadedCallback {
        /**
         * Called when this item's pdu and slideshow are finished loading.
         *
         * @param messageItem the MessageItem that finished loading.
         */
        void onPduLoaded(MessageItem messageItem);
    }
}
