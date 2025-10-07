/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick
import QtQuick.Controls
import UntitledProject

Rectangle {
    id: rectangle
    width: 1400
    height: 700
    color: Constants.backgroundColor


    Button {
        id: explorar
        width: 100
        height: 42
        text: qsTr("EXPLORAR")
        anchors.verticalCenter: parent.verticalCenter
        highlighted: true
        font.styleName: "Bold"
        anchors.verticalCenterOffset: -280
        anchors.horizontalCenterOffset: 365
        checkable: true
        anchors.horizontalCenter: parent.horizontalCenter

        Connections {
            target: explorar
            onClicked: animation.start()
        }
    }

    Button {
        id: fusion
        width: 100
        height: 42
        text: qsTr("FUSIONAR")
        anchors.verticalCenter: parent.verticalCenter
        highlighted: true
        font.styleName: "Bold"
        flat: false
        Connections {
            target: fusion
            function onClicked() { animation.start() }
        }
        checkable: true
        anchors.verticalCenterOffset: -280
        anchors.horizontalCenterOffset: 592
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Button {
        id: cargar
        width: 100
        height: 42
        text: qsTr("CARGAR")
        anchors.verticalCenter: parent.verticalCenter
        highlighted: true
        flat: false
        font.styleName: "Bold"
        Connections {
            target: cargar
            function onClicked() { animation.start() }
        }
        checkable: true
        anchors.verticalCenterOffset: -280
        anchors.horizontalCenterOffset: 479
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Image {
        id: img
        x: 32
        y: 117
        width: 926
        height: 516
        source: "qrc:/qtquickplugin/images/template_image.png"
        fillMode: Image.PreserveAspectFit
    }

    Text {
        id: titulo
        x: 436
        y: 15
        text: qsTr("VISOR DE IMÁGENES")
        font.pixelSize: 40
        font.styleName: "Bold"
        font.weight: Font.DemiBold
        font.family: "Courier"
        rotation: 0
    }

    Text {
        id: text1
        x: 62
        y: 67
        text: qsTr("Archivo de imagen:")
        font.pixelSize: 20
    }

    Rectangle {
        id: ruta_img
        x: 246
        y: 67
        width: 698
        height: 29
        color: "#ffffff"
    }


    Text {
        id: brillo
        x: 974
        y: 117
        text: qsTr("Brillo: ")
        font.pixelSize: 20
        font.styleName: "Semibold"

        Slider {
            id: porcentaje_barra_brillo
            x: 247
            y: 0
            width: 168
            height: 27
            value: 0.5
            rotation: 0
        }

        ComboBox {
            id: porcentaje_brillo
            x: 159
            y: 0
            width: 82
            height: 27
            clip: false
        }
    }


    Text {
        id: contraste
        x: 974
        y: 156
        text: qsTr("Contraste:")
        font.pixelSize: 20
        font.styleName: "Semibold"
        Slider {
            id: porcentaje_barra_contrate
            x: 247
            y: 0
            width: 168
            height: 27
            value: 0.5
            rotation: 0
        }

        ComboBox {
            id: porcentaje_contrate
            x: 159
            y: 0
            width: 82
            height: 27
            clip: false
        }
    }

    Text {
        id: rotar
        x: 974
        y: 194
        text: qsTr("Rotación:")
        font.pixelSize: 20
        font.styleName: "Semibold"
        Slider {
            id: porcentaje_rotar_barra
            x: 247
            y: 0
            width: 168
            height: 27
            value: 0.5
            rotation: 0
        }

        ComboBox {
            id: porcentaje_rotar
            x: 159
            y: 0
            width: 82
            height: 27
            clip: false
        }
    }

    Text {
        id: transparencia
        x: 974
        y: 232
        text: qsTr("Transparencia:")
        font.pixelSize: 20
        font.styleName: "Semibold"
        Slider {
            id: porcentaje_transparencia_barra
            x: 247
            y: 0
            width: 168
            height: 27
            value: 0.5
            rotation: 0
        }

        ComboBox {
            id: porcentaje_transparencia
            x: 159
            y: 0
            width: 82
            height: 27
            clip: false
        }
    }

    Text {
        id: binarizar
        x: 974
        y: 271
        text: qsTr("Binarizar:")
        font.pixelSize: 20
        font.styleName: "Semibold"

        ComboBox {
            id: valor_binarizar
            x: 159
            y: 0
            width: 82
            height: 27
            clip: false
        }
    }

    RadioButton {
        id: zonas_claras
        x: 974
        y: 309
        visible: true
        text: qsTr("Zonas claras")
        font.styleName: "Semibold"
        clip: false
        checked: false
    }

    RadioButton {
        id: zonas_oscuras
        x: 1118
        y: 309
        visible: true
        text: qsTr("Zonas oscuras")
        font.styleName: "Semibold"
        clip: false
        checked: false
    }


    Text {
        id: rgb
        x: 974
        y: 400
        text: qsTr("Canales RGB:")
        font.pixelSize: 20
        font.styleName: "Semibold"

        CheckBox {
            id: red
            x: 0
            y: 36
            width: 76
            height: 24
            text: qsTr("Red")
            checked: false
            font.styleName: "Semibold"
        }

        CheckBox {
            id: green
            x: 131
            y: 36
            width: 92
            height: 24
            text: qsTr("Green")
            font.styleName: "Semibold"
            checked: false
        }

        CheckBox {
            id: blue
            x: 254
            y: 36
            width: 76
            height: 24
            text: qsTr("Blue")
            font.styleName: "Semibold"
            checked: false
        }
    }

    Text {
        id: cmy
        x: 974
        y: 471
        text: qsTr("Canales CMY:")
        font.pixelSize: 20
        font.styleName: "Semibold"
        CheckBox {
            id: cyan
            x: 0
            y: 36
            width: 76
            height: 24
            text: qsTr("Cyan")
            font.styleName: "Semibold"
            checked: false
        }

        CheckBox {
            id: magenta
            x: 131
            y: 36
            width: 107
            height: 24
            text: qsTr("Magenta")
            font.styleName: "Semibold"
            checked: false
        }

        CheckBox {
            id: yellow
            x: 254
            y: 36
            width: 96
            height: 24
            text: qsTr("Yellow")
            font.styleName: "Semibold"
            checked: false
        }
    }

    Button {
        id: actualizar
        width: 121
        height: 42
        text: qsTr("ACTUALIZAR")
        anchors.verticalCenter: parent.verticalCenter
        highlighted: true
        font.styleName: "Bold"
        flat: false
        Connections {
            target: actualizar
            function onClicked() { animation.start() }
        }
        checkable: true
        anchors.verticalCenterOffset: 262
        anchors.horizontalCenterOffset: 335
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Button {
        id: guardar
        width: 121
        height: 42
        text: qsTr("GUARDAR")
        anchors.verticalCenter: parent.verticalCenter
        highlighted: true
        font.styleName: "Bold"
        flat: false
        Connections {
            target: guardar
            function onClicked() { animation.start() }
        }
        checkable: true
        anchors.verticalCenterOffset: 262
        anchors.horizontalCenterOffset: 623
        anchors.horizontalCenter: parent.horizontalCenter
    }

    Button {
        id: zoom
        width: 121
        height: 42
        text: qsTr("ZOOM")
        anchors.verticalCenter: parent.verticalCenter
        highlighted: true
        font.styleName: "Bold"
        flat: false
        Connections {
            target: zoom
            function onClicked() { animation.start() }
        }
        checkable: true
        anchors.verticalCenterOffset: 262
        anchors.horizontalCenterOffset: 480
        anchors.horizontalCenter: parent.horizontalCenter
    }

    CheckBox {
        id: histograma
        x: 1118
        y: 363
        width: 184
        height: 24
        text: qsTr("Visualizar Histograma")
        font.styleName: "Semibold"
        checked: false
    }

    CheckBox {
        id: negativo
        x: 974
        y: 363
        width: 113
        height: 24
        text: qsTr("Negativo")
        font.styleName: "Semibold"
        checked: false
    }













    states: [
        State {
            name: "clicked"
            when: explorar.checked
        }
    ]
}

/*##^##
Designer {
    D{i:0}D{i:1;locked:true}D{i:3;locked:true}D{i:5;locked:true}D{i:7;locked:true}D{i:8;locked:true}
D{i:9;locked:true}D{i:10;locked:true}D{i:11;locked:true}D{i:14;locked:true}D{i:17;locked:true}
D{i:20;locked:true}D{i:23;locked:true}D{i:25;locked:true}D{i:26;locked:true}D{i:27}
D{i:29}D{i:30}D{i:31}D{i:35}D{i:37}D{i:39}D{i:41}D{i:42}
}
##^##*/
