package us.bmaupin.test;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

public class Test extends Activity {
	private static final String TAG = "Test";
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
		DatabaseHelper wordsHelper = new DatabaseHelper(this);
		SQLiteDatabase wordsDb = wordsHelper.getReadableDatabase();
        
        Log.d(TAG, "START db creation");
        ProfileDatabaseHelper profileHelper = new ProfileDatabaseHelper(this);
        SQLiteDatabase profileDb = profileHelper.getReadableDatabase();
        Log.d(TAG, "FINISH db creation");
        profileDb.close();
        profileHelper.close();
        
        wordsDb.execSQL("attach database ? as profileDb", 
        		new String[] {this.getDatabasePath("profiles.db").getPath()});
        
        String[] sqlSelectionArgs = new String[1];
        String sql = "SELECT * from words where _ID IS ?";
        sqlSelectionArgs[0] = "NULL";
        Log.d(TAG, "sqlSelectionArgs=" + sqlSelectionArgs);
        Log.d(TAG, "sqlSelectionArgs[0]=" + sqlSelectionArgs[0]);
//        Log.d(TAG, "sqlSelectionArgs[1]" + sqlSelectionArgs[1]);
        
        String test = "1";
        
        Cursor cursor = wordsDb.rawQuery(sql, sqlSelectionArgs);
        cursor.moveToFirst();
        
        
        /*
        String sql = "SELECT  *" +
        		" FROM " + DatabaseHelper.DB_TABLE_NAME +
        		" LEFT JOIN profileDb." + ProfileDatabaseHelper.DB_TABLE_NAME + 
        		" ON " + DatabaseHelper.DB_TABLE_NAME + "._ID = profileDb." + 
        		ProfileDatabaseHelper.DB_TABLE_NAME + "." + 
        		ProfileDatabaseHelper.CARD_ID;
//        		" WHERE " + ProfileDatabaseHelper.STATUS + " IS NULL;";
		
        Cursor cursor = wordsDb.rawQuery(sql, null);
//        cursor.moveToFirst();
        
        Log.d(TAG, "START getting cards");
        
        int id;
        for (int i=1; i<501; i++) {
            cursor.moveToNext();
            id = cursor.getInt(0);
        }
        
        Log.d(TAG, "FINISH getting cards");
        */
    }
}