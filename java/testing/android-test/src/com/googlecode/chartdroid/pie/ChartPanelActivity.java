/*
 * Source originally from the chartdroid project, revision 299
 * http://code.google.com/p/chartdroid/
 * 
 * This file has been modified from the original source by bmaupin:
 * - chartdroid icons removed
 * - constants from PlotData class integrated
 * - constants from IntentConstants class integrated
 * - unused code removed
 * - references to chart resources renamed
 */

package com.googlecode.chartdroid.pie;

import java.util.ArrayList;
import java.util.List;

import com.googlecode.chartdroid.pie.ColorSwatchKeyAdapter.PieDataElement;

import ca.bmaupin.test.R;

import android.app.ListActivity;
import android.content.Intent;
import android.os.Bundle;
import android.provider.BaseColumns;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

public class ChartPanelActivity extends ListActivity {    
    static final String TAG = "ChartPanelActivity"; 

    // Pie chart extras
    public static final String EXTRA_COLORS = "com.googlecode.chartdroid.intent.extra.COLORS";
    public static final String EXTRA_LABELS = "com.googlecode.chartdroid.intent.extra.LABELS";
    public static final String EXTRA_DATA = "com.googlecode.chartdroid.intent.extra.DATA";
    
    int[] color_values;
    String[] data_labels;
    int[] data_values;
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.chart_panel_statistics);
        
        LinearLayout layout = (LinearLayout) findViewById(R.id.chart_panel_statictics);
        layout.setOnClickListener(new OnClickListener() {
            @Override
            public void onClick(View arg0) {
                finish();
            }
        });
        
        TextView title_holder = (TextView) findViewById(R.id.chart_title_placeholder);
        title_holder.setText(getIntent().getStringExtra(Intent.EXTRA_TITLE));
        
        ImageView img = (ImageView) findViewById(R.id.chart_image_placeholder);
        
        // Zip the data.
        List<PieDataElement> list = new ArrayList<PieDataElement>();
        
        color_values = getIntent().getIntArrayExtra(ChartPanelActivity.EXTRA_COLORS);
        data_labels = getIntent().getStringArrayExtra(ChartPanelActivity.EXTRA_LABELS);
        data_values = getIntent().getIntArrayExtra(ChartPanelActivity.EXTRA_DATA);
        
        int i = 0;
        for (int datum : data_values) {
            PieDataElement slice = new PieDataElement();
            slice.color = color_values[i % color_values.length];
            slice.label = data_labels[i];
            slice.datum = datum;
            list.add(slice);
            
            i++;
        }

        // Set up our adapter
        ColorSwatchKeyAdapter adapter = new ColorSwatchKeyAdapter(this) {
            // prevent the chart key list from being clickable
            public boolean isEnabled(int position) {
                return false; 
            } 
        };
        adapter.setData(list);
        setListAdapter(adapter);

        PieChartDrawable pie = new PieChartDrawable(this, img, data_values, color_values);
        img.setImageDrawable( pie );
    }
}

final class PlotData implements BaseColumns {
    public static final String COLUMN_AXIS_INDEX = "COLUMN_AXIS_INDEX";
    public static final String COLUMN_DATUM_VALUE = "COLUMN_DATUM_VALUE";
    public static final String COLUMN_DATUM_LABEL = "COLUMN_DATUM_LABEL";
}
