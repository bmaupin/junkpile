package ca.bmaupin.androidplayground;

import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Locale;

import android.support.v7.app.ActionBarActivity;
import android.telephony.TelephonyManager;
import android.content.Context;
import android.net.ConnectivityManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ToggleButton;
import ca.bmaupin.androidplayground.ReflectionHelper;

public class MainActivity extends ActionBarActivity {
	private static final String TAG = "MainActivity";
	
	private String mCountryIso;
	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		
//import android.location.Country;
//import android.location.CountryDetector;
//import android.location.CountryListener;
		
//	    private CountryDetector mCountryDetector;
//	    private CountryListener mCountryListener;
		
		
//		mCountryDetector = (CountryDetector) getSystemService(Context.COUNTRY_DETECTOR);
		
		String countryDetectorString = ReflectionHelper.getString("android.content.Context", "COUNTRY_DETECTOR");
		
		/*
		try {
//			Class countryDetectorClass = Class.forName("android.location.CountryDetector");
			
			
			
			Class serviceManagerClass = Class.forName("android.os.ServiceManager");
	        Method getService = serviceManagerClass.getMethod("getService", String.class);
	        Object mCountryDetector = getService.invoke(serviceManagerClass, countryDetectorString);
	        
	        Class countryListenerClass = Class.forName("android.location.CountryListener");
	        
	        Object mCountryListener = countryListenerClass.newInstance() {
	            @Override
	            public synchronized void onCountryDetected(Country country) {
	                mCountryIso = country.getCountryIso();
	            }
	        };
		} catch (Exception e) {
			
		}
		
		
/*		
		Class CountryDetector = Class.forName("android.location.CountryDetector");
		Method getService = CountryDetector.getMethod("getService", String.class);
		CountryDetector mCountryDetector = (CountryDetector) getService.invoke(serviceManagerClass, "country_detector");
		
        mCountryListener = new CountryListener() {
            @Override
            public synchronized void onCountryDetected(Country country) {
                mCountryIso = country.getCountryIso();
            }
        };
        mCountryDetector.addCountryListener(mCountryListener, getMainLooper());
*/
		
		
		// Tinker with country codes
		/*
		TelephonyManager tm = (TelephonyManager)getSystemService(Context.TELEPHONY_SERVICE);

	    Log.d(TAG, "tm.getSimCountryIso()=" + tm.getSimCountryIso());
		Log.d(TAG, "tm.getPhoneType()=" + tm.getPhoneType());
	    Log.d(TAG, "tm.getNetworkCountryIso()=" + tm.getNetworkCountryIso());
	    Log.d(TAG, "Locale.getDefault().getCountry()=" + Locale.getDefault().getCountry());
		*/
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
	    	Log.e(TAG, "setMobileDataEnabled() - get setMobileDataEnabled() method", e);
	    }
	    dataMtd.setAccessible(true);
	    try {
	        dataMtd.invoke(dataManager, enabled);
	    } catch (IllegalArgumentException | IllegalAccessException | InvocationTargetException e) {
	    	Log.e(TAG, "setMobileDataEnabled() - dataMtd.invoke()", e);
	    }
	}
}
