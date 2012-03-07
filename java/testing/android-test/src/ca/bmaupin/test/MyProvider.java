package ca.bmaupin.test;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.util.Log;


public class MyProvider extends ContentProvider {
    private static final String TAG = "MyProvider";
    public static final String AUTHORITY = "com.example.myapp.myprovider";
    public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY 
            + "/path");

    @Override
    public Cursor query(Uri uri, String[] projection, String selection,
            String[] selectionArgs, String sortOrder) {
        Log.d(TAG, "query()");
        
        if ("axes".equals(uri.getQueryParameter("aspect") )) {
            Log.d(TAG, "axes");
            // serve the axes metadata
            
            MatrixCursor cursor = new MatrixCursor(
                    new String[] {"COLUMN_AXIS_LABEL"}
            );
            
            cursor.addRow(new Object[] {"axis"});
            
            return cursor;
            
        } else if ("series".equals(uri.getQueryParameter("aspect") )) {
            Log.d(TAG, "series");
            // serve the series metadata
            
            MatrixCursor cursor = new MatrixCursor(
                    new String[] {
                            "_id",
                            "COLUMN_SERIES_LABEL",
                            "COLUMN_SERIES_LINE_STYLE",
                            "COLUMN_SERIES_LINE_THICKNESS"
                            }
            );
            
            cursor.addRow(new Object[] {
                    0,
                    "Summary",
                    3,
                    10f
            });
            
            return cursor;
        } else {
            Log.d(TAG, "data");
            // serve the data 
            
            MatrixCursor cursor = new MatrixCursor(
                    new String[] {
                            "COLUMN_SERIES_INDEX",
                            "COLUMN_DATUM_LABEL",
                            "AXIS_A"}
            );
            
            cursor.addRow(new Object[] {
                    0,
                    "known",
                    12
            });
            cursor.addRow(new Object[] {
                    0,
                    "iffy",
                    5
            });
            cursor.addRow(new Object[] {
                    0,
                    "unknown",
                    3
            });
            
            return cursor;
        }
    }
    
    @Override
    public String getType(Uri uri) {
        Log.d(TAG, "getType()");
        return "vnd.android.cursor.dir/vnd.com.googlecode.chartdroid.graphable";
    }
    
    @Override
    public int delete(Uri arg0, String arg1, String[] arg2) {
        // TODO Auto-generated method stub
        return 0;
    }

    @Override
    public Uri insert(Uri arg0, ContentValues arg1) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public boolean onCreate() {
        // TODO Auto-generated method stub
        return false;
    }



    @Override
    public int update(Uri arg0, ContentValues arg1, String arg2, String[] arg3) {
        // TODO Auto-generated method stub
        return 0;
    }

}
