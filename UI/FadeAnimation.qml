import QtQuick 2.12

SequentialAnimation{
    id: root
    property QtObject target
    property string fadeProperty: "opacity"
    property int fadeDuration: 250
    property alias outValue: outAnimation.to
    property alias inValue: inAnimation.to
    property alias outEasingType: outAnimation.easing.type
    property alias inEasingType: inAnimation.easing.type
    property string easingType: "Quad"

    NumberAnimation{
        id: outAnimation
        target: root.target
        property: root.fadeProperty
        duration: root.fadeDuration
        to: 0
        easing.type: Easing["In"+root.easingType]
    }

    PropertyAction{}

    NumberAnimation{
        id: inAnimation
        target: root.target
        property: root.fadeProperty
        duration: root.fadeDuration
        to: 1
        easing.type: Easing["Out"+root.easingType]
    }
}