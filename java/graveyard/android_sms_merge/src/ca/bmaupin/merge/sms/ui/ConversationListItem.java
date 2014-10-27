/*
 * Derived from com.android.mms.ui.ConversationListItem
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.Typeface;
import android.graphics.drawable.Drawable;
import android.os.Handler;
import android.text.Spannable;
import android.text.SpannableStringBuilder;
import android.text.style.ForegroundColorSpan;
import android.text.style.StyleSpan;
import android.text.style.TextAppearanceSpan;
import android.util.AttributeSet;
import android.util.Log;
import android.view.View;
import android.widget.QuickContactBadge;
import android.widget.RelativeLayout;
import android.widget.TextView;

import ca.bmaupin.merge.sms.R;
import ca.bmaupin.merge.sms.data.Conversation;

/**
 * This class manages the view for given conversation.
 */
public class ConversationListItem extends RelativeLayout {
    private Context mContext;
    private TextView mSubjectView;
    private TextView mFromView;
    private TextView mDateView;
    private View mAttachmentView;
    private QuickContactBadge mAvatarView;

    static private Drawable sDefaultContactImage;

    private Conversation mConversation;

    public static final StyleSpan STYLE_BOLD = new StyleSpan(Typeface.BOLD);

    public ConversationListItem(Context context) {
        super(context);
        mContext = context;
    }

    public ConversationListItem(Context context, AttributeSet attrs) {
        super(context, attrs);
        mContext = context;

        if (sDefaultContactImage == null) {
            sDefaultContactImage = context.getResources().getDrawable(R.drawable.ic_contact_picture);
        }
    }

    @Override
    protected void onFinishInflate() {
        super.onFinishInflate();

        mFromView = (TextView) findViewById(R.id.from);
        mSubjectView = (TextView) findViewById(R.id.subject);

        mDateView = (TextView) findViewById(R.id.date);
        mAttachmentView = findViewById(R.id.attachment);
        mAvatarView = (QuickContactBadge) findViewById(R.id.avatar);
    }

    public Conversation getConversation() {
        return mConversation;
    }

    /**
     * Only used for header binding.
     */
    public void bind(String title, String explain) {
        mFromView.setText(title);
        mSubjectView.setText(explain);
    }

    private CharSequence formatMessage() {
//        final int color = android.R.styleable.Theme_textColorSecondary;
    	// Attempt to fix the above line (http://stackoverflow.com/a/1717532/399105)
        TypedArray a = mContext.obtainStyledAttributes(R.styleable.ConversationListItem);
        final int color = a.getResourceId(R.styleable.ConversationListItem_android_textColorSecondary, 0);
        
        String from = mConversation.getRecipients().formatNames(", ");

        SpannableStringBuilder buf = new SpannableStringBuilder(from);

        if (mConversation.getMessageCount() > 1) {
            int before = buf.length();
            buf.append(mContext.getResources().getString(R.string.message_count_format,
                    mConversation.getMessageCount()));
            buf.setSpan(new ForegroundColorSpan(
                    mContext.getResources().getColor(R.color.message_count_color)),
                    before, buf.length(), Spannable.SPAN_INCLUSIVE_EXCLUSIVE);
        }

        return buf;
    }

    private void updateAvatarView() {
        Drawable avatarDrawable;
        if (mConversation.getRecipients().size() == 1) {
            Contact contact = mConversation.getRecipients().get(0);
            avatarDrawable = contact.getAvatar(mContext, sDefaultContactImage);

            if (contact.existsInDatabase()) {
                mAvatarView.assignContactUri(contact.getUri());
            } else {
                mAvatarView.assignContactFromPhone(contact.getNumber(), true);
            }
        } else {
            // TODO get a multiple recipients asset (or do something else)
            avatarDrawable = sDefaultContactImage;
            mAvatarView.assignContactUri(null);
        }
        mAvatarView.setImageDrawable(avatarDrawable);
        mAvatarView.setVisibility(View.VISIBLE);
    }

    public final void bind(Context context, final Conversation conversation) {
        //if (DEBUG) Log.v(TAG, "bind()");

        mConversation = conversation;

        boolean hasAttachment = conversation.hasAttachment();
        mAttachmentView.setVisibility(hasAttachment ? VISIBLE : GONE);

        // Date
        mDateView.setText(MessageUtils.formatTimeStampString(context, conversation.getDate()));

        // From.
        mFromView.setText(formatMessage());

        // Subject
        mSubjectView.setText(conversation.getSnippet());
        LayoutParams subjectLayout = (LayoutParams)mSubjectView.getLayoutParams();
        // We have to make the subject left of whatever optional items are shown on the right.
        subjectLayout.addRule(RelativeLayout.LEFT_OF, hasAttachment ? R.id.attachment :
            (R.id.date));

        updateAvatarView();
    }

    public final void unbind() {
    }
}
