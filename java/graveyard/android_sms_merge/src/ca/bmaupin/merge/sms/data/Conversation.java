/*
 * Derived from com.android.mms.data.Conversation
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.data;

import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import android.content.AsyncQueryHandler;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.provider.Telephony.Sms.Conversations;
import android.provider.Telephony.Threads;
import android.text.TextUtils;
import android.util.Log;
import ca.bmaupin.merge.sms.LogTag;
import ca.bmaupin.merge.sms.R;

public class Conversation {
    private static final String TAG = "Mms/conv";
	private static final boolean DEBUG = false;
	
    public static final Uri sAllThreadsUri =
            Threads.CONTENT_URI.buildUpon().appendQueryParameter("simple", "true").build();

    public static final String[] ALL_THREADS_PROJECTION = {
        Threads._ID, Threads.DATE, Threads.MESSAGE_COUNT, Threads.RECIPIENT_IDS,
        Threads.SNIPPET, Threads.SNIPPET_CHARSET, Threads.READ, Threads.ERROR,
        Threads.HAS_ATTACHMENT
    };
	
    private static final int ID             = 0;
    private static final int DATE           = 1;
    private static final int MESSAGE_COUNT  = 2;
    private static final int RECIPIENT_IDS  = 3;
    private static final int SNIPPET        = 4;
    private static final int HAS_ATTACHMENT = 8;
	
	private final Context mContext;
	
    // The thread ID of this conversation.  Can be zero in the case of a
    // new conversation where the recipient set is changing as the user
    // types and we have not hit the database yet to create a thread.
    private long mThreadId;

    private ContactList mRecipients;    // The current set of recipients.
    private long mDate;                 // The last update time.
    private int mMessageCount;          // Number of messages.
    private String mSnippet;            // Text of the most recent message.
    private boolean mHasAttachment;     // True if any message has an attachment.
	
    private static boolean sLoadingThreads;
    
    public Conversation(Context context, Cursor cursor, boolean allowQuery) {
        if (DEBUG) {
            Log.v(TAG, "Conversation constructor cursor, allowQuery: " + allowQuery);
        }
        mContext = context;
        fillFromCursor(context, this, cursor, allowQuery);
    }
    
    /**
     * Returns a temporary Conversation (not representing one on disk) wrapping
     * the contents of the provided cursor.  The cursor should be the one
     * returned to your AsyncQueryHandler passed in to {@link #startQueryForAll}.
     * The recipient list of this conversation can be empty if the results
     * were not in cache.
     */
    public static Conversation from(Context context, Cursor cursor) {
        // First look in the cache for the Conversation and return that one. That way, all the
        // people that are looking at the cached copy will get updated when fillFromCursor() is
        // called with this cursor.
        long threadId = cursor.getLong(ID);
        if (threadId > 0) {
            Conversation conv = Cache.get(threadId);
            if (conv != null) {
                fillFromCursor(context, conv, cursor, false);   // update the existing conv in-place
                return conv;
            }
        }
        Conversation conv = new Conversation(context, cursor, false);
        try {
            Cache.put(conv);
        } catch (IllegalStateException e) {
            LogTag.error(TAG, "Tried to add duplicate Conversation to Cache (from cursor): " +
                    conv);
            if (!Cache.replace(conv)) {
                LogTag.error("Converations.from cache.replace failed on " + conv);
            }
        }
        return conv;
    }
    
    /**
     * Returns the thread ID of this conversation.  Can be zero if
     * {@link #ensureThreadId} has not been called yet.
     */
    public synchronized long getThreadId() {
        return mThreadId;
    }
    
    /**
     * Returns the recipient set of this conversation.
     */
    public synchronized ContactList getRecipients() {
        return mRecipients;
    }
    
    /**
     * Returns the time of the last update to this conversation in milliseconds,
     * on the {@link System#currentTimeMillis} timebase.
     */
    public synchronized long getDate() {
        return mDate;
    }
    
    /**
     * Returns the number of messages in this conversation, excluding the draft
     * (if it exists).
     */
    public synchronized int getMessageCount() {
        return mMessageCount;
    }
    
    /**
     * Returns a snippet of text from the most recent message in the conversation.
     */
    public synchronized String getSnippet() {
        return mSnippet;
    }
    
    /**
     * Returns true if any messages in the conversation have attachments.
     */
    public synchronized boolean hasAttachment() {
        return mHasAttachment;
    }
    
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
    
    /**
     * Fill the specified conversation with the values from the specified
     * cursor, possibly setting recipients to empty if {@value allowQuery}
     * is false and the recipient IDs are not in cache.  The cursor should
     * be one made via {@link #startQueryForAll}.
     */
    private static void fillFromCursor(Context context, Conversation conv,
                                       Cursor c, boolean allowQuery) {
        synchronized (conv) {
            conv.mThreadId = c.getLong(ID);
            conv.mDate = c.getLong(DATE);
            conv.mMessageCount = c.getInt(MESSAGE_COUNT);

            // Replace the snippet with a default value if it's empty.
            String snippet = c.getString(SNIPPET);
            if (TextUtils.isEmpty(snippet)) {
                snippet = context.getString(R.string.no_subject_view);
            }
            conv.mSnippet = snippet;

            conv.mHasAttachment = (c.getInt(HAS_ATTACHMENT) != 0);
        }
        // Fill in as much of the conversation as we can before doing the slow stuff of looking
        // up the contacts associated with this conversation.
        String recipientIds = c.getString(RECIPIENT_IDS);
        ContactList recipients = ContactList.getByIds(recipientIds, allowQuery);
        synchronized (conv) {
            conv.mRecipients = recipients;
        }

        if (Log.isLoggable(LogTag.THREAD_CACHE, Log.VERBOSE)) {
            Log.d(TAG, "fillFromCursor: conv=" + conv + ", recipientIds=" + recipientIds);
        }
    }
    
    /**
     * Private cache for the use of the various forms of Conversation.get.
     */
    private static class Cache {
        private static Cache sInstance = new Cache();
        static Cache getInstance() { return sInstance; }
        private final HashSet<Conversation> mCache;
        private Cache() {
            mCache = new HashSet<Conversation>(10);
        }

        /**
         * Return the conversation with the specified thread ID, or
         * null if it's not in cache.
         */
        static Conversation get(long threadId) {
            synchronized (sInstance) {
                if (Log.isLoggable(LogTag.THREAD_CACHE, Log.VERBOSE)) {
                    LogTag.debug("Conversation get with threadId: " + threadId);
                }
                for (Conversation c : sInstance.mCache) {
                    if (DEBUG) {
                        LogTag.debug("Conversation get() threadId: " + threadId +
                                " c.getThreadId(): " + c.getThreadId());
                    }
                    if (c.getThreadId() == threadId) {
                        return c;
                    }
                }
            }
            return null;
        }
        
        /**
         * Put the specified conversation in the cache.  The caller
         * should not place an already-existing conversation in the
         * cache, but rather update it in place.
         */
        static void put(Conversation c) {
            synchronized (sInstance) {
                // We update cache entries in place so people with long-
                // held references get updated.
                if (Log.isLoggable(LogTag.THREAD_CACHE, Log.VERBOSE)) {
                    Log.d(TAG, "Conversation.Cache.put: conv= " + c + ", hash: " + c.hashCode());
                }

                if (sInstance.mCache.contains(c)) {
                    if (DEBUG) {
                        dumpCache();
                    }
                    throw new IllegalStateException("cache already contains " + c +
                            " threadId: " + c.mThreadId);
                }
                sInstance.mCache.add(c);
            }
        }
        
        /**
         * Replace the specified conversation in the cache. This is used in cases where we
         * lookup a conversation in the cache by threadId, but don't find it. The caller
         * then builds a new conversation (from the cursor) and tries to add it, but gets
         * an exception that the conversation is already in the cache, because the hash
         * is based on the recipients and it's there under a stale threadId. In this function
         * we remove the stale entry and add the new one. Returns true if the operation is
         * successful
         */
        static boolean replace(Conversation c) {
            synchronized (sInstance) {
                if (Log.isLoggable(LogTag.THREAD_CACHE, Log.VERBOSE)) {
                    LogTag.debug("Conversation.Cache.put: conv= " + c + ", hash: " + c.hashCode());
                }

                if (!sInstance.mCache.contains(c)) {
                    if (DEBUG) {
                        dumpCache();
                    }
                    return false;
                }
                // Here it looks like we're simply removing and then re-adding the same object
                // to the hashset. Because the hashkey is the conversation's recipients, and not
                // the thread id, we'll actually remove the object with the stale threadId and
                // then add the the conversation with updated threadId, both having the same
                // recipients.
                sInstance.mCache.remove(c);
                sInstance.mCache.add(c);
                return true;
            }
        }
        
        static void dumpCache() {
            synchronized (sInstance) {
                LogTag.debug("Conversation dumpCache: ");
                for (Conversation c : sInstance.mCache) {
                    LogTag.debug("   conv: " + c.toString() + " hash: " + c.hashCode());
                }
            }
        }
        
        /**
         * Remove all conversations from the cache that are not in
         * the provided set of thread IDs.
         */
        static void keepOnly(Set<Long> threads) {
            synchronized (sInstance) {
                Iterator<Conversation> iter = sInstance.mCache.iterator();
                while (iter.hasNext()) {
                    Conversation c = iter.next();
                    if (!threads.contains(c.getThreadId())) {
                        iter.remove();
                    }
                }
            }
            if (DEBUG) {
                LogTag.debug("after keepOnly");
                dumpCache();
            }
        }
    }
    
    /**
     * Set up the conversation cache.  To be called once at application
     * startup time.
     */
    public static void init(final Context context) {
        Thread thread = new Thread(new Runnable() {
                @Override
                public void run() {
                    cacheAllThreads(context);
                }
            }, "Conversation.init");
        thread.setPriority(Thread.MIN_PRIORITY);
        thread.start();
    }
    
    /**
     * Are we in the process of loading and caching all the threads?.
     */
    public static boolean loadingThreads() {
        synchronized (Cache.getInstance()) {
            return sLoadingThreads;
        }
    }
    
    private static void cacheAllThreads(Context context) {
        if (Log.isLoggable(LogTag.THREAD_CACHE, Log.VERBOSE)) {
            LogTag.debug("[Conversation] cacheAllThreads: begin");
        }
        synchronized (Cache.getInstance()) {
            if (sLoadingThreads) {
                return;
                }
            sLoadingThreads = true;
        }

        // Keep track of what threads are now on disk so we
        // can discard anything removed from the cache.
        HashSet<Long> threadsOnDisk = new HashSet<Long>();

        // Query for all conversations.
        Cursor c = context.getContentResolver().query(sAllThreadsUri,
                ALL_THREADS_PROJECTION, null, null, null);
        try {
            if (c != null) {
                while (c.moveToNext()) {
                    long threadId = c.getLong(ID);
                    threadsOnDisk.add(threadId);

                    // Try to find this thread ID in the cache.
                    Conversation conv;
                    synchronized (Cache.getInstance()) {
                        conv = Cache.get(threadId);
                    }

                    if (conv == null) {
                        // Make a new Conversation and put it in
                        // the cache if necessary.
                        conv = new Conversation(context, c, true);
                        try {
                            synchronized (Cache.getInstance()) {
                                Cache.put(conv);
                            }
                        } catch (IllegalStateException e) {
                            LogTag.error("Tried to add duplicate Conversation to Cache" +
                                    " for threadId: " + threadId + " new conv: " + conv);
                            if (!Cache.replace(conv)) {
                                LogTag.error("cacheAllThreads cache.replace failed on " + conv);
                            }
                        }
                    } else {
                        // Or update in place so people with references
                        // to conversations get updated too.
                        fillFromCursor(context, conv, c, true);
                    }
                }
            }
        } finally {
            if (c != null) {
                c.close();
            }
            synchronized (Cache.getInstance()) {
                sLoadingThreads = false;
            }
        }

        // Purge the cache of threads that no longer exist on disk.
        Cache.keepOnly(threadsOnDisk);

        if (Log.isLoggable(LogTag.THREAD_CACHE, Log.VERBOSE)) {
            LogTag.debug("[Conversation] cacheAllThreads: finished");
            Cache.dumpCache();
        }
    }
}
