package ca.bmaupin.test;

import android.content.Context;
import android.graphics.Paint;
import android.util.AttributeSet;
import android.util.Log;
import android.util.TypedValue;
import android.widget.TextView;

public class FontFitTextView extends TextView {
    private String TAG = "FontFitTextView";
    
    public FontFitTextView(Context context) {
        super(context);
    }

    public FontFitTextView(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    /* Resize the font so the specified text fits in the text box
     * assuming the text box is the specified width.
     */
    private void refitText(String text, int viewWidth) {
        if (viewWidth <= 0) {
            return;
        }
        
        Paint paint = this.getPaint();
        int maxWidth = viewWidth - this.getPaddingLeft() - 
                this.getPaddingRight();

//        
        Log.d(TAG, "viewWidth=" + viewWidth);
        Log.d(TAG, "maxWidth=" + maxWidth);
        Log.d(TAG, "this.getTextSize()=" + this.getTextSize());
        Log.d(TAG, "paint.measureText(text)=" + paint.measureText(text));
        
        // no need to shrink the text if it isn't larger than the max size
        if (paint.measureText(text) < maxWidth) {
            return;
        }

        float hi = paint.measureText(text);
        float lo = 2;
        final float threshold = 0.5f; // How close we have to be

        while ((hi - lo) > threshold) {
            float size = (hi + lo) / 2;
            paint.setTextSize(size);
            if (paint.measureText(text) >= maxWidth) 
                hi = size; // too big
            else
                lo = size; // too small
        }
        // Use lo so that we undershoot rather than overshoot
        this.setTextSize(TypedValue.COMPLEX_UNIT_PX, lo);
    }
/*
    @Override
    protected void onMeasure(int widthMeasureSpec, int heightMeasureSpec) {
        super.onMeasure(widthMeasureSpec, heightMeasureSpec);
        int parentWidth = MeasureSpec.getSize(widthMeasureSpec);
        int height = getMeasuredHeight();
        refitText(this.getText().toString(), parentWidth);
        this.setMeasuredDimension(parentWidth, height);
    }
*/
    @Override
    protected void onTextChanged(final CharSequence text, final int start, 
            final int lengthBefore, final int lengthAfter) {
        Log.d("FontFitTextView", "onTextChanged()");
        // resize the text if it changes
        refitText(text.toString(), this.getWidth());
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        Log.d("FontFitTextView", "onSizeChanged()");
        if (w != oldw) {
            // resize the text if the view size changes
            refitText(this.getText().toString(), w);
        }
    }
}
