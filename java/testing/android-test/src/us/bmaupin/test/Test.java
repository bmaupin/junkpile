package us.bmaupin.test;

import android.app.Activity;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;

public class Test extends Activity {
	private static final String TAG = "Test";
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        Log.d(TAG, "START db creation");
        RankDatabaseHelper dbHelper = new RankDatabaseHelper(this);
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        Log.d(TAG, "FINISH db creation");
        
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