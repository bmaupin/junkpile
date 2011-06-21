import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.provider.BaseColumns;
import android.util.Log;

public class DatabaseHelper extends SQLiteOpenHelper {
 // The tag will be used for logging
    public static final String TAG = "MyDatabase";
    
    // The name of your database
    public static final String DATABASE_NAME = "mydatabase.db";
    // The version of your database (increment this every time you change something)
    public static final int DATABASE_VERSION = 1;
    // The name of the table in your database
    public static final String DB_TABLE_NAME = "mytable";

    // The name of each column in the database
    public static final String _ID = BaseColumns._ID;
    public static final String TITLE = "title";
    public static final String DESCRIPTION = "description";
    public static final String TAGS = "tags";
    
    // variable to tell us whether onCreate() or onUpgrade() has been called
    boolean dbNeedsRefreshing = false;
    
    private final Context myContext;
    private SQLiteDatabase db;
    
    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
        this.myContext = context;
    }
    
    @Override
    public synchronized SQLiteDatabase getReadableDatabase() {
        // this will create a database if one doesn't already exist
        db = super.getReadableDatabase();
        
        Log.d(TAG, "getReadableDatabase called");
        Log.d(TAG, "dbNeedsRefreshing: " + dbNeedsRefreshing);
        
        if (dbNeedsRefreshing) {
            refreshDb();
        }
        
        return db;
    }

    @Override
    public synchronized SQLiteDatabase getWritableDatabase() {
        // this will create a database if one doesn't already exist
        db = super.getWritableDatabase();
        
        Log.d(TAG, "getWritableDatabase called");
        Log.d(TAG, "dbNeedsRefreshing: " + dbNeedsRefreshing);
        
        if (dbNeedsRefreshing) {
            refreshDb();
        }

        return db;
    }
    
    /**
     * Handles everything that's necessary to do before and after copying the 
     * packaged database to the application database on the system.
     */
    private void refreshDb() {
        try {
            Log.d(TAG, "db version: " + db.getVersion());
            // keep track of whether the database was read only
            boolean readOnly = db.isReadOnly();
            /*  the database will be open at this point (after a 
             *  getReadable/Writable database call) and needs to be closed
             *  so it can be overwritten with our packaged db
             */
            db.close();
            copyDatabase();
            // reopen database connection as writable, which should update the version
            db = super.getWritableDatabase();
            // update the version manually in case it gets missed somewhere
            if (db.getVersion() != DATABASE_VERSION) {
                Log.d(TAG, "changing version of db to " + DATABASE_VERSION);
                db.setVersion(DATABASE_VERSION);
            }
            // if the database was previously read only, close and reopen read only
            if (readOnly) {
                db.close();
                db = super.getReadableDatabase();
            }
        } catch (IOException e) {
// TODO: how do we properly handle errors here?
            e.printStackTrace();
        }
        dbNeedsRefreshing = false;
    }
    
    /**
     * Copies the packaged database from the local assets folder to the existing 
     * database in the system folder, from where it can be accessed and handled.
     * This is done by transfering bytestream.
     * */
    private void copyDatabase() throws IOException {
        // Open your local db as the input stream
        InputStream myInput = myContext.getAssets().open("databases/" + DATABASE_NAME);
        
        // Path to the just created empty db
        String outFileName = myContext.getDatabasePath(DATABASE_NAME).getAbsolutePath();
        
        // Open the empty db as the output stream
        OutputStream myOutput = new FileOutputStream(outFileName);
        
        // transfer bytes from the input file to the output file
        byte[] buffer = new byte[1024];
        int length;
        while ((length = myInput.read(buffer)) > 0) {
            myOutput.write(buffer, 0, length);
        }
        
        // Close the streams
        myOutput.flush();
        myOutput.close();
        myInput.close();
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        dbNeedsRefreshing = true;
        Log.d(TAG, "onCreate called");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        dbNeedsRefreshing = true;
        Log.d(TAG, "onUpgrade called");
    }
}