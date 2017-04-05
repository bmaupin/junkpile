import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    var epub: Epub!
    // var epubTitle = "My title"

    override func setUp() {
        super.setUp()

        // epub = Epub(title: epubTitle)
    }

    override func tearDown() {
        // TODO: add code to delete generated epub

        super.tearDown()
    }

    func testEpubInitFromFile() {
        // TODO: Bundle.init(for: ) not yet implemented in Linux
        //let testEpubFilePath = Bundle(for: type(of: self)).url(forResource: "test", withExtension: "epub")!
        let testEpubFilePath = Bundle(path: FileManager.default.currentDirectoryPath + "/Tests/EpubTests")!.url(forResource: "test", withExtension: "epub")!
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
