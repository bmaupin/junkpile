package us.bmaupin.test;

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.view.ViewGroup.LayoutParams;
import android.widget.CheckBox;
import android.widget.LinearLayout;
import android.widget.RelativeLayout;
import android.widget.TableLayout;
import android.widget.TableRow;
import android.widget.TextView;
import android.widget.Toast;

public class Test extends Activity {
	private static final String TAG = "Test";
	private static final int DIALOG_SELECT_COLOR_ID = 0;
	
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        showDialog(DIALOG_SELECT_COLOR_ID);
        
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
        
        String[] sqlSelectionArgs = new String[1];
        String sql = "SELECT * from words where _ID IS ?";
        sqlSelectionArgs[0] = "NULL";
        Log.d(TAG, "sqlSelectionArgs=" + sqlSelectionArgs);
        Log.d(TAG, "sqlSelectionArgs[0]=" + sqlSelectionArgs[0]);
//        Log.d(TAG, "sqlSelectionArgs[1]" + sqlSelectionArgs[1]);
        
        String test = "1";
        
        Cursor cursor = wordsDb.rawQuery(sql, sqlSelectionArgs);
        cursor.moveToFirst();
        */
        
        
        /*
        String sql = "SELECT  *" +
        		" FROM " + DatabaseHelper.DB_TABLE_NAME +
        		" LEFT JOIN profileDb." + ProfileDatabaseHelper.DB_TABLE_NAME + 
        		" ON " + DatabaseHelper.DB_TABLE_NAME + "._ID = profileDb." + 
        		ProfileDatabaseHelper.DB_TABLE_NAME + "." + 
        		ProfileDatabaseHelper.CARD_ID;
//        		" WHERE " + ProfileDatabaseHelper.STATUS + " IS NULL;";
		
        Cursor cursor = wordsDb.rawQuery(sql, null);
//        cursor.moveToFirst();
        
        Log.d(TAG, "START getting cards");
        
        int id;
        for (int i=1; i<501; i++) {
            cursor.moveToNext();
            id = cursor.getInt(0);
        }
        
        Log.d(TAG, "FINISH getting cards");
        */
    }
    
    @Override
    protected Dialog onCreateDialog(int id) {
        switch (id) {
            case DIALOG_SELECT_COLOR_ID:
                return createSelectColorDialog();
        }
        return null;
    }

    private Dialog createSelectColorDialog() {
        final CharSequence[] items = {"Red", "Green", "Blue"};

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
/*        
        LinearLayout linearLayout = new LinearLayout(this);
        linearLayout.setPadding(0, -6, 0, -10);
        CheckBox checkBox = new CheckBox(this);
        TextView textView = new TextView(this);
        textView.setText("Save as default");
        linearLayout.addView(checkBox);
        linearLayout.addView(textView);
*/
        LayoutInflater inflater = (LayoutInflater) this.getSystemService(LAYOUT_INFLATER_SERVICE);
        ViewGroup layout = (ViewGroup) inflater.inflate(R.layout.card_order_dialog,
                (ViewGroup) findViewById(R.id.card_order_dialog_layout));
        
//        TableLayout layout = (TableLayout) inflater.inflate(R.layout.card_order_dialog,
//                (ViewGroup) findViewById(R.id.card_order_dialog_layout));
        
//        layout.setPadding(0, -6, 0, -10);
        layout.setPadding(0, -10, 0, -15);
        layout.setClipToPadding(false);
        builder.setView(layout);
        
        builder.setTitle("Pick a color");
        builder.setItems(items, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int item) {
                Toast.makeText(getApplicationContext(), items[item], Toast.LENGTH_SHORT).show();
            }
        });


        AlertDialog ad = builder.create();
        return ad;
    }
    
    private Dialog createSelectColorDialogOld2() {
        final CharSequence[] items = {"Red", "Green", "Blue"};

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        
        LinearLayout linearLayout = new LinearLayout(this);
        linearLayout.setPadding(0, -6, 0, -10);
        CheckBox checkBox = new CheckBox(this);
        TextView textView = new TextView(this);
        textView.setText("Save as default");
        linearLayout.addView(checkBox);
        linearLayout.addView(textView);
        builder.setView(linearLayout);
        
        builder.setTitle("Pick a color");
        builder.setItems(items, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int item) {
                Toast.makeText(getApplicationContext(), items[item], Toast.LENGTH_SHORT).show();
            }
        });

        AlertDialog ad = builder.create();
        return ad;
    }
    
    private Dialog createSelectColorDialogOld() {
        final CharSequence[] items = {"Red", "Green", "Blue"};

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        
        CheckBox checkBox = new CheckBox(this);
        TextView textView = new TextView(this);
//        RelativeLayout linearLayout = new RelativeLayout(this);
        

        LinearLayout linearLayout = new LinearLayout(this);
        
        
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(LinearLayout.LayoutParams.WRAP_CONTENT,
              LinearLayout.LayoutParams.WRAP_CONTENT);
        
//        lp.setMargins(0, -6, 0, -10);
        
//        linearLayout.setLayoutParams(new LayoutParams(LinearLayout.LayoutParams.FILL_PARENT,
//                        LinearLayout.LayoutParams.FILL_PARENT));
//        linearLayout.setOrientation(1);
//        textView.setText("Save as default (dont' show this again)");
        textView.setText("Save as default");
        
//        checkBox.setPadding(0, 0, 0, 0);
        
//        linearLayout.setPadding(0, 0, 0, 0);
//        linearLayout.setPadding(0,-6,0,-10);
        linearLayout.setPadding(0,-9,0,-13);
        
//        linearLayout.setMargins(0,3,0,3);
        
        
//        lp.setMargins(0,0,0,0);
//        lp.setMargins(1,1,1,1);
//        lp.setMargins(0, -6, 0, -10);
        //lp.setMargins(0,5,0,5);
//        lp.setMargins(0,2,0,2);
        lp.setMargins(0,-3,0,-3);
        

//        lp2.setMargins(0,0,0,0);
        
//        lp.setWeight(1);
        linearLayout.setLayoutParams(lp);
        
//        checkBox.setPadding(0, 3, 0, 3);
        
        linearLayout.addView(checkBox);
        linearLayout.addView(textView);

        builder.setView(linearLayout);
        builder.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
                    public void onClick(DialogInterface arg0, int arg1) {
        }});
        
        
        builder.setTitle("Pick a color");
        builder.setItems(items, new DialogInterface.OnClickListener() {
            public void onClick(DialogInterface dialog, int item) {
                Toast.makeText(getApplicationContext(), items[item], Toast.LENGTH_SHORT).show();
            }
        });
        

        AlertDialog ad = builder.create();
        return ad;
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