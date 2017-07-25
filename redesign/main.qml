import QtQuick 2.6
import QtQuick.Window 2.2
import QtGraphicalEffects 1.0

Window {
    id: root
    width: 530
    height: 320
    flags: Qt.FramelessWindowHint | Qt.Window
    color: "transparent"

    Item {
        id: pipeline
        x: 540
        y: 0
        width: 130
        height: 320
        visible: false

        RectangularGlow {
            anchors.fill: pipeline_box
            color: "#000000"
            glowRadius: 10
            cornerRadius: 25
        }

        RectangularGlow {
            anchors.fill: small_tr
            color: "#000000"
            glowRadius: 10
            cornerRadius: 25
        }

        Rectangle {
            id: pipeline_box
            x: 0
            y: 0
            width: 130
            height: 320
            color: "#ffffff"
        }

        Rectangle {
            id: small_tr
            x: -7
            y: 285
            width: 15
            height: 15
            color: "#ffffff"
            rotation: 45
        }

        Rectangle {
            id: rectangle1
            x: 0
            y: 270
            width: 130
            height: 50
            color: "#ffffff"
        }

        Rectangle {
            id: rectangle2
            x: 0
            y: 0
            width: 130
            height: 40
            color: "#ffffff"
        }
    }

    Item {
        id: main
        width: 530
        height: 320

        Loader {
            source: "nav_box.qml"
        }

        Item {
            id: task_choose
            width: 530
            height: 320
            visible: true

            RectangularGlow {
                anchors.fill: task_choose_tag
                color: "#000000"
                glowRadius: 10
                cornerRadius: 25
            }
            RectangularGlow {
                anchors.fill: task_choose_box
                color: "#000000"
                cached: false
                anchors.rightMargin: 360
                glowRadius: 10
                cornerRadius: 25
            }

            Rectangle {
                id: task_choose_box
                x: 140
                y: 0
                width: 390
                height: 320
                color: "#ffffff"

                Loader {
                    source: "task_choose_box.qml"
                }
            }

            Rectangle {
                id: task_choose_tag
                x: 0
                y: 0
                width: 140
                height: 50
                visible: true
                color: "#ffffff"

                Text {
                    id: text0
                    text: qsTr("选择任务")
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 18
                }
            }
        }

        Item {
            id: task_create
            x: 0
            y: 0
            width: 530
            height: 320
            visible: false

            RectangularGlow {
                anchors.fill: task_create_tag
                color: "#000000"
                glowRadius: 10
                cornerRadius: 25
            }
            RectangularGlow {
                anchors.fill: task_create_box
                color: "#000000"
                anchors.rightMargin: 360
                glowRadius: 10
                cornerRadius: 25
            }

            Rectangle {
                id: task_create_box
                x: 140
                y: 0
                width: 390
                height: 320
                color: "#ffffff"
                Loader {
                    source:"task_create_box.qml";
                }
            }

            Rectangle {
                id: task_create_tag
                x: 0
                y: 50
                width: 140
                height: 50
                color: "#ffffff"

                Text {
                    id: text1
                    text: qsTr("创建任务")
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 18
                }
            }
        }

        Item {
            id: contact
            x: 0
            y: 0
            width: 530
            height: 320
            visible: false

            RectangularGlow {
                anchors.fill: contact_tag
                color: "#000000"
                glowRadius: 10
                cornerRadius: 25
            }
            RectangularGlow {
                anchors.fill: contact_box
                color: "#000000"
                anchors.rightMargin: 360
                glowRadius: 10
                cornerRadius: 25
            }

            Rectangle {
                id: contact_box
                x: 140
                y: 0
                width: 390
                height: 320
                color: "#ffffff"
            }

            Rectangle {
                id: contact_tag
                x: 0
                y: 100
                width: 140
                height: 50
                color: "#ffffff"

                Text {
                    id: text2
                    text: qsTr("联系作者")
                    horizontalAlignment: Text.AlignHCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 18
                }
            }
        }

        MouseArea {
            id: drag_area1
            x: 140
            y: 0
            width: 390
            height: 40
            property variant clickPos: "1,1"
            onPressed: {
                clickPos = Qt.point(mouse.x, mouse.y)
            }

            onPositionChanged: {
                var delta = Qt.point(mouse.x - clickPos.x, mouse.y - clickPos.y)
                root.x += delta.x
                root.y += delta.y
            }
        }

        MouseArea {
            id: drag_area2
            x: 140
            y: 40
            width: 45
            height: 280
            property variant clickPos: "1,1"
            onPressed: {
                clickPos = Qt.point(mouse.x, mouse.y)
            }

            onPositionChanged: {
                var delta = Qt.point(mouse.x - clickPos.x, mouse.y - clickPos.y)
                root.x += delta.x
                root.y += delta.y
            }
        }
    }
}
