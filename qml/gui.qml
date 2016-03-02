import Material 0.2
import Material.ListItems 0.1 as ListItem
import Material.Extras 0.1

import QtQuick 2.4
import QtQuick.Layouts 1.1
import QtQuick.Controls.Styles 1.4

ApplicationWindow{
    title: qsTr("Copy Everything")
    minimumHeight: Units.dp(400)
    minimumWidth: Units.dp(300)
    maximumHeight: Units.dp(400)
    maximumWidth: Units.dp(300)
    visible: true
    style: ApplicationWindowStyle {
            background: BorderImage {
                source: "img/login_background.jpg"
                border { left: 0; top: 0; right: 0; bottom: 0 }
            }
    }

    theme {
        primaryColor: "blue"
        accentColor: "red"
        tabHighlightColor: "white"
    }

    id: appWin
    objectName: "appWin"

    FontLoader {
        id: fontLoader
        source: "fonts/LobsterTwo-Bold.ttf"
    }

    Item{
        id: loginHandle
        objectName: "loginHandle"
        function loginResult(outcome){
           if(outcome == "good"){
               loginHandle.setError(passwordField, Palette.colors["green"]["500"], "")
               loginHandle.setError(emailField, Palette.colors["green"]["500"], "")
               progressCircle.visible = true;
               progressCircle.color = Palette.colors["green"]["900"]
               progressCircle.indeterminate = false;
               errorLabel.visible = false;
               checkDone.visible = true;
           }else{
               emailField.readOnly = false;
               passwordField.readOnly = false;
               submitButton.enabled = true;
               progressCircle.visible = false;

               errorLabel.text = outcome;
               errorLabel.color = Palette.colors["red"]["500"];
               errorLabel.visible = true;

               var lowerCaseOutcome = outcome.toLowerCase()
               if (lowerCaseOutcome.indexOf("password") > -1){
                   loginHandle.setError(passwordField, Palette.colors["red"]["500"], "Incorrect Password")
               }else if (lowerCaseOutcome.indexOf("email") > -1 || lowerCaseOutcome.indexOf("user") > -1){
                   loginHandle.setError(emailField, Palette.colors["red"]["500"], "Incorrect Email")
               }
           }
        }

        function setError(obj, color, outcome){
            obj.errorColor = color
            obj.helperText = outcome
            obj.hasError = true
        }
    }

    Action{
        id: quitAction
        text: "&Exit"
        shortcut: "Ctrl+Q"
        onTriggered: py.stop()
        tooltip: "Quit the program"
    }

    View {
            anchors.centerIn: parent

            width: Units.dp(250)
            height: Units.dp(350)

            elevation: 1
            radius: Units.dp(3)

            ColumnLayout {
                id: column
                spacing: Units.dp(0)
                width: Units.dp(250)
                anchors {
                    centerIn: parent
                    topMargin: Units.dp(16)
                    bottomMargin: Units.dp(0)
                }

                Label {
                    id: titleLabel
                    font.family: fontLoader.name
                    font.weight: Font.Bold
                    text: "Copy Everything"
                    color: "black"
                    font.pixelSize: Units.dp(35)

                    anchors {
                        horizontalCenter: parent.horizontalCenter
                        margins: Units.dp(100)
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Units.dp(8)
                }

                ListItem.Standard {
                    Layout.preferredHeight: Units.dp(60)
                    content: TextField {
                        objectName: "emailField"
                        id: emailField
                        anchors.centerIn: parent
                        width: parent.width
                        placeholderText: "Email"
                        floatingLabel: false
                        color: Palette.colors["blue"]["500"]
                        validator: RegExpValidator {
                            regExp:/\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*/
                        }
                        onTextChanged: {
                            emailField.errorColor = Palette.colors["blue"]["500"];
                            emailField.helperText = ""
                        }
                    }
                }

                ListItem.Standard {
                    Layout.preferredHeight: Units.dp(60)
                    content: TextField {
                        objectName: "passwordField"
                        id: passwordField
                        anchors.centerIn: parent
                        width: parent.width
                        placeholderText: "Password"
                        floatingLabel: false
                        echoMode: TextInput.Password
                        color: Palette.colors["blue"]["500"]

                        onTextChanged: {
                            emailField.errorColor = Palette.colors["blue"]["500"];
                            emailField.helperText = ""
                        }
                        onAccepted: {
                            if (passwordField.text === "password") {
                                loginHandle.setError(passwordField, "blue", "Nice 'password'");
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Units.dp(10)
                }

                ListItem.Standard{
                    content:
                    Button {
                        objectName: "submitButton"
                        id: submitButton
                        backgroundColor: "#448684"
                        text: "Sign in or Register"
                        enabled: true
                        anchors.horizontalCenter: parent.horizontalCenter
                        onClicked:{
                            if(emailField.length == 0 && passwordField.length == 0){
                                Qt.openUrlExternally("https://copyeverythingapp.com");
                                errorLabel.text = "Opened registration page in browser";
                                errorLabel.color = "#448684";
                                errorLabel.visible = true;
                                return;
                            }

                            if(emailField.length < 4){
                               loginHandle.setError(emailField, Palette.colors["red"]["500"], "Incorrect Email");
                            }else{
                               loginHandle.setError(emailField, Palette.colors["blue"]["500"], "");
                            }
                            if(passwordField.length < 8){
                                loginHandle.setError(passwordField, Palette.colors["red"]["500"], "Incorrect Password");
                            }else{
                                loginHandle.setError(passwordField, Palette.colors["blue"]["500"], "");
                            }

                            if(emailField.length > 0 && passwordField.length >= 8){
                                submitButton.enabled = false;
                                emailField.readOnly = true;
                                passwordField.readOnly = true;
                                progressCircle.visible = true;
                                errorLabel.visible = false;
                                py.login(emailField.text, passwordField.text)
                            }
                        }
                    }
                }

                Item {
                    Layout.fillWidth: true
                    Layout.preferredHeight: Units.dp(8)
                }


                ListItem.Standard{
                    content:
                    Label {
                        id: errorLabel
                        font.family: "Roboto"
                        text: "Error connecting to server, trying again..."
                        color: Palette.colors["red"]["500"]
                        font.pixelSize: Units.dp(12)

                        anchors {
                            horizontalCenter: parent.horizontalCenter
                            margins: Units.dp(100)
                        }
                        visible: false
                    }
                    Icon {
                        id: checkDone
                        anchors.centerIn: parent
                        name: "action/done"
                        color: Palette.colors["green"]["900"]
                        visible: false
                    }
                    ProgressCircle {
                        id: progressCircle
                        Layout.alignment: Qt.AlignCenter
                        indeterminate: true
                        color: "#448684"
                        anchors.horizontalCenter: parent.horizontalCenter
                        width: Units.dp(50)
                        height: Units.dp(50)
                        minimumValue: 0
                        maximumValue: 100
                        value: 100
                        dashThickness: Units.dp(4)
                        visible: false
                    }
                }
            }
        }
}
