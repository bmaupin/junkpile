package us.bmaupin.test;

import android.app.Activity;
import android.database.Cursor;
import android.database.DatabaseUtils.InsertHelper;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;

public class Test extends Activity {
    public static final String table = "mytable";
    
	private static final String TAG = "Test";
	// Log.d(TAG, "START db creation");

    /* (non-Javadoc)
     * @see android.app.Activity#onCreate(android.os.Bundle)
     */
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        DatabaseHelper dbHelper = new DatabaseHelper(this);
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        
        int rowsToAdd = 2000;
        String sql = "SELECT COALESCE(MAX(_ID), 0) FROM " + table;
        
        InsertHelper ih = new InsertHelper(db, table);
        final int STATUS_COLUMN = ih.getColumnIndex(DatabaseHelper.STATUS);
        
        Log.d(TAG, "start insertion");
        for (int i=1; i<rowsToAdd + 1; i++) {
            ih.prepareForInsert();
            // insert a row with a status of 0 (unseen)
            ih.bind(STATUS_COLUMN, 0);
            ih.execute();
        }
//
        Cursor cursor = db.rawQuery(sql, null);
        cursor.moveToFirst();
        Log.d(TAG, "rows=" + cursor.getInt(0));
        cursor.close();
    }
}