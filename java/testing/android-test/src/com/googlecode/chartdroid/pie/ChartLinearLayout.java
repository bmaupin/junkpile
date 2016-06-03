package com.googlecode.chartdroid.pie;

import android.content.Context;
import android.util.AttributeSet;
import android.view.MotionEvent;
import android.widget.LinearLayout;

public class ChartLinearLayout extends LinearLayout {
    public ChartLinearLayout(Context context) {
        super(context);
    }

    public ChartLinearLayout(Context context, AttributeSet attrs) {
        super(context, attrs);
    }

    @Override
    public boolean onInterceptTouchEvent(MotionEvent ev) {
        // don't pass the touch event on
        return true;
    }
}
