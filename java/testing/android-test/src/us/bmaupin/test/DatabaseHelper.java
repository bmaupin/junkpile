package us.bmaupin.test;

// $Id: DatabaseHelper.java 109 2011-03-09 20:53:40Z bmaupin $

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.BaseColumns;
import android.util.Log;

public class DatabaseHelper extends SQLiteOpenHelper {
    public static final String TAG = "MyDatabase";
    public static final String DATABASE_NAME = "mydatabase.db";
    public static final int DATABASE_VERSION = 10;
    public static final String DB_TABLE_NAME = "mytable";
    public static final String STATUS = "status";

    public static final String DB_TABLE_CREATE =
        "CREATE TABLE " + DB_TABLE_NAME + " (" +
        BaseColumns._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
        STATUS + " INTEGER);";
   
    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(DB_TABLE_CREATE);       
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        Log.w(TAG, "Upgrading database from version " + oldVersion + " to "
                + newVersion + ", which will destroy all old data");
        db.execSQL("DROP TABLE IF EXISTS " + DB_TABLE_NAME);
        onCreate(db);
    }
}