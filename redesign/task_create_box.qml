import QtQuick 2.0

Item {




    MouseArea {
        id: start_btn
        x: 250
        y: 270
        width: 140
        height: 50
        onClicked: {
            pipeline.visible = true
        }

        Rectangle {
            id: start_tag
            x: 0
            y: 0
            width: 140
            height: 50
            color: "#ffa900"
            Text {
                id: start_text
                color: "#ffffff"
                text: qsTr("开始")
                font.bold: true
                wrapMode: Text.WrapAtWordBoundaryOrAnywhere
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                font.pixelSize: 18
            }
        }
    }
}
