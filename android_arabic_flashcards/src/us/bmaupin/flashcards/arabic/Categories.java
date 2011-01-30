package us.bmaupin.flashcards.arabic;

// $Id$

import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.DialogInterface.OnClickListener;
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
					chooseAWSChapter();
				}
			}
			});

	}
	
	private void chooseAWSChapter() {
		Log.d(TAG, "chooseAWSChapter");
		
		AlertDialog.Builder ad = new AlertDialog.Builder(context);
		ad.setTitle(R.string.choose_aws_chapter_title);

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

}
