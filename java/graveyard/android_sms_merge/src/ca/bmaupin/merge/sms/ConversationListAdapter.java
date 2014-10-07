package ca.bmaupin.merge.sms;

import android.content.Context;
import android.database.Cursor;
import android.support.v4.widget.SimpleCursorAdapter;
import android.widget.ArrayAdapter;

public class ConversationListAdapter extends SimpleCursorAdapter {

	public ConversationListAdapter(Context context, int layout, Cursor c,
			String[] from, int[] to, int flags) {
		super(context, layout, c, from, to, flags);
		// TODO Auto-generated constructor stub
	}
}
