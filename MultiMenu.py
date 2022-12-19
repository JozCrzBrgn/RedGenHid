import sys
from os import mkdir as newDir
import math
from ui_ProgramAG import *
from ui_Functions import *
from ErrorPYQT5 import ErrorWindow
from FileTools import *
from clases_mpl_pyqt import *
import GradienteHidraulico as gh
import AlgoritmoGenetico as ag

class UIMainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """
            MANEJADOR DE EVENTOS
        """

        # Dar capacidad de mover la pantalla
        def moveWindow(event):
            #
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos()+event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        self.ui.frame_top.mouseMoveEvent = moveWindow

        # Abrir y cerrar menu principal
        self.ui.frame_left_menu.enterEvent = lambda e:self.Fn_MenuInteractivo(e)
        self.ui.frame_left_menu.leaveEvent = lambda e:self.Fn_MenuInteractivo(e)

        """ Acciones a realizar cuando se incia el programa """
        UIFunctions.Fn_Inicializar(self)

        """ Acciones que realizan los Botones """
        UIFunctions.Fn_Buttons(self)

        """ Acciones que realizan los RadioButtons """
        UIFunctions.Fn_RadioButtons(self)
        self.ui.rb_lineal.click()

        ''' Añadir renglones a la tabla de diametros y precios '''
        UIFunctions.Wgt_SpinBox(self)


    """
        #########################
        #  ATRIBUTOS DE LA GUI  #
        #########################
    """
    def Fn_MenuInteractivo(self,e):
        """Funcion para hacer interactivo el menu"""
        if e.type() == 10:
            UIFunctions.toggleMenu(self, 400, True)
            self.ui.btn_page_0.setHidden(False)
            self.ui.btn_page_1.setHidden(False)
            self.ui.btn_page_3.setHidden(False)
            self.ui.btn_page_5.setHidden(False)
        elif e.type() == 11:
            UIFunctions.toggleMenu(self, 400, True)
            self.ui.btn_page_0.setHidden(True)
            self.ui.btn_page_1.setHidden(True)
            self.ui.btn_page_3.setHidden(True)
            self.ui.btn_page_5.setHidden(True)

    def mousePressEvent(self, event):
        """Funcion para arrastrar la pantalla"""
        self.dragPos = event.globalPos()

    def CerrarApp(self):
        #Cerrar la aplicacion
        self.close()

    def Minim(self):
        """Funcion para minimizar la pantalla"""
        self.showMinimized()

    def msgErrorBox(self,mensage):
        print("si salio el mensaje")
        self.msgError = ErrorWindow()
        self.msgError.show()
        self.msgError.TextoError(mensage)

    def Fn_EmptyTable(self, table):
        val = 0
        row = table.rowCount()
        col = table.columnCount()
        for i in range(row):
            for j in range(col):
                if table.item(i, j).text()=="":
                    val+=1
        return val


    """
        ###########################################
        #  PAGINA: ANALISIS DE REDES HIDRAULICAS  #
        ###########################################
    """


    def Atr_RadioButton_Interactivo(self,val):
        """Funcion para hacer interactivo el grupo datos
        oculta o muestra los diferentes grupos de datos
        del groupBox"""
        if val == "man":
            self.ui.gb_csv.setHidden(True)
            self.ui.gb_excel.setHidden(True)
            self.ui.gb_manual.setHidden(False)
            self.ui.btn_load_info.setHidden(False)
            self.ui.btn_load_info_epanet.setHidden(True)
            self.ui.btn_load_info_XY.setHidden(True)
            self.ui.btn_load_info.setText("Ajustar Tablas")
        elif val == "csv":
            self.ui.gb_csv.setHidden(False)
            self.ui.gb_manual.setHidden(True)
            self.ui.gb_excel.setHidden(True)
            self.ui.btn_load_info.setHidden(True)
            self.ui.btn_load_info_epanet.setHidden(True)
            self.ui.btn_load_info_XY.setHidden(True)
        elif val == "xlsx":
            self.ui.gb_csv.setHidden(True)
            self.ui.gb_manual.setHidden(True)
            self.ui.gb_excel.setHidden(False)
            self.ui.btn_load_info.setHidden(False)
            self.ui.btn_load_info_epanet.setHidden(True)
            self.ui.btn_load_info_XY.setHidden(True)
            self.ui.btn_load_info.setText("Cargar Excel")
        elif val == "inp":
            self.ui.gb_csv.setHidden(True)
            self.ui.gb_manual.setHidden(True)
            self.ui.gb_excel.setHidden(True)
            self.ui.btn_load_info.setHidden(True)
            self.ui.btn_load_info_XY.setHidden(False)
            self.ui.btn_load_info_epanet.setHidden(False)

    def Fn_BuscadorDeArchivos(self, formato):
        """Abrir el buscador de Archivos"""
        options = QtWidgets.QFileDialog.Options()
        #options |= QtWidgets.QFileDialog.DontUseNativeDialog
        if formato == "csv":
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                "Archivos csv (*" + formato + ")", options=options)
            if fileName:
                return fileName

        if formato == "xlsx":
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                "Archivos xlsx (*" + formato + ")", options=options)
            if fileName:
                return fileName

        if formato == "inp":
            fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                                "Archivos inp (*" + formato + ")", options=options)
            if fileName:
                return fileName


    def Atr_MANUAL(self):
        """Ajuste de tabla a modo manual para su llenado"""
        if self.ui.rb_manual.isChecked() == True:

            # Fijamos el número de nodos a capturar
            row_n = self.ui.txt_manual_nod.value()
            if row_n == 0:
                self.msgErrorBox("NO SE INDICÓ EL NÚMERO DE NODOS")
            else:
                row_n = self.ui.txt_manual_nod.value()
                self.ui.tbl_nod.setRowCount(row_n)
                self.ui.tbl_nod.resizeColumnsToContents()
                self.ui.tbl_nod.clearContents()

            # Fijamos el número de tuberias a capturar
            row_t = self.ui.txt_manual_tub.value()
            if row_t == 0:
                self.msgErrorBox("NO SE INDICÓ EL NÚMERO DE TUBERÍAS")
            else:
                self.ui.tbl_tub.setRowCount(row_t)
                self.ui.tbl_tub.resizeColumnsToContents()
                self.ui.tbl_tub.clearContents()


    def Atr_XLSX(self):
        """Llenado de tablas de nodos y tuberias usando un archivo de excel"""
        if self.ui.rb_xslx.isChecked() == True:
            try:
                # Abre el buscador de archivos *.xlsx
                ruta_nombre = self.Fn_BuscadorDeArchivos("xlsx")
                # Obtiene el nombre de las hojas donde estan los nodos y tuberias
                Sht_Nod = self.ui.txt_excel_nod.text()
                Sht_Tub = self.ui.txt_excel_tub.text()
                # Vacia toda la informacion de nodos y tuberias a su respectiva tabla
                data_n, data_t = FileManipulation.XSLX_Read(ruta_nombre, Sht_Nod, Sht_Tub)
                self.Atr_LlenadoTablaNod_CSVXSLX(data_n)
                self.Atr_LlenadoTablaTub_CSVXSLX(data_t)
            except:
                self.msgErrorBox("ERROR EN LOS NOMBRES DE LAS HOJAS")

    def Atr_CSVnod(self):
        """Llenado de tabla de nodo usando un archivo de csv"""
        if self.ui.rb_csv.isChecked() == True:
            try:
                ruta_nombre = self.Fn_BuscadorDeArchivos("csv")
                datos = FileManipulation.CSV_Read(ruta_nombre,'Nodos')
                self.Atr_LlenadoTablaNod_CSVXSLX(datos)
            except:
                self.msgErrorBox("ERROR AL CARGAR ARCHIVO *.csv")

    def Atr_CSVtub(self):
        """Llenado de tabla de tuberias usando un archivo de csv"""
        if self.ui.rb_csv.isChecked() == True:
            try:
                ruta_nombre = self.Fn_BuscadorDeArchivos("csv")
                datos = FileManipulation.CSV_Read(ruta_nombre)
                self.Atr_LlenadoTablaTub_CSVXSLX(datos)
            except:
                self.msgErrorBox("ERROR AL CARGAR ARCHIVO *.csv")

    def Atr_INP(self):
        if self.ui.rb_inp.isChecked() == True:
            try:
                ruta_nombre = self.Fn_BuscadorDeArchivos("inp")
                if ruta_nombre == None:
                    self.msgErrorBox("NO SE CARGO EL ARCHIVO *.inp")
                else:
                    EpTools = FileManipulation(ruta_nombre)
                    EpTools.PropiedadesNodos()
                    Prop_Nod = EpTools.PropiedadesNodos()
                    Prop_Tub = EpTools.PropiedadesTuberias()
                    self.Atr_LlenadoTablaNodTub_INP(Prop_Nod, Prop_Tub)
            except:
                self.msgErrorBox("ERROR AL CARGAR ARCHIVO *.inp")


    def Atr_LlenadoTablaNodTub_INP(self, datos_n, datos_t, datos_XY = []):
        """Vaciamos los datos de los nodos a su tabla"""
        row = len(datos_n[0])
        self.ui.tbl_nod.clearContents()
        self.ui.tbl_nod.setRowCount(0)
        for i in range(0, row):
            self.ui.tbl_nod.insertRow(i)
            coordX = QtWidgets.QTableWidgetItem(str(datos_n[0][i]))
            coordY = QtWidgets.QTableWidgetItem(str(datos_n[1][i]))
            celda_nod = QtWidgets.QTableWidgetItem(str(datos_n[2][i]))
            celda_q = QtWidgets.QTableWidgetItem(str(datos_n[3][i]))
            celda_type = QtWidgets.QTableWidgetItem(str(datos_n[4][i]))
            celda_z = QtWidgets.QTableWidgetItem(str(datos_n[5][i]))
            self.ui.tbl_nod.setItem(i, 0, coordX)     # Coordenda X
            self.ui.tbl_nod.setItem(i, 1, coordY)     # Coordenada Y
            self.ui.tbl_nod.setItem(i, 2, celda_nod)  # Id del nodo
            self.ui.tbl_nod.setItem(i, 3, celda_q)    # Gasto o Altura
            self.ui.tbl_nod.setItem(i, 4, celda_type) # Tipo del Nodo
            self.ui.tbl_nod.setItem(i, 5, celda_z)    # Nivel Topografico
        self.ui.tbl_nod.resizeColumnsToContents()

        """Vaciamos los datos de las tuberias a su tabla"""
        row = len(datos_t[0])
        self.ui.tbl_tub.clearContents()
        self.ui.tbl_tub.setRowCount(0)
        ini_fin = datos_t[1]
        for i in range(0, row):
            self.ui.tbl_tub.insertRow(i)
            celda_tub = QtWidgets.QTableWidgetItem(str(datos_t[0][i]))
            celda_ni = QtWidgets.QTableWidgetItem(str(ini_fin[i][0]))
            celda_nf = QtWidgets.QTableWidgetItem(str(ini_fin[i][1]))
            celda_l = QtWidgets.QTableWidgetItem(str(datos_t[2][i]))
            celda_d = QtWidgets.QTableWidgetItem(str(datos_t[3][i]))
            celda_km = QtWidgets.QTableWidgetItem(str(round(datos_t[4][i], 4)))
            celda_ks = QtWidgets.QTableWidgetItem(str(round(datos_t[5][i], 6)))
            self.ui.tbl_tub.setItem(i, 0, celda_tub) # ID de la tuberia
            self.ui.tbl_tub.setItem(i, 1, celda_ni) # Nodo inicial
            self.ui.tbl_tub.setItem(i, 2, celda_nf) # Nodo final
            self.ui.tbl_tub.setItem(i, 3, celda_l) # Longitud
            self.ui.tbl_tub.setItem(i, 4, celda_d) # Diametro
            self.ui.tbl_tub.setItem(i, 5, celda_km) # Perdidas Menores
            self.ui.tbl_tub.setItem(i, 6, celda_ks) # Rugosidad
        self.ui.tbl_nod.resizeColumnsToContents()

    def Atr_INP_XY(self):
        """Llenado de coordenadas usando un archivo de csv"""
        if self.ui.rb_inp.isChecked() == True:
            try:
                ruta_nombre = self.Fn_BuscadorDeArchivos("csv")
                datos = FileManipulation.CSV_Read(ruta_nombre)
                self.Atr_LlenadoCoordenadas_XY(datos)
            except:
                self.msgErrorBox("ERROR AL CARGAR COORDENADAS *.csv")

    def Atr_LlenadoCoordenadas_XY(self, datos_XY):
        """Vaciamos los datos de las tuberias a su tabla"""
        row = len(datos_XY)
        for i in range(0, row):
            x = round(float(datos_XY[i][1]), 2)
            y = round(float(datos_XY[i][2]), 2)
            coordX = QtWidgets.QTableWidgetItem(str(x))
            coordY = QtWidgets.QTableWidgetItem(str(y))
            self.ui.tbl_nod.setItem(i, 0, coordX)  # Coordenda X
            self.ui.tbl_nod.setItem(i, 1, coordY)  # Coordenada Y
        self.ui.tbl_nod.resizeColumnsToContents()


    def Atr_LlenadoTablaNod_CSVXSLX(self, datos): # --> OK
        """Vaciamos los datos de los nodos a su tabla"""
        row = len(datos)
        col = len(datos[0])
        self.ui.tbl_nod.clearContents()
        self.ui.tbl_nod.setRowCount(0)
        for i in range(row): # range(0,row)
            self.ui.tbl_nod.insertRow(i) # i-1
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(datos[i][j]))
                self.ui.tbl_nod.setItem(i, j, celda) # i-1
        self.ui.tbl_nod.resizeColumnsToContents()

    # CargarTuberias_CSVXSLX
    def Atr_LlenadoTablaTub_CSVXSLX(self, datos): # --> OK
        """Vaciamos los datos de las tuberias a su tabla"""
        row = len(datos)
        col = len(datos[0])
        self.ui.tbl_tub.clearContents()
        self.ui.tbl_tub.setRowCount(0)
        for i in range(row):
            self.ui.tbl_tub.insertRow(i)
            for j in range(col):
                celda = QtWidgets.QTableWidgetItem(str(datos[i][j]))
                self.ui.tbl_tub.setItem(i, j, celda)
        self.ui.tbl_tub.resizeColumnsToContents()


    """
        ################################################
        #  PAGINA: VISUALIZACIÓN DE LA RED HIDRAULICA  #
        ################################################
    """

    def Atr_DibujarRedHidraulicaSeguros(self):
        if self.Fn_EmptyTable(self.ui.tbl_nod) > 0:
            self.msgErrorBox("CELDA VACIA EN LA TABLA DE NODOS")
        elif self.Fn_EmptyTable(self.ui.tbl_tub) > 0:
            self.msgErrorBox("CELDA VACIA EN LA TABLA DE TUBERÍAS")
        elif self.Fn_EmptyTable(self.ui.tbl_nod) == 0 and self.Fn_EmptyTable(self.ui.tbl_tub) == 0:
            try:
                self.Atr_DibujarRedHidraulica()
            except:
                self.msgErrorBox("ERROR EN LOS VALORES DE LAS TABLAS")

    def Atr_DibujarRedHidraulica(self):
        # Extraer datos de la tabla de nodos
        [Vec_Nodx, Vec_Nody, Vec_Nodo, Vec_tipo, Vec_QH, Vec_cota, T_str2num, T_num2str] = self.Fn_Nodos()

        # Extraer datos de la tabla de tuberias
        [Vec_tuberia, ini_fin, Vec_Long, Vec_diam, Vec_km, Vec_ks] = self.Fn_Tuberias()

        # Acomodar data
        ndx_coord = []
        ndy_coord = []
        nex_coord = []
        ney_coord = []
        num_ren_nod = len(Vec_Nodo)
        for i in range(num_ren_nod):
            if Vec_tipo[i] == 'E':
                nex_coord.append(Vec_Nodx[i])
                ney_coord.append(Vec_Nody[i])
            elif Vec_tipo[i] == 'N':
                ndx_coord.append(Vec_Nodx[i])
                ndy_coord.append(Vec_Nody[i])

        # Dibujar Tuberias (Lineas)
        self.ploteo = self.ui.widget_Visualizar_RH.canvas
        self.ploteo.ax.clear()
        cont = 0
        for vec in ini_fin:
            n1x = Vec_Nodx[T_str2num[vec[0]] - 1]
            n1y = Vec_Nody[T_str2num[vec[0]] - 1]
            n2x = Vec_Nodx[T_str2num[vec[1]] - 1]
            n2y = Vec_Nody[T_str2num[vec[1]] - 1]
            self.ploteo.ax.plot([n1x, n2x], [n1y, n2y], 'c-', linewidth=5)

            tx = 0.5 * (n1x + n2x)
            ty = 0.5 * (n1y + n2y)

            # Visualizacion de los Id´s para las tuberias (Solamente)
            if self.ui.rb_IdTuberias.isChecked() == True or self.ui.rb_IdNodTub.isChecked() == True:
                self.ploteo.ax.text(tx, ty, Vec_tuberia[cont], weight="bold")

            # Popiedades de las Tuberias en funcion del CheckBox
            if self.ui.rb_Long.isChecked() == True:
                lbl = str(Vec_Long[cont]) + "mts"
                self.ploteo.ax.text(tx, ty - 0.5, lbl, weight="bold")
            elif self.ui.rb_Diam.isChecked() == True:
                lbl = str(Vec_diam[cont]) + "mm"
                self.ploteo.ax.text(tx, ty - 0.5, lbl, weight="bold")
            elif self.ui.rb_ks.isChecked() == True:
                lbl = str(Vec_ks[cont]) + "mm"
                self.ploteo.ax.text(tx, ty - 0.5, lbl, weight="bold")
            elif self.ui.rb_km.isChecked() == True:
                lbl = str(Vec_km[cont])
                self.ploteo.ax.text(tx, ty - 0.5, lbl, weight="bold")
            cont+=1

        # Dibujar Nodos (Circulos)
        self.ploteo.ax.plot(ndx_coord, ndy_coord, 'ok')

        # Dibujar Embalse (Diamantes)
        self.ploteo.ax.plot(nex_coord, ney_coord, 'Dm')

        # Visualizaciones de Id´s para los nodos (Solamente)
        for i in range(num_ren_nod):
            if self.ui.rb_IdNodos.isChecked() == True or self.ui.rb_IdNodTub.isChecked() == True:
                self.ploteo.ax.text(Vec_Nodx[i], Vec_Nody[i], T_num2str[Vec_Nodo[i]], weight="bold")

            # Popiedades de los Nodos en funcion del CheckBox
            if self.ui.rb_Demandas.isChecked() == True:
                if Vec_tipo[i] == 'E':
                    lbl = str(Vec_QH[i]) + "mts"
                else:
                    lbl = str(Vec_QH[i]) + "L/s"
                self.ploteo.ax.text(Vec_Nodx[i]+0.5,Vec_Nody[i]+0.5, lbl, weight="bold")
            elif self.ui.rb_Cotas.isChecked() == True:
                lbl = str(Vec_cota[i]) + "mts"
                self.ploteo.ax.text(Vec_Nodx[i] + 0.5, Vec_Nody[i] + 0.5, lbl, weight="bold")

        # Ajustar Ejes
        xmax = max(Vec_Nodx)
        ymax = max(Vec_Nody)
        xmin = min(Vec_Nodx)
        ymin = min(Vec_Nody)
        self.ploteo.ax.axis([-xmax*0.5, xmax*1.5, -ymax*0.5, ymax*1.5])

        # Color de fondo del mpl
        self.ploteo.ax.set_facecolor('#FFFFFF')

        # Ajuste de los parametros del plot
        self.ploteo.fig.subplots_adjust(0, 0, 1, 1)  # left,bottom,right,top

        # Mostrar el dibujo en el mpl
        self.ploteo.draw()

    """
        ###########################################
        #  PAGINA: ANALISIS DE LA RED HIDRAULICA  #
        ###########################################
    """

    def Fn_Nodos(self):
        Vec_Nodx = []
        Vec_Nody = []
        Vec_Nodo = []
        Vec_Nodo_str = []
        Vec_tipo = []
        Vec_QH = []
        Vec_cota = []
        # Extraer datos de la tabla de nodos
        num_ren_nod = self.ui.tbl_nod.rowCount()
        for i in range(num_ren_nod):
            Coord_x = float(self.ui.tbl_nod.item(i, 0).text())
            Coord_y = float(self.ui.tbl_nod.item(i, 1).text())
            nodo = self.ui.tbl_nod.item(i, 2).text()
            qh = float(self.ui.tbl_nod.item(i, 3).text())
            Tipo_nodo = self.ui.tbl_nod.item(i, 4).text()
            cota = float(self.ui.tbl_nod.item(i, 5).text())
            Vec_Nodx.append(Coord_x)
            Vec_Nody.append(Coord_y)
            Vec_Nodo.append(i + 1)
            Vec_Nodo_str.append(nodo)
            Vec_QH.append(qh)
            Vec_tipo.append(Tipo_nodo)
            Vec_cota.append(cota)
        T_str2num = dict(zip(Vec_Nodo_str, Vec_Nodo))
        T_num2str = dict(zip(Vec_Nodo, Vec_Nodo_str))
        return Vec_Nodx, Vec_Nody, Vec_Nodo, Vec_tipo, Vec_QH, Vec_cota, T_str2num, T_num2str

    def Fn_Tuberias(self):
        # Extraer datos de la tabla de tuberias
        Vec_tuberia = []
        ini_fin = []
        Vec_Long = []
        Vec_diam = []
        Vec_km = []
        Vec_ks = []
        num_ren_tub = self.ui.tbl_tub.rowCount()
        for i in range(num_ren_tub):
            tuberia = self.ui.tbl_tub.item(i, 0).text()
            ni = self.ui.tbl_tub.item(i, 1).text()
            nf = self.ui.tbl_tub.item(i, 2).text()
            L = float(self.ui.tbl_tub.item(i, 3).text())
            diam = float(self.ui.tbl_tub.item(i, 4).text())
            km_val = float(self.ui.tbl_tub.item(i, 5).text())
            ks_val = float(self.ui.tbl_tub.item(i, 6).text())
            Vec_tuberia.append(tuberia)
            ini_fin.append([ni, nf])
            Vec_Long.append(L)
            Vec_diam.append(diam)
            Vec_km.append(km_val)
            Vec_ks.append(ks_val)
        return Vec_tuberia, ini_fin, Vec_Long, Vec_diam, Vec_km, Vec_ks

    def Atr_AnalisisRedHidraulicaSeguros(self):
        if self.Fn_EmptyTable(self.ui.tbl_nod) > 0:
            self.msgErrorBox("CELDA VACIA EN LA TABLA DE NODOS")
        elif self.Fn_EmptyTable(self.ui.tbl_tub) > 0:
            self.msgErrorBox("CELDA VACIA EN LA TABLA DE TUBERÍAS")
        elif self.Fn_EmptyTable(self.ui.tbl_nod) == 0 and self.Fn_EmptyTable(self.ui.tbl_tub) == 0:
            try:
                self.Atr_AnalisisRedHidraulica()
            except:
                self.msgErrorBox("ERROR EN LOS VALORES DE LAS TABLAS")

    def Atr_AnalisisRedHidraulica(self):
        [Vec_Nodx, Vec_Nody, Vec_Nodo, Vec_tipo, Vec_QH, Vec_cota, T_str2num, T_num2str] = self.Fn_Nodos()
        [Vec_tuberia, ini_fin, Vec_Long, Vec_diam, Vec_km, Vec_ks] = self.Fn_Tuberias()

        data_nod = []
        for i in range(len(Vec_Nodo)):
            data_nod.append([Vec_Nodo[i], Vec_QH[i], Vec_tipo[i], Vec_cota[i]])

        data_tub = []
        for i in range(len(Vec_tuberia)):
            data_tub.append([Vec_tuberia[i], T_str2num[ini_fin[i][0]], T_str2num[ini_fin[i][1]],
                             Vec_Long[i], Vec_diam[i],round(Vec_km[i], 2), round(Vec_ks[i], 4)])

        self.PmaxD = self.ui.txt_PDmax.value()
        self.PminD = self.ui.txt_PDmin.value()
        self.VmaxD = self.ui.txt_VDmax.value()
        self.VminD = self.ui.txt_VDmin.value()

        # Extraer Data de la Tabla de Precio-Diametro
        x = []
        self.DiamCom = []
        num_ren_diam = self.ui.tbl_Dcom.rowCount()
        for i in range(num_ren_diam):
            diam = float(self.ui.tbl_Dcom.item(i, 0).text())
            x.append(diam)
        self.DiamCom = x

        rh = gh.RedHidraulica(data_nod, data_tub, self.PmaxD, self.PminD, self.VmaxD, self.VminD, self.DiamCom)

        Tuberias = rh.Tub
        Nodos = rh.Nod
        Grad = gh.Gradiente(Tuberias, Nodos)
        [Caudal, Velocidad, Altura, Presion, Fricc, Perd, er, ini_fin] = Grad.Resolver()

        self.ui.lbl_vmax.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                 'MÁXIMA: {:.2f} metros/seg'.format(max(Velocidad)[0]) +
                                 '</span></p></body></html>')
        self.ui.lbl_vmin.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                 'MÍNIMA: {:.2f} metros/seg'.format(min(Velocidad)[0]) +
                                 '</span></p></body></html>')
        self.ui.lbl_pmax.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                 'MÁXIMA: {:.2f} metros'.format(max(Presion)[0]) +
                                 '</span></p></body></html>')
        self.ui.lbl_pmin.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                 'MÍNIMA: {:.2f} metros'.format(min(Presion)[0]) +
                                 '</span></p></body></html>')
        err_porcentual = er[-1]
        if err_porcentual <= 0.00001:
            self.ui.lbl_err.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                    'EJECUCIÓN EXITOSA: {:.9f} %'.format(err_porcentual) +
                                    '</span></p></body></html>')
        else:
            self.ui.lbl_err.setText('<html><head/><body><p><span style=" color:#ff0000; font-weight:600;">' +
                                    'MALA EJECUCIÓN: {:.6f} %'.format(err_porcentual) +
                                    '</span></p></body></html>')

        """Vaciamos los resultados de las tuberias a su tabla"""
        row = len(Caudal)
        self.ui.tbl_res_tub.clearContents()
        self.ui.tbl_res_tub.setRowCount(0)
        for i in range(row):
            self.ui.tbl_res_tub.insertRow(i)

            t = QtWidgets.QTableWidgetItem(str(Vec_tuberia[i]))
            ni = QtWidgets.QTableWidgetItem(str(T_num2str[ini_fin[i][0]]))
            nf = QtWidgets.QTableWidgetItem(str(T_num2str[ini_fin[i][1]]))
            q = QtWidgets.QTableWidgetItem(str(round(Caudal[i][0],2)))
            v = QtWidgets.QTableWidgetItem(str(round(Velocidad[i][0],2)))
            hf = QtWidgets.QTableWidgetItem(str(round(Perd[i][0],2)))
            f = QtWidgets.QTableWidgetItem(str(round(Fricc[i][0],5)))

            self.ui.tbl_res_tub.setItem(i, 0, t)
            self.ui.tbl_res_tub.setItem(i, 1, ni)
            self.ui.tbl_res_tub.setItem(i, 2, nf)
            self.ui.tbl_res_tub.setItem(i, 3, q)
            self.ui.tbl_res_tub.setItem(i, 4, v)
            self.ui.tbl_res_tub.setItem(i, 5, hf)
            self.ui.tbl_res_tub.setItem(i, 6, f)

        self.ui.tbl_res_tub.resizeColumnsToContents()

        """Vaciamos los resultados de los nodos a su tabla"""
        row = len(Presion)
        self.ui.tbl_res_nod.clearContents()
        self.ui.tbl_res_nod.setRowCount(0)
        for i in range(row):
            self.ui.tbl_res_nod.insertRow(i)
            
            n = QtWidgets.QTableWidgetItem(str(T_num2str[Vec_Nodo[i+1]]))
            dem = QtWidgets.QTableWidgetItem(str(round(Vec_QH[i+1], 2)))
            alt = QtWidgets.QTableWidgetItem(str(round(Altura[i][0], 2)))
            press = QtWidgets.QTableWidgetItem(str(round(Presion[i][0], 2)))

            self.ui.tbl_res_nod.setItem(i, 0, n)
            self.ui.tbl_res_nod.setItem(i, 1, dem)
            self.ui.tbl_res_nod.setItem(i, 2, alt)
            self.ui.tbl_res_nod.setItem(i, 3, press)
        self.ui.tbl_res_nod.resizeColumnsToContents()

        try:
            self.Fn_GrafResultadosGradiente(Vec_Nodo, Presion, self.PminD, self.PmaxD,
                                            self.ui.widget_pres.canvas, T_num2str)

        except:
            self.msgErrorBox("ERROR EN LA GRÁFICA DE PRESIÓN")

        try:
            self.Fn_GrafResultadosGradiente(Vec_tuberia, Velocidad, self.VminD, self.VmaxD,
                                            self.ui.widget_vel.canvas)
        except:
            self.msgErrorBox("ERROR EN LA GRÁFICA DE VELOCIDAD")

        try:
            self.Fn_GrafErrPorcentual(er)
        except:
            self.msgErrorBox("ERROR EN LA GRÁFICA DE ERROR")


    """
        ##################################################
        #  GRÁFICA DE RESULTADOS DE VELOCIDAD Y PRESION  #
        ##################################################
    """
    def Fn_GrafResultadosGradiente(self, NodTub, Vector, Vecmin, Vecmax, widget, Trans = None):

        self.ploteo = widget
        self.ploteo.ax.clear()

        # Ajuste de los parametros del plot
        self.ploteo.fig.subplots_adjust(0.05, 0.1, 1, 1) # left,bottom,right,top

        col = []
        titulo = []
        Val_Grafica = []
        for i in range(len(Vector)):
            Val_Grafica.append(Vector[i][0])
            if Vector[i][0] <= Vecmin:
                col.append('#CCECFF')
            elif Vector[i][0] >= Vecmax:
                col.append('#CCECFF')
            else:
                col.append('#1f77b4')

            if Trans != None:
                titulo.append(Trans[NodTub[i+1]])
            elif Trans == None:
                titulo.append(NodTub[i])

        if Trans != None:
            self.ploteo.ax.axhline(y=Vecmin, linewidth=2, color='m', linestyle="--",
                                   label='Presión Minima de Diseño')
            self.ploteo.ax.axhline(y=Vecmax, linewidth=2, color='green', linestyle="--",
                                   label='Presión Maxima de Diseño')
        elif Trans == None:
            self.ploteo.ax.axhline(y=Vecmin, linewidth=2, color='m', linestyle="--",
                                   label='Velocidad Minima de Diseño')
            self.ploteo.ax.axhline(y=Vecmax, linewidth=2, color='green', linestyle="--",
                                   label='Velocidad Maxima de Diseño')
        self.ploteo.ax.legend()
        self.ploteo.ax.bar(titulo, Val_Grafica, color=col)

        # Color de los lados del Plot
        self.ploteo.ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes

        self.ploteo.draw()

    """
        #################################
        #  GRAFICA DE ERROR PORCENTUAL  #
        #################################
    """

    def Fn_GrafErrPorcentual(self, V_err):
        num = [i + 1 for i in range(len(V_err))]
        self.ploteo = self.ui.widget_err_porcentual.canvas
        self.ploteo.ax.clear()
        # Shade the area between y1 and line y=0
        self.ploteo.ax.fill_between(num, V_err, 0,
                                    color='blue',  # The outline color
                                    alpha=0.2)  # Transparency of the fill
        # Color de los lados del Plot
        self.ploteo.ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes
        # Show the plot
        self.ploteo.draw()


    """
        ################################
        #  PAGINA: ALGORITMO GENÉTICO  #
        ################################
    """

    def Prop_AnadirRenglonSinCombo(self):
        val = self.ui.txt_num_diametros.value()
        self.ui.tbl_Dcom.setRowCount(val)
        self.ui.tbl_Dcom.update()

    def Atr_AlgoritmoGeneticoSeguridad(self):
        # Datos de Poblacion
        tasa_mutacion = self.ui.txt_tasa_mut.value()
        num_generaciones = self.ui.txt_num_gen.value()
        tamano_poblacion = self.ui.txt_tam_pob.value()
        # Datos de Diseño
        self.PmaxD = self.ui.txt_PDmax.value()
        self.PminD = self.ui.txt_PDmin.value()
        self.VmaxD = self.ui.txt_VDmax.value()
        self.VminD = self.ui.txt_VDmin.value()
        val = False
        if tamano_poblacion == 0:
            self.msgErrorBox("TAMAÑO DE POBLACIÓN NO PUEDE SER CERO !!")
            val = True
        elif num_generaciones == 0:
            self.msgErrorBox("NÚMERO DE GENERACIONES NO PUEDE SER CERO !!")
            val = True
        elif tasa_mutacion == 0:
            self.msgErrorBox("TASA DE MUTACIÓN NO PUEDE SER CERO !!")
            val = True
        elif self.PmaxD == 0:
            self.msgErrorBox("PRESIÓN MÁXIMA NO PUEDE SER CERO !!")
            val = True
        elif self.PmaxD <= self.PminD:
            self.msgErrorBox("PRESIÓN MÁXIMA DEBE SER LA MAYOR !!")
            val = True
        elif self.VmaxD == 0:
            self.msgErrorBox("VELOCIDAD MÁXIMA NO PUEDE SER CERO !!")
            val = True
        elif self.VmaxD <= self.VminD:
            self.msgErrorBox("VELOCIDAD MÁXIMA DEBE SER LA MAYOR !!")
            val = True
        elif self.PminD == 0:
            self.msgErrorBox("PRESIÓN MÍNIMA NO PUEDE SER CERO !!")
            val = True
        elif self.PminD >= self.PmaxD:
            self.msgErrorBox("PRESIÓN MÍNIMA DEBE SER LA MENOR !!")
            val = True
        elif self.VminD == 0:
            self.msgErrorBox("VELOCIDAD MÍNIMA NO PUEDE SER CERO !!")
            val = True
        elif self.VminD >= self.VmaxD:
            self.msgErrorBox("VELOCIDAD MÍNIMA DEBE SER LA MENOR !!")
            val = True
        return val


    def Atr_RadioButton_Regresiones(self):

        # Extraer Data de la Tabla de Precio-Diametro
        x = []
        y = []
        self.DiamCom = []
        num_ren_diam = self.ui.tbl_Dcom.rowCount()
        for i in range(num_ren_diam):
            diam = float(self.ui.tbl_Dcom.item(i, 0).text())
            precio = float(self.ui.tbl_Dcom.item(i, 1).text())
            x.append(diam)
            y.append(precio)
        self.DiamCom = x
        if self.ui.rb_lineal.isChecked() == True:
            # y = m*x + b
            N = len(x)
            SXY = sum([x[i] * y[i] for i in range(N)])
            SX2 = sum([x[i] ** 2 for i in range(N)])
            SX = sum(x)
            SY = sum(y)
            Xp = sum(x) / N
            Yp = sum(y) / N
            m1 = SX * SY - N * SXY
            m2 = SX ** 2 - N * SX2
            m = round(m1 / m2, 5)
            b = round(Yp - m * Xp, 5)
            # Coeficiente de determinación R2
            Yr = [m * x[i] + b for i in range(N)]
            y_Yr_2 = sum([(y[i] - Yr[i]) ** 2 for i in range(N)])
            y_Yp_2 = sum([(y[i] - Yp) ** 2 for i in range(N)])
            R2 = 1 - (y_Yr_2 / y_Yp_2)
            self.K1 = m
            self.K2 = b
            self.RegTipo = "Lineal"

            self.ui.lbl_R2.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                    'Coef. de Determinación: {:.5f}'.format(R2) +
                                    '</span></p></body></html>')

        elif self.ui.rb_potencial.isChecked() == True:
            # y = a*x**b
            N = len(x)
            X = [math.log10(i) for i in x]
            Y = [math.log10(i) for i in y]
            SXY = sum([X[i] * Y[i] for i in range(N)])
            SX2 = sum([X[i] ** 2 for i in range(N)])
            SX = sum(X)
            SY = sum(Y)
            Xp = sum(X) / N
            Yp = sum(Y) / N
            b1 = N * SXY - SX * SY
            b2 = N * SX2 - SX ** 2
            b = round(b1 / b2, 5)
            A = Yp - b * Xp
            a = round(10 ** A, 5)
            # Coeficiente de determinación R2
            Yr = [a * x[i] ** b for i in range(N)]
            y_Yr_2 = sum([(y[i] - Yr[i]) ** 2 for i in range(N)])
            y_Yp_2 = sum([(y[i] - Yp) ** 2 for i in range(N)])
            R2 = 1 - (y_Yr_2 / y_Yp_2)
            self.K1 = a
            self.K2 = b
            self.RegTipo = "Potencial"
            self.ui.lbl_R2.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                   'Coef. de Determinación: {:.5f}'.format(R2) +
                                   '</span></p></body></html>')

        elif self.ui.rb_exponencial.isChecked() == True:
            # y = b*10**mx
            N = len(x)
            Y = [math.log10(i) for i in y]
            SXY = sum([x[i] * Y[i] for i in range(N)])
            SX2 = sum([x[i] ** 2 for i in range(N)])
            SX = sum(x)
            SY = sum(Y)
            Xp = sum(x) / N
            Yp = sum(Y) / N
            m1 = SX * SY - N * SXY
            m2 = SX ** 2 - N * SX2
            m = round(m1 / m2, 5)
            B = Yp - m * Xp
            b = round(10 ** B, 5)
            # Coeficiente de determinación R2
            Yr = [b * math.pow(10, m * x[i]) for i in range(N)]
            y_Yr_2 = sum([(y[i] - Yr[i]) ** 2 for i in range(N)])
            y_Yp_2 = sum([(y[i] - Yp) ** 2 for i in range(N)])
            R2 = 1 - (y_Yr_2 / y_Yp_2)

            self.K1 = b
            self.K2 = m
            self.RegTipo = "Exponencial"
            self.ui.lbl_R2.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                   'Coef. de Determinación: {:.5f}'.format(R2) +
                                   '</span></p></body></html>')

    def Atr_AlgoritmoGenetico(self):
        # Datos de Poblacion
        tasa_mutacion = self.ui.txt_tasa_mut.value()
        num_generaciones = self.ui.txt_num_gen.value()
        tamano_poblacion = self.ui.txt_tam_pob.value()
        if tamano_poblacion%2 != 0:
            tamano_poblacion += 1
        # Datos de Diseño
        self.PmaxD = self.ui.txt_PDmax.value()
        self.PminD = self.ui.txt_PDmin.value()
        self.VmaxD = self.ui.txt_VDmax.value()
        self.VminD = self.ui.txt_VDmin.value()
        # Extraer Data de la Tabla de Precio-Diametro
        x = []
        self.DiamCom = []
        num_ren_diam = self.ui.tbl_Dcom.rowCount()
        for i in range(num_ren_diam):
            diam = float(self.ui.tbl_Dcom.item(i, 0).text())
            x.append(diam)
        self.DiamCom = x
        # Data de Tablas
        [Vec_Nodx, Vec_Nody, Vec_Nodo, Vec_tipo, Vec_QH, Vec_cota, T_str2num, T_num2str] = self.Fn_Nodos()
        [Vec_tuberia, ini_fin, Vec_Long, Vec_diam, Vec_km, Vec_ks] = self.Fn_Tuberias()
        # Acomodo de la Informacion de las tablas
        data_nod = []
        for i in range(len(Vec_Nodo)):
            data_nod.append([Vec_Nodo[i], Vec_QH[i], Vec_tipo[i], Vec_cota[i]])

        data_tub = []
        for i in range(len(Vec_tuberia)):
            data_tub.append([Vec_tuberia[i], T_str2num[ini_fin[i][0]], T_str2num[ini_fin[i][1]],
                             Vec_Long[i], Vec_diam[i], round(Vec_km[i], 2), round(Vec_ks[i], 4)])
        # Creacion de la Clase "Red Hidraulica"
        rh = gh.RedHidraulica(data_nod, data_tub, self.PmaxD, self.PminD, self.VmaxD, self.VminD, self.DiamCom)
        # Creacion de la Clase "Algoritmo Genetico"
        AG = ag.AlgoritmoGenetico(rh, self.K1, self.K2, self.RegTipo, tamano_poblacion, tasa_mutacion, num_generaciones)
        # Mejores diametros encontrados
        [MI, hora, minuto, segundo] = AG.resolver()
        self.ListaGene = []
        self.ListaCostoC = []
        for i in range(1, len(MI)):
            self.ListaCostoC.append(round(MI[i][3],2))
            self.ListaGene.append(MI[i][4])
        # Velocidades (maximas y minima) y Presiones (maximas y minimas)
        Sol_red = ag.Individuo(rh, self.K1, self.K2, self.RegTipo, MI[-1][0])
        # Mostrar resultados al FrontEnd
        best_diam = MI[-1][0]
        row = len(Vec_tuberia)
        self.ui.tbl_mejor_diam.clearContents()
        self.ui.tbl_mejor_diam.setRowCount(0)
        for i in range(row):
            self.ui.tbl_mejor_diam.insertRow(i)
            t2 = QtWidgets.QTableWidgetItem(str(Vec_tuberia[i]))
            d2 = QtWidgets.QTableWidgetItem(str(round(best_diam[i], 2)))
            self.ui.tbl_mejor_diam.setItem(i, 0, t2)
            self.ui.tbl_mejor_diam.setItem(i, 1, d2)
        self.ui.tbl_mejor_diam.resizeColumnsToContents()

        self.ui.lbl_mejor_gen.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                      'MEJOR GENERACIÓN: {:.0f}'.format(MI[-1][4]) +
                                      '</span></p></body></html>')
        self.ui.lbl_CC.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                               'COSTO DE CONSTRUCCIÓN:  $ {:0,.2f}'.format(MI[-1][3]) +
                               '</span></p></body></html>')
        self.ui.lbl_CH.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                               'COSTO HIDRÁULICO: {:.4f}'.format(MI[-1][1]) +
                               '</span></p></body></html>')
        self.ui.lbl_time.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                 'TIEMPO DE EJECUCIÓN: {} hrs : {} min : {} seg'.format(hora, minuto, segundo) +
                                 '</span></p></body></html>')

        if MI[-1][1] > 0:
            self.ui.lbl_CH.setText('<html><head/><body><p><span style=" color:#ff0000; font-weight:600;">' +
                                   'COSTO HIDRÁULICO: {:.4f}'.format(MI[-1][1]) +
                                   '</span></p></body></html>')
        else:
            self.ui.lbl_CH.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                   'COSTO HIDRÁULICO: {:.4f}'.format(MI[-1][1]) +
                                   '</span></p></body></html>')

        if Sol_red.v_max >= self.VmaxD:
            self.ui.lbl_res_vmax.setText('<html><head/><body><p><span style=" color:#ff0000; font-weight:600;">' +
                                         'VELOCIDAD MÁXIMA: {:.2f} metros/seg'.format(Sol_red.v_max) +
                                         '</span></p></body></html>')
        else:
            self.ui.lbl_res_vmax.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                         'VELOCIDAD MÁXIMA: {:.2f} metros/seg'.format(Sol_red.v_max) +
                                         '</span></p></body></html>')

        if Sol_red.v_min <= self.VminD:
            self.ui.lbl_res_vmin.setText('<html><head/><body><p><span style=" color:#ff0000; font-weight:600;">' +
                                         'VELOCIDAD MÍNIMA: {:.2f} metros/seg'.format(Sol_red.v_min) +
                                         '</span></p></body></html>')
        else:
            self.ui.lbl_res_vmin.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                         'VELOCIDAD MÍNIMA: {:.2f} metros/seg'.format(Sol_red.v_min) +
                                         '</span></p></body></html>')

        if Sol_red.p_max >= self.PmaxD:
            self.ui.lbl_res_pmax.setText('<html><head/><body><p><span style=" color:#ff0000; font-weight:600;">' +
                                         'PRESIÓN MÁXIMA: {:.2f} metros'.format(Sol_red.p_max) +
                                         '</span></p></body></html>')
        else:
            self.ui.lbl_res_pmax.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                         'PRESIÓN MÁXIMA: {:.2f} metros'.format(Sol_red.p_max) +
                                         '</span></p></body></html>')

        if Sol_red.p_min <= self.PminD:
            self.ui.lbl_res_pmin.setText('<html><head/><body><p><span style=" color:#ff0000; font-weight:600;">' +
                                         'PRESIÓN MÍNIMA: {:.2f} metros'.format(Sol_red.p_min) +
                                         '</span></p></body></html>')
        else:
            self.ui.lbl_res_pmin.setText('<html><head/><body><p><span style=" color:#55ffff; font-weight:600;">' +
                                         'PRESIÓN MÍNIMA: {:.2f} metros'.format(Sol_red.p_min) +
                                         '</span></p></body></html>')
        # Graficamos las generaciones:
        self.Fn_GeneracionCosto()
        # Resultados temporales:
        self.Gen_tempo = MI[-1][4]
        self.Cc_tempo = MI[-1][3]
        self.Ch_tempo = MI[-1][1]
        self.Diam_tempo = MI[-1][0]



    """
        ####################################
        #  GRAFICA DE GENERACION VS COSTO  #
        ####################################
    """

    def Fn_GeneracionCosto(self):
        self.ploteo = self.ui.widget_gen_vs_costo.canvas
        self.ploteo.ax.clear()
        # Ajuste de los parametros del plot
        self.ploteo.fig.subplots_adjust(0.1, 0.1, 1, 1)  # left,bottom,right,top
        # Shade the area between y1 and line y=0
        self.ploteo.ax.fill_between(self.ListaGene, self.ListaCostoC, 0,
                                    color='m',  # The outline color
                                    alpha=0.2)  # Transparency of the fill
        # Color de los lados del Plot
        self.ploteo.ax.tick_params(colors='white', which='both')  # 'both' refers to minor and major axes
        # Show the plot
        self.ploteo.draw()

    """
        ###########################
        #  RESULTADOS TEMPORALES  #
        ###########################
    """
    def Fn_ResultadosTemporales(self):
        # Agregar los resultados en la tabla
        num_ren = self.ui.tbl_diam_temp.rowCount()
        if num_ren == 0:
            self.ui.tbl_diam_temp.setRowCount(1)
            tb_g = QtWidgets.QTableWidgetItem(str(self.Gen_tempo))
            tb_cc = QtWidgets.QTableWidgetItem(str(round(self.Cc_tempo,2)))
            tb_ch = QtWidgets.QTableWidgetItem(str(round(self.Ch_tempo,2)))
            tb_d = QtWidgets.QTableWidgetItem(str(self.Diam_tempo))
            self.ui.tbl_diam_temp.setItem(0, 0, tb_g)
            self.ui.tbl_diam_temp.setItem(0, 1, tb_cc)
            self.ui.tbl_diam_temp.setItem(0, 2, tb_ch)
            self.ui.tbl_diam_temp.setItem(0, 3, tb_d)
            self.ui.tbl_diam_temp.resizeColumnsToContents()
        else:
            self.ui.tbl_diam_temp.setRowCount(num_ren+1)
            tb_g = QtWidgets.QTableWidgetItem(str(self.Gen_tempo))
            tb_cc = QtWidgets.QTableWidgetItem(str(round(self.Cc_tempo,2)))
            tb_ch = QtWidgets.QTableWidgetItem(str(round(self.Ch_tempo,2)))
            tb_d = QtWidgets.QTableWidgetItem(str(self.Diam_tempo))
            self.ui.tbl_diam_temp.setItem(num_ren, 0, tb_g)
            self.ui.tbl_diam_temp.setItem(num_ren, 1, tb_cc)
            self.ui.tbl_diam_temp.setItem(num_ren, 2, tb_ch)
            self.ui.tbl_diam_temp.setItem(num_ren, 3, tb_d)
            self.ui.tbl_diam_temp.resizeColumnsToContents()

        # Agregar los numeros en el combobox
        for i in range(num_ren+1):
            index = self.ui.cb_diam_cargar.findText(str(i+1))
            self.ui.cb_diam_cargar.removeItem(index)
            self.ui.cb_diam_cargar.addItem(str(i+1))

    def Fn_ExportarDiam(self):
        # Titulos de costos y generaciones
        L_1 = ["generacion", "Costo Const", "Costo Hidra"]
        # Titulos de los diametros
        ren0 = self.ui.tbl_mejor_diam.rowCount()
        L_2 = []
        for i in range(ren0):
            # Nomenclatura de los diametros
            NOM = self.ui.tbl_mejor_diam.item(i, 0).text()
            L_2.append(NOM)
        # Union de los Titulos
        L_1.extend(L_2)

        ren = self.ui.tbl_diam_temp.rowCount()
        Lista_varios = []
        Lista_varios.append(L_1)
        for i in range(ren):
            # Valores de costos
            GEN = int(self.ui.tbl_diam_temp.item(i, 0).text())
            CC = float(self.ui.tbl_diam_temp.item(i, 1).text())
            CH = float(self.ui.tbl_diam_temp.item(i, 2).text())
            # Primera lista
            List_gchd = [int(GEN), float(CC), float(CH)]
            # Valores de diametros
            DIAM = self.ui.tbl_diam_temp.item(i, 3).text()
            # Segunda lista
            List_str_D = list(DIAM[1:-1].split(","))
            col = len(List_str_D)
            List_D = [float(List_str_D[k]) for k in range(col)]
            # Combinacion de listas 1 y 2
            List_gchd.extend(List_D)
            # Lista de Listas
            Lista_varios.append(List_gchd)
        # Transformacion de listas a Zip
        Listas_zip = zip(*Lista_varios)
        # Guardar en CSV
        nombre = self.ui.txt_nom_export.text()
        try:
            # Creamos un nuevo directorio
            newDir("C://RedGenHid")
            # Guardamos el archivo
            path = 'C://RedGenHid//'
            pathFile = path + nombre + '.csv'
            with open(pathFile, 'w') as f:
                write = csv.writer(f)
                for val in Listas_zip:
                    write.writerow(val)
        except OSError:
            # Guardamos el archivo
            path = 'C://RedGenHid//'
            pathFile = path + nombre + '.csv'
            with open(pathFile, 'w') as f:
                write = csv.writer(f)
                for val in Listas_zip:
                    write.writerow(val)

    def Fn_CargarListaDiametros(self):
        # Obtener el diametro deseado
        val = int(self.ui.cb_diam_cargar.currentText())-1
        # Valores de diametros en cadena de caracteres
        DIAM = self.ui.tbl_diam_temp.item(val, 3).text()
        # Valores de diametros en formato de lista tipo float
        List_str_D = list(DIAM[1:-1].split(","))
        col = len(List_str_D)
        List_D = [float(List_str_D[k]) for k in range(col)]
        # Vaciamos los datos a la tabla y columna correspondiente
        row = len(List_D)
        for i in range(0, row):
            d_temp = QtWidgets.QTableWidgetItem(str(List_D[i]))
            self.ui.tbl_tub.setItem(i, 4, d_temp)  # Diametro

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myapp = UIMainWindow()
    myapp.show()
    sys.exit(app.exec_())