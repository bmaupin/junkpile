import Foundation

internal struct Util {
    static func createTempDirectory(prefix: String) -> URL? {
        let tempFolderPath = NSTemporaryDirectory() + prefix + NSUUID().uuidString
        let tempFolderURL = URL(fileURLWithPath: tempFolderPath, isDirectory: true)

        do {
            try FileManager.default.createDirectory(at: tempFolderURL, withIntermediateDirectories: true,
                attributes: nil)
        } catch {
            return nil
        }

        return tempFolderURL
    }
}
