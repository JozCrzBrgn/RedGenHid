
# importar todos los elementos necesarios
import csv
import xlrd
from epanettools.epanettools import EPANetSimulation, Node, Link

class FileManipulation(object):
    def __init__(self, File):
        ObjRed = EPANetSimulation(File) # Objeto Red
        self.ObjNodos = ObjRed.network.nodes # Objeto Nodos
        self.ObjTuberias = ObjRed.network.links # Objeto Tuberias
        self.num_nod = len(self.ObjNodos) # Numero de nodos
        self.num_tub = len(self.ObjTuberias) # Numero de tuberias


    def PropiedadesNodos(self):
        """
        :return:
        """
        # PROPIEDADAES DE LAS NODOS
        en = Node.value_type['EN_ELEVATION']  # Elevaciones
        bd = Node.value_type['EN_BASEDEMAND']  # Demandas Base
        tkl = Node.value_type['EN_TANKLEVEL']  # Altura del tanque

        List_Numero_Nodos = []  # Index entero del elemento.
        List_Indx_Nodos = []  # Index string del elemento.
        List_Tipo_Nodo = []  # Tipo de Nodo ('E' ó 'N').
        List_Elev_Nod = []  # Cota del Nodo, (Metros).
        List_DemBase_Nod = []  # Demanda en el Nodo, (L/s).
        List_Tank_Lev = []  # Elevacion del Tanque, (Metros).

        for i in range(self.num_nod):
            if self.ObjNodos[i + 1].node_type == 0:
                tipo = 'N'  # JUNCTION
            elif self.ObjNodos[i + 1].node_type == 2 or self.ObjNodos[i + 1].node_type == 1:
                tipo = 'E'  # TANK

            List_Numero_Nodos.append(self.ObjNodos[i + 1].index)
            List_Indx_Nodos.append(self.ObjNodos[i + 1].id)
            List_Tipo_Nodo.append(tipo)
            List_Elev_Nod.append(round(self.ObjNodos[i + 1].results[en][0],2))
            List_DemBase_Nod.append(round(self.ObjNodos[i + 1].results[bd][0],2))
            List_Tank_Lev.append(round(self.ObjNodos[i + 1].results[tkl][0],2))

        # INFORMACION DE LOS NODOS DE MANERA ORDENADA:
        cont = List_Tipo_Nodo.count('E')  # Contador numero de Tanques
        nn = cont + 1  # Numero de nodos demanda
        ee = 0  # Numero de Tanques
        nn_new = 1  # Numero de nodos demanda corregido

        Coord_X = []
        Coord_Y = []
        List_Nodos_str = []  # NumeroNodo
        Gasto_o_Altura = []  # Gasto_o_Altura
        Tipo_elemento = []  # Tipo_elemento
        Nivel_Topografico = []  # Nivel_Topografico

        for i in range(self.num_nod):
            # NumeroNodo.append(nn_new)  # Despues ordenada
            nn_new += 1
            if List_Tipo_Nodo[i] == 'E':
                # n_antes_ordenada.insert(ee, List_Numero_Nodos[i])
                List_Nodos_str.insert(ee, List_Indx_Nodos[i])
                Gasto_o_Altura.insert(ee, List_Tank_Lev[i])
                Tipo_elemento.insert(ee, List_Tipo_Nodo[i])
                Nivel_Topografico.insert(ee, List_Elev_Nod[i])
                Coord_X.insert(ee, 0)
                Coord_Y.insert(ee, 0)
                ee += 1
            elif List_Tipo_Nodo[i] == 'N':
                # n_antes_ordenada.insert(nn, List_Numero_Nodos[i])
                List_Nodos_str.insert(nn, List_Indx_Nodos[i])
                Gasto_o_Altura.insert(nn, List_DemBase_Nod[i])
                Tipo_elemento.insert(nn, List_Tipo_Nodo[i])
                Nivel_Topografico.insert(nn, List_Elev_Nod[i])
                Coord_X.insert(nn, 0)
                Coord_Y.insert(nn, 0)
                nn += 1

        return Coord_X, Coord_Y, List_Nodos_str, Gasto_o_Altura, Tipo_elemento, Nivel_Topografico


    def PropiedadesTuberias(self):
        """

        :return:
        """
        l = Link.value_type['EN_LENGTH']
        d = Link.value_type['EN_DIAMETER']
        ml = Link.value_type['EN_MINORLOSS']
        r = Link.value_type['EN_ROUGHNESS']
        List_Tuberias = []
        ini_fin = []
        Long_Tub = []
        Diam_Tub = []
        PM_Tub = []
        Rug_Tub = []
        for i in range(self.num_tub):
            ni = self.ObjTuberias[i + 1].start.id
            nf = self.ObjTuberias[i + 1].end.id
            ini_fin.append([ni, nf])
            Long_Tub.append(round(self.ObjTuberias[i + 1].results[l][0],2))
            Diam_Tub.append(round(self.ObjTuberias[i + 1].results[d][0],2))
            PM_Tub.append(self.ObjTuberias[i + 1].results[ml][0])
            Rug_Tub.append(self.ObjTuberias[i + 1].results[r][0])
            List_Tuberias.append(self.ObjTuberias[i + 1].id)
        return List_Tuberias, ini_fin, Long_Tub, Diam_Tub, PM_Tub, Rug_Tub

    def CSV_Read(filepath,Nod_or_Tub = None):
        with open(filepath) as File:
            reader = csv.reader(File, delimiter=',', quotechar=',',
                                quoting=csv.QUOTE_MINIMAL)
            NodosTuberias = []
            for row in reader:
                NodosTuberias.append(row)

            NodosTuberias.remove(NodosTuberias[0])

            if Nod_or_Tub == 'Nodos':
                NodosTuberias = sorted(NodosTuberias, key=lambda tipo: tipo[4])

        return NodosTuberias

    def XSLX_Read(fileName, Sht_Nod, Sht_Tub):
        # Cargamos el Libro de Excel a usar
        wb = xlrd.open_workbook(fileName)
        # Buscamos las hojas
        sheet_Nod = wb.sheet_by_name(Sht_Nod)
        rows_n = sheet_Nod.nrows # Numero de renglones (hoja nodos)
        sheet_Tub = wb.sheet_by_name(Sht_Tub)
        rows_t = sheet_Tub.nrows # Numero de renglones (hoja tuberias)
        # Variables auxiliares
        data_n = []; values = []; cont = 0
        # Data de los Nodos
        for j in range(rows_n):
            for i in range(6):
                if cont == 6:
                    data_n.append(values)
                    values = []
                    cont = 0
                n = sheet_Nod.cell_value(j, i)
                values.append(n)
                cont += 1
        data_n.append(values)
        data_n.remove(data_n[0])
        data_n = sorted(data_n, key=lambda tipo: tipo[4])

        # Variables auxiliares
        data_t = []; values = []; cont = 0
        # Data de las Tuberias
        for j in range(rows_t):
            for i in range(7):
                if cont == 7:
                    data_t.append(values)
                    values = []
                    cont = 0
                t = sheet_Tub.cell_value(j, i)
                values.append(t)
                cont += 1
        data_t.append(values)
        data_t.remove(data_t[0])

        return data_n, data_t
