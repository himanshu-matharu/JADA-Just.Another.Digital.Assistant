import QtQuick 2.12
import QtQuick.Controls 2.12

ApplicationWindow{
    visible: true
    width: 1024
    height: 576
    title: "JADA"
    color: "transparent"

    flags: Qt.FramelessWindowHint | Qt.Window

    property string centerText: ""
    Behavior on centerText {
        FadeAnimation{
            target:center
        }
    }
    property string topText: ""
    Behavior on topText {
        FadeAnimation{
            target: top
        }
    }
    property string bottomText: ""
    Behavior on bottomText {
        FadeAnimation{
            target: bottom
        }
    }
    property QtObject backend

    Rectangle{
        anchors.fill: parent
        color: "black"
        radius: 10

        Rectangle{
            anchors.fill: parent
            width: parent.width - 30
            height: parent.height
            color: "transparent"

            Button{
                id: start
                objectName: "startButton"
                anchors.centerIn: parent
                text: qsTr("Start")
                property bool stateVisible: true
                visible: opacity!=0

                background: Rectangle{
                    color: "black"
                }

                contentItem: Text{
                    color: "white"
                    font.pixelSize: 36
                    text: start.text
                }

                states:[
                    State {
                        when: start.stateVisible
                        PropertyChanges {
                            target: start
                            opacity:1
                        }
                    },
                    State {
                        when: !start.stateVisible
                        PropertyChanges {
                            target: start
                            opacity:0
                        }
                    }
                ]
                transitions: Transition{
                    NumberAnimation {
                        property:"opacity"
                        duration:500
                        easing.type:Easing.InOutQuad
                    }
                }
            }

            Text {
                id:center
                objectName: "center"
                font.pixelSize: 30
                color:"white"
                property bool stateVisible: false
                opacity:0
                visible: opacity!=0
                text: centerText
                wrapMode: Text.WordWrap
                anchors.fill: parent
                verticalAlignment: Text.AlignVCenter
                horizontalAlignment: Text.AlignHCenter

                states:[
                    State {
                        when: center.stateVisible
                        PropertyChanges {
                            target: center
                            opacity:1
                        }
                    },
                    State {
                        when: !center.stateVisible
                        PropertyChanges {
                            target: center
                            opacity:0
                        }
                    }
                ]
                transitions: Transition{
                    NumberAnimation {
                        property:"opacity"
                        duration:500
                        easing.type:Easing.InOutQuad
                    }
                }

            }

            Text {
                id: top
                objectName: "top"
                anchors{
                    top : parent.top
                    topMargin : 30
                    horizontalCenter : parent.horizontalCenter
                }
                font.pixelSize : 25
                color:"white"
                property bool stateVisible: false
                opacity:0
                visible: opacity!=0
                text: topText
                states:[
                    State {
                        when: top.stateVisible
                        PropertyChanges {
                            target: top
                            opacity:1
                        }
                    },
                    State {
                        when: !top.stateVisible
                        PropertyChanges {
                            target: top
                            opacity:0
                        }
                    }
                ]
                transitions: Transition{
                    NumberAnimation {
                        property:"opacity"
                        duration:500
                        easing.type:Easing.InOutQuad
                    }
                }
            }

            Text {
                id: bottom
                objectName: "bottom"
                anchors{
                    bottom : parent.bottom
                    bottomMargin : 30
                    horizontalCenter : parent.horizontalCenter
                }
                font.pixelSize : 25
                color:"white"
                property bool stateVisible: false
                opacity:0
                visible: opacity!=0
                text: bottomText
                states:[
                    State {
                        when: bottom.stateVisible
                        PropertyChanges {
                            target: bottom
                            opacity:1
                        }
                    },
                    State {
                        when: !bottom.stateVisible
                        PropertyChanges {
                            target: bottom
                            opacity:0
                        }
                    }
                ]
                transitions: Transition{
                    NumberAnimation {
                        property:"opacity"
                        duration:500
                        easing.type:Easing.InOutQuad
                    }
                }
            }

            Rectangle{
                anchors.centerIn: parent
                width: 400
                height: 300
                color: "transparent"

                AnimatedImage{
                    anchors.centerIn: parent
                    id: idleAnimation
                    objectName: "idleAnimation"
                    source: "./gifs/idle.gif"
                    property bool stateVisible: false
                    opacity:0
                    visible: opacity!=0
                    states:[
                        State {
                            when: idleAnimation.stateVisible
                            PropertyChanges {
                                target: idleAnimation
                                opacity:1
                            }
                        },
                        State {
                            when: !idleAnimation.stateVisible
                            PropertyChanges {
                                target: idleAnimation
                                opacity:0
                            }
                        }
                    ]
                    transitions: Transition{
                        NumberAnimation {
                            property:"opacity"
                            duration:250
                            easing.type:Easing.InOutQuad
                        }
                    }
                }

                AnimatedImage{
                    anchors.centerIn: parent
                    id: processAnimation
                    objectName: "processAnimation"
                    source: "./gifs/processing.gif"
                    property bool stateVisible: false
                    opacity:0
                    visible: opacity!=0
                    states:[
                        State {
                            when: processAnimation.stateVisible
                            PropertyChanges {
                                target: processAnimation
                                opacity:1
                            }
                        },
                        State {
                            when: !processAnimation.stateVisible
                            PropertyChanges {
                                target: processAnimation
                                opacity:0
                            }
                        }
                    ]
                    transitions: Transition{
                        NumberAnimation {
                            property:"opacity"
                            duration:250
                            easing.type:Easing.InOutQuad
                        }
                    }
                }
            }
        }
    }

    Connections {
        target: backend

        function onCenter(msg){
            centerText = msg
        }

        function onTop(msg){
            topText = msg
        }

        function onBottom(msg){
            bottomText = msg
        }
    }
}