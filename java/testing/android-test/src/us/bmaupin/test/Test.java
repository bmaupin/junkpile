package us.bmaupin.test;

import java.util.Arrays;

import com.googlecode.chartdroid.pie.ChartPanelActivity;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
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
/*                
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
                
                final String[] demo_pie_labels = new String[] {
                    "known",
                    "iffy",
                    "unknown"
                };
                final int[] demo_pie_data = new int[] {12, 5, 3};
/*                int[] colors = new int[demo_pie_labels.length];
                for (int j=0; j<demo_pie_labels.length; j++)
                                colors[j] = Color.HSVToColor(new float[] {360 * j / (float) colors.length, 0.6f, 1});
                Log.d(TAG, "colors=" + Arrays.toString(colors));
*/              
                int[] colors = {-10027162, -3276954, -39322};
                // color-blind safe colors
/*                int[] colors = {
                        Color.parseColor("#1BA1E2"),
                        -3276954,
                        Color.parseColor("#674f00")
                        };
*/
//                Intent i = new Intent("com.googlecode.chartdroid.intent.action.PLOT");
                Intent i = new Intent(Test.this, ChartPanelActivity.class);
                i.addCategory("com.googlecode.chartdroid.intent.category.PIE_CHART");
                i.putExtra(Intent.EXTRA_TITLE, "Summary");
                i.putExtra("com.googlecode.chartdroid.intent.extra.LABELS", demo_pie_labels);
                i.putExtra("com.googlecode.chartdroid.intent.extra.DATA", demo_pie_data);
                i.putExtra("com.googlecode.chartdroid.intent.extra.COLORS", colors);
                startActivity(i);
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