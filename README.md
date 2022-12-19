# RedGenHid
__Tesis de posgrado:__ __"ANÁLISIS HIDRÁULICO DE REDES DE DISTRIBUCION DE AGUA POTABLE, CON ALGORITMO GENÉTICO Y SU APLICACIÓN A LA RED DEL MUNICIPIO DE TEZOYUCA EN EL ESTADO DE MÉXICO".__

## _Descripción:_
A través de una aplicación utilizando Algoritmos Genéticos programada en Python y Qt Designer, se desarrolla un programa para determinar los diámetros más adecuados de tuberías en redes para que al realizar un análisis hidráulico se cumpla con las siguientes características:
1. El costo y diseño de la red sea el mínimo posible.
2. Se cumpla con las normas de velocidad y presión dadas por el usuario.
3. Los resultados dados por el programa deben ser corroborados usando 
Epanet 2, con un margen de error menor al 1% de los datos buscados.
4. Usar el programa computacional no requiere un conocimiento profundo de 
programación o algoritmos genéticos.

## _Objetivos:_
<ul>
  <li>Utilizar los algoritmos genéticos como una herramienta útil para resolver problemas de optimización, donde el espacio de búsqueda es demasiado grande.</li>
  <li>Que los usuarios finales, es decir, los estudiantes, puedan utilizarlo sin la necesidad de invertir grandes cantidades de tiempo en el aprendizaje del programa y sin miedo a que el programa devuelva respuestas extrañas que pueda confundirlos.</li>
  <li>Acercar y motivar a los estudiantes de ingeniería civil al aprendizaje de técnicas más modernas como son los algoritmos genéticos aplicados a problemas de hidráulica de tuberías.</li>
  <li>Automatizar el cálculo del diámetro de tuberías de una red de distribución de agua potable, utilizando los algoritmos genéticos como método para obtener los diámetros más económicos que cumplan con la velocidad y presión dadas por el usuario.</li>
  <li>Servir como un complemento de Epanet 2 para los fines citados en el punto anteriormente mencionado, pues también se trabaja con archivos de extensión *.inp.</li>
</ul>

## _Tecnologías usadas:_
![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![PyCharm](https://img.shields.io/badge/PyCharm-000000.svg?&style=for-the-badge&logo=PyCharm&logoColor=white)
![Qt](https://img.shields.io/badge/Qt-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![Adobe_Photoshop](https://img.shields.io/badge/Adobe%20Photoshop-31A8FF?style=for-the-badge&logo=Adobe%20Photoshop&logoColor=black)
![Canva](https://img.shields.io/badge/Canva-%2300C4CC.svg?&style=for-the-badge&logo=Canva&logoColor=white)

## _Diseño de la aplicación:_
A continuacion se hará una breve descripción de la interfaz gráfica de usuario de la aplicación. Para una explicación más detallada consultar el capítulo IV de la tesis <a href="https://github.com/JozCrzBrgn/RedGenHid/tree/main/archivos_ejemplo_">TESIS_B190303.pdf</a>.

### GUI: Inicialización.
Al inicializar el programa aparecerá la ventana de **_Inicialización_** , su función es la de cargar el Progressbar desde cero hasta 100%. El diseño mediante Qt Designer es el siguiente:
  
<img src="/src_/init.gif">

### GUI: Menú desplegable.
Esta es la página con la que se recibe al usuario, su única función es la de mostrar el nombre del programa y dar una pequeña reseña de su función. Independientemente de la página en la que nos encontremos, siempre estará un menú colocado en el lado izquierdo de nuestro programa que se desplegará cada que el ratón pase encima de él. Este menú nos permitirá navegar entre las diferentes paginas disponibles. El diseño mediante Qt Designer es el siguiente:

<img src="/src_/menu.gif">

### GUI: Introducir datos.
Esta interfaz se compone de dos **_QGroupBox_**, el de **_DATOS_** y el de **_RED HIDRAULICA_** que se describen a continuación:

<ul>
  <strong>DATOS:</strong>
  <li>
      <strong>Se pueden introducir datos al programa de forma manual o en formatos: *.csv, *.xlsx y *.inp.</strong>
      <a href="https://github.com/JozCrzBrgn/RedGenHid/tree/main/archivos_ejemplo_">Archivos de ejemplo (CSV, XLSX, INP)</a>
  </li>
  <li>
      <strong>En el manual se describe detalladamente y con un ejemplo como ingresar los datos de la red hidraulica.</strong>
      <a href="https://github.com/JozCrzBrgn/RedGenHid/tree/main/archivos_ejemplo_">Manual REDGENHID.pdf</a>
  </li>
  <li><strong>Se desplega en tablas la información ingresada.</strong></li>
</ul>

<ul>
  <strong>RED HIDRAULICA:</strong>
  <li><strong>Tiene multiples opciones para visualizar en la red.</strong></li>
  <li><strong>Cuenta con un botón para visualizar la red.</strong></li>
</ul>

<img src="/src_/datos.gif">

### GUI: Análisis de Redes Hidráulicas.
En esta página se muestran los resultados del análisis de la red hidráulica utilizando el método del gradiente. El diseño mediante Qt Designer es el siguiente:

<img src="/src_/analisis.gif">

### GUI: Algoritmo Genético.
En esta interfaz se debe dar información adicional al programa antes de poder ejecutar el algoritmo genético, el cual nos dará los diámetros óptimos para la red hidráulica.

<ul>
  <strong>Datos requeridos:</strong>
  <li><strong>Tamaño de población.</strong></li>
  <li><strong>Número de generaciones.</strong></li>
  <li><strong>Tasa de mutación.</strong></li>
  <li><strong>Velocidad máxima y mínima.</strong></li>
  <li><strong>Presión máxima y mínima.</strong></li>
  <li><strong>Diámetros a combinar.</strong></li>
</ul>

<img src="/src_/ag.gif">
 
### GUI: Circular progressbar.
Debido a que el algoritmo genético tiende a demorar en su ejecución, se informa al usuario el progreso del algoritmo usando un progressbar, de esta forma se sabe cuánto porcentaje de avance lleva. El diseño mediante Qt Designer es el siguiente:

<img src="/src_/circ_prog.gif">

## _Elementos clave y sus clases en python:_
Como cualquier programa, se hace uso de la POO para poder representar objetos y sus respectivos atributos de la realidad. A continuacion se hará una breve descripción de los objetos utilizados en la aplicación. Para una explicación más detallada consultar el capítulo III de la tesis <a href="https://github.com/JozCrzBrgn/RedGenHid/tree/main/archivos_ejemplo_">TESIS_B190303.pdf</a>.. 

### Elemento: Nodo.
<img src="/src_appCDT/esquema0.png">
<img src="/src_appCDT/esquema0.png">

### Elemento: Tubería.
<img src="/src_appCDT/esquema0.png">
<img src="/src_appCDT/esquema0.png">

### Elemento: Red Hidraulica.
<img src="/src_appCDT/esquema0.png">
<img src="/src_appCDT/esquema0.png">

### Elemento: Individuo.
<img src="/src_appCDT/esquema0.png">

#### Prop1
#### Prop2
#### Prop3
#### Prop4

### Elemento: Algoritmo Genético.
<img src="/src_appCDT/esquema0.png">

#### Prop1
#### Prop2
#### Prop3
#### Prop4

<h3>
  <i>Puedes descargar una demo dando click en la imagen:</i>
</h3>

<a href="https://drive.google.com/file/d/16mCfvvjA4rNxpOv869UGEddF-_7z5xna/view?usp=sharing">
  <img src="/src_/icono.ico" width=200>
</a>
