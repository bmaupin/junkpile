/*
 * Derived from com.android.mms.ui.ComposeMessageActivity
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import ca.bmaupin.merge.sms.data.Conversation;

public class ComposeMessageActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        mIsSmsEnabled = MmsConfig.isSmsEnabled(this);
        super.onCreate(savedInstanceState);

        resetConfiguration(getResources().getConfiguration());

        setContentView(R.layout.compose_message_activity);
        setProgressBarVisibility(false);

        // Initialize members for UI elements.
        initResourceRefs();

        mContentResolver = getContentResolver();
        mBackgroundQueryHandler = new BackgroundQueryHandler(mContentResolver);

        initialize(savedInstanceState, 0);

        if (TRACE) {
            android.os.Debug.startMethodTracing("compose");
        }
    }
	
    public static Intent createIntent(Context context, long threadId) {
        Intent intent = new Intent(context, ComposeMessageActivity.class);

        if (threadId > 0) {
            intent.setData(Conversation.getUri(threadId));
        }

        return intent;
    }
}
