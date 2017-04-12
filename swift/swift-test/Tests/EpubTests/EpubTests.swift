import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    var epub: Epub!
    var testEpubFileURL: URL!

    override func setUp() {
        super.setUp()

        print("DEBUG: setUp")

        // TODO: Bundle.init(for: ) not yet implemented in Linux
        let bundle = Bundle(for: type(of: self))

        print("DEBUG: bundle=" + String(describing: bundle))

        // let bundle = Bundle(path: FileManager.default.currentDirectoryPath + "/Tests/EpubTests")!
        testEpubFileURL = bundle.url(forResource: "test", withExtension: "epub")!

        print("DEBUG: testEpubFileURL=" + String(describing: testEpubFileURL))
    }

    override func tearDown() {
        // TODO: add cleanup code

        super.tearDown()
    }

    func testEpubInitFromFile() {
        print("DEBUG: testEpubInitFromFile()")

        let _ = Epub(fromFile: testEpubFileURL)

        // TODO: test to make sure the epub's actually been successfully opened (get title, etc)
    }

    static var allTests : [(String, (EpubTests) -> () throws -> Void)] {
        return [
            ("testEpubInitFromFile", testEpubInitFromFile),
        ]
    }
}

#if os(Linux)
extension Bundle {
    convenience init(for aClass: AnyClass) {
        if String(describing: aClass).hasSuffix("Tests") {
            self.init(path: FileManager.default.currentDirectoryPath + "/Tests/" + String(describing: aClass))!
        } else {
            self.init(path: "")!
        }
    }
}
#endif
