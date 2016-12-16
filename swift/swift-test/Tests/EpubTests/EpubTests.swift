import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    func testExample() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        XCTAssertEqual(Epub().text, "Hello, World!")
    }


    static var allTests : [(String, (EpubTests) -> () throws -> Void)] {
        return [
            ("testExample", testExample),
        ]
    }
}
