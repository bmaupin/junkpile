package us.bmaupin.flashcards.arabic;

// $Id$

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import android.content.Context;
import android.database.Cursor;
import android.database.CursorIndexOutOfBoundsException;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

public class CardHelper {
	private static final String TAG = "Cards";
	private DatabaseHelper helper;
	private SQLiteDatabase db;
	private Cursor cursor;
	private RankDatabaseHelper ranksHelper;
	private SQLiteDatabase ranksDb;
	private List<Map<String, String>> cardHistory = new ArrayList<Map<String, String>>();
	private String currentCategory = "All";
	private String currentSubCategory;
	private List<Integer> nullRanks = new ArrayList<Integer>();
	
	public CardHelper(Context context) {
/*		super();
		this.helper = helper;
		this.db = db;
		this.cursor = cursor;
		this.ranksHelper = ranksHelper;
		this.ranksDb = ranksDb;
		this.currentCategory = currentCategory;
*/	
		helper = new DatabaseHelper(context);
		db = helper.getReadableDatabase();
		
		ranksHelper = new RankDatabaseHelper(context);
		ranksDb = ranksHelper.getReadableDatabase();
//		createCursor();
	}
	
	public void close() {
		// clean up after ourselves
		ranksHelper.close();
		helper.close();
	}
	
	private void createCursor() {
		// Perform a managed query. The Activity will handle closing
		// and re-querying the cursor when needed.
//		SQLiteDatabase db = helper.getReadableDatabase();
		String[] FROM = { "english", "arabic" };
		cursor = db.query("words", FROM, null, null, null, null, null);
//		startManagingCursor(cursor);
	}
	
	// loadCards in arabicFlashcards should prob be called something like loadViews
	void loadCards() {
		List<Integer> currentCardIds = new ArrayList<Integer>();
		Map<Integer, Integer> currentCardRanks = new HashMap<Integer, Integer>();
		Map<Integer, Integer> currentCardWeights = new HashMap<Integer, Integer>();

// TODO: in the future, do we want to put all this into some kind of list/array?		
//		String[] columns = { "_ID", "english", "arabic" };
		String[] columns = { "_ID" };
		String selection = null;
		
		if (currentCategory.equals("Ahlan wa sahlan")) {
			selection = "aws_chapter = " + currentSubCategory;
		}
		
		cursor = db.query("words", columns, selection, null, null, null, null);
		cursor.moveToFirst();
		
//		while (cursor.moveToNext()) {
// TODO: for now, only get 5 cards
		for (int i=1; i<6; i++) {
			int thisId = cursor.getInt(0);
			currentCardIds.add(thisId);
// TESTING		
			cursor.moveToNext();
		}
		
		currentCardRanks = loadRanks(currentCardIds);

//		
		Log.d(TAG, "loadCards: currentCardRanks:");
		for (Map.Entry<Integer, Integer> entry : currentCardRanks.entrySet()) {
			Log.d(TAG, entry.getKey() + "\t" + entry.getValue());
		}
		
		currentCardWeights = buildWeights(currentCardRanks);

//		
		Log.d(TAG, "loadCards: currentCardWeights:");
		for (Map.Entry<Integer, Integer> entry : currentCardWeights.entrySet()) {
			Log.d(TAG, entry.getKey() + "\t" + entry.getValue());
		}
//		
		Log.d(TAG, "loadCards: nullRanks:");
		for (int thisID : nullRanks) {
			Log.d(TAG, "" + thisID);
		}
	}
	
	
	
	void loadCards(String category) {
		currentCategory = category;
		loadCards();
	}
	
	void loadCards(String category, String subCategory) {
		currentCategory = category;
		currentSubCategory = subCategory;
		loadCards();
	}
	
	Map<Integer, Integer> loadRanks(List<Integer> currentCardIds) {
		Map<Integer, Integer> currentCardRanks = new HashMap<Integer, Integer>();
		String[] columns = { "rank" };
		
		// for each card ID in current cards
		for (int thisId : currentCardIds) {
			String selection = "_ID = " + thisId;
			// get its rank
			cursor = ranksDb.query("ranks", columns, selection, null, null, null, null);
			cursor.moveToFirst();
			int thisRank = cursor.getInt(0);
			// put it in currentCardRanks
			currentCardRanks.put(thisId, thisRank);
		}
		
		return currentCardRanks;
	}
	
	Map<Integer, Integer> buildWeights(Map<Integer, Integer> currentCardRanks) {
		Map<Integer, Integer> currentCardWeights = new HashMap<Integer, Integer>();
		// initialize the running total of weights
		int runningTotal = 0;
		
		
		// first we need to sort the ranks
		currentCardRanks = sortByValue(currentCardRanks);
		
// TODO: iterate java map: http://stackoverflow.com/questions/1066589/java-iterate-through-hashmap
// TODO: sort java map: http://stackoverflow.com/questions/109383/how-to-sort-a-mapkey-value-on-the-values-in-java
		
		// for each card and its rank
		for (Map.Entry<Integer, Integer> entry : currentCardRanks.entrySet()) {
			// if it doesn't have a rank, add it to the list of cards with no rank
			if (entry.getValue().equals(0)) {
				nullRanks.add(entry.getKey());
			} else {
				runningTotal += entry.getValue();
				currentCardWeights.put(runningTotal, entry.getKey());
			}
		}
		
		return currentCardWeights;
	} 
	
	// nextCard in arabicflashcards should prob be called something like showNextCard
	Map<String, String> nextCard() {
		String[] columns = { "english", "arabic" };
		String selection = "_ID = ?";
		String[] selectionArgs = new String[1];
		int thisId;
		Map<String, String> thisCard = new HashMap<String, String>();
		
		if (!nullRanks.isEmpty()) {
			// remove the first element from the list
			thisId = nullRanks.remove(0);
			selectionArgs[0] = "" + thisId;
			this.cursor = ranksDb.query("ranks", columns, selection, selectionArgs, null, null, null);
			cursor.moveToFirst();
			
			String english = cursor.getString(0);
			String arabic = cursor.getString(1);

			thisCard.put("english", english);
			thisCard.put("arabic", arabic);
			
			// add word to the card history
			cardHistory.add(thisCard);
// TODO: implement else {  // select cards by rank
		// if we've no more cards
		} else {
			// load more
			loadCards();
			return nextCard();
		}
		
		return thisCard;
	}
	
	Map<String, String> prevCard() {
		if (!cardHistory.isEmpty()) {
			// return the last card
			return cardHistory.remove(cardHistory.size() - 1);
		// if cardHistory is empty
		} else {
// TODO: implement if cardHistory is empty	
			Map<String, String> thisCard = new HashMap<String, String>();
			thisCard.put("error", "no previous cards");
			return thisCard;
		}
	}
	
	// from http://stackoverflow.com/questions/109383/how-to-sort-a-mapkey-value-on-the-values-in-java
	static Map sortByValue(Map map) {
	     List list = new LinkedList(map.entrySet());
	     Collections.sort(list, new Comparator() {
	          public int compare(Object o1, Object o2) {
	               return ((Comparable) ((Map.Entry) (o1)).getValue())
	              .compareTo(((Map.Entry) (o2)).getValue());
	          }
	     });

	    Map result = new LinkedHashMap();
	    for (Iterator it = list.iterator(); it.hasNext();) {
	        Map.Entry entry = (Map.Entry)it.next();
	        result.put(entry.getKey(), entry.getValue());
	    }
	    return result;
	}
}
