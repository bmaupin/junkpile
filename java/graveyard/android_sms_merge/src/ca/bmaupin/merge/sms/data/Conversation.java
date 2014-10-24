/*
 * Derived from com.android.mms.data.Conversation
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.data;

import android.content.Context;
import android.database.Cursor;
import android.util.Log;

public class Conversation {
    private static final String TAG = "Mms/conv";
	private static final boolean DEBUG = false;
	
	private final Context mContext;
	
    private Conversation(Context context, Cursor cursor, boolean allowQuery) {
        if (DEBUG) {
            Log.v(TAG, "Conversation constructor cursor, allowQuery: " + allowQuery);
        }
        mContext = context;
        fillFromCursor(context, this, cursor, allowQuery);
    }
}
