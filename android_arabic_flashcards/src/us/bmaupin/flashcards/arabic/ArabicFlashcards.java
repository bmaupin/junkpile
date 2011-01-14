package us.bmaupin.flashcards.arabic;

import java.util.HashMap;
import java.util.Map;

import org.amr.arabic.ArabicReshaper;
import org.amr.arabic.ArabicUtilities;

import us.bmaupin.flashcards.arabic.DatabaseHelper;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.graphics.Typeface;
import android.os.Bundle;
import android.util.Log;
import android.view.GestureDetector;
import android.view.KeyEvent;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.GestureDetector.SimpleOnGestureListener;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.RelativeLayout;
import android.widget.TextView;
import android.widget.ViewFlipper;


public class ArabicFlashcards extends Activity {
	private static final String TAG = "ArabicFlashcards";
	public static final String PREFS_NAME = "FlashcardPrefsFile";
	private DatabaseHelper helper;
	private int cursorPosition;
	private Cursor cursor;
	private String currentLang;
	private String defaultLang;
	private SharedPreferences settings;
	
	// class variables for swipe
    private static final int SWIPE_MIN_DISTANCE = 120;
    private static final int SWIPE_MAX_OFF_PATH = 250;
	private static final int SWIPE_THRESHOLD_VELOCITY = 200;
	private GestureDetector gestureDetector;
	View.OnTouchListener gestureListener;
	private Animation slideLeftIn;
	private Animation slideLeftOut;
	private Animation slideRightIn;
    private Animation slideRightOut;
    private ViewFlipper vf;
    
//    private TextView leftView;
//    private TextView centerView;
//    private TextView rightView;
    
    private TextView currentView;
    private Map<String, String> currentWord;

	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	Log.d(TAG, "onCreate called");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        vf = (ViewFlipper)findViewById(R.id.flipper);
        slideLeftIn = AnimationUtils.loadAnimation(this, R.anim.slide_left_in);
        slideLeftOut = AnimationUtils.loadAnimation(this, R.anim.slide_left_out);
        slideRightIn = AnimationUtils.loadAnimation(this, R.anim.slide_right_in);
        slideRightOut = AnimationUtils.loadAnimation(this, R.anim.slide_right_out);
        
        gestureDetector = new GestureDetector(new MyGestureDetector());
        gestureListener = new View.OnTouchListener() {
            public boolean onTouch(View v, MotionEvent event) {
                if (gestureDetector.onTouchEvent(event)) {
                    return true;
                }
                return false;
            }
        };
        
        helper = new DatabaseHelper(this);
        
		// Restore preferences
        settings = getSharedPreferences(PREFS_NAME, 0);
        cursorPosition = settings.getInt("cursorPosition", -2);
        Log.d(TAG, "onCreate, cursorPosition: " + cursorPosition);
        
        defaultLang = Settings.getDefaultLang(this);
        
		if (currentLang == null || currentLang.equals("")) {
			currentLang = defaultLang;
		}
        
        createCursor();
        
        // cursorPosition will be -2 if it hasn't been stored yet
		if (cursorPosition == -2) {
			cursor.moveToFirst();
		} else {
			cursor.moveToPosition(cursorPosition);
		}
		cursorPosition = cursor.getPosition();
		
//      Typeface face=Typeface.createFromAsset(getAssets(), "fonts/sil-lateef/LateefRegOT.ttf");
//      Typeface face=Typeface.createFromAsset(getAssets(), "fonts/tahoma.ttf");
		Typeface face=Typeface.createFromAsset(getAssets(), "fonts/DejaVuSans.ttf");

		// set the typeface for the three TextViews within the ViewFlipper
        TextView leftView = (TextView)vf.findViewById(R.id.leftView);
        TextView centerView = (TextView)vf.findViewById(R.id.centerView);
        TextView rightView = (TextView)vf.findViewById(R.id.rightView);
        leftView.setTypeface(face);
        centerView.setTypeface(face);
        rightView.setTypeface(face);   
    }

	@Override
	protected void onStart() {
		// TODO Auto-generated method stub
		super.onStart();
		
		Log.d(TAG, "onStart called");
	}
    
	@Override
	protected void onResume() {
		super.onResume();
		
		Log.d(TAG, "onResume called");
		
		// whenever settings activity is called, android closes the database
		// cursor so it loses its position
//		cursor.moveToPosition(cursorPosition);
		
		// get the default card language again in case it's changed
		defaultLang = Settings.getDefaultLang(this);
		// show the first card (do it here in case default card language changed)
		loadCards();
	}
    
    @Override
    protected void onStop(){
    	// TODO Auto-generated method stub
    	super.onStop();
       
		Log.d(TAG, "onStop called");
    }
    
	@Override
	protected void onPause() {
		super.onPause();
		
		Log.d(TAG, "onPause called");
		
		// We need an Editor object to make preference changes.
		// All objects are from android.context.Context
		SharedPreferences settings = getSharedPreferences(PREFS_NAME, 0);
		SharedPreferences.Editor editor = settings.edit();
		editor.putInt("cursorPosition", cursorPosition);
		
		// Commit the edits!
		editor.commit();
	}

	@Override
	protected void onDestroy() {
		super.onDestroy();
		Log.d(TAG, "onDestroy called");
		
		// close the database helper so android doesn't whine
		helper.close();
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
    	case R.id.menu_about:
    		startActivity(new Intent(this, About.class));
    		return true;
    	case R.id.menu_exit:
    		finish();
    		return true;
    	case R.id.menu_settings:
    		startActivity(new Intent(this, Settings.class));
    		return true;
    	}
    	return false;
    }
    
	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
		Log.d(TAG, "onKeyDown: keycode=" + keyCode + ", event="
				+ event);
		switch (keyCode) {
		case KeyEvent.KEYCODE_DPAD_UP:
			break;
		case KeyEvent.KEYCODE_DPAD_DOWN:
			break;
		case KeyEvent.KEYCODE_DPAD_LEFT:
			prevCard();
			break;
		case KeyEvent.KEYCODE_DPAD_RIGHT:
			nextCard();
			break;
		case KeyEvent.KEYCODE_DPAD_CENTER:
			flipCard();
			break;
		default:
			return super.onKeyDown(keyCode, event);
		}
		return true;
	}
    
	private void createCursor() {
		// Perform a managed query. The Activity will handle closing
		// and re-querying the cursor when needed.
		SQLiteDatabase db = helper.getReadableDatabase();
		String[] FROM = { "english", "arabic" };
		cursor = db.query("words", FROM, null, null, null, null, null);
		startManagingCursor(cursor);
	}

	private Map<String, String> getWord(int thisPosition, boolean updatePosition) {
		Log.d(TAG, "getWord(position), cursorPosition: " + cursorPosition);

		cursor.moveToPosition(thisPosition);
		
		if (cursor.isAfterLast()) {
			cursor.moveToFirst();
			Log.d(TAG, "cursor.moveToFirst() called, position: " + cursor.getPosition());
		} else if (cursor.isBeforeFirst()) {
			cursor.moveToLast();
			Log.d(TAG, "cursor.moveToLast() called, position: " + cursor.getPosition());
		}
		// we don't want to update cursorPosition if we're getting the word for prev or next card
		if (updatePosition) {
			cursorPosition = cursor.getPosition();
		}
		
		Log.d(TAG, "getWord, cursorPosition: " + cursorPosition);
		
		Log.d(TAG, "getWord getting string");
		String english = cursor.getString(0);
		String arabic = cursor.getString(1);
		Log.d(TAG, "getWord got string");
		
		Map<String, String> thisWord = new HashMap<String, String>();
		
		thisWord.put("english", english);
		thisWord.put("arabic", arabic);
		
		Log.d(TAG, "getWord returning thisWord");
		return thisWord;
	}
	
	private Map<String, String> getWordAtPosition(int thisPosition) {
		return getWord(thisPosition, false);
	}
	
	private Map<String, String> getCurrentWord() {
		return getWord(cursorPosition, true);
	}
	
	private void showWord(TextView thisView, Map<String, String> thisWord, String thisLang) {
		Log.d(TAG, "showWord called, thisLang: " + thisLang);
		currentLang = thisLang;
		if (thisLang.equals("english")) {
			Log.d(TAG, "showWord, showing english");
			thisView.setTextSize(42f);
			thisView.setText(thisWord.get(thisLang));
		} else if (thisLang.equals("arabic")) {
			Log.d(TAG, "showWord, showing arabic");
			thisView.setTextSize(56f);
			thisView.setText(ArabicUtilities.reshape(thisWord.get(thisLang)));
		}
	}
	
	private void showWord(TextView thisView, Map<String, String> thisWord) {
		Log.d(TAG, "showWord called, defaultLang: " + defaultLang);
		showWord(thisView, thisWord, defaultLang);
	}
	
	private void flipCard() {
		if (currentLang.equals("english")) {
			showWord(currentView, currentWord, "arabic");
		} else if (currentLang.equals("arabic")) {
			showWord(currentView, currentWord, "english");
		}
	}
	
	private void loadCards() {
		Log.d(TAG, "loadCards called");
		//TextView thisView = (TextView) vf.getChildAt(vf.getDisplayedChild() -1);
		//vf.getChildAt(vf.getDisplayedChild() - 1); // previous
		//vf.getChildAt(vf.getDisplayedChild() + 1); // next
		
		ViewGroup currentLayout = (RelativeLayout)vf.getCurrentView();
//		int currentLayoutId = currentLayout.getId();
		currentView = (TextView) currentLayout.getChildAt(0);
		currentWord = getCurrentWord();
		showWord(currentView, currentWord);

		// TODO: pretty sure this won't work, but we'll need to figure it out at some point
/*		
		ViewGroup leftLayout = (RelativeLayout)findViewById(currentLayoutId - 1);
		TextView leftView = (TextView)leftLayout.getChildAt(0);
		Map<String, String> prevWord = getWordAtPosition(cursorPosition - 1);
		showWord(leftView, prevWord);
		
		ViewGroup rightLayout = (RelativeLayout)findViewById(currentLayoutId + 1);
		TextView rightView = (TextView)rightLayout.getChildAt(0);
		Map<String, String> nextWord = getWordAtPosition(cursorPosition + 1);
		showWord(rightView, nextWord);
*/
		
/*
		ViewGroup currentLayout = (RelativeLayout)vf.getCurrentView();
		
		vf.
		
		ViewGroup leftLayout = (RelativeLayout)vf.getLeft();
	
		
		ViewGroup thisLayout = (RelativeLayout)vf.getCurrentView();
//		int Id = thisView.getId();
//		Log.d(TAG, "onSingleTapUp: Id:" + Id);
		TextView thisView = (TextView) thisLayout.getChildAt(0);
		thisView.setText("success!");
*/

	}
	
	private void nextCard() {
    	vf.setInAnimation(slideLeftIn);
        vf.setOutAnimation(slideLeftOut);
    	vf.showNext();
    	cursorPosition++;
    	loadCards();
	}
	
	private void prevCard() {
    	vf.setInAnimation(slideRightIn);
        vf.setOutAnimation(slideRightOut);
    	vf.showPrevious();
    	cursorPosition--;
    	loadCards();
	}
	
    class MyGestureDetector extends SimpleOnGestureListener {
        @Override
        public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
            try {
                if (Math.abs(e1.getY() - e2.getY()) > SWIPE_MAX_OFF_PATH)
                    return false;
                // right to left swipe
                if(e1.getX() - e2.getX() > SWIPE_MIN_DISTANCE && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                	nextCard();
                	return true;
                }  else if (e2.getX() - e1.getX() > SWIPE_MIN_DISTANCE && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                	prevCard();
                	return true;
                }
            } catch (Exception e) {
                // nothing
            }
            return false;
        }

		@Override
		public boolean onSingleTapUp(MotionEvent e) {
			Log.d(TAG, "onSingleTapUp");
			flipCard();
			return true;
		}
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
    	Log.d(TAG, "onTouchEvent called");
        if (gestureDetector.onTouchEvent(event))
	        return true;
	    else
	    	return false;
    }
       
}
