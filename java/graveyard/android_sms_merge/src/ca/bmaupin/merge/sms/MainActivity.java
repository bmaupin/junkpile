package ca.bmaupin.merge.sms;

import ca.bmaupin.merge.sms.data.Conversation;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.ActionBar;
import android.support.v4.app.Fragment;
import android.content.AsyncQueryHandler;
import android.database.sqlite.SQLiteException;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;
import android.os.Build;
import android.provider.Telephony.Threads;



public class MainActivity extends ActionBarActivity {
	private static final String TAG = "ConversationList";
	
    private static final int THREAD_LIST_QUERY_TOKEN       = 1701;
    
    private AsyncQueryHandler mQueryHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        //setContentView(R.layout.conversation_list_screen);
        
        if (savedInstanceState == null) {
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.container, new PlaceholderFragment())
                    .commit();
        }
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
            //View rootView = inflater.inflate(R.layout.fragment_main, container, false);
            
            View rootView = inflater.inflate(R.layout.conversation_list_screen, container, false);
            
            TextView tv = (TextView) rootView.findViewById(R.id.test_textview);
            
            tv.setText("Hey, it worked!");
            
            return rootView;
        }
    }
    
    private void startAsyncQuery() {
        try {
//            ((TextView)(getListView().getEmptyView())).setText(R.string.loading_conversations);

            Conversation.startQueryForAll(mQueryHandler, THREAD_LIST_QUERY_TOKEN);
//            Conversation.startQuery(mQueryHandler, UNREAD_THREADS_QUERY_TOKEN, Threads.READ + "=0");
        } catch (SQLiteException e) {
        	Log.e(TAG, "SQLiteException: " + e);
        }
    }
}
