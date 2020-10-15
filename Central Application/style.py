def global_style():
    
    """ Return a stylesheet for the application.
    """


    stylesheet = """

    QMainWindow {
        background-color: #21275C;
    }

    QFrame {
        background-color: lightblue;
        border-width: 2px;
        border-style: solid;
        border-color: grey;
    }

    QPushButton {
        border-style: solid;
        border-width: 0px;
        background-color: white;
        color: #21275C;
    }

    QLabel {
        border-style: solid;
        border-width: 0px;
        color: White;
        background-color: #21275C;
    }

    QWidget#ItemWindow {
        background-color: #8AA2C0;
    }


    """


    return stylesheet
