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
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteException;
import android.util.Log;

public class CardHelper {
	private static final String TAG = "Cards";
	private DatabaseHelper helper;
	private SQLiteDatabase db;
	private Cursor cursor;
	private RankDatabaseHelper ranksHelper;
	private SQLiteDatabase ranksDb;
	private String currentCategory = "All";
	private List<Integer> nullRanks;
	
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
		
		RankDatabaseHelper ranksHelper = new RankDatabaseHelper(context);
		ranksDb = ranksHelper.getReadableDatabase();
//		createCursor();
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
	void loadCards(String category, String subCategory) {
		List<Integer> currentCardIds = new ArrayList<Integer>();
		Map<Integer, Integer> currentCardRanks = new HashMap<Integer, Integer>();
		Map<Integer, Integer> currentCardWeights = new HashMap<Integer, Integer>();

// TODO: in the future, do we want to put all this into some kind of list/array?		
//		String[] columns = { "_ID", "english", "arabic" };
		String[] columns = { "_ID" };
		String selection = null;
		
		if (category.equals("Ahlan wa sahlan")) {
			selection = "aws_chapter = " + subCategory;
		}
		
		cursor = db.query("words", columns, selection, null, null, null, null);
		
// TODO: for now, only get 5 cards		
		for (int i=1; i<6; i++) {
			cursor.moveToFirst();
			int thisId = cursor.getInt(0);
			currentCardIds.add(thisId);
			cursor.moveToFirst();
		}
		
		currentCardRanks = loadRanks(currentCardIds);
		
		Log.d(TAG, "loadCards");
		for (Map.Entry<Integer, Integer> entry : currentCardRanks.entrySet()) {
			Log.d(TAG, entry.getKey() + "\t" + entry.getValue());
		}
		
//		currentCardWeights = buildWeights(currentCardRanks);
	}
	
	
	
	void loadCards(String category) {
		loadCards(category, null);
	}
	
	Map<Integer, Integer> loadRanks(List<Integer> currentCardIds) {
		Map<Integer, Integer> currentCardRanks = new HashMap<Integer, Integer>();
		String[] columns = { "rank" };
		
		for (int thisId : currentCardIds) {
			String selection = "_ID = " + thisId;
//			try {
				this.cursor = ranksDb.query("ranks", columns, selection, null, null, null, null);
//			} catch (SQLiteException e) {
//				Log.d(TAG, "loadCards: SQLiteException: " + e.getMessage());
//			}
// TODO: implement CursorIndexOutOfBoundsException handling here?				
//			try {
				cursor.moveToFirst();
//			} catch 
			int thisRank = cursor.getInt(0);
			currentCardRanks.put(thisId, thisRank);
		}
		
		return currentCardRanks;
	}
	
	/*
	Map<Integer, Integer> buildWeights(Map<Integer, Integer> currentCardRanks) {
		Map<Integer, Double> currentCardWeights = new HashMap<Integer, Double>();
//		List<Double> totals = new ArrayList<Double>();
		
//		Iterator it = currentCardRanks.keySet().iterator();
		
		// initialize the running total of weights
		double runningTotal = 0;
		
// TODO: we need to sort the currentCardRanks first		
		
// TODO: iterate java map: http://stackoverflow.com/questions/1066589/java-iterate-through-hashmap
// TODO: sort java map: http://stackoverflow.com/questions/109383/how-to-sort-a-mapkey-value-on-the-values-in-java
		
		// for each card and its rank
		for (Map.Entry<Integer, Integer> entry : currentCardRanks.entrySet()) {
			// if it doesn't have a rank, add it to the list of cards with no rank
			if (entry.getValue() == null) {
				nullRanks.add(entry.getKey());
			} else {
//				runningTotal += entry.getValue();
				currentCardWeights.put()
			}
			
			/*
			String selection = "_ID = " + thisId;
			this.cursor = db.query("ranks", columns, selection, null, null, null, null);
			int thisRank = cursor.getInt(0);
			currentCardRanks.put(thisId, thisRank);
			
		}
		
		return currentCardWeights;
	}
	*/
	
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
	
	// nextCard in arabicflashcards should prob be called something like showNextCard
	void nextCard() {
		
	}
}
