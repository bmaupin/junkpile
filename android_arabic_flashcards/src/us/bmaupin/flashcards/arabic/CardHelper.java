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
import java.util.Random;

import android.content.ContentValues;
import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

public class CardHelper {
	private static final String TAG = "CardHelper";
	private DatabaseHelper wordsHelper;
	private SQLiteDatabase wordsDb;
	private Cursor cursor = null;
	private RankDatabaseHelper ranksHelper;
	private SQLiteDatabase ranksDb;
	private List<Integer> cardHistory = new ArrayList<Integer>();
	private int cardHistoryIndex = 0;
	private int rankedCardsShown = 0;
	private String currentCategory = "All";
	private String currentSubCategory;
	private List<Integer> currentRankedIds = new ArrayList<Integer>();
	private List<Integer> currentUnrankedIds = new ArrayList<Integer>();
	private WeightedRandomGenerator weightedCardIds;
	
	public CardHelper(Context context) {
		wordsHelper = new DatabaseHelper(context);
		wordsDb = wordsHelper.getReadableDatabase();
		
		ranksHelper = new RankDatabaseHelper(context);
		ranksDb = ranksHelper.getReadableDatabase();
	}
	
	public void close() {
		// clean up after ourselves
		cursor.close();
		ranksHelper.close();
		wordsHelper.close();
	}
	
	// loadCards in arabicFlashcards should prob be called something like loadViews
	private void loadCards(boolean categoryChanged) {
		Log.d(TAG, "loadCards called");
		List<Integer> currentCardIds = new ArrayList<Integer>();
		List<Integer> currentOrderedRanks = new ArrayList<Integer>();
		
		// these need to be emptied each time loadCards is called
		currentRankedIds.clear();
		currentUnrankedIds.clear();
		
		// create a new cursor if necessary
		if (categoryChanged || cursor == null || cursor.isClosed()) {
// TODO: in the future, do we want to put all this into some kind of list/array?		
//			String[] columns = { "_ID", "english", "arabic" };
			String[] columns = { "_ID" };
			String selection = null;
			
			if (currentCategory.equals("Ahlan wa sahlan")) {
				selection = "aws_chapter = " + currentSubCategory;
			}
			
			cursor = wordsDb.query("words", columns, selection, null, null, null, null);
			cursor.moveToFirst();
		}
		
// TODO: for now, only get 5 cards
		// only get 100 cards at a time
		for (int i=1; i<6; i++) {
			int thisId = cursor.getInt(0);
			currentCardIds.add(thisId);
			
// TODO: we're probably going to run into issues if we have, for instance, 103 cards on the second goaround
			// if there are no more cards to get
			if (!cursor.moveToNext()) {
				// close the cursor and move along
				cursor.close();
				break;
			}
		}
		
		currentOrderedRanks = loadRanks(currentCardIds);

		if (!currentOrderedRanks.isEmpty()) {
			weightedCardIds = new WeightedRandomGenerator(currentOrderedRanks);
		}
		
//		
		Log.d(TAG, "loadCards: currentOrderedRanks:");
		for (int thisRank : currentOrderedRanks) { 
			Log.d(TAG, "" + thisRank);
		}
//		
		Log.d(TAG, "loadCards: currentRankedIds:");
		for (int thisID : currentRankedIds) {
			Log.d(TAG, "" + thisID);
		}
//		
		Log.d(TAG, "loadCards: currentUnrankedIds:");
		for (int thisID : currentUnrankedIds) {
			Log.d(TAG, "" + thisID);
		}
	}
	
	void loadCategory(String category) {
		currentCategory = category;
		loadCards(true);
	}
	
	void loadCategory(String category, String subCategory) {
		currentCategory = category;
		currentSubCategory = subCategory;
		loadCards(true);
	}	
	
	private List<Integer> loadRanks(List<Integer> currentCardIds) {
		Map<Integer, Integer> currentCardRanks = new HashMap<Integer, Integer>();
		List<Integer> currentOrderedRanks = new ArrayList<Integer>();
		String[] columns = { "rank" };
		
		// for each card ID in current cards
		for (int thisId : currentCardIds) {
			String selection = "_ID = " + thisId;
			// get its rank
			Cursor thisCursor = ranksDb.query("ranks", columns, selection, null, null, null, null);
			thisCursor.moveToFirst();
			int thisRank = thisCursor.getInt(0);
			thisCursor.close();
			
			// if the rank for this particular card is 0
			if (thisRank == 0) {
				// add it to the list of cards with no rank
				currentUnrankedIds.add(thisId);
			} else {
				// put it in currentCardRanks
				currentCardRanks.put(thisId, thisRank);
			}
		}
		
		if (!currentCardRanks.isEmpty()) {
//			
			Log.d(TAG, "loadRanks: processing ranks");
			
			// the binary search function we'll be using later needs this to be sorted
			currentCardRanks = sortByValue(currentCardRanks);
			
			// for each card and its rank
			for (Map.Entry<Integer, Integer> entry : currentCardRanks.entrySet()) {
				// put the id into the list of ranked ids
				currentRankedIds.add(entry.getKey());
				// put the rank into the list of ranks
				currentOrderedRanks.add(entry.getValue());
			}
		}
			
		return currentOrderedRanks;
	}
	
	private class WeightedRandomGenerator {
		private List<Double> totals = new ArrayList<Double>();
		
		private WeightedRandomGenerator(List<Integer> weights) {
			double runningTotal = 0;
			
			for (int thisRank: weights) {
				runningTotal += thisRank;
				totals.add(runningTotal);
			}
		}
		
		private int next() {
			Random rnd = new Random(System.nanoTime());
			Double rndNum = rnd.nextDouble() * totals.get(totals.size() - 1);
			int sNum = Collections.binarySearch(totals, rndNum);
			int idx = (sNum < 0) ? (Math.abs(sNum) - 1) : sNum;
			return idx;
		}
	}
	
	private Map<String, String> getCard(int thisId) {
		Log.d(TAG, "getCard: thisId=" + thisId);
		
		String[] columns = { "english", "arabic" };
		String selection = "_ID = ?";
		String[] selectionArgs = new String[1];
		Map<String, String> thisCard = new HashMap<String, String>();
		
		selectionArgs[0] = "" + thisId;
		Cursor thisCursor = wordsDb.query("words", columns, selection, selectionArgs, null, null, null);
		thisCursor.moveToFirst();
		
		String english = thisCursor.getString(0);
		String arabic = thisCursor.getString(1);
		thisCursor.close();
		
		thisCard.put("ID", "" + thisId);
		thisCard.put("english", english);
		thisCard.put("arabic", arabic);
		
		// add word to the card history
		cardHistory.add(thisId);
		
		return thisCard;
	}
	
	private int getRank(String thisId) {
		String[] columns = { RankDatabaseHelper.RANK };
		String selection = "_ID = " + thisId;
		// get its rank
		Cursor thisCursor = ranksDb.query(RankDatabaseHelper.DB_TABLE_NAME, columns, selection, null, null, null, null);
		thisCursor.moveToFirst();
		int thisRank = thisCursor.getInt(0);
		thisCursor.close();
		return thisRank;
	}
	
	Map<String, String> nextCard() {
		Log.d(TAG, "nextCard called");
//		
		Log.d(TAG, "nextCard: cardHistoryIndex=" + cardHistoryIndex);
		
		// if we're going forward through the card history
		if (cardHistoryIndex > 0) {
			cardHistoryIndex --;
			// get the next card in the card history
			int thisId = cardHistory.get(cardHistory.size() - (cardHistoryIndex + 1));
			Map<String, String> thisCard = getCard(thisId);
// TODO: this seems messy; most of the time getCard is called, we want the rank...
			// update its rank
			thisCard.put("rank", "" + getRank(thisCard.get("ID")));
			// return it
			return thisCard;

		// if some of the selected cards don't have ranks, that means they 
		// haven't been shown yet, so show them
		} else if (!currentUnrankedIds.isEmpty()) {
			// remove the first element from the list
			int thisId = currentUnrankedIds.remove(0);
			Map<String, String> thisCard = getCard(thisId);
			thisCard.put("rank", "0");
			return thisCard;

		} else if (rankedCardsShown < currentRankedIds.size()) {
//			
			Log.d(TAG, "nextCard: rankedCardsShown=" + rankedCardsShown);
			Log.d(TAG, "nextCard: currentRankedIds.size()=" + currentRankedIds.size());
			Log.d(TAG, "nextCard: currentUnrankedIds.size()=" + currentUnrankedIds.size());
			
			int thisId = 0;

// TODO: we might need to make sure that there are more than 5 cards to show in the first place
			// try 5 times to get a card that isn't one of the last 5 shown
			for (int i=1; i<7; i++) {
//				
				Log.d(TAG, "nextCard: i=" + i);
				
				// on the 6th try
				if (i == 6) {
					Random rnd = new Random(System.nanoTime());
					// return a random card
					thisId = currentRankedIds.get((int)(rnd.nextDouble() * (currentRankedIds.size())));
					break;
				}
				
				// get the next weighted card ID
				thisId = currentRankedIds.get(weightedCardIds.next());
				
				// if there is no card history, then we're good to go
				if (cardHistory.size() == 0) {
					break;
				// make sure the card history is at least 5
				} else if (cardHistory.size() < 5) {
					// if it's less than 5, just make sure the card isn't in the history
					if (!cardHistory.contains(thisId)) {
						break;
					}
				// if this ID isn't one of the last 5 shown
				} else if (!cardHistory.subList(cardHistory.size() - 5, cardHistory.size()).contains(thisId)) {
					// show it
					break;
				}
			}
			
			Map<String, String> thisCard = getCard(thisId);
			// get its rank
			thisCard.put("rank", "" + getRank(thisCard.get("ID")));
			// increment the counter of ranked cards shown
			rankedCardsShown ++;
			// return it
			return thisCard;
			
		// if we've no more cards
		} else {
			// load more
			loadCards(false);
			// reset the counter of ranked cards shown
			rankedCardsShown = 0;
			return nextCard();
		}
		
//		return thisCard;
	}
	
	Map<String, String> prevCard() {
//
		Log.d(TAG, "prevCard: cardHistoryIndex=" + cardHistoryIndex);
		
		// if we have anything in card history
		if (cardHistory.size() > 1) {
			cardHistoryIndex ++;
			// get the previous card in the card history
			int thisId = cardHistory.get(cardHistory.size() - (cardHistoryIndex + 1));
			Map<String, String> thisCard = getCard(thisId);		
			// update its rank
			thisCard.put("rank", "" + getRank(thisCard.get("ID")));
			// return it
			return thisCard;
			
		// if cardHistory is empty
		} else {
// TODO: implement if cardHistory is empty
			Map<String, String> thisCard = new HashMap<String, String>();
			thisCard.put("error", "no previous cards");
			return thisCard;
		}
	}
	
	/**
	 * Update the rank of the current card
	 * @param currentCardId
	 * @param currentCardRank
	 * @param direction
	 */
	void updateRank(String currentCardId, int currentCardRank, String direction) {
		// if we're not going through the card history
		if (cardHistoryIndex < 1) {
			// update the card's rank
			if (direction == "right") {
				updateRankNormal(currentCardId, currentCardRank);
			} else if (direction == "up") {
				updateRankKnown(currentCardId);
			} else if (direction == "down") {
				updateRankNotKnown(currentCardId, currentCardRank);
			}
		}
	}
	
	/**
	 * Updates the rank of a card during a normal (right) swipe
	 * @param thisCardId
	 * @param thisCardRank
	 */
	private void updateRankNormal(String thisCardId, int thisCardRank) {
		/*
		String sql = "UPDATE " + RankDatabaseHelper.DB_TABLE_NAME + " SET " + 
				RankDatabaseHelper.RANK + " = " + RankDatabaseHelper.RANK + 
				" + 1 WHERE _ID = " + thisId; 
		
		ranksDb.execSQL(sql);
		
		/*
		String whereClause = "_ID = ?";
		String[] whereArgs = {thisId};
		
		ContentValues cv=new ContentValues();
		cv.put(RankDatabaseHelper.RANK, RankDatabaseHelper.RANK + "+ 1");
		
		ranksDb.update(RankDatabaseHelper.DB_TABLE_NAME, cv, whereClause, whereArgs);
		*/
		
		int newCardRank;
		
		// don't go any lower than 2; 1 is reserved for cards we know
		if (thisCardRank == 1 || thisCardRank == 2) {
			return;
		// if a card is unranked, set the default starting rank to 20
		} else if (thisCardRank == 0) {
			newCardRank = 20;
		// reduce the rank by 1
		} else {
			newCardRank = thisCardRank - 1;
		}
		
		String whereClause = "_ID = ?";
		String[] whereArgs = {thisCardId};
		
		ContentValues cv=new ContentValues();
		cv.put(RankDatabaseHelper.RANK, newCardRank);
		
		ranksDb.update(RankDatabaseHelper.DB_TABLE_NAME, cv, whereClause, whereArgs);
	}
	
	/**
	 * Updates the rank of a card marked as "known"
	 * @param thisCardId
	 * @param thisCardRank
	 */
	private void updateRankKnown(String thisCardId) {
		String whereClause = "_ID = ?";
		String[] whereArgs = {thisCardId};
		
		ContentValues cv=new ContentValues();
		// set the rank to 1
		cv.put(RankDatabaseHelper.RANK, 1);
		
		ranksDb.update(RankDatabaseHelper.DB_TABLE_NAME, cv, whereClause, whereArgs);
	}
	
	/**
	 * Updates the rank of a card marked as "not known"
	 * @param thisCardId
	 * @param thisCardRank
	 */
	private void updateRankNotKnown(String thisCardId, int thisCardRank) {
		// if a card is unranked, set the default starting rank to 20
		if (thisCardRank == 0) {
			thisCardRank = 20;
		}
		// increase the rank by 2
		thisCardRank = thisCardRank + 2;
		
		String whereClause = "_ID = ?";
		String[] whereArgs = {thisCardId};
		
		ContentValues cv=new ContentValues();
		cv.put(RankDatabaseHelper.RANK, thisCardRank);
		
		ranksDb.update(RankDatabaseHelper.DB_TABLE_NAME, cv, whereClause, whereArgs);
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
