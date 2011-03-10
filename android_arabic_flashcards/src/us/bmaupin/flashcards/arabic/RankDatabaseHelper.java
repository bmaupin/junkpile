package us.bmaupin.flashcards.arabic;

// $Id$

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.BaseColumns;
import android.util.Log;

public class RankDatabaseHelper extends SQLiteOpenHelper {
	// tag for log messages
	public static final String TAG = "RankDatabaseHelper";

    // The name of your database
    public static final String DATABASE_NAME = "ranks.db";
    // The version of your database (increment this every time you change something)
    public static final int DATABASE_VERSION = 1;
    // The name of the table in your database
    public static final String DB_TABLE_NAME = "ranks";
   
    // The name of each column in the database
    public static final String RANK = "rank";
    
    private final Context context;    
    // SQL Statement to create a new database.
    public static final String DB_TABLE_CREATE =
        "CREATE TABLE " + DB_TABLE_NAME + " (" +
        BaseColumns._ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
        RANK + " INTEGER);";
   
    // The constructor method
    public RankDatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.context = context;
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
//        db.execSQL("DROP TABLE IF EXISTS " + DB_TABLE_NAME);
//        onCreate(db);
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
    	int ranksRows = cursor.getInt(0);
    	Log.d(TAG, "initializeDb: ranksRows=" + ranksRows );
    	
    	// get the difference, fill the ranks db with that number of empty rows
    	int rowsToAdd = cardsRows - ranksRows;
    	Log.d(TAG, "initializeDb: rowsToAdd=" + rowsToAdd );
    	ContentValues cv=new ContentValues();
    	for (int i=1; i<rowsToAdd + 1; i++) {
    		db.insert(DB_TABLE_NAME, RANK, cv);
    	}
    	
    	cursor = db.rawQuery(sql, null);
    	cursor.moveToFirst();
    	ranksRows = cursor.getInt(0);
    	Log.d(TAG, "initializeDb: ranksRows=" + ranksRows );
    	cursor.close();
    	
// TODO: db fill takes way too long (>5 sec), need to do little by little, or show user progress
    }
}
