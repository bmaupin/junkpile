package us.bmaupin.test;

// $Id: ProfileDatabaseHelper.java 173 2011-04-13 18:42:48Z bmaupin $

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
    public static final int DATABASE_VERSION = 3;
    // profile name; this will be used as the database table name
//    private String DB_TABLE_NAME;
//    private static final String DEFAULT_PROFILE_NAME = "profile1";
    public static final String DB_TABLE_NAME = "profile1";
    
    // The name of each column in the database
//    public static final String CARD_ID = "card_ID";
    public static final String STATUS = "status";
    
    // SQL Statement to create a new database.
    private String DB_TABLE_CREATE =
        "CREATE TABLE " + DB_TABLE_NAME + " (" +
        BaseColumns._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
        STATUS + " INTEGER);";
    
//  CARD_ID + " INTEGER, " +
    
    private final Context context;
    
    /*
    // The constructor method
    public ProfileDatabaseHelper(Context context, String DB_TABLE_NAME) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
//        ProfileDatabaseHelper.DB_TABLE_NAME = DB_TABLE_NAME;
        this.context = context;
    }
    */
    
    public ProfileDatabaseHelper(Context context) {
//    	this(context, DEFAULT_PROFILE_NAME);
    	super(context, DATABASE_NAME, null, DATABASE_VERSION);
    	this.context = context;
    }
    
	@Override
	public synchronized SQLiteDatabase getReadableDatabase() {
		// TODO Auto-generated method stub
		return super.getReadableDatabase();
	}
	
	public String getDB_TABLE_NAME() {
    	return DB_TABLE_NAME;
    }
    
    /* Called when the super class getWritableDatabase (or getReadableDatabase)
     * method determines that the database doesn't exist yet and needs to be created
     */
    @Override
    public void onCreate(SQLiteDatabase db) {
    	Log.d(TAG, "onCreate called");
        db.execSQL(DB_TABLE_CREATE);
        
        initializeDb(db);
    }

    /* Called when the super class getWritableDatabase (or getReadableDatabase)
     * method determines that the existing database isn't the same version as
     * the latest version
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        Log.w(TAG, "Upgrading database from version " + oldVersion + " to "
                + newVersion + ", which will destroy all old data");
        db.execSQL("DROP TABLE IF EXISTS " + DB_TABLE_NAME);
        onCreate(db);
// TODO: upgrade the db properly
    }
    
    void initializeDb (SQLiteDatabase db) {
    	String sql = "SELECT COALESCE(MAX(_ID), 0) FROM " + DatabaseHelper.DB_TABLE_NAME;
    	
    	// get the number of rows in the cards db
    	DatabaseHelper cardsHelper = new DatabaseHelper(context);
        SQLiteDatabase cardsDb = cardsHelper.getReadableDatabase();
        Cursor cardsCursor = cardsDb.rawQuery(sql, null);
        cardsCursor.moveToFirst();
        int cardsRows = cardsCursor.getInt(0);
        Log.d(TAG, "initializeDb: cardsRows=" + cardsRows );
        cardsCursor.close();
        cardsHelper.close();
        
        // get the number of rows in the cards db
        sql = "SELECT COALESCE(MAX(_ID), 0) FROM " + DB_TABLE_NAME;
    	Cursor cursor = db.rawQuery(sql, null);
    	cursor.moveToFirst();
    	int profileRows = cursor.getInt(0);
    	Log.d(TAG, "initializeDb: profileRows=" + profileRows );
    	
    	// get the difference, fill the profile db with that number of empty rows
    	int rowsToAdd = cardsRows - profileRows;
    	Log.d(TAG, "initializeDb: rowsToAdd=" + rowsToAdd );
    	Log.d(TAG, "initializeDb: rowsToAdd=" + rowsToAdd );
    	/*
    	ContentValues cv=new ContentValues();
    	for (int i=1; i<rowsToAdd + 1; i++) {
    		db.insert(DB_TABLE_NAME, RANK, cv);
    	}
    	*/
    	
    	InsertHelper ih = new InsertHelper(db, DB_TABLE_NAME);
    	
//    	final int ID_COLUMN = ih.getColumnIndex(BaseColumns._ID);
    	final int STATUS_COLUMN = ih.getColumnIndex(ProfileDatabaseHelper.STATUS);
    	
    	
    	for (int i=1; i<rowsToAdd + 1; i++) {
    		ih.prepareForInsert();
//    		ih.bind(ID_COLUMN, RANK_COLUMN);
    		// just insert an empty row with null values
    		ih.bind(STATUS_COLUMN, 0);
    		ih.execute();
    	}
    	
    	cursor = db.rawQuery(sql, null);
    	cursor.moveToFirst();
    	profileRows = cursor.getInt(0);
    	Log.d(TAG, "initializeDb: profileRows=" + profileRows );
    	cursor.close();
    	
// TODO: db fill takes way too long (>5 sec), need to do little by little, or show user progress
    }
}
