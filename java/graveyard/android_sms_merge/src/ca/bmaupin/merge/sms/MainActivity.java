package ca.bmaupin.merge.sms;

import android.support.v7.app.ActionBarActivity;
import android.support.v4.app.Fragment;
import android.support.v4.app.LoaderManager;
import android.support.v4.content.CursorLoader;
import android.support.v4.content.Loader;
import android.app.LoaderManager.LoaderCallbacks;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Telephony.Threads;
import android.provider.Telephony.Sms.Conversations;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;



public class MainActivity extends ActionBarActivity implements LoaderManager.LoaderCallbacks<Cursor> {
	private static final int CONVERSATION_LOADER = 0;
	
	private static final int SNIPPET        = 4;
//	private static final int SNIPPET_CHARSET = 5;
	
	
	
	public static final Uri sAllThreadsUri =
	        Threads.CONTENT_URI.buildUpon().appendQueryParameter("simple", "true").build();
	
    public static final String[] ALL_THREADS_PROJECTION = {
        Threads._ID, Threads.DATE, Threads.MESSAGE_COUNT, Threads.RECIPIENT_IDS,
        Threads.SNIPPET, Threads.SNIPPET_CHARSET, Threads.READ, Threads.ERROR,
        Threads.HAS_ATTACHMENT
    };
	

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
        
        getSupportLoaderManager().initLoader(CONVERSATION_LOADER, null, this);
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
    public static class PlaceholderFragment extends Fragment {

        public PlaceholderFragment() {
        }

        @Override
        public View onCreateView(LayoutInflater inflater, ViewGroup container,
                Bundle savedInstanceState) {
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
    }

	@Override
	public Loader<Cursor> onCreateLoader(int loaderID, Bundle bundle) {
	    /*
	     * Takes action based on the ID of the Loader that's being created
	     */
	    switch (loaderID) {
	        case CONVERSATION_LOADER:
	            // Returns a new CursorLoader
	            return new CursorLoader(
                    this,
                    sAllThreadsUri,
                    ALL_THREADS_PROJECTION,
					null, // selection
					null, // selectionArgs
                    Conversations.DEFAULT_SORT_ORDER
	            );
	        default:
	            // An invalid id was passed in
	            return null;
	    }
	}


	@Override
	public void onLoadFinished(Loader<Cursor> arg0, Cursor c) {
		if (c.getCount() == 0) {
// TODO handle if no results found
//            ((TextView)(getListView().getEmptyView())).setText(R.string.no_conversations);
        } else {
        	c.moveToNext();
        	
        	((TextView) findViewById(R.id.test_textview)).setText(c.getString(SNIPPET));
        }
		
	}


	@Override
	public void onLoaderReset(Loader<Cursor> arg0) {
		// TODO Auto-generated method stub
		
	}
}
