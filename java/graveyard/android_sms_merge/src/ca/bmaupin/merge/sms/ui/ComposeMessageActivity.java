/*
 * Derived from com.android.mms.ui.ComposeMessageActivity
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import android.app.Activity;
import android.content.ContentResolver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.text.InputFilter;
import android.text.InputFilter.LengthFilter;
import android.util.Log;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.TextView;
import ca.bmaupin.merge.sms.R;
import ca.bmaupin.merge.sms.data.Conversation;

public class ComposeMessageActivity extends Activity {
    private ContentResolver mContentResolver;

    private BackgroundQueryHandler mBackgroundQueryHandler;
    
    private MessageListView mMsgListView;        // ListView for messages in this conversation
    public MessageListAdapter mMsgListAdapter;  // and its corresponding ListAdapter
	
    @Override
    protected void onCreate(Bundle savedInstanceState) {
// TODO
//        mIsSmsEnabled = MmsConfig.isSmsEnabled(this);
        super.onCreate(savedInstanceState);

        setContentView(R.layout.compose_message_activity);
        setProgressBarVisibility(false);

        // Initialize members for UI elements.
        initResourceRefs();

// TODO        
//        mContentResolver = getContentResolver();
//        mBackgroundQueryHandler = new BackgroundQueryHandler(mContentResolver);

// TODO
//        initialize(savedInstanceState, 0);
    }
	
    //==========================================================
    // Private methods
    //==========================================================

    /**
     * Initialize all UI elements from resources.
     */
    private void initResourceRefs() {
        mMsgListView = (MessageListView) findViewById(R.id.history);
        mMsgListView.setDivider(null);      // no divider so we look like IM conversation.

        // called to enable us to show some padding between the message list and the
        // input field but when the message list is scrolled that padding area is filled
        // in with message content
        mMsgListView.setClipToPadding(false);

        mMsgListView.setOnSizeChangedListener(new OnSizeChangedListener() {
            public void onSizeChanged(int width, int height, int oldWidth, int oldHeight) {
                if (Log.isLoggable(LogTag.APP, Log.VERBOSE)) {
                    Log.v(TAG, "onSizeChanged: w=" + width + " h=" + height +
                            " oldw=" + oldWidth + " oldh=" + oldHeight);
                }

                if (!mMessagesAndDraftLoaded && (oldHeight-height > SMOOTH_SCROLL_THRESHOLD)) {
                    // perform the delayed loading now, after keyboard opens
                    loadMessagesAndDraft(3);
                }


                // The message list view changed size, most likely because the keyboard
                // appeared or disappeared or the user typed/deleted chars in the message
                // box causing it to change its height when expanding/collapsing to hold more
                // lines of text.
                smoothScrollToEnd(false, height - oldHeight);
            }
        });

        mBottomPanel = findViewById(R.id.bottom_panel);
        mTextEditor = (EditText) findViewById(R.id.embedded_text_editor);
        mTextEditor.setOnEditorActionListener(this);
        mTextEditor.addTextChangedListener(mTextEditorWatcher);
        mTextEditor.setFilters(new InputFilter[] {
                new LengthFilter(MmsConfig.getMaxTextLimit())});
        mTextCounter = (TextView) findViewById(R.id.text_counter);
        mSendButtonMms = (TextView) findViewById(R.id.send_button_mms);
        mSendButtonSms = (ImageButton) findViewById(R.id.send_button_sms);
        mSendButtonMms.setOnClickListener(this);
        mSendButtonSms.setOnClickListener(this);
        mTopPanel = findViewById(R.id.recipients_subject_linear);
        mTopPanel.setFocusable(false);
        mAttachmentEditor = (AttachmentEditor) findViewById(R.id.attachment_editor);
        mAttachmentEditor.setHandler(mAttachmentEditorHandler);
        mAttachmentEditorScrollView = findViewById(R.id.attachment_editor_scroll_view);
    }
    
    public static Intent createIntent(Context context, long threadId) {
        Intent intent = new Intent(context, ComposeMessageActivity.class);

        if (threadId > 0) {
            intent.setData(Conversation.getUri(threadId));
        }

        return intent;
    }
}
