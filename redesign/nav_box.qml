import QtQuick 2.0

Item {
    id: nav
    width: 145
    height: 320
    Rectangle {
        id: nav_bar
        width: 145
        height: 270
        color: "#ce4617"
    }
    MouseArea {
        id: task_choose_tab
        x: 0
        y: 0
        width: 140
        height: 50

        Text {
            id: task_choose_text
            color: "#ffffff"
            text: qsTr("选择任务")
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 18
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
        }
        onClicked: {
            task_choose.visible = true
            task_create.visible = false
            contact.visible = false
        }
    }

    MouseArea {
        id: mouseArea1
        x: 0
        y: 50
        width: 140
        height: 50

        Text {
            id: text5
            color: "#ffffff"
            text: qsTr("创建任务")
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 18
            anchors.horizontalCenter: parent.horizontalCenter
            font.bold: true
            anchors.verticalCenter: parent.verticalCenter
        }
        onClicked: {
            task_choose.visible = false
            task_create.visible = true
            contact.visible = false
        }
    }

    MouseArea {
        id: mouseArea2
        x: 0
        y: 100
        width: 140
        height: 50

        Text {
            id: text6
            color: "#ffffff"
            text: qsTr("联系作者")
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 18
            anchors.horizontalCenter: parent.horizontalCenter
            font.bold: true
            anchors.verticalCenter: parent.verticalCenter
        }
        onClicked: {
            task_choose.visible = false
            task_create.visible = false
            contact.visible = true
        }
    }

    MouseArea {
        id: mouseArea3
        x: 0
        y: 270
        width: 140
        height: 50

        Rectangle {
            id: exit_tag
            x: 0
            y: 0
            width: 145
            height: 50
            color: "#b02d00"
        }

        Text {
            id: exit_text
            color: "#ffffff"
            text: qsTr("退出")
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: 18
        }
        onClicked: Qt.quit()
    }
}
