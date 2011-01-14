package us.bmaupin.flashcards.arabic;

//$Id$

import android.content.Context;
import android.os.Bundle;
import android.preference.PreferenceActivity;
import android.preference.PreferenceManager;

public class Settings extends PreferenceActivity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		addPreferencesFromResource(R.xml.settings);
	}
	
	public static String getDefaultLang(Context context) {
		return PreferenceManager.getDefaultSharedPreferences(context)
		       .getString("defaultLang", "arabic");
	}
}
