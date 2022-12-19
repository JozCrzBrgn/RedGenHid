import sys
from splash_screen import *

class ProgBar(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Ui_SplashScreen2()
        self.ui.setupUi(self)

        # REMOVE TITLE FROM BAR
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # BACKGROUND TO TRANSPARENT
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.progressBarValue(0,1)
        self.show()

    # GIVE VALUE TO PROGRESSBAR
    def progressBarValue(self, value, total):
        # PROGRESS STYLESHEET BASE:
        stylesheet = """
        QFrame{
        border-radius: 150px;
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1}
         rgba(255, 85, 255, 0), stop:{STOP_2} rgba(0, 170, 255, 255));
        }
        """

        # GET PROGRESS BAR VALUE, CONVERT TO FLOAT AND INVERT VALUES
        # STOP WORKS TO 1.000 TO 0.000
        progress = (total - value)/float(total)

        # GET NEW VALUES
        stop_1 = str(progress-0.001)
        stop_2 = str(progress)

        # SET VALUES TO NEW STYLESHEET
        newStylesheet = stylesheet.replace("{STOP_1}",stop_1).replace("{STOP_2}",stop_2)

        #APPLY STYLESHEET WITH NEW VALUES
        self.ui.circularProgress.setStyleSheet(newStylesheet)
        self.ui.labelPorcentaje.setText('<html><head/><body><p>' +
                                        str(int(value*100/total)) +
                                        '<span style=" vertical-align:super;">%</span></p></body></html>')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = ProgBar()
    myapp.show()
    sys.exit(app.exec_())
