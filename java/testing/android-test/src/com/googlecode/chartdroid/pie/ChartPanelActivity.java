package com.googlecode.chartdroid.pie;

import java.util.ArrayList;
import java.util.List;

import us.bmaupin.test.R;

import android.app.ListActivity;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.BaseColumns;
import android.util.Log;
import android.view.Window;
import android.widget.ImageView;
import android.widget.TextView;

import com.googlecode.chartdroid.pie.ColorSwatchKeyAdapter.PieDataElement;

public class ChartPanelActivity extends ListActivity {    
    static final String TAG = "ChartPanelActivity"; 

    // Pie chart extras
    public static final String EXTRA_COLORS = "com.googlecode.chartdroid.intent.extra.COLORS";
    public static final String EXTRA_LABELS = "com.googlecode.chartdroid.intent.extra.LABELS";
    public static final String EXTRA_DATA = "com.googlecode.chartdroid.intent.extra.DATA";
    
    String[] data_labels;
    int[] data_values;
    int[] color_values;
    
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().requestFeature(Window.FEATURE_LEFT_ICON);
        setContentView(R.layout.panel_statistics);
        
        color_values = getIntent().getIntArrayExtra(ChartPanelActivity.EXTRA_COLORS);
/*        if (color_values == null) {
            color_values = getResources().getIntArray(R.array.colors_watermelon);
        }
*/
        
        TextView title_holder = (TextView) findViewById(R.id.chart_title_placeholder);
        title_holder.setText(getIntent().getStringExtra(Intent.EXTRA_TITLE));
        
        ImageView img = (ImageView) findViewById(R.id.image_placeholder);

        Uri intent_data = getIntent().getData();
        
        // Zip the data.
        List<PieDataElement> list = new ArrayList<PieDataElement>();
        if (intent_data != null) {
            // We have been passed a cursor to the data via a content provider.
            
            Log.d(TAG, "Querying content provider for: " + intent_data);
// TODO: managedQuery is deprecated
            Cursor cursor = managedQuery(intent_data,
                    new String[] {BaseColumns._ID, PlotData.COLUMN_AXIS_INDEX, PlotData.COLUMN_DATUM_VALUE},
                    null, null, null);

            int data_column = cursor.getColumnIndex(PlotData.COLUMN_DATUM_VALUE);
            int label_column = cursor.getColumnIndex(PlotData.COLUMN_DATUM_LABEL);

//          data_labels = new String[cursor.getCount()];
            data_values = new int[cursor.getCount()];
            
            int i=0;
            if (cursor.moveToFirst()) {
                do {
                    PieDataElement slice = new PieDataElement();
                    slice.datum = cursor.getInt(data_column);
                    data_values[i] = slice.datum;
                    
                    slice.label = cursor.getString(label_column);
                    slice.color = color_values[i % color_values.length];
                    list.add(slice);
                    
                    i++;
                } while (cursor.moveToNext());
            }
        } else {
            
            data_values = getIntent().getIntArrayExtra(ChartPanelActivity.EXTRA_DATA);
            data_labels = getIntent().getStringArrayExtra(ChartPanelActivity.EXTRA_LABELS);

            
            int i = 0;
            for (int datum : data_values) {
                PieDataElement slice = new PieDataElement();
                slice.color = color_values[i % color_values.length];
                slice.label = data_labels[i];
                slice.datum = datum;
                list.add(slice);
                
                i++;
            }
        }
        

        // Set up our adapter
        ColorSwatchKeyAdapter adapter = new ColorSwatchKeyAdapter(this);
        adapter.setData(list);
        setListAdapter(adapter);


        PieChartDrawable pie = new PieChartDrawable(this, img, data_values, color_values);
        img.setImageDrawable( pie );
    }
    

    // =============================================

    // TODO: We should probably store the data, in case there's a lot of it
    @Override
    public Object onRetainNonConfigurationInstance() {

        return null;
    }
}


final class PlotData implements BaseColumns {
    public static final String COLUMN_AXIS_INDEX = "COLUMN_AXIS_INDEX";
    public static final String COLUMN_DATUM_VALUE = "COLUMN_DATUM_VALUE";
    public static final String COLUMN_DATUM_LABEL = "COLUMN_DATUM_LABEL";
}
