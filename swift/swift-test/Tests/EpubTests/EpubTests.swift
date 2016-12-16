import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    var epub: Epub?
    var epubTitle = "My title"

    override func setUp() {
        super.setUp()

        epub = Epub(title: epubTitle)
    }

    override func tearDown() {
        // TODO: add code to delete generated epub

        super.tearDown()
    }

    // func testExample() {
    //     // This is an example of a functional test case.
    //     // Use XCTAssert and related functions to verify your tests produce the correct results.
    //     XCTAssertEqual(Epub().text, "Hello, World!")
    // }

    static var allTests : [(String, (EpubTests) -> () throws -> Void)] {
        return [
            // ("testExample", testExample),
        ]
    }
}
