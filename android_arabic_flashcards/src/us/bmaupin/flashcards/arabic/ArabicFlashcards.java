package us.bmaupin.flashcards.arabic;

// $Id$

import java.util.Map;

import org.amr.arabic.ArabicUtilities;

import android.app.Activity;
import android.content.Intent;
import android.content.SharedPreferences;
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
	String selectedChapter;
	public static final String PREFS_NAME = "FlashcardPrefsFile";
	private static final int GET_CATEGORY = 0;
	private CardHelper ch;
//	private DatabaseHelper helper;
//	private SQLiteDatabase db;
// TODO: do we want to remember last card position?  card ID would probably be more
//	universal than cursor position
//	private int cursorPosition;
//	private Cursor cursor;
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
    
    private String currentCardId;
    private int currentCardRank;
    private TextView currentView;
    private Map<String, String> currentWord;

	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	Log.d(TAG, "onCreate called");
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
//        test();
        
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
        
    	ch = new CardHelper(this);
        
//        helper = new DatabaseHelper(this);
//        db = helper.getReadableDatabase();
        
		// Restore preferences
        settings = getSharedPreferences(PREFS_NAME, 0);
//        cursorPosition = settings.getInt("cursorPosition", -2);
//        Log.d(TAG, "onCreate, cursorPosition: " + cursorPosition);
        
        defaultLang = Settings.getDefaultLang(this);
        
		if (currentLang == null || currentLang.equals("")) {
			currentLang = defaultLang;
		}
        
//        createCursor();
        
        // cursorPosition will be -2 if it hasn't been stored yet
//		if (cursorPosition == -2) {
//			cursor.moveToFirst();
//		} else {
//			cursor.moveToPosition(cursorPosition);
//		}
//		cursorPosition = cursor.getPosition();
		
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
		
//		ch.loadCards();
		
		// get the default card language again in case it's changed
		defaultLang = Settings.getDefaultLang(this);
		// show the first card (do it here in case default card language changed)
//		loadViews();
// TODO: show the last saved card instead of the next card?
		showFirstCard();
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
//		editor.putInt("cursorPosition", cursorPosition);
		
		// Commit the edits!
		editor.commit();
	}

	@Override
	protected void onDestroy() {
		super.onDestroy();
		Log.d(TAG, "onDestroy called");
		
		// close the database helper so android doesn't whine
//		helper.close();
		ch.close();
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
    	case R.id.menu_categories:
    		Intent intent = new Intent(this, Categories.class);
    		startActivityForResult(intent, GET_CATEGORY);
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
	protected void onActivityResult(int requestCode, int resultCode, Intent data) {
		// TODO Auto-generated method stub
		super.onActivityResult(requestCode, resultCode, data);
		
		switch(requestCode) {
			case (GET_CATEGORY) : {
				if (resultCode == Activity.RESULT_OK) {
					String category = data.getStringExtra("category");
					Log.d(TAG, "onActivityResult: category=" + category);
					
					if (category.equals("Ahlan wa sahlan")) {
						String chapter = data.getStringExtra("aws_chapter");
						Log.d(TAG, "onActivityResult: chapter=" + chapter);

						ch.loadCategory(category, chapter);
					}
				}
				break;
			}
		}
	}

	@Override
	public boolean onKeyDown(int keyCode, KeyEvent event) {
		Log.d(TAG, "onKeyDown: keycode=" + keyCode + ", event="
				+ event);
		switch (keyCode) {
		case KeyEvent.KEYCODE_DPAD_UP:
			showNextCard("up");
			break;
		case KeyEvent.KEYCODE_DPAD_DOWN:
			showNextCard("down");
			break;
		case KeyEvent.KEYCODE_DPAD_LEFT:
			showPrevCard();
			break;
		case KeyEvent.KEYCODE_DPAD_RIGHT:
			showNextCard("right");
			break;
		case KeyEvent.KEYCODE_DPAD_CENTER:
			flipCard();
			break;
		default:
			return super.onKeyDown(keyCode, event);
		}
		return true;
	}
    
	/*
	private void createCursor() {
		// Perform a managed query. The Activity will handle closing
		// and re-querying the cursor when needed.
//		SQLiteDatabase db = helper.getReadableDatabase();
		String[] FROM = { "english", "arabic" };
		cursor = db.query("words", FROM, null, null, null, null, null);
		startManagingCursor(cursor);
	}
	*/
	/*
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
	/*
	private Map<String, String> getWordAtPosition(int thisPosition) {
		return getWord(thisPosition, false);
	}
	*/
	/*
	private Map<String, String> getCurrentWord() {
		return getWord(cursorPosition, true);
	}
	*/
	
	/**
	 * Given a view, a word, and a language, shows the word in the view and 
	 * formats it depending on the language
	 */
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
	
	/*
	private void loadViews() {
		Log.d(TAG, "loadViews called");
		//TextView thisView = (TextView) vf.getChildAt(vf.getDisplayedChild() -1);
		//vf.getChildAt(vf.getDisplayedChild() - 1); // previous
		//vf.getChildAt(vf.getDisplayedChild() + 1); // next
		
		ViewGroup currentLayout = (RelativeLayout)vf.getCurrentView();
//		int currentLayoutId = currentLayout.getId();
		currentView = (TextView) currentLayout.getChildAt(0);
// TODO: get current (prob next) card
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
/*
	}
*/
	/*
	private void showNextCard() {
    	vf.setInAnimation(slideLeftIn);
        vf.setOutAnimation(slideLeftOut);
    	vf.showNext();
// TODO: get next card
    	cursorPosition++;
    	loadViews();
	}
	
	private void showPrevCard() {
    	vf.setInAnimation(slideRightIn);
        vf.setOutAnimation(slideRightOut);
    	vf.showPrevious();
// TODO: get previous card    	
    	cursorPosition--;
    	loadViews();
	}
	*/

	private void showFirstCard() {
		currentWord = ch.nextCard();
    	// store the ID and rank of the current Word
    	currentCardId = currentWord.get("ID");
    	currentCardRank = stringToInteger(currentWord.get("rank"));
    	
//
    	Log.d(TAG, "showNextCard: currentWord=" + currentWord);
    	ViewGroup currentLayout = (RelativeLayout)vf.getCurrentView();
    	currentView = (TextView) currentLayout.getChildAt(0);
    	showWord(currentView, currentWord);
	}
	
	private void showNextCard(String direction) {
    	vf.setInAnimation(slideLeftIn);
        vf.setOutAnimation(slideLeftOut);
    	vf.showNext();
    	
    	// update the rank of the current card
    	ch.updateRank(currentCardId, currentCardRank, direction);
    	// get the next one
    	currentWord = ch.nextCard();
    	
    	// store the ID and rank of the current Word
    	currentCardId = currentWord.get("ID");
    	currentCardRank = stringToInteger(currentWord.get("rank"));
    	
//
    	Log.d(TAG, "showNextCard: currentWord=" + currentWord);
    	ViewGroup currentLayout = (RelativeLayout)vf.getCurrentView();
    	currentView = (TextView) currentLayout.getChildAt(0);
    	showWord(currentView, currentWord);
	}
	
	private void showPrevCard() {
    	vf.setInAnimation(slideRightIn);
        vf.setOutAnimation(slideRightOut);
    	vf.showPrevious();
    	
    	currentWord = ch.prevCard();
    	// store the ID and rank of the current Word
    	currentCardId = currentWord.get("ID");
    	currentCardRank = stringToInteger(currentWord.get("rank"));
    	
//
    	Log.d(TAG, "showNextCard: currentWord=" + currentWord);
    	ViewGroup currentLayout = (RelativeLayout)vf.getCurrentView();
    	currentView = (TextView) currentLayout.getChildAt(0);
    	showWord(currentView, currentWord);
	}
	
    class MyGestureDetector extends SimpleOnGestureListener {
        @Override
        public boolean onFling(MotionEvent e1, MotionEvent e2, float velocityX, float velocityY) {
            try {
            	/*
                if (Math.abs(e1.getY() - e2.getY()) > SWIPE_MAX_OFF_PATH)
                    return false;
                // right to left swipe
                if(e1.getX() - e2.getX() > SWIPE_MIN_DISTANCE && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                	showNextCard();
                	return true;
                }  else if (e2.getX() - e1.getX() > SWIPE_MIN_DISTANCE && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                	showPrevCard();
                	return true;
                }
                */
            	// from http://stackoverflow.com/questions/4098198/adding-fling-gesture-to-an-image-view-android
            	// right to left
                if(e1.getX() - e2.getX() > SWIPE_MIN_DISTANCE && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                	showNextCard("right");
                	return true;
                // left to right
                }  else if (e2.getX() - e1.getX() > SWIPE_MIN_DISTANCE && Math.abs(velocityX) > SWIPE_THRESHOLD_VELOCITY) {
                	showPrevCard();
                	return true;
                }
                // bottom to top
                if(e1.getY() - e2.getY() > SWIPE_MIN_DISTANCE && Math.abs(velocityY) > SWIPE_THRESHOLD_VELOCITY) {
//                	Toast.makeText(getApplicationContext(), "TODO: swiped up", Toast.LENGTH_SHORT).show();
                	showNextCard("up");
                    return true;
                // top to bottom
                }  else if (e2.getY() - e1.getY() > SWIPE_MIN_DISTANCE && Math.abs(velocityY) > SWIPE_THRESHOLD_VELOCITY) {
//                	Toast.makeText(getApplicationContext(), "TODO: swiped down", Toast.LENGTH_SHORT).show();
                	showNextCard("down");
                	return true;
                }
                return false;
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
    
    /*
    private void test() {
    	CardHelper ch = new CardHelper(this);
    	ch.loadCategory("Ahlan wa sahlan", "3");
    	ch.close();
    	/*
        RankDatabaseHelper ranksHelper = new RankDatabaseHelper(this);
        SQLiteDatabase ranksDb = ranksHelper.getReadableDatabase();
        ranksHelper.initializeDb(ranksDb, 5);
        ranksHelper.close();
        
    }
	*/
    
    int stringToInteger(String s) {
    	try {
    		int i = Integer.parseInt(s.trim());
    		return i;
    	} catch (NumberFormatException e) {
    		Log.d(TAG, "stringToInteger: error: " + e.getMessage());
    		return 0;
    	}
    }
}
