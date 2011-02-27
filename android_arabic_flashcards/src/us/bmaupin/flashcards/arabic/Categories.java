package us.bmaupin.flashcards.arabic;

// $Id$

import java.util.ArrayList;
import java.util.List;

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.DialogInterface.OnClickListener;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
//import android.app.ListActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.ListView;
import android.widget.Toast;
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
		
		
//		View v1 = new View(this, null, 0);
		
//		lv.addView(child, params)

		
		
		lv.setOnItemClickListener(new OnItemClickListener() {
			@Override
			public void onItemClick(AdapterView<?> parent, View view, int pos,
					long id) {
				
				CharSequence itemText = adapter.getItem(pos);
				
				if (itemText.equals("Ahlan wa sahlan")) {
					Log.d(TAG, "chose AWS");
//					chooseAWSChapter();
					showDialog(DIALOG_AWS_CHAPTER_ID);
//					DEBUG					
					Toast toast = Toast.makeText(context, "selectedChapter: " + selectedChapter, Toast.LENGTH_LONG);
					toast.show();
					/*
					if (selectedChapter != null) {
						Intent result = new Intent();
						result.putExtra(EXTRA_CATEGORY, "Ahlan wa sahlan");
						result.putExtra(EXTRA_AWS_CHAPTER, selectedChapter);
						
						setResult(RESULT_OK, result);
						finish();
					} else {
						setResult(RESULT_CANCELED, null);
						finish();
					}
					*/
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
//		        Toast.makeText(getApplicationContext(), chapters[i], Toast.LENGTH_SHORT).show();
				Log.d(TAG, "createAWSChapterDialog: int=" + item);
				Log.d(TAG, "createAWSChapterDialog: chapter=" + chapters[item]);
				selectedChapter = chapters[item];
		    }
		});
		AlertDialog ad = builder.create();
		return ad;
	}
	
	private void chooseAWSChapterOld() {
		Log.d(TAG, "chooseAWSChapter");
		
		AlertDialog.Builder ad = new AlertDialog.Builder(context);
		ad.setTitle(R.string.choose_aws_chapter_title);
		
		final String[] chapters = getChapters();
		
		ad.setItems(chapters, new OnClickListener() {
					@Override
					public void onClick(DialogInterface dialoginterface, int i) {
						// TODO Auto-generated method stub
						Log.d(TAG, "chooseAWSChapter: int=" + i);
						Log.d(TAG, "chooseAWSChapter: chapter=" + chapters[i]);
						selectedChapter = chapters[i];
					}
				});

			ad.show();
		
		/*
		ad.setItems(R.array.aws_chapters, 
			new OnClickListener() {

				@Override
				public void onClick(DialogInterface dialoginterface, int i) {
					// TODO Auto-generated method stub
					Log.d(TAG, "chooseAWSChapter: int=" + i);
				}
			});

		ad.show();
*/

		
		
/*		
		String title = "It is Pitch Black";
		String message = "You are likely to be eaten by a grue.";
		String button1String = "Go Back";
		String button2String = "Move Forward";
		AlertDialog.Builder ad = new AlertDialog.Builder(context);
		ad.setTitle(title);
		ad.setMessage(message);
		ad.show();
		
/*
		AlertDialog.Builder ad = new AlertDialog.Builder(context);
		ad.setTitle(R.string.choose_aws_chapter_title);
		ad.setMessage(message);
		ad.setPositiveButton(button1String,

		
		new AlertDialog.Builder(context)
			.setTitle(R.string.choose_aws_chapter_title)
			.setItems(R.array.aws_chapters,
			new DialogInterface.OnClickListener() {
				public void onClick(DialogInterface dialoginterface,
				int i) {
					Log.d(TAG, "chooseAWSChapter: int=" + i);
//				Toast toast = Toast.makeText(context, i, Toast.LENGTH_SHORT);
//				toast.show();
				}
			})
			.show();
*/
	}

/*	
	class ChooseAWSChapter extends Activity {

		public ChooseAWSChapter(Context context) {
			super(context);
				
		}

		@Override
		protected void onCreate(Bundle savedInstanceState) {
			super.onCreate(savedInstanceState);
			
			setContentView(R.layout.awschapters);
			
			int layoutID = android.R.layout.simple_list_item_1;
			final ArrayAdapter<CharSequence> adapter = ArrayAdapter.createFromResource(
					this, R.array.aws_chapters,
					layoutID);
			final ListView tlv = (ListView)findViewById(R.id.myListView);
			
			tlv.setAdapter(adapter);
		}
		
	}
	
//	class AWSChapters extends Di {
		
//	}
*/

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
