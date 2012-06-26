package ca.bmaupin.test;

import android.content.Context;
import android.os.Build;
import android.text.Layout.Alignment;
import android.text.StaticLayout;
import android.text.TextPaint;
import android.text.TextUtils.TruncateAt;
import android.util.AttributeSet;
import android.util.Log;
import android.widget.TextView;

public class AutofitTextView extends TextView {
    private String TAG = "AutofitTextView";
    
    // Text view line spacing multiplier
    private float mSpacingMult = 1.0f;

    // Text view additional line spacing
    private float mSpacingAdd = 0.0f;
    
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
        
        TextPaint tp = this.getPaint();
        int maxWidth = viewWidth - this.getPaddingLeft() - 
                this.getPaddingRight();
        int maxHeight = this.getHeight() - this.getPaddingTop()
                - this.getPaddingBottom();
        
        // split up slashed and dashed words, but include the punctuation when
        // resizing so they don't end up on the next line
        text = text.replace("/", "/ ");
        text = text.replace("-", "- ");
        
        String[] words = text.split(" ");
        
        for (String word : words) {
            // if this word isn't larger than the max size
            if (tp.measureText(word) < maxWidth) {
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
                tp.setTextSize(size);
                if (tp.measureText(word) >= maxWidth) 
                    hi = size; // too big
                else
                    lo = size; // too small
            }

            // go ahead and resize the text now so the rezise won't have to 
            // happen again once the largest word has been resized.  use lo so 
            // that we undershoot rather than overshoot.
            tp.setTextSize(lo);
        }
        
        // if the text is too high
        while (getTextHeight(text, tp, maxWidth, this.getTextSize()) > 
                maxHeight) {
            // reduce the font size by 1 until it fits
            tp.setTextSize(this.getTextSize() - 1f);
        }
        
        // force the view to be redrawn and the line wrapping to be 
        // recalculated
//TODO: not sure where honeycomb falls in this
        // pre ICS
        if (Integer.parseInt(Build.VERSION.SDK) < 14) {
            setEllipsize(null);
        // ICS and above
        } else {
            setEllipsize(TruncateAt.END);
        }
    }

    // Set the text size of the text paint object and use a static layout to render text off screen before measuring
    private int getTextHeight(CharSequence source, TextPaint paint, int width, 
            float textSize) {
        // Update the text paint object
        paint.setTextSize(textSize);
        // Measure using a static layout
        StaticLayout layout = new StaticLayout(source, paint, width, 
                Alignment.ALIGN_NORMAL, mSpacingMult, mSpacingAdd, true);
        return layout.getHeight();
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
