/*
 * Derived from android.database.sqlite.SqliteWrapper
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.android;

import ca.bmaupin.merge.sms.R;
import android.content.ContentResolver;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteException;
import android.net.Uri;
import android.util.Log;
import android.widget.Toast;

public final class SqliteWrapper {
    private static final String TAG = "SqliteWrapper";
    private static final String SQLITE_EXCEPTION_DETAIL_MESSAGE
    = "unable to open database file";
	
    // FIXME: need to optimize this method.
    private static boolean isLowMemory(SQLiteException e) {
        return e.getMessage().equals(SQLITE_EXCEPTION_DETAIL_MESSAGE);
    }
    
    public static void checkSQLiteException(Context context, SQLiteException e) {
        if (isLowMemory(e)) {
            Toast.makeText(context, R.string.low_memory,
                    Toast.LENGTH_SHORT).show();
        } else {
            throw e;
        }
    }
    
    public static Cursor query(Context context, ContentResolver resolver, Uri uri,
            String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        try {
            return resolver.query(uri, projection, selection, selectionArgs, sortOrder);
        } catch (SQLiteException e) {
            Log.e(TAG, "Catch a SQLiteException when query: ", e);
            checkSQLiteException(context, e);
            return null;
        }
    }
}
