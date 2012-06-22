package ca.bmaupin.test;

import android.content.Context;
import android.graphics.Paint;
import android.os.Build;
import android.text.TextUtils.TruncateAt;
import android.util.AttributeSet;
import android.util.Log;
import android.util.TypedValue;
import android.widget.TextView;

public class AutofitTextView extends TextView {
    private String TAG = "AutofitTextView";
    
    public AutofitTextView(Context context) {
        super(context);
    }

    public AutofitTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    /* Resize the font so the specified text fits in the text box
     * assuming the text box is the specified width.
     */
    private void refitText(String text, int viewWidth) {
        Log.d(TAG, "refitText()");
        if (viewWidth <= 0) {
            return;
        }
        
        float newSize = 0;
        Paint paint = this.getPaint();
        int maxWidth = viewWidth - this.getPaddingLeft() - 
                this.getPaddingRight();
        
        String[] words = text.split(" ");
        
        for (String word : words) {
            // if this word isn't larger than the max size
            if (paint.measureText(word) < maxWidth) {
                // go to the next
                continue;
            }

            float hi = this.getTextSize();
            // 14sp (this is technically px) is the size used for 
            // textAppearance.Small.  don't think we want any smaller.
            float lo = 14;
            final float threshold = 0.5f; // How close we have to be

            while ((hi - lo) > threshold) {
                float size = (hi + lo) / 2;
                paint.setTextSize(size);
                if (paint.measureText(word) >= maxWidth) 
                    hi = size; // too big
                else
                    lo = size; // too small
            }
            
            // only update newSize the first time or if the new value is smaller
            if (newSize == 0 || lo < newSize) {
                // Use lo so that we undershoot rather than overshoot
                newSize = lo;
            }
        }
        
        if (newSize != 0) {
            this.setTextSize(TypedValue.COMPLEX_UNIT_PX, newSize);
            // recalculate the line wrapping
            // pre ICS
            if (Integer.parseInt(Build.VERSION.SDK) < 14) {
                setEllipsize(null);
            // ICS and above
            } else {
                setEllipsize(TruncateAt.END);
            }
        }
    }

// TODO this doesn't seem to be necessary, at least not for what we're using 
// this class for
/*
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        Log.d(TAG, "onMeasure()");
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        int parentWidth = MeasureSpec.getSize(widthMeasureSpec);
        int height = getMeasuredHeight();
        this.setMeasuredDimension(parentWidth, height);
    }
*/

    @Override
    protected void onTextChanged(final CharSequence text, final int start, 
            final int lengthBefore, final int lengthAfter) {
        Log.d(TAG, "onTextChanged()");
        // resize the text if it changes
        refitText(text.toString(), this.getWidth());
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        Log.d(TAG, "onSizeChanged()");
        if (w != oldw) {
            // resize the text if the view size changes
            refitText(this.getText().toString(), w);
        }
    }
}
