def global_style():

    """ Return a stylesheet for the application.
    """


    stylesheet = """

    QMainWindow {
        background-color: white;
    }

    QFrame {
        background-color: lightblue;
        border-width: 2px;
        border-style: solid;
        border-color: grey;
    }

    QListWidget {
        background-color: white;
    }

    QLineEdit {
        border-width: 2px;
        border-style: solid;
        border-color: white;
    }

    QPushButton {
        border-style: solid;
        border-width: 0px;
        background-color: white;
        color: grey;
    }

    QLabel {
        border-style: solid;
        border-width: 0px;
        color: white;
    }


    """


    return stylesheet
