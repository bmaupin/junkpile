import XCTest
@testable import PDF

class PDFTests: XCTestCase {
    func testExample() {
        // This is an example of a functional test case.
        // Use XCTAssert and related functions to verify your tests produce the correct results.
        XCTAssertEqual(PDF().text, "Hello, World!")
    }


    static var allTests : [(String, (PDFTests) -> () throws -> Void)] {
        return [
            ("testExample", testExample),
        ]
    }
}
