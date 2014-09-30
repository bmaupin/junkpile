package ca.bmaupin.merge.sms.ui;

import ca.bmaupin.merge.sms.R;
import android.content.Context;
import android.util.AttributeSet;
import android.widget.RelativeLayout;
import android.widget.TextView;

public class ConversationListItem extends RelativeLayout {
	private TextView mSubjectView;

	public ConversationListItem(Context context) {
		super(context);
	}
	
	public ConversationListItem(Context context, AttributeSet attrs) {
		super(context, attrs);
	}

	@Override
	protected void onFinishInflate() {
		super.onFinishInflate();
		
		mSubjectView = (TextView) findViewById(R.id.subject);
	}

	public final void bind(Context context) {
//		mSubjectView.setText(conversation.getSnippet());
		mSubjectView.setText("Test conversation item");
	}

}
