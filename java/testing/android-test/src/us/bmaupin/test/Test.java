package us.bmaupin.test;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;

public class Test extends Activity {
	private static final String TAG = "Test";
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main_with_button);

        Button buttonTest = (Button) findViewById(R.id.button_test);
        buttonTest.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                Intent i = new Intent(Intent.ACTION_VIEW, 
                        MyProvider.CONTENT_URI);
//                i.putExtra(
//                        "com.googlecode.chartdroid.intent.extra.SERIES_LINE_THICKNESSES", 
//                        new float[] {5f});
                startActivity(i);
                
                
                /*
                 * ACTION_VIEW
                Intent intent = new Intent(ChooseStudySet.this, 
                        ChooseCardGroup.class);
                startActivityForResult(intent, REQUEST_CARD_SET_BROWSE);
                */
            }
        });
        
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