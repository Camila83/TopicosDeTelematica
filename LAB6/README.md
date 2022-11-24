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
![image](https://user-images.githubusercontent.com/37966987/203662605-a264a747-bd5a-4ffd-bd43-9582873e5b83.png)

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
![image](https://user-images.githubusercontent.com/37966987/203662687-e242c6e5-c1c8-48d2-9995-264e70c69fe9.png)

Podemos ver que los datos de salida en S3.
![image](https://user-images.githubusercontent.com/37966987/203662711-e501bc2c-2e32-418f-a740-0a02d88e27c3.png)

#Ejecutar el wordcount en JupyterHub Notebooks EMR con datos en S3 (tanto datos de entrada como de salida) usando un clúster EMR

Copiamos el notebook Data_processing_using_PySpark.ipynb.
Ejecutamos las celdas del notebook.
![image](https://user-images.githubusercontent.com/37966987/203667657-90d3d654-3437-4adb-88b6-35ca5b6c4833.png)

![image](https://user-images.githubusercontent.com/37966987/203667666-e0c0f489-900a-4bc6-9a55-4326ff258e13.png)

![image](https://user-images.githubusercontent.com/37966987/203667675-3aaa88e7-c25f-48bd-85cd-d2e648f8ab01.png)

![image](https://user-images.githubusercontent.com/37966987/203667686-96da11fc-ff7f-49d6-93d4-b587698bb9bd.png)

![image](https://user-images.githubusercontent.com/37966987/203667694-d95c2714-6d2f-47d8-84aa-0256de190282.png)

![image](https://user-images.githubusercontent.com/37966987/203667703-9d7f29bc-0cae-480c-b0b4-93c5732b5fad.png)

![image](https://user-images.githubusercontent.com/37966987/203667715-b60196bb-7d3d-4fb5-98e8-c1dd1ad8824e.png)

![image](https://user-images.githubusercontent.com/37966987/203667725-d39fc1af-a4ea-495a-b7cb-46270b3a5bf4.png)

![image](https://user-images.githubusercontent.com/37966987/203667733-057b5733-8767-4f97-ad97-fec72dfe5cbd.png)

![image](https://user-images.githubusercontent.com/37966987/203667767-ec3787ca-6f7d-4454-9047-c9bed94c875f.png)

![image](https://user-images.githubusercontent.com/37966987/203667783-e37dc67e-d2f3-42c7-924f-7f80996769b8.png)

![image](https://user-images.githubusercontent.com/37966987/203667790-db573012-1665-4e49-92a4-9673f547855d.png)

![image](https://user-images.githubusercontent.com/37966987/203667800-5207e0e9-abe6-417f-a6be-1a5140dc8aa5.png)

![image](https://user-images.githubusercontent.com/37966987/203667807-d57966e5-a476-48eb-9b21-4bb80d4de402.png)

![image](https://user-images.githubusercontent.com/37966987/203667814-54cd6c45-40d8-4fea-8f07-7ea1cefab109.png)

Podemos ver que el dataframe quedó guardado en S3 en ambos formatos.
![image](https://user-images.githubusercontent.com/37966987/203668256-a618f028-d4e6-4d2f-8363-f20078c54140.png)

## REFERENCIAS
https://github.com/st0263eafit/st0263-2022-2/

#### versión README.md -> 1.0 (2022-agosto)
