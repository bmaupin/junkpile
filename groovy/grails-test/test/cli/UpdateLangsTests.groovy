import grails.test.AbstractCliTestCase

class UpdateLangsTests extends AbstractCliTestCase {
    protected void setUp() {
        super.setUp()
    }

    protected void tearDown() {
        super.tearDown()
    }

    void testUpdateLangs() {

        execute(["update-langs"])

        assertEquals 0, waitForProcess()
        verifyHeader()
    }
}
