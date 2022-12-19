

from PyQt5 import QtCore, QtWidgets

class UIFunctions(QtWidgets.QMainWindow):
    def toggleMenu(self, maxWidth, enable):

        if enable:
            # Get width
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # Set max width
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # Animation
            self.animation = QtCore.QPropertyAnimation(self.ui.frame_left_menu, b'minimumWidth')
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()


    def Fn_Inicializar(self):
        """  Menu Desplegable """
        # Inicializar el programa siempre en la pantalla de inicio
        self.ui.Pages_Widget.setCurrentWidget(self.ui.pagina_0)
        # Quitar Titulo Predefinido de Pantalla
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Ocultar los botones del menu desplegable
        self.ui.btn_page_0.setHidden(True)
        self.ui.btn_page_1.setHidden(True)
        self.ui.btn_page_3.setHidden(True)
        self.ui.btn_page_5.setHidden(True)
        """ PAGINA: Introducir Datos """
        # Ocultar los groupBox y cambiar nombre del boton de carga de archivos
        self.ui.gb_csv.setHidden(True)
        self.ui.gb_excel.setHidden(True)
        self.ui.gb_manual.setHidden(False)
        self.ui.btn_load_info_epanet.setHidden(True)
        self.ui.btn_load_info.setText("Ajustar Tablas")
        # Crear Tabla de Nodos
        self.ui.txt_manual_nod.setValue(8)
        #                nod, demanda, tipo, cota  'Tanque'
        dataNod = [[22.0, 07.0, 'Embalse',50.0, 'E', 1.0],
                   [00.0, 07.0, 'nodo2', 70.0, 'N', 0.0],
                   [15.0, 05.0, 'nodo6', 60.0, 'N', 2.0],
                   [00.0, 00.0, 'nodo1', 100.0,'N', 3.0],
                   [15.0, 00.0, 'nodo5', 50.0, 'N', 4.0],
                   [22.0, 00.0, 'nodo7', 70.0, 'N', 6.0],
                   [06.0, 07.0, 'nodo4', 50.0, 'N', 7.0],
                   [06.0, 00.0, 'nodo3', 80.0, 'N', 8.0]]
        row = len(dataNod)
        col = len(dataNod[0])
        for i in range(row):
            self.ui.tbl_nod.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataNod[i][j]))
                self.ui.tbl_nod.setItem(i, j, celda)
        self.ui.tbl_nod.resizeColumnsToContents()
        # Crear Tabla de Tuberias
        self.ui.txt_manual_tub.setValue(10)
        dataTub = [['t1', 'nodo2', 'nodo4', 120.0, 254.0, 4.3, 0.0015],
                   ['t2', 'nodo5', 'nodo6', 60.0,  250.0, 2.4, 0.0015],
                   ['t3', 'nodo3', 'nodo1', 120.0, 250.0, 4.3, 0.0015],
                   ['t4', 'nodo7', 'nodo5', 100.0, 250.0, 3.8, 0.0015],
                   ['t5', 'nodo6', 'nodo4', 150.0, 300.0, 4.6, 0.0015],
                   ['t6', 'Embalse','nodo6', 500.0, 200.0, 3.6, 0.0015],
                   ['t7', 'nodo4', 'nodo3', 200.0, 200.0, 5.4, 0.0015],
                   ['t8', 'nodo5', 'nodo3', 80.0,  250.0, 3.2, 0.0015],
                   ['t9', 'Embalse','nodo7', 60.0,  250.0, 2.4, 0.0015],
                   ['t10','nodo2', 'nodo1', 200.0, 200.0, 5.4, 0.0015]]
        row = len(dataTub)
        col = len(dataTub[0])
        for i in range(row):
            self.ui.tbl_tub.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataTub[i][j]))
                self.ui.tbl_tub.setItem(i, j, celda)
        self.ui.tbl_tub.resizeColumnsToContents()
        """ PAGINA: Algoritmos Geneticos """
        # Condiciones iniciales para la poblacion
        self.ui.txt_tam_pob.setValue(5)
        self.ui.txt_num_gen.setValue(5)
        self.ui.txt_tasa_mut.setValue(0.05)
        # Restriciones de Diseño
        self.ui.txt_VDmax.setValue(5)
        self.ui.txt_VDmin.setValue(0.6)
        self.ui.txt_PDmax.setValue(50)
        self.ui.txt_PDmin.setValue(15)
        # Crear Tabla de Diametros a Usar
        self.ui.txt_num_diametros.setValue(19)

        dataDcom = [[50, 12.66],[60, 15.64], [75, 14.69], [100, 33.06], [150, 38.21], [200, 44.54],
                    [250, 52.09], [300, 60.08]]
        """dataDcom = [[50, 12.66], [75, 14.69], [100, 33.06], [150, 38.21], [200, 44.54],
                    [250, 52.09], [300, 60.08], [350, 70.05], [400, 77.99], [450, 86.63],
                    [500, 97.39], [600, 112.29], [750, 130.60], [800, 153.96], [1000, 173.27],
                    [1200, 203.32], [1400, 232.70], [1500, 247.17], [1800, 289.81]]"""
        row = len(dataDcom)
        col = len(dataDcom[0])
        for i in range(row):
            self.ui.tbl_Dcom.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(dataDcom[i][j]))
                self.ui.tbl_Dcom.setItem(i, j, celda)
        self.ui.tbl_Dcom.resizeColumnsToContents()
        # Crear Tabla de Mejores Diametros
        self.ui.tbl_mejor_diam.resizeColumnsToContents()


    def Fn_Buttons(self):
        """ Menu Desplegable """
        # Cerrar aplicacion
        self.ui.btn_close.clicked.connect(self.CerrarApp)
        # Minimizar la aplicacion
        self.ui.btn_max.clicked.connect(self.Minim)
        # Movernos entre Paginas
        self.ui.btn_page_0.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.pagina_0))
        self.ui.btn_page_1.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.pagina_1))
        self.ui.btn_page_3.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.pagina_3))
        self.ui.btn_page_5.clicked.connect(lambda: self.ui.Pages_Widget.setCurrentWidget(self.ui.pagina_5))

        """ PAGINA: Introducir Datos """
        # Botones de Carga de Datos para Manual:
        self.ui.btn_load_info.clicked.connect(self.Atr_MANUAL)
        # Botones de Carga de Datos para Excel:
        self.ui.btn_load_info.clicked.connect(self.Atr_XLSX)
        # Botones de Carga de Datos para CSV
        self.ui.btn_csv_nod.clicked.connect(self.Atr_CSVnod)
        self.ui.btn_csv_tub.clicked.connect(self.Atr_CSVtub)
        # Botones de Carga de Datos para Epanet
        self.ui.btn_load_info_epanet.clicked.connect(self.Atr_INP)
        self.ui.btn_load_info_XY.clicked.connect(self.Atr_INP_XY)
        # Botones que permite visualizar la red hidraulica:
        self.ui.btn_visualizar.clicked.connect(self.Atr_DibujarRedHidraulicaSeguros)

        """ PAGINA: Analisis de la Red Hidraulica """
        self.ui.btn_AnalisisRedHid.clicked.connect(self.Atr_AnalisisRedHidraulicaSeguros)


        """ PAGINA: Algoritmo Genetico"""
        self.ui.btn_AG.clicked.connect(self.Atr_AlgoritmoGenetico)
        self.ui.btn_guardar_diam_temp.clicked.connect(self.Fn_ResultadosTemporales)
        self.ui.btn_exportar_diam.clicked.connect(self.Fn_ExportarDiam)
        self.ui.btn_cargar_diam.clicked.connect(self.Fn_CargarListaDiametros)




    def Fn_RadioButtons(self):
        """ PAGINA: Introducir Datos """
        self.ui.rb_manual.clicked.connect(lambda: self.Atr_RadioButton_Interactivo("man"))
        self.ui.rb_inp.clicked.connect(lambda: self.Atr_RadioButton_Interactivo("inp"))
        self.ui.rb_csv.clicked.connect(lambda: self.Atr_RadioButton_Interactivo("csv"))
        self.ui.rb_xslx.clicked.connect(lambda: self.Atr_RadioButton_Interactivo("xlsx"))

        """ PAGINA: Algoritmo Genetico"""
        self.ui.rb_lineal.clicked.connect(lambda: self.Atr_RadioButton_Regresiones())
        self.ui.rb_potencial.clicked.connect(lambda: self.Atr_RadioButton_Regresiones())
        self.ui.rb_exponencial.clicked.connect(lambda: self.Atr_RadioButton_Regresiones())

    def Wgt_SpinBox(self):
        # Añadir renglones a la tabla de diametros y precios
        self.ui.txt_num_diametros.valueChanged.connect(self.Prop_AnadirRenglonSinCombo)








