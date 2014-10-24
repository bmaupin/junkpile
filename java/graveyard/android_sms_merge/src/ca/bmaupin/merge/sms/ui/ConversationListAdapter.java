/*
 * Derived from com.android.mms.ui.ConversationListAdapter
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import android.content.Context;
import android.database.Cursor;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AbsListView;
import android.widget.CursorAdapter;

import ca.bmaupin.merge.sms.R;
import ca.bmaupin.merge.sms.data.Conversation;

/**
 * The back-end data adapter for ConversationList.
 */
//TODO: This should be public class ConversationListAdapter extends ArrayAdapter<Conversation>
public class ConversationListAdapter extends CursorAdapter implements AbsListView.RecyclerListener {
    private static final String TAG = "ConversationListAdapter";
    private static final boolean LOCAL_LOGV = false;

    private final LayoutInflater mFactory;

    public ConversationListAdapter(Context context, Cursor cursor) {
        super(context, cursor, false /* auto-requery */);
        mFactory = LayoutInflater.from(context);
    }

    @Override
    public void bindView(View view, Context context, Cursor cursor) {
        if (!(view instanceof ConversationListItem)) {
            Log.e(TAG, "Unexpected bound view: " + view);
            return;
        }

        ConversationListItem headerView = (ConversationListItem) view;
        Conversation conv = Conversation.from(context, cursor);
        headerView.bind(context, conv);
    }

    public void onMovedToScrapHeap(View view) {
        ConversationListItem headerView = (ConversationListItem)view;
        headerView.unbind();
    }

    @Override
    public View newView(Context context, Cursor cursor, ViewGroup parent) {
        if (LOCAL_LOGV) Log.v(TAG, "inflating new view");
        return mFactory.inflate(R.layout.conversation_list_item, parent, false);
    }
}