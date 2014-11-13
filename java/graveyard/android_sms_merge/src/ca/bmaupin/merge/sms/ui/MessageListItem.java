/*
 * Derived from com.android.mms.ui.MessageListItem
 * (tag android-4.4.4_r2.0.1)
 */

package ca.bmaupin.merge.sms.ui;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.text.style.ForegroundColorSpan;
import android.util.AttributeSet;
import android.widget.LinearLayout;

import ca.bmaupin.merge.sms.MmsApp;
import ca.bmaupin.merge.sms.R;

public class MessageListItem extends LinearLayout {
    private String mDefaultCountryIso;
    static private Drawable sDefaultContactImage;
	
    public MessageListItem(Context context) {
        super(context);
        mDefaultCountryIso = MmsApp.getApplication().getCurrentCountryIso();

        if (sDefaultContactImage == null) {
            sDefaultContactImage = context.getResources().getDrawable(R.drawable.ic_contact_picture);
        }
    }

    public MessageListItem(Context context, AttributeSet attrs) {
        super(context, attrs);

        int color = mContext.getResources().getColor(R.color.timestamp_color);
        mColorSpan = new ForegroundColorSpan(color);
        mDefaultCountryIso = MmsApp.getApplication().getCurrentCountryIso();

        if (sDefaultContactImage == null) {
            sDefaultContactImage = context.getResources().getDrawable(R.drawable.ic_contact_picture);
        }
    }
    
    ForegroundColorSpan mColorSpan = null;  // set in ctor
}
