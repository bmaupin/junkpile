package com.googlecode.chartdroid.pie;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.widget.RelativeLayout;

public class ChartRelativeLayout extends RelativeLayout {
    public ChartRelativeLayout(Context context) {
        super(context);
    }

    public ChartRelativeLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        // don't pass the touch event on
        return true;
    }
}
