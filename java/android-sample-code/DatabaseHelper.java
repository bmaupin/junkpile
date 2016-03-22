/*
 Copyright (C) 2011 bmaupin <bmaupin@users.noreply.github.com>
 
 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 
 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 
 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

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

    // SQL Statement to create a new database.
    public static final String DB_TABLE_CREATE =
        "CREATE TABLE " + DB_TABLE_NAME + " (" +
        _ID + " INTEGER PRIMARY KEY AUTOINCREMENT, " +
        TITLE + " TEXT, " +
        DESCRIPTION + " TEXT, " +
        TAGS + " TEXT);";
   
    // The constructor method
    public DatabaseHelper(Context context) {
        super(context, DATABASE_NAME, null, DATABASE_VERSION);
    }

    /* Called when the super class getWritableDatabase (or getReadableDatabase)
     * method determines that the database doesn't exist yet and needs to be created
     */
    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL(DB_TABLE_CREATE);       
    }

    /* Called when the super class getWritableDatabase (or getReadableDatabase)
     * method determines that the existing database isn't the same version as
     * the latest version
     */
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        Log.w(TAG, "Upgrading database from version " + oldVersion + " to "
                + newVersion + ", which will destroy all old data");
        // this is probably not the best way to do it...
        db.execSQL("DROP TABLE IF EXISTS " + DB_TABLE_NAME);
        onCreate(db);
    }
}