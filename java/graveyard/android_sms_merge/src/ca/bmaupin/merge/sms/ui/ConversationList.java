/*
 * Derived from com.android.mms.ui.ConversationList
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import com.android.mms.MmsConfig;
import com.android.mms.util.DraftCache;

import ca.bmaupin.merge.sms.R;
import ca.bmaupin.merge.sms.data.Contact;
import ca.bmaupin.merge.sms.data.Conversation;
import android.app.ListActivity;
import android.content.AsyncQueryHandler;
import android.content.ContentResolver;
import android.database.Cursor;
import android.database.sqlite.SQLiteException;
import android.database.sqlite.SqliteWrapper;
import android.os.Bundle;
import android.view.View;
import android.widget.ListView;
import android.widget.TextView;

public class ConversationList extends ListActivity {
    private static final int THREAD_LIST_QUERY_TOKEN       = 1701;
	
    private ThreadListQueryHandler mQueryHandler;
    private ConversationListAdapter mListAdapter;
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.conversation_list_screen);
        
        ListView listView = getListView();
        
        // Tell the list view which view to display when the list is empty
        listView.setEmptyView(findViewById(R.id.empty));

        initListAdapter();
    }
    
    @Override
    public void onPause() {
        super.onPause();

        // Don't listen for changes while we're paused.
        mListAdapter.setOnContentChangedListener(null);
    }
    
    @Override
    protected void onResume() {
        super.onResume();

        mListAdapter.setOnContentChangedListener(mContentChangedListener);
    }
    
    private final ConversationListAdapter.OnContentChangedListener mContentChangedListener =
            new ConversationListAdapter.OnContentChangedListener() {
            @Override
            public void onContentChanged(ConversationListAdapter adapter) {
                startAsyncQuery();
            }
        };

    private void initListAdapter() {
        mListAdapter = new ConversationListAdapter(this, null);
        mListAdapter.setOnContentChangedListener(mContentChangedListener);
        setListAdapter(mListAdapter);
        getListView().setRecyclerListener(mListAdapter);
    }
    
    @Override
    protected void onStart() {
        super.onStart();

        startAsyncQuery();

        // we invalidate the contact cache here because we want to get updated presence
        // and any contact changes. We don't invalidate the cache by observing presence and contact
        // changes (since that's too untargeted), so as a tradeoff we do it here.
        // If we're in the middle of the app initialization where we're loading the conversation
        // threads, don't invalidate the cache because we're in the process of building it.
        // TODO: think of a better way to invalidate cache more surgically or based on actual
        // TODO: changes we care about
        if (!Conversation.loadingThreads()) {
            Contact.invalidateCache();
        }
    }
    
    @Override
    protected void onStop() {
        super.onStop();

        // Close the cursor in the ListAdapter if the activity stopped.
        Cursor cursor = mListAdapter.getCursor();
        
        if (cursor != null && !cursor.isClosed()) {
            cursor.close();
        }

        mListAdapter.changeCursor(null);
    }
    
    private void startAsyncQuery() {
        try {
            ((TextView)(getListView().getEmptyView())).setText(R.string.loading_conversations);

            Conversation.startQueryForAll(mQueryHandler, THREAD_LIST_QUERY_TOKEN);
        } catch (SQLiteException e) {
            SqliteWrapper.checkSQLiteException(this, e);
        }
    }
    
    private final class ThreadListQueryHandler extends AsyncQueryHandler {
        public ThreadListQueryHandler(ContentResolver contentResolver) {
            super(contentResolver);
        }
    }
}
