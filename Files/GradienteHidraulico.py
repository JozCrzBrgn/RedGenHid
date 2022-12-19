import math
import numpy as np

class Nodos(object):
    def __init__(self, NumeroNodo, Gasto_o_Altura, Tipo_elemento, Nivel_Topografico):
        """

        *** VARIABLES PRINCIPALES ***

        :param NumeroNodo: Número del nodo a usar.
        :param Gasto_o_Altura: Gasto si es un Nodo, Altura si es un Tanque (L/s).
        :param Tipo_elemento: Tanque--> 'E', Nodo--> 'N'.
        :param Nivel_Topografico: Cota de Terreno del nodo (Metros).

        """
        self.nn = NumeroNodo
        self.tipo = Tipo_elemento
        self.msnm = Nivel_Topografico
        self.q = 0  # Gasto de demanda nodal
        self.h = 0  # Altura del embalse

        if self.tipo == 'E':
            self.h = Gasto_o_Altura
        elif self.tipo == 'N':
            self.q = Gasto_o_Altura / 1000

    def __str__(self):
        if self.tipo == 'E':
            print('Tipo de Elemento: Embalse o Tanque')
        else:
            print('Tipo de Elemento: Nodo')
        print('Numero de nodo: ', str(self.nn))
        print('Cota de Nivel: ', str(self.msnm), ' metros')
        if self.tipo == 'E':
            print('La altura es: ', str(self.h), ' metros')
        else:
            print('La demanda es: ', str(self.q * 1000), ' L/s')
        return ""


class Tuberias(object):
    def __init__(self, Numerotub, n_ini, n_fin, Longiud, diametro, perd_menores, Rugosidad_Absoluta):
        """

        *** VARIABLES PRINCIPALES ***

        :param Numerotub: Numero de la tuberia.
        :param n_ini: Nodo inicial de la tuberia.
        :param n_fin: Nodo final de la tuberia.
        :param Longiud: Longitud de la tuberia.
        :param diametro: Diametro de la tuberia (Milimetros).
        :param perd_menores: Perdida Menor de la tuberia (Adimencional).
        :param Rugosidad_Absoluta: Rugosidad Absoluta de la tuberia (Milimetros).
        """
        self.ni = n_ini
        self.nf = n_fin
        self.nt = Numerotub
        self.L = Longiud
        self.d = diametro / 1000
        self.km = perd_menores
        self.ks = Rugosidad_Absoluta / 1000

    def Direccion(self):
        """
        :return: Vector de Direccion de la tuberia.
        """
        return [self.ni, self.nf]

    def Area(self):
        """
        :return: Area de la seccion tranversal de la tuberia (Metros).
        """
        return 0.25 * math.pi * self.d ** 2

    def __str__(self):
        print('Numero de tuberia: ', str(self.nt))
        print('[Nodo inicial, Nodo final]: ', str([self.ni, self.nf]))
        print('Longitud de la tuberia: ', str(self.L), ' metros')
        print('Diametreo de la tuberia: ', str(self.d * 1000), ' milimetros')
        print('Pérdidas Menores: ', str(round(self.km, 4)))
        print('Rugosidad Absoluta: ', str(round(self.ks * 1000, 5)), ' milimetros')
        print('Area de la tuberia: ', str(round(self.Area(), 4)), ' m2')
        return ""


class RedHidraulica(object):
    def __init__(self, data_nod, data_tub, Pdmax, Pdmin, Vdmax, Vdmin, DiametroComercial):

        # Listas con
        self.dataN = data_nod
        self.dataT = data_tub

        # Restricciones Hidraulicas
        self.Pd_max = Pdmax  # Presion Maxima de Diseño, (m.c.a.).
        self.Pd_min = Pdmin  # Presion Minima de Diseño, (m.c.a.).
        self.Vd_max = Vdmax  # Velocidad Maxima de Diseño, (m/s).
        self.Vd_min = Vdmin  # Velocidad Minima de Diseño, (m/s).

        # Diametros y valores de regresiones
        self.Dcom = DiametroComercial  # Diametro comercial

        self.Nod = []
        row_n = len(self.dataN)
        for i in range(row_n):
            self.Nod.append(Nodos(self.dataN[i][0], self.dataN[i][1], self.dataN[i][2], self.dataN[i][3]))

        self.Tub = []
        row_t = len(self.dataT)
        for i in range(row_t):
            self.Tub.append(
                Tuberias(self.dataT[i][0], self.dataT[i][1], self.dataT[i][2], self.dataT[i][3], self.dataT[i][4],
                         self.dataT[i][5], self.dataT[i][6]))

        self.num_nod = len(self.Nod)  # Numero total de Nodos (sin distinguir entre embalces)
        self.num_tub = len(self.Tub)  # Numero total de Tuberias

    def __str__(self):
        print('Numero de tuberias: ', str(self.num_tub))
        print('Numero de nodos: ', str(self.num_nod))
        print('Vdmax: ', self.Vd_max, ' Vdmin: ', self.Vd_min, ' Pdmax: ', self.Pd_max, ' Pdmin: ', self.Pd_min)
        print('Diametros comerciales a usar: ', self.Dcom)
        return ""


class Gradiente(object):
    def __init__(self, Tuberias, Nodos, Viscocidad_dinamica = None):
        """
            *** VARIABLES PRINCIPALES ***

        :param Tuberias:
        :param Nodos:
        :param Viscocidad_dinamica:
        """
        self.Lt = Tuberias
        self.Ln = Nodos
        if Viscocidad_dinamica == None:
            self.v = 1.141*10**-6
        else:
            self.v = Viscocidad_dinamica

        """
            *** VARIABLES SECUNDARIAS ***

        :param num_nod: Numero total de Nodos (sin distinguir entre embalces).
        :param NT: Numero total de Tuberias.
        :param NS: Numero de Embalces.
        :param NN: Numero de Nodos.
        :param Cota: Cotas de cada Nodo.
        :param D_Cota: Diferencia de alturas entre la cota del Embalce y las cotas de los Nodos.
        :param Qd: Vector de Demandas en los nodos, (m3/s).
        :param Ho: Vector de Altura de los embalses, (Metros).
        :param n_dw: Numero de Darcy-Weisbach.
        :param ini_fin: Vector de Direccion del flujo la tuberia.
        """
        self.num_nod = len(self.Ln) # Numero total de Nodos (sin distinguir entre embalces)
        self.NT = len(self.Lt) # Numero total de Tuberias
        self.NS = 0 # Numero de Embalces
        self.NN = 0 # Numero de Nodos
        self.Cota = [] # Cotas de cada Nodo
        self.D_Cota = [] # Diferencia de alturas entre la cota del Embalce y las cotas de los Nodos
        self.Qd = []
        self.Ho = []
        self.n_dw = 2 # Numero de Darcy-Weisbach
        self.ini_fin = []
        self.I = np.eye(self.NT) # Matriz Identidad I
        self.N = np.eye(self.NT) * self.n_dw # Matriz diagonal Darcy-Weisbach



        # DEMANDAS, ALTURAS Y COTAS
        Cota = []
        Demanda = []
        AlturaEmbalce = []
        for i in range(self.NT):
            if i <= (self.num_nod-1):
                if self.Ln[i].tipo == 'E':
                    AlturaEmbalce.append([self.Ln[i].h])
                    self.NS += 1
                elif self.Ln[i].tipo == 'N':
                    Demanda.append([self.Ln[i].q])
                    self.NN += 1
                Cota.append([self.Ln[i].msnm])
            self.ini_fin.append([self.Lt[i].Direccion()[0], self.Lt[i].Direccion()[1]])

        self.Cota = np.array(Cota)
        self.D_Cota = [self.Cota[0] - val for val in self.Cota]
        self.Qd = np.array(Demanda)
        self.Ho = np.array(AlturaEmbalce)

        # Matrices A12, A21 y A10
        self.__MatricesPrincipales()


    """
        METODO PARA OBTENER LAS MATRICES: A12, A21 y A10
    """
    def __MatricesPrincipales(self):
        """
        :return:
                A12: Matriz de conectividad (-1 inicio y 1 final).
                A21: Matriz Transpuesta de A12 --> A21.
                A10: Matriz Topologica tramo a nudo.
        """
        # Matriz de conectividad (-1 inicio y 1 final)
        self.A12 = []
        A12 = np.zeros((self.NT, self.NN + self.NS))
        for i in range(self.NT):
            ni = self.ini_fin[i][0] - 1
            nf = self.ini_fin[i][1] - 1
            A12[i][ni] = -1
            A12[i][nf] = 1
        self.A12 = A12[:, self.NS:(self.NN + self.NS)]

        # Matriz Transpuesta de A12 --> A21
        self.A21 = []
        self.A21 = np.transpose(self.A12)

        # Matriz Topologica tramo a nudo
        self.A10 = []
        self.A10 = A12[:, 0:self.NS]

        return self.A12, self.A21, self.A10

    """
        ECUACION DE VELOCIDAD
    """
    def __Vel(self, A, Q):
        """
        :param A: Area de la seccion transversal de la tuberia, (m2).
        :param Q: Caudal que corre por la tuberia, (L/s).
        :return:
                V: Velocidad que corre por la tuberia, (m/s).
        """
        return Q / A

    """
        NUMERO DE REYNOLDS
    """
    def __Re(self, V, d):
        """
        :param V: Velocidad que corre por la tuberia, (m/s).
        :param d: Diametro de la tuberia, (Metros).
        :return:
                Re: Numero de Reynols, (Adimencional).
        """
        return abs(V * d / self.v)

    """
        ECUACION DE SWAMEE-JAIN
    """
    def __SwameeJain(self, Re, d, ks):
        """
        :param Re: Numero de Reynols, (Adimencional).
        :param d: Diametro de la tuberia, (Metros).
        :param ks: Rugosidad Absoluta de la tuberia (Metros).
        :return:
                f: Factor de Friccion, (Adimencinoal).
        """
        v1 = ks / (3.71 * d)
        v2 = 5.74 / (Re ** 0.9)
        v3 = math.log10(v1 + v2)
        v4 = v3 ** 2
        f = 0.25 / v4
        return f

    def __HagenPoiseuille(self, Re):
        f = 64 / Re
        return f

    def __ColebrookWhite(self, Re, d, ks):
        def Fricc(Re, ks, d, x):
            a = ks / (3.7 * d)
            b = 2.51 * x / Re
            return - 2 * math.log10(a + b) - x

        def Fricc_p(Re, ks, d, x):
            a = - 2 / math.log (10)
            b = ks / (3.7 * d)
            c = 2.51 * x / Re
            d = 2.51 / Re
            return (a * d / (b + c)) - 1

        tol = 0.00001  # Tolerancia permitida del error.
        error = 100  # Error de inicialización.
        while error >= tol:
            if error == 100:
                x1 = self.__SwameeJain(Re, d, ks)
            Fxp = Fricc_p(Re, ks, d, x1)
            Fx = Fricc(Re, ks, d, x1)
            x2 = x1 - (Fx / Fxp)
            error = abs((x2 - x1) / x2) * 100
            x1 = x2
        f = 1 / (x1 ** 2)
        return f

    def Fn_Friccion(self, Re, d, ks):
        if Re < 2200:
            return self.__HagenPoiseuille(Re)
        elif Re >= 2200:
            return self.__ColebrookWhite(Re, d, ks)

    """
        METODO PARA INVERTIR LA DIRECCION DE UNA TUBERIA
    """
    def __InvertirTuberia(self, Caudal):
        """
        :param Caudal: Vector del Caudal en una tuberia, (L/s).
        :return:
                ini_fin: Vector de Direccion del flujo la tuberia.
        """
        aux = self.ini_fin
        self.ini_fin = []
        for i in range(self.NT):
            if Caudal[i] < 0:
                self.ini_fin.append([aux[i][1], aux[i][0]])
            else:
                self.ini_fin.append([aux[i][0], aux[i][1]])
        return self.ini_fin

    """
        METODO RESOLVER:
    """
    def Resolver(self):
        """
        :return:
                Caudal: Vector del Caudal en una tuberia, (L/s).
                Velocidad: Vector de Velocidad que corre por la tuberia, (m/s).
                Altura: Vector de Altura Piezometrica en cada nodo, (Metros).
                Presion: Vector de Presion en cada nodo, (Metros).
                er: Error porcentual de la iteracion, (%).
        """
        iter = 0
        Velocidad = np.zeros((self.NT, 1))
        Perd = np.zeros((self.NT, 1))
        Fricc = np.zeros((self.NT, 1))

        while iter < self.NT:
            self.__MatricesPrincipales()
            [self.Caudal, self.Altura, self.Presion, self.er] = self.__Calcular()
            if self.Caudal.min() < 0:
                self.__InvertirTuberia(self.Caudal)
                iter += 1
            elif self.Caudal.min() >= 0:
                for i in range(self.NT):
                    Velocidad[i] = (self.Caudal[i] / 1000) / self.Lt[i].Area()
                    diam2 = self.Lt[i].d
                    ks2 = self.Lt[i].ks
                    Reynolds2 = self.__Re(Velocidad[i], diam2)
                    Fricc[i] = self.Fn_Friccion(Reynolds2, ks2, diam2)
                    #Perd[i] = (Fricc[i] * self.Lt[i].L / diam2) * ((Velocidad[i] ** 2) / 19.62)
                    Perd[i] = 1000*(Fricc[i] / diam2) * ((Velocidad[i] ** 2) / 19.62)

                break
        return self.Caudal, Velocidad, self.Altura, self.Presion, Fricc, Perd, self.er, self.ini_fin


    def __Calcular(self):
        itera = 1
        er = 100
        ErrorLista = []

        # Iteraciones
        while er > 0.00001 and itera < 2 * self.NN:
            A11 = np.zeros((self.NT, self.NT))
            A11_p = np.zeros((self.NT, self.NT))
            if itera == 1:
                Qi = np.ones((self.NT, 1)) * 0.1

            for j in range(self.NT):
                Area = self.Lt[j].Area()
                diametro = self.Lt[j].d
                ks = self.Lt[j].ks
                km = self.Lt[j].km
                V = self.__Vel(Area, Qi[j])
                Re = self.__Re(V, diametro)
                f = self.Fn_Friccion(Re, diametro, ks)
                Longitud = self.Lt[j].L
                alpha = ((f * Longitud / diametro) + km) / (19.62 * (Area ** 2))
                beta = 0
                gamma = 0
                a = alpha * (Qi[j] ** (self.n_dw - 1))
                b = beta
                c = gamma / Qi[j]
                A11[j][j] = a + b + c
                A11_p[j][j] = a

            # Calculo de la Altura Piezometrica H(i+1)
            h1 = np.linalg.inv(np.matmul(self.N, A11_p))
            h2 = np.linalg.inv(np.matmul(np.matmul(self.A21, h1), self.A12))
            h3 = np.matmul(A11, Qi) + np.matmul(self.A10, self.Ho)
            h4 = np.matmul(np.matmul(self.A21, h1), h3)
            h5 = h4 - np.matmul(self.A21, Qi) + self.Qd
            H = -np.matmul(h2, h5)

            # Calculo del Caudal Q(i+1)
            Qanterior = np.linalg.norm(Qi)
            q1 = self.I - np.matmul(h1, A11)
            q2 = np.matmul(self.A12, H) + np.matmul(self.A10, self.Ho)
            Qi = np.matmul(q1, Qi) - np.matmul(h1, q2)
            Qactual = np.linalg.norm(Qi)

            # Error Relativo Porcentual
            er = abs((Qactual - Qanterior) / Qactual) * 100
            ErrorLista.append(er)
            itera += 1

        Caudal = Qi * 1000
        Presion = np.zeros((self.NN, 1))
        Altura = np.zeros((self.NN, 1))

        for i in range(self.NN):
            Presion[i] = H[i] + self.D_Cota[i + self.NS]
            Altura[i] = self.Cota[i + self.NS] + Presion[i]

        return Caudal, Altura, Presion, ErrorLista
