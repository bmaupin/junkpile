import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    var epub: Epub!
    var testEpubFilePath: URL!

    override func setUp() {
        super.setUp()

        // TODO: Bundle.init(for: ) not yet implemented in Linux
        //let bundle = Bundle(for: type(of: self))
        let bundle = Bundle(path: FileManager.default.currentDirectoryPath + "/Tests/EpubTests")!
        testEpubFilePath = bundle.url(forResource: "test", withExtension: "epub")!
    }

    override func tearDown() {
        // TODO: add cleanup code

        super.tearDown()
    }

    func testEpubInitFromFile() {
        let _ = Epub(fromFile: testEpubFilePath)

        // TODO: test to make sure the epub's actually been successfully opened (get title, etc)
    }

    static var allTests : [(String, (EpubTests) -> () throws -> Void)] {
        return [
            ("testEpubInitFromFile", testEpubInitFromFile),
        ]
    }
}
