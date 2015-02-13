package ca.bmaupin.androidplayground;

import java.lang.reflect.Field;

import android.util.Log;

public class ReflectionHelper {
	public static final String TAG = "ReflectionHelper";
	
	public static String getString(String className, String stringName) {
		Class<?> reflectedClass = null;
		try {
			reflectedClass = Class.forName(className);
		} catch (ClassNotFoundException e) {
			Log.e(TAG, "getString() - Class.forName(className)", e);
		}
		Field reflectedField = null;
		try {
			reflectedField = reflectedClass.getField(stringName);
		} catch (NoSuchFieldException e) {
			Log.e(TAG, "getString() - reflectedClass.getField(stringName)", e);
		}
		String reflectedString = null;
		try {
			reflectedString = (String) reflectedField.get(String.class);
		} catch (IllegalAccessException | IllegalArgumentException e) {
			Log.e(TAG, "getString() - reflectedField.get(String.class)", e);
		}
		
		return reflectedString;
	}
}
