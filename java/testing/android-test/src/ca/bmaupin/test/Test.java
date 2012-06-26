package ca.bmaupin.test;

import android.app.Activity;
import android.graphics.Typeface;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;

public class Test extends Activity {
	private static final String TAG = "Test";
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        AutofitTextView tv = (AutofitTextView) findViewById(R.id.leftView);

// english: 38f
//        tv.setTextSize(42f);  // 71      70
//        tv.setTextSize(41f);  // 55  16
//        tv.setTextSize(40f);  // 41  14
//        tv.setTextSize(39f);  // 31  10  35
//        tv.setTextSize(38f);  // 25   6  26
//        tv.setTextSize(37f);  // 22   3  22
//        tv.setTextSize(36f);  // 11   9  14
        tv.setTextSize(35f);  // 6    5
        
        String ARABIC_TYPEFACE = "fonts/KacstOne.ttf";
        
        tv.setTypeface(Typeface.createFromAsset(getAssets(), 
                ARABIC_TYPEFACE));
        
// arabic: 56f
//        tv.setTextSize(56f);  // 23 (me)
//      tv.setTextSize(55f);  // 19
//        tv.setTextSize(54f);  // 16
//        tv.setTextSize(53f);  // 16
//        tv.setTextSize(52f);  // 12
//      tv.setTextSize(51f);  // 11
//      tv.setTextSize(50f);  // 8
        
        
        
        
        // short word
//        tv.setText("test");
        // long word
//        tv.setText("internationally");
//        tv.setText("test");
        
        // multiple words
//        tv.setText("test some words");
//        tv.setText("supercalafragalisticexpialadocious");
        // multiple long words
//        Log.d(TAG, "tv.getTextSize())" + tv.getTextSize());
        
//        tv.setText("mathematics, appointmentslongword playgrounds,  international");
//        tv.setText("longword mathematics, playgrounds, mathematics");
//        Log.d(TAG, "tv.getTextSize())" + tv.getTextSize());
        
/*        
        tv.setText("test");
        tv.setText("mathematics, appointmentslongword playgrounds,  international");
        tv.setText("test");
        tv.setText("mathematics, appointmentslongword playgrounds,  international");
        tv.setText("test");
        tv.setText("internationally");
        tv.setText("test some words");
        tv.setText("internationally");
        tv.setText("appointments mathematics, playgrounds, mathematics");
        tv.setText("mathematics, appointmentslongword playgrounds,  international");
*/
//        tv.setText("immediately (parents, siblings) and extended families; extended families");

    }
    
    /* Inflates the menu */
    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.menu, menu);
        return true;
    }
    
    /* Handles menu selections */
    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
        case R.id.menu_exit:
            finish();
            return true;
        }
        return false;
    }
}
