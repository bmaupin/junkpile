import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    var epub: Epub!
    var testEpubFilePath: URL!

    override func setUp() {
        super.setUp()

        // print("self: " + String(describing: self))
        // print("type(of: self): " + String(describing: type(of: self)))
        // print("type(of: type(of: self)): " + String(describing: type(of: type(of: self))))

        // TODO: Bundle.init(for: ) not yet implemented in Linux
        let bundle = Bundle(for: type(of: self))
        // let bundle = Bundle(path: FileManager.default.currentDirectoryPath + "/Tests/EpubTests")!
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
