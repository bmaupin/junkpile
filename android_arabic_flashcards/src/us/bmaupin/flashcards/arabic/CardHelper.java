package us.bmaupin.flashcards.arabic;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.util.Log;

public class CardHelper {
	private static final String TAG = "Cards";
	private DatabaseHelper helper;
	private SQLiteDatabase db;
	private Cursor cursor;
	private RankDatabaseHelper ranksHelper;
	private SQLiteDatabase ranksDb;
	private String currentCategory = "All";
	
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
		
		String[] columns = { "_ID", "english", "arabic" };
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
	}
	
	void loadCards(String category) {
		loadCards(category, null);
	}
	
	Map<Integer, Integer> loadRanks(List<Integer> currentCardIds) {
		Map<Integer, Integer> currentCardRanks = new HashMap<Integer, Integer>();
		String[] columns = { "rank" };
		
		for (int thisId : currentCardIds) {
			String selection = "_ID = " + thisId;
			this.cursor = db.query("ranks", columns, selection, null, null, null, null);
			int thisRank = cursor.getInt(0);
			currentCardRanks.put(thisId, thisRank);
		}
		
		return currentCardRanks;
	}
	
	// nextCard in arabicflashcards should prob be called something like showNextCard
	void nextCard() {
		
	}
}
