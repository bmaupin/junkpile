package org.example;

import org.apache.log4j.Logger;

public class App {
    static Logger logger = Logger.getLogger(App.class);

    public static void main(String[] args) {
        testLoggingWithStackTraces();
    }

    private static void testLoggingWithStackTraces() {
        makeStackTraceLonger();
    }

    private static void makeStackTraceLonger() {
        notLongEnough();
    }

    private static void notLongEnough() {
        okayThatsEnough();
    }

    private static void okayThatsEnough() {
        logErrorWithStackTrace();
    }

    private static void logErrorWithStackTrace() {
        logger.error("Test error message, without stack trace");
        logger.error("Test error message, without stack trace");
        logger.error("Test error message, with stack trace", new IllegalArgumentException("Test exception message"));
        logger.error("Test error message, without stack trace");
        logger.error("Test error message, without stack trace");
    }
}
