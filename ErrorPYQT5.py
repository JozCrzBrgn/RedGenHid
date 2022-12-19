import sys
from ui_Error import *

class ErrorWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Ui_UI_Error()
        self.ui.setupUi(self)

        # REMOVE TITLE FROM BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # BACKGROUND TO TRANSPARENT
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # BUTTON
        self.ui.btn_close.clicked.connect(self.close)

        self.show()

        self.TextoError("Error de PResion")

    def TextoError(self,texto):
        self.ui.label.setText(texto)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = ErrorWindow()
    myapp.show()
    sys.exit(app.exec_())
