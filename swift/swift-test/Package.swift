import PackageDescription

let package = Package(
    name: "Epub",
    dependencies: [
        // TODO: Replace this with a pure Swift zip library when that becomes available because:
        //  - A pure Swift library wouldn't require separate installation of C zip libraries
        //  - Pure Swift libraries can be used within the REPL
        .Package(url: "https://github.com/PerfectlySoft/Perfect-Zip.git",
                 majorVersion: 2)
    ]
)
