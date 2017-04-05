import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    var epub: Epub!
    // var epubTitle = "My title"
    var testEpubFilePath: URL!

    override func setUp() {
        super.setUp()

        // TODO: Bundle.init(for: ) not yet implemented in Linux
        //let bundle = Bundle(for: type(of: self))
        let bundle = Bundle(path: FileManager.default.currentDirectoryPath + "/Tests/EpubTests")!
        testEpubFilePath = bundle.url(forResource: "test", withExtension: "epub")!

        // epub = Epub(title: epubTitle)
    }

    override func tearDown() {
        // TODO: add code to delete generated epub

        super.tearDown()
    }

    func testEpubInitFromFile() {
        let _ = Epub(fromFile: testEpubFilePath)
    }

    // func testExample() {
    //     // This is an example of a functional test case.
    //     // Use XCTAssert and related functions to verify your tests produce the correct results.
    //     XCTAssertEqual(Epub().text, "Hello, World!")
    // }

    static var allTests : [(String, (EpubTests) -> () throws -> Void)] {
        return [
            ("testEpubInitFromFile", testEpubInitFromFile),
        ]
    }
}
