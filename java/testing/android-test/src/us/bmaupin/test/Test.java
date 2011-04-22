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
    	List<String> currentUnseenIds = new ArrayList<String>();
    	
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        Log.d(TAG, "START db creation");
        ProfileDatabaseHelper profileHelper = new ProfileDatabaseHelper(this);
        SQLiteDatabase profileDb = profileHelper.getReadableDatabase("default3");
        Log.d(TAG, "FINISH db creation");
        profileDb.close();
        profileHelper.close();
        
        /*
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
        
        String sql = "SELECT _ID FROM " + DatabaseHelper.DB_TABLE_NAME +
        	" WHERE _ID IN (SELECT _ID FROM profileDb." + 
        	ProfileDatabaseHelper.DB_TABLE_NAME + " WHERE " + 
        	ProfileDatabaseHelper.STATUS + "= 1);";
		
        Cursor cursor = wordsDb.rawQuery(sql, null);
        cursor.moveToFirst();
        
        while (cursor.moveToNext()) {
        	currentUnseenIds.add(cursor.getString(0));
        }
        
        cursor.close();
        
        Log.d(TAG, "onCreate: currentUnseenIds.size()=" + currentUnseenIds.size());
        Toast.makeText(this, currentUnseenIds.size() + "", Toast.LENGTH_LONG).show();
        */
        
        /*
        ImageView i = (ImageView) findViewById(R.id.knownCheck);
        i.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				ImageView i = (ImageView)arg0;
				i.setImageResource(R.drawable.btn_check_buttonless_on);
				
//				vs.showNext();
			}
        	
        });
        */
        
        
        
//        ImageView i = new ImageView(this);
//        i.setImageResource(R.drawable.btn_check_buttonless_on);
//        i.setAdjustViewBounds(true); // set the ImageView bounds to match the Drawable's dimensions
        
//        TextView text = (TextView) findViewById(R.id.myTextView);
        
        /*
        ViewSwitcher vs = new ViewSwitcher(this);
        
        ImageView buttonChecked = (ImageView) findViewById(R.id.imageView1);
        ImageView buttonUnchecked = (ImageView) findViewById(R.id.imageView1);
        buttonUnchecked.setImageResource(R.drawable.btn_check_buttonless_off);
        
        vs.addView(buttonChecked);
        vs.addView(buttonUnchecked);
        */
        
//        ImageView i = (ImageView) findViewById(R.id.imageView1);
        
        /*
        i.setOnTouchListener(new OnTouchListener() {
            public boolean onTouch(View arg0, MotionEvent arg1) {
                // TODO Process touch event, return true if handled
                return false;
            }
        });
        */
        
        /*
        i.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View arg0) {
				ImageView i = (ImageView)findViewById(R.id.imageView1);
				i.setImageResource(R.drawable.btn_check_buttonless_off);
				
//				vs.showNext();
			}
        	
        });
        */
    }
}