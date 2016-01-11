package ca.bmaupin.androidtvtest;

import android.os.Bundle;
import android.app.Activity;
import android.view.Display;
import android.view.WindowManager;
import android.widget.TextView;

import java.util.Arrays;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Display display = getWindowManager().getDefaultDisplay();
        WindowManager.LayoutParams params = getWindow().getAttributes();
        TextView tv1 = (TextView) findViewById(R.id.tv1);
        TextView tv2 = (TextView) findViewById(R.id.tv2);
        TextView tv3 = (TextView) findViewById(R.id.tv3);
        TextView tv4 = (TextView) findViewById(R.id.tv4);

        // Get supported refresh rates (Lollipop)
        float[] refreshRates = display.getSupportedRefreshRates();
        tv1.setText("Supported display refresh rates: \n" + Arrays.toString(refreshRates));

        // Get current preferred refresh rate (Lollipop)
        tv2.setText("Current preferred refresh rate: \n" + params.preferredRefreshRate);

        // Get supported modes (Marshmallow)
        Display.Mode[] modes = display.getSupportedModes();
        tv3.setText("Supported display modes: \n" + Arrays.toString(modes));

        // Get current preferred mode (Marshmallow)
        Display.Mode preferredMode = null;
        for (Display.Mode mode : modes) {
            if (mode.getModeId() == params.preferredDisplayModeId) {
                preferredMode = mode;
                break;
            }
        }
        tv4.setText("Current preferred mode: \n" + preferredMode);
    }

}
