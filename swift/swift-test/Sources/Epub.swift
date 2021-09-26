import Foundation
import PerfectZip

public struct Epub {
    let tempDirectoryPrefix = "swift-epub"

    var tempDirectory: URL!

    private init() {
        tempDirectory = Util.createTempDirectory(prefix: tempDirectoryPrefix)
    }

    init(fromFile fileURL: URL) {
        self.init()
        // TODO handle this error better
        do {
            try extractEpubFile(fileURL: fileURL)
        } catch (let error) {
            print(error)
        }
    }

    func extractEpubFile(fileURL: URL) throws {
        let zip = Zip()

        let UnzipResult = zip.unzipFile(
            source: fileURL.path,
            destination: tempDirectory.path,
            overwrite: true
        )

        if UnzipResult != ZipStatus.ZipSuccess {
            throw UnzipResult
        }
    }
}
