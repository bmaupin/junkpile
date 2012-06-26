package ca.bmaupin.test;

import android.app.Activity;
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
        tv.setTextSize(38f);
//        tv.setTextSize(22.868164f);
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
        
        tv.setText("test");
        tv.setText("internationally");
        tv.setText("test some words");
        tv.setText("internationally");
        tv.setText("appointments mathematics, playgrounds, mathematics");
        tv.setText("mathematics, appointmentslongword playgrounds,  international");
*/
        tv.setText("Feast of Immolation/sacrifice");
        tv.setText("good-looking");
        tv.setText("immediately (parents, siblings) and extended families; extended families");
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
