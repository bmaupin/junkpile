import XCTest
@testable import Epub

class EpubTests: XCTestCase {
    let testEpubFileName = "test.epub"

    func testEpubInitFromFile() {
        let bundle = Bundle(for: type(of: self))

        XCTAssertNotNil(bundle, "bundle is nil")

        // TODO: clean this up once we get test resources working in OS X
        print("DEBUG bundle.bundlePath: " + bundle.bundlePath)
        print("DEBUG bundle.bundleURL: " + bundle.bundleURL.absoluteString)
        print("DEBUG bundle.resourcePath: " + bundle.resourcePath!)
        print("DEBUG bundle.resourceURL: " + bundle.resourceURL!.absoluteString)
        print("DEBUG bundle.path(forResource: \"test\", ofType: \"epub\"): " + bundle.path(forResource: "test", ofType: "epub")!)
        print("DEBUG bundle.url(forResource: \"test\", withExtension: \"epub\"): " + bundle.url(forResource: "test", withExtension: "epub")!.absoluteString)

        let testEpubFileURL = bundle.url(
            forResource: testEpubFileName.components(separatedBy: ".")[0],
            withExtension: testEpubFileName.components(separatedBy: ".")[1])

        XCTAssertNotNil(testEpubFileURL, "testEpubFileURL is nil")

        let _ = Epub(fromFile: testEpubFileURL!)
    }

    static var allTests : [(String, (EpubTests) -> () throws -> Void)] {
        return [
            ("testEpubInitFromFile", testEpubInitFromFile),
        ]
    }
}

// TODO: Bundle.init(for: ) not yet implemented in Linux
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
