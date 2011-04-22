package us.bmaupin.test;

//$Id: ProfileDatabaseHelper.java 181 2011-04-22 18:09:34Z bmaupin $

import java.util.ArrayList;
import java.util.List;

import android.content.Context;
import android.database.Cursor;
import android.database.DatabaseUtils.InsertHelper;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.BaseColumns;
import android.util.Log;

public class ProfileDatabaseHelper extends SQLiteOpenHelper {
    // tag for log messages
    public static final String TAG = "ProfileDatabaseHelper";

    // The name of your database
    public static final String DATABASE_NAME = "profiles.db";
    // The version of your database (increment this every time you change something)
    public static final int DATABASE_VERSION = 1;
    // profile name; this will be used as the database table name
    private String profileTableName = "profile1";
    
    // The name of each column in the database
    public static final String STATUS = "status";
    
    // SQL Statement to create a new database.
    private final String DB_TABLE_CREATE =
        "CREATE TABLE %s (" +
        BaseColumns._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
        STATUS + " INTEGER);";
    
    private final Context context;

    // The constructor method
    public ProfileDatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.context = context;
    }
    
    @Override
    public synchronized SQLiteDatabase getReadableDatabase() {
        List<String> tables = new ArrayList<String>();
        final String SQL_GET_ALL_TABLES = "SELECT name FROM " + 
            "sqlite_master WHERE type='table' ORDER BY name";
        
        // fetch the database
        SQLiteDatabase db = super.getReadableDatabase();
        // get the list of tables in the db
        Cursor cursor = db.rawQuery(SQL_GET_ALL_TABLES, null);
        cursor.moveToFirst();
        while (cursor.moveToNext()) {
            tables.add(cursor.getString(0));
        }
        cursor.close();
        // if the table we want isn't in the db, create it
        if (!tables.contains(profileTableName)) {
            // create the profile table
            db.execSQL(String.format(DB_TABLE_CREATE, profileTableName));
            // initialize the profile table
            initializeProfileTable(db, profileTableName);
        }
        
        return db;
    }
    
    public synchronized SQLiteDatabase getReadableDatabase(String profileTableName) {
        Log.d(TAG, "our getReadableDatabase called");
        Log.d(TAG, "our getReadableDatabase: this.profileTableName=" + profileTableName);
        this.profileTableName = profileTableName;
        Log.d(TAG, "our getReadableDatabase: this.profileTableName=" + profileTableName);
        return getReadableDatabase();
    }
    
    public String getprofileTableName() {
        return profileTableName;
    }
    
    /* Called when the super class getWritableDatabase (or getReadableDatabase)
     * method determines that the database doesn't exist yet and needs to be created
     */
    @Override
    public void onCreate(SQLiteDatabase db) {
//
        Log.d(TAG, "onCreate called");
    }
    
    /* Called when the super class getWritableDatabase (or getReadableDatabase)
     * method determines that the existing database isn't the same version as
     * the latest version
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        Log.w(TAG, "Upgrading database from version " + oldVersion + " to "
                + newVersion + ", which will destroy all old data");
//        db.execSQL("DROP TABLE IF EXISTS " + DB_TABLE_NAME);
//        onCreate(db);
//TODO: upgrade the db properly
//        initializeDb(db);
    }
    
    void initializeProfileTable (SQLiteDatabase db, String profileTable) {
        String sql = "SELECT COALESCE(MAX(_ID), 0) FROM " + DatabaseHelper.DB_TABLE_NAME;
    
        // get the number of rows in the cards db
        DatabaseHelper cardsHelper = new DatabaseHelper(context);
        SQLiteDatabase cardsDb = cardsHelper.getReadableDatabase();
        Cursor cardsCursor = cardsDb.rawQuery(sql, null);
        cardsCursor.moveToFirst();
        int cardsRows = cardsCursor.getInt(0);
        Log.d(TAG, "initializeDb: cardsRows=" + cardsRows );
        cardsCursor.close();
        cardsDb.close();
        cardsHelper.close();
        
        // get the number of rows in the cards db
        sql = "SELECT COALESCE(MAX(_ID), 0) FROM " + profileTable;
        Cursor cursor = db.rawQuery(sql, null);
        cursor.moveToFirst();
        int profileRows = cursor.getInt(0);
        Log.d(TAG, "initializeDb: profileRows=" + profileRows );
        
        // get the difference, fill the profile db with that number of empty rows
        int rowsToAdd = cardsRows - profileRows;
        Log.d(TAG, "initializeDb: rowsToAdd=" + rowsToAdd );
        
        InsertHelper ih = new InsertHelper(db, profileTable);
        
        final int STATUS_COLUMN = ih.getColumnIndex(ProfileDatabaseHelper.STATUS);
        
        for (int i=1; i<rowsToAdd + 1; i++) {
            ih.prepareForInsert();
            // insert a row with a status of 0 (unseen)
//            ih.bind(STATUS_COLUMN, 0);
            ih.execute();
        }
//
        cursor = db.rawQuery(sql, null);
        cursor.moveToFirst();
        profileRows = cursor.getInt(0);
        Log.d(TAG, "initializeDb: profileRows=" + profileRows );
        cursor.close();
    
    //TODO: db fill takes way too long (>5 sec), need to do little by little, or show user progress
    }
}
