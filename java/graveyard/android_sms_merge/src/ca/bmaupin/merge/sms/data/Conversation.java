package ca.bmaupin.merge.sms.data;

import android.content.AsyncQueryHandler;
import android.net.Uri;
import android.provider.Telephony.Threads;
import android.provider.Telephony.Sms.Conversations;

public class Conversation {
    public static final Uri sAllThreadsUri =
	    Threads.CONTENT_URI.buildUpon().appendQueryParameter("simple", "true").build();
	
	public static final String[] ALL_THREADS_PROJECTION = {
	    Threads._ID, Threads.DATE, Threads.MESSAGE_COUNT, Threads.RECIPIENT_IDS,
	    Threads.SNIPPET, Threads.SNIPPET_CHARSET, Threads.READ, Threads.ERROR,
	    Threads.HAS_ATTACHMENT
	};
	
	
    /**
     * Start a query for all conversations in the database on the specified
     * AsyncQueryHandler.
     *
     * @param handler An AsyncQueryHandler that will receive onQueryComplete
     *                upon completion of the query
     * @param token   The token that will be passed to onQueryComplete
     */
    public static void startQueryForAll(AsyncQueryHandler handler, int token) {
        handler.cancelOperation(token);

        // This query looks like this in the log:
        // I/Database(  147): elapsedTime4Sql|/data/data/com.android.providers.telephony/databases/
        // mmssms.db|2.253 ms|SELECT _id, date, message_count, recipient_ids, snippet, snippet_cs,
        // read, error, has_attachment FROM threads ORDER BY  date DESC

        startQuery(handler, token, null);
    }
    
    /**
     * Start a query for in the database on the specified AsyncQueryHandler with the specified
     * "where" clause.
     *
     * @param handler An AsyncQueryHandler that will receive onQueryComplete
     *                upon completion of the query
     * @param token   The token that will be passed to onQueryComplete
     * @param selection   A where clause (can be null) to select particular conv items.
     */
    public static void startQuery(AsyncQueryHandler handler, int token, String selection) {
        handler.cancelOperation(token);

        // This query looks like this in the log:
        // I/Database(  147): elapsedTime4Sql|/data/data/com.android.providers.telephony/databases/
        // mmssms.db|2.253 ms|SELECT _id, date, message_count, recipient_ids, snippet, snippet_cs,
        // read, error, has_attachment FROM threads ORDER BY  date DESC

        handler.startQuery(token, null, sAllThreadsUri,
                ALL_THREADS_PROJECTION, selection, null, Conversations.DEFAULT_SORT_ORDER);
    }
	
}
