import QtQuick 2.2
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.0

ApplicationWindow {
    title: "Go experiment"
    width: 600
    height: 400

    RowLayout {
        anchors.fill: parent

        Rectangle {
            width: 200
            color: "lightgrey"
        }

        TextArea {
            // Hide the frame around the text area
            frameVisible: false
            Layout.fillHeight: true
            Layout.fillWidth: true
        }
    }
}
