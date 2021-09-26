import Foundation

internal struct Util {
    static func createTempDirectory(prefix: String = "") -> URL? {
        let tempDirPath = NSTemporaryDirectory() + prefix + NSUUID().uuidString
        let tempDirURL = URL(fileURLWithPath: tempDirPath, isDirectory: true)

        do {
            try FileManager.default.createDirectory(at: tempDirURL, withIntermediateDirectories: true,
                attributes: nil)
        } catch {
            return nil
        }

        return tempDirURL
    }
}
