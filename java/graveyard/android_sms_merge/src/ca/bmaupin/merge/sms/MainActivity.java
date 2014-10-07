package ca.bmaupin.merge.sms;

import android.support.v4.app.ListFragment;
import android.support.v4.app.LoaderManager;
import android.support.v4.content.CursorLoader;
import android.support.v4.content.Loader;
import android.support.v4.widget.SimpleCursorAdapter;
import android.support.v7.app.ActionBarActivity;
import android.content.Context;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Telephony.Threads;
import android.provider.Telephony.Sms.Conversations;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ListView;



public class MainActivity extends ActionBarActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new ConversationListFragment())
                    .commit();
        }
    }


    @Override
	public View onCreateView(String name, Context context, AttributeSet attrs) {
		// TODO Auto-generated method stub
		return super.onCreateView(name, context, attrs);
	}


	@Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();
        if (id == R.id.action_settings) {
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
	
    /**
     * A placeholder fragment containing a simple view.
     */
    public static class ConversationListFragment extends ListFragment
    		implements LoaderManager.LoaderCallbacks<Cursor> {
    	SimpleCursorAdapter mListAdapter;
    	
    	private static final int SNIPPET        = 4;
//    	private static final int SNIPPET_CHARSET = 5;
    	public static final Uri sAllThreadsUri =
    	        Threads.CONTENT_URI.buildUpon().appendQueryParameter("simple", "true").build();
    	
        public static final String[] ALL_THREADS_PROJECTION = {
            Threads._ID, Threads.DATE, Threads.MESSAGE_COUNT, Threads.RECIPIENT_IDS,
            Threads.SNIPPET, Threads.SNIPPET_CHARSET, Threads.READ, Threads.ERROR,
            Threads.HAS_ATTACHMENT
        };

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
        	
	        // Create an empty adapter we will use to display the loaded data.
	        // We pass null for the cursor, then update it in onLoadFinished()
			mListAdapter = new SimpleCursorAdapter(
					getActivity(),
					R.layout.conversation_list_item,
					null,
					new String[] {Threads.SNIPPET},
					new int[] {R.id.subject},
					0
					);
	        setListAdapter(mListAdapter);
        	
            View rootView = inflater.inflate(R.layout.fragment_main, container, false);
            return rootView;
        }

		@Override
		public void onActivityCreated(Bundle savedInstanceState) {
			// TODO Auto-generated method stub
			super.onActivityCreated(savedInstanceState);
			
			/*
			Cursor mCursor = getActivity().getContentResolver().query(
					sAllThreadsUri,
					ALL_THREADS_PROJECTION,
					null, // selection
					null, // selectionArgs
					Conversations.DEFAULT_SORT_ORDER
					);
					
					
					/*
				    UserDictionary.Words.CONTENT_URI,   // The content URI of the words table
				    mProjection,                        // The columns to return for each row
				    mSelectionClause                    // Selection criteria
				    mSelectionArgs,                     // Selection criteria
				    mSortOrder);
				    */ 
			
// TEST			
//			TextView tv = (TextView) getActivity().findViewById(R.id.test_textview);
//			tv.setText("Howdy");
		}

		@Override
		public void onListItemClick(ListView l, View v, int position, long id) {
			// TODO Auto-generated method stub
			super.onListItemClick(l, v, position, id);
		}
		
		@Override
		public Loader<Cursor> onCreateLoader(int loaderID, Bundle bundle) {
	        return new CursorLoader(
	            getActivity(),
	            sAllThreadsUri,
	            ALL_THREADS_PROJECTION,
				null, // selection
				null, // selectionArgs
	            Conversations.DEFAULT_SORT_ORDER
	        );
		}

		@Override
		public void onLoadFinished(Loader<Cursor> loader, Cursor data) {
	/*
			lv = (ListView) findViewById(android.R.id.list);
			
			// if there are no results
			if (data.getCount() == 0) {
			    // let the user know
			    lv.setEmptyView(findViewById(android.R.id.empty));
			} else {
			    // otherwise clear it, so it won't flash in between cursor loads
			    lv.setEmptyView(null);
			}
	*/
			
			mListAdapter.swapCursor(data);
			
	/*		
			if (c.getCount() == 0) {
	// TODO handle if no results found
//	            ((TextView)(getListView().getEmptyView())).setText(R.string.no_conversations);
	        } else {
	        	c.moveToNext();
	        	
//	        	TextView mSubjectView = (TextView) findViewById(R.id.subject);
//	        	mSubjectView.setText("Test conversation item");
	        	
	        	
//	        	((TextView) findViewById(R.id.test_textview)).setText(c.getString(SNIPPET));
	        	
	        	
	        	// get fragment view and the conversation list item child view
	        	
	        	
	        	// call its bind method
	        }
	*/		
		}


		@Override
		public void onLoaderReset(Loader<Cursor> loader) {
	        // This is called when the last Cursor provided to onLoadFinished()
	        // above is about to be closed.  We need to make sure we are no
	        // longer using it.
	        mListAdapter.swapCursor(null);
	    }
    }
}
