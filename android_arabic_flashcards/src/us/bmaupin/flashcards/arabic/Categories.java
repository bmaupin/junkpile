package us.bmaupin.flashcards.arabic;

// $Id$

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.AdapterView.OnItemClickListener;

public class Categories extends Activity {
	private static final String TAG = "Categories";
	//unique dialog id
	private static final int DIALOG_AWS_CHAPTER_ID = 0;
	protected static final String EXTRA_CATEGORY = null;
	protected static final String EXTRA_AWS_CHAPTER = null;
	String selectedChapter;
	private DatabaseHelper helper;
	private SQLiteDatabase db; 
	
	Context context = Categories.this;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.categories);

		int layoutID = android.R.layout.simple_list_item_1;
		
		final ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(
				this, R.array.categories_main_items,
				layoutID);
		
		final ListView lv = (ListView)findViewById(R.id.myListView);
		
		lv.setAdapter(adapter);	

		lv.setOnItemClickListener(new OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int pos,
					long id) {
				
				CharSequence itemText = adapter.getItem(pos);
				
				if (itemText.equals("Ahlan wa sahlan")) {
					Log.d(TAG, "chose AWS");
					showDialog(DIALOG_AWS_CHAPTER_ID);
				}
			}
			});

	}
	
	@Override
	protected Dialog onCreateDialog(int id) {
		switch (id) {
			case DIALOG_AWS_CHAPTER_ID:
				return createAWSChapterDialog();
		}
		return null;
	}
	
	private Dialog createAWSChapterDialog() {
		Log.d(TAG, "createAWSChapterDialog");
		
		final String[] chapters = getChapters();
		
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setTitle(R.string.choose_aws_chapter_title);
		builder.setItems(chapters, new DialogInterface.OnClickListener() {
		    public void onClick(DialogInterface dialog, int item) {
				Log.d(TAG, "createAWSChapterDialog: int=" + item);
				Log.d(TAG, "createAWSChapterDialog: chapter=" + chapters[item]);
				
				Intent result = new Intent();
				result.putExtra(EXTRA_CATEGORY, "Ahlan wa sahlan");
				result.putExtra(EXTRA_AWS_CHAPTER, chapters[item]);
				
				setResult(RESULT_OK, result);
				finish();
		    }
		});
		AlertDialog ad = builder.create();
		return ad;
	}
	
	private String[] getChapters() {
		Log.d(TAG, "getChapters called");
		String[] chapters;
	    
	    String[] FROM = {"aws_chapter"};
	    // as much fun as it'd be, let's not get null values
	    String WHERE = "aws_chapter not NULL";
	    
        helper = new DatabaseHelper(this);
        db = helper.getReadableDatabase();
	    
	    Cursor mCursor = db.query(true, "words", FROM, WHERE, null, null, null, null, null);
	    startManagingCursor(mCursor);
	    
	    // get the number of chapters since we're using an immutable array
	    int chapterCount = mCursor.getCount();
	    Log.d(TAG, "getChapters: chapterCount=" + chapterCount);
	    
	    chapters = new String[chapterCount];
	    int chapterIndex = 0;
	    while (mCursor.moveToNext()) {
	    	chapters[chapterIndex] = mCursor.getString(0);
	    	chapterIndex ++;   	
	    }
	    
	    // close the database connection
	    helper.close();
	    Log.d(TAG, "getChapters: returning");
	    return chapters;
	}
}
