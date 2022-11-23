# info de la materia: ST0263 Topicos especiales en telematica
#
# Estudiante(s): Camila Mejia Muñoz, cmejiam10@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
#
#
# 1. breve descripción de la actividad
Realizar una aplicación monolítica no escalable desplegada en AWS, con nombre de dominio y certificado SSL válido.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
Ejecutar el wordcount por linea de comando 'pyspark' INTERACTIVO en EMR con datos en HDFS vía ssh en el nodo master.
Ejecutar el wordcount por linea de comando 'pyspark' INTERACTIVO en EMR con datos en S3 (tanto de entrada como de salida) vía ssh en el nodo master.

Despliegue de la aplicación Moodle con Docker y nginx en la instancia de AWS. Asignación de un dominio propio con certificado SSL válido con Let's Encrypt.
Implementación de un balanceador de cargas con Docker y nginx en una instancia de AWS, en la capa de aplicación del Moodle.
Implementación de un servidor de base de datos con Docker en una instancia de AWS, conectado al Moodle.
Implementación de un servidor para archivos con Docker en una instancia de AWS, conectado al Moodle.


## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)



# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se utilizaron servicios de AWS:
EMR: Amazon EMR es una plataforma de clúster administrada que simplifica la ejecución de los marcos de trabajo de Big Data, tales comoApache HadoopyApache Spark, enAWSpara procesar y analizar grandes cantidades de datos.
S3: Amazon Amazon S3 es un servicio de almacenamiento de objetos que ofrece escalabilidad, disponibilidad de datos, seguridad y rendimiento líderes en el sector.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## detalles del desarrollo.

Nos conectamos al nodo master del EMR

#Ejecutar el wordcount por linea de comando 'pyspark' INTERACTIVO en EMR con datos en HDFS vía ssh en el nodo master.

Cargamos los datasets en el nodo

```
sudo yum install git -y
git clone https://github.com/st0263eafit/st0263-2022-2.git
```
Creamos la carpeta /user/hadoop/datasets en Hue con hdfs.

```
hdfs dfs -mkdir /user/hadoop/datasets

```
Copiamos los datasets a Hue con hdfs.
```
hdfs dfs -copyFromLocal st0263-2022-2/bigdata/datasets/* /user/hadoop/datasets
```
Ejecutamos el wordcount con los siguientes comandos.
```
pyspark
>>> files_rdd = sc.textFile("hdfs:///user/hadoop/datasets/gutenberg-small/*.txt")
>>> wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
>>> wc = wc_unsort.sortBy(lambda a: -a[1])
>>> for tupla in wc.take(10):
...  print(tupla)
...
```
Guardamos los datos de salida en Hue con hdfs.

```
>>> wc.saveAsTextFile("hdfs:///tmp/wcout1")
```
Podemos ver los datos de salida en Hue en la carpeta /tmp/wcout1.
IMAGEN1

#Ejecutar el wordcount por linea de comando 'pyspark' INTERACTIVO en EMR con datos en S3 (tanto de entrada como de salida) vía ssh en el nodo master

Creamos un bucket S3 y cargamos los datasets desde nuestros archivos.
```


>>> files_rdd = sc.textFile("s3://notebookscmejiam10/datasets/gutenberg-small/*.txt")
>>> wc_unsort = files_rdd.flatMap(lambda line: line.split()).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
>>> wc = wc_unsort.sortBy(lambda a: -a[1])
>>> for tupla in wc.take(10):
...  print(tupla)
...
```
Guardamos los datos de salida en Hue con hdfs.
```
>>> wc.saveAsTextFile("hdfs:///tmp/wcout2")
```

Guardamos los datos de salida en S3.
```
>>> wc.saveAsTextFile("s3://notebookscmejiam10/wcout2")
```

Podemos ver los datos de salida en Hue en la carpeta /tmp/wcout2.

IMAGEN2

Podemos ver que los datos de salida en S3.
IMAGEN 3

#Ejecutar el wordcount en JupyterHub Notebooks EMR con datos en S3 (tanto datos de entrada como de salida) usando un clúster EMR

Copiamos el notebook del wordcount y lo ejecutamos.


## REFERENCIAS
https://github.com/st0263eafit/st0263-2022-2/

#### versión README.md -> 1.0 (2022-agosto)
