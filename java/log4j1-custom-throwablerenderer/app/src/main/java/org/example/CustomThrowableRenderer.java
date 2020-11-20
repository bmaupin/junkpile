    package org.example;

    import org.apache.log4j.DefaultThrowableRenderer;
    import org.apache.log4j.spi.ThrowableRenderer;

    import java.util.ArrayList;
    import java.util.Arrays;

    public class CustomThrowableRenderer implements ThrowableRenderer {
        private final DefaultThrowableRenderer defaultRenderer = new DefaultThrowableRenderer();

        @Override
        public String[] doRender(Throwable throwable) {
            String[] defaultRepresentation = defaultRenderer.doRender(throwable);
            String[] newRepresentation = {String.join("|", Arrays.asList(defaultRepresentation))};

            return newRepresentation;
        }
    }
