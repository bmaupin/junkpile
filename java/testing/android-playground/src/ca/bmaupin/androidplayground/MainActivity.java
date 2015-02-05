package ca.bmaupin.androidplayground;

import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;

import android.support.v7.app.ActionBarActivity;
import android.content.Context;
import android.net.ConnectivityManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ToggleButton;

public class MainActivity extends ActionBarActivity {
	private static final String TAG = "MainActivity";

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}
	
	public void onToggleClicked(View view) {
	    // Is the toggle on?
	    boolean on = ((ToggleButton) view).isChecked();
	    
	    if (on) {
	    	setMobileDataEnabled(this, true);
	    } else {
	    	setMobileDataEnabled(this, false);
	    }
	}
	
	private void setMobileDataEnabled(Context context, boolean enabled) {
	    ConnectivityManager dataManager;
	    dataManager  = (ConnectivityManager)getSystemService(Context.CONNECTIVITY_SERVICE);
	    Method dataMtd = null;
	    try {
	        dataMtd = ConnectivityManager.class.getDeclaredMethod("setMobileDataEnabled", boolean.class);
	    } catch (NoSuchMethodException e) {
	        // TODO Auto-generated catch block
	        e.printStackTrace();
	    }
	    dataMtd.setAccessible(true);
	    try {
	        dataMtd.invoke(dataManager, enabled);
	    } catch (IllegalArgumentException e) {
	        // TODO Auto-generated catch block
	        e.printStackTrace();
	    } catch (IllegalAccessException e) {
	        // TODO Auto-generated catch block
	        e.printStackTrace();
	    } catch (InvocationTargetException e) {
	        // TODO Auto-generated catch block
	        e.printStackTrace();
	    }
	}
}
