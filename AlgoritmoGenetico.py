import GradienteHidraulico as gh
import random as random
import timeit
from progressBarPYQT5 import ProgBar
from PyQt5.QtCore import QCoreApplication

class Individuo:
    def __init__(self, RedHidraulica, K1, K2, RegTipo, DiametroTuberias = []):

        self.I_cn = RedHidraulica.Nod  # Clase Nodos (Datos de los nodos)
        self.I_ct = RedHidraulica.Tub  # Clase Tuberia (Datos de las tuberias)
        self.Dcom = RedHidraulica.Dcom  # Diametro comercial
        self.diametros = DiametroTuberias  # Diametros de la tueberia
        self.K1 = K1
        self.K2 = K2
        self.RT = RegTipo

        # Restricciones Hidraulicas
        self.Pd_max = RedHidraulica.Pd_max  # Presion Maxima de Diseño, (m.c.a.).
        self.Pd_min = RedHidraulica.Pd_min  # Presion Minima de Diseño, (m.c.a.).
        self.Vd_max = RedHidraulica.Vd_max  # Velocidad Maxima de Diseño, (m/s).
        self.Vd_min = RedHidraulica.Vd_min  # Velocidad Minima de Diseño, (m/s).

        # Inicializamos el cromosoma, el diametro y el fitness en vacio pues recibirán datos despues
        self.num_tub = len(self.I_ct)  # Longitud del Cromosoma
        self.Penalizacion = 0
        self.Fit = 0

        # Creacion de la lista DiametroTuberias
        if len(self.diametros) == 0:
            # Se crean diametros al azar
            for i in range(self.num_tub):
                val = round(random.randint(0, len(self.Dcom) - 1))
                self.diametros.append(self.Dcom[val])
                self.I_ct[i].d = self.diametros[i] / 1000
        else:
            for i in range(self.num_tub):
                self.I_ct[i].d = self.diametros[i] / 1000

        # Ejecutamos el Metodo del Gradiente para evaluar al individuo hidraulicamente
        self.cg = gh.Gradiente(self.I_ct, self.I_cn).Resolver() # [Q, V, H, P, f, hf, er]

        self.Vel = self.cg[1]
        self.v_min = float(min(self.Vel))
        self.v_max = float(max(self.Vel))

        self.Press = self.cg[3]
        self.p_min = float(min(self.Press))
        self.p_max = float(max(self.Press))

    def __str__(self):
        print("Diametros: ", self.diametros)
        print("Velocidades:")
        print("Minima : ", round(self.v_min,3), "m/s, Maxima: ", round(self.v_max,3), "m/s")
        print("Presiones: ")
        print("Minima : ", round(self.p_min,3), "m.c.a., Maxima: ", round(self.p_max,3), "m.c.a.")
        print("Error porcentual: ",self.cg[6], "%")
        print("Costo de Construccion: ", round(self.Cc(), 3))
        print("Costo Hidraulico: ", round(self.penalizacion(), 3))
        print("Fitness: ", round(self.Fitness(), 3))
        return ""

    ''' Funcion del Costo Constructivo '''

    def Cc(self):
        self.Costo = 0
        # Costo = L * ( K1 * D + K2 )
        if self.RT == "Lineal":
            for i in range(self.num_tub):
                self.Costo += self.I_ct[i].L * (self.K1 * self.diametros[i] + self.K2)

        # Costo = L * (K1 * 10 ** (K2 * D))
        elif self.RT == "Exponencial":
            for i in range(self.num_tub):
                self.Costo += self.I_ct[i].L * (self.K1 * 10 ** (self.K2 * self.diametros[i]))

        # Costo = L * (K1 * D ** K2)
        elif self.RT == "Potencial":
            for i in range(self.num_tub):
                self.Costo += self.I_ct[i].L * (self.K1 * self.diametros[i] ** self.K2)

        return self.Costo  # Costo de construcción de este individuo en pesos

    def penalizacion(self):

        # Penalizacion Hidraulica
        if (self.v_min < self.Vd_max) and (self.v_min >= self.Vd_min):
            P_vmin = 0
        else:
            P_vmin = 10*abs(self.v_min - self.Vd_min)

        if (self.v_max <= self.Vd_max) and (self.v_max > self.Vd_min):
            P_vmax = 0
        else:
            P_vmax = 10*abs(self.v_max - self.Vd_max)

        if (self.p_max <= self.Pd_max) and (self.p_max > self.Pd_min):
            P_pmax = 0
        else:
            P_pmax = abs(self.p_max - self.Pd_max)

        if (self.p_min < self.Pd_max) and (self.p_min >= self.Pd_min):
            P_pmin = 0
        else:
            P_pmin = abs(self.p_min - self.Pd_min)

        # Penalizacion Hidraulica total para el individuo
        self.Penalizacion = P_pmax + P_pmin + P_vmax + P_vmin
        return self.Penalizacion

    def Fitness(self):
        self.Fit = self.Cc() * (1 + self.penalizacion())
        return self.Fit


class AlgoritmoGenetico():
    def __init__(self,RedHidraulica ,k1, k2, RegreTipo, tamano_poblacion, tasa_mutacion, num_generaciones):

        self.rh = RedHidraulica
        self.K1 = k1
        self.K2 = k2
        self.RT = RegreTipo
        self.tam_pob = tamano_poblacion
        self.tasa_mutacion = tasa_mutacion
        self.num_gene = num_generaciones

        self.Dcom = RedHidraulica.Dcom
        self.poblacion = []
        self.poblacion_evaluada = []
        self.suma_porcentajes = []
        self.mejores_padres = []
        self.mejor_individuo = []

    def __str__(self):
        print("Tamaño de la poblacion", self.tam_pob)
        print("Tasa de Mutacion: ", self.tasa_mutacion)
        print("Numero de generaciones: ", self.num_gene)
        print("Diametros Comerciales a usar: ", self.Dcom)
        print("Tipo de Regresion: ", self.RT)
        return ""

        # RedHidraulica, K1, K2, RegTipo, DiametroTuberias = []

    def inicializar_poblacion(self):  # -->
        self.poblacion = []
        for i in range(self.tam_pob):
            ind = Individuo(self.rh, self.K1, self.K2, self.RT, [])
            self.poblacion.append(ind)
        return self.poblacion

    def poblacion_eval(self):  # -->
        self.poblacion_evaluada = []
        for i in range(self.tam_pob):
            self.poblacion_evaluada.append(self.poblacion[i].Fitness())
        return self.poblacion_evaluada

    def ordenar_poblacion(self):  # -->
        self.poblacion = sorted(self.poblacion,
                                key=lambda poblacion: poblacion.Fit,
                                reverse=True)

    def porcentaje_acumulado(self):  # -->
        Fitness_inv = []
        for i in range(self.tam_pob):
            Fitness_inv.append(1 / self.poblacion_evaluada[i])
        Sfx = sum(Fitness_inv)
        fx_Sfx = []
        for i in range(self.tam_pob):
            if i == 0:
                fx_Sfx.append(Fitness_inv[i] / Sfx)
            else:
                fx_Sfx.append(fx_Sfx[i - 1] + Fitness_inv[i] / Sfx)
        self.suma_porcentajes = fx_Sfx
        return self.suma_porcentajes

    def ruleta_aleatoria(self):  # -->
        self.mejores_padres = []
        num_tiros = self.tam_pob
        for i in range(0, num_tiros - 1):
            tiro = random.random()
            if tiro <= self.suma_porcentajes[0]:
                self.mejores_padres.append(self.poblacion[0].diametros)
            else:
                for j in range(1, num_tiros):
                    if self.suma_porcentajes[j - 1] < tiro and tiro <= self.suma_porcentajes[j + 1]:
                        self.mejores_padres.append(self.poblacion[j].diametros)
                        break
        self.elitismo()
        return self.mejores_padres

    def nueva_poblacion(self, new_padres):
        self.poblacion = []
        for i in range(self.tam_pob):
            ind = Individuo(self.rh, self.K1, self.K2, self.RT, new_padres[i])
            self.poblacion.append(ind)
        return self.poblacion

    def crossover(self):
        padres = []
        madres = []
        '''Separamos en padres y madres'''
        for i in range(0, self.tam_pob, 2):
            padres.append(self.poblacion[i].diametros)
            madres.append(self.poblacion[i + 1].diametros)
        ''' Cruzamos los padres y madres'''
        Hijos = []
        for i in range(len(padres)):
            padre = padres[i]
            madre = madres[i]
            corte = round(random.random() * (len(padre) - 1))
            Hijo1 = padre[0:corte] + madre[corte::]
            Hijo2 = madre[0:corte] + padre[corte::]
            Hijos.append(Hijo1)
            Hijos.append(Hijo2)
        return Hijos

    def mutacion(self, hijos):  # --> OK
        mut = []
        for i in range(len(hijos)):
            h = hijos[i]
            for j in range(len(h)):
                if random.random() < self.tasa_mutacion:
                    h[j] = self.Dcom[round(random.randint(0, len(self.Dcom) - 1))]
            mut.append(h)
        return mut

    def mejor_individuo_especie(self, gene):  # --> OK
        mejor_de_la_especie = min(self.poblacion, key=lambda poblacion: poblacion.Fit)

        diam = mejor_de_la_especie.diametros
        val = mejor_de_la_especie.Fit
        hid = mejor_de_la_especie.Penalizacion
        cos = mejor_de_la_especie.Costo

        if gene == 0:
            self.mejor_individuo.append([diam, hid, val, cos, gene])
        if (gene > 0) and (val < self.mejor_individuo[-1][2]):
            self.contador = 0
            self.mejor_individuo.append([diam, hid, val, cos, gene])
        else:
            self.contador += 1

        return self.mejor_individuo

    def elitismo(self):
        self.mejores_padres.append(self.mejor_individuo[-1][0])

    def TiempoEjecucion(self, seg):
        hr = seg / 3600
        hora = int(hr)  # Hora
        minu = (hr - hora) * 60
        minuto = int(minu)  # Minutos
        segundo = int(round((minu - minuto) * 60, 0))
        return hora, minuto, segundo

    def resolver(self):
        tic = timeit.default_timer()
        # Inicializamos la poblacion:
        self.inicializar_poblacion()
        self.contador = 0
        self.main = ProgBar()
        self.main.show()

        for i in range(self.num_gene):

            # self.generacion.append(i)
            QCoreApplication.processEvents()
            self.main.repaint()
            self.main.progressBarValue(i, self.num_gene)

            # Evaluamos la poblacion para posteriormente ordenarla:
            self.poblacion_eval()

            # Ordenamos la poblacion:
            self.ordenar_poblacion()
            self.poblacion_eval()

            # Seleccionamos al mejor individuo de la poblacion
            self.mejor_individuo_especie(i)

            # Calculamos un porcentaje acumulado para cada individuo que servira para el filtro de la ruleta:
            self.porcentaje_acumulado()

            # Ponemos a competir a los individuos a traves de la seleccion por ruleta:
            Rul = self.ruleta_aleatoria()

            # Creamos una nueva poblacion tomando en cuenta el filtro de ruleta:
            self.nueva_poblacion(Rul)
            self.poblacion_eval()

            # Seleccionamos al mejor individuo de la poblacion
            self.mejor_individuo_especie(i)

            # Reproducimos la poblacion (Crossover):
            crom_cross = self.crossover()

            # Mutamos la poblacion:
            muta = self.mutacion(crom_cross)

            # Creamos una nueva poblacion tomando en cuenta los genes mutados:
            self.nueva_poblacion(muta)

            if self.contador >= 100:
                print("Generacion con solucion mas optima: ", i)
                break

        # Tiempo de ejecución del AG
        toc = timeit.default_timer()
        Dtt = (toc - tic)
        [hora, minuto, segundo] = self.TiempoEjecucion(Dtt)

        return self.mejor_individuo, hora, minuto, segundo