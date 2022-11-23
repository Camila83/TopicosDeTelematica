# info de la materia: ST0263 Topicos especiales en telematica
#
# Estudiante(s): Camila Mejia Muñoz, cmejiam10@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# <para borrar: EL OBJETIVO DE ESTA DOCUMENTACÍON ES QUE CUALQUIER LECTOR CON EL REPO, EN ESPECIAL EL PROFESOR, ENTIENDA EL ALCANCE DE LO DESARROLLADO Y QUE PUEDA REPRODUCIR SIN EL ESTUDIANTE EL AMBIENTE DE DESARROLLO Y EJECUTAR Y USAR LA APLICACIÓN SIN PROBLEMAS>
# <nombre del proyecto, lab o actividad>
#
# 1. breve descripción de la actividad
Realizar una aplicación monolítica no escalable desplegada en AWS, con nombre de dominio y certificado SSL válido.

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)


Despliegue de la aplicación Moodle con Docker y nginx en la instancia de AWS. Asignación de un dominio propio con certificado SSL válido con Let's Encrypt.
Implementación de un balanceador de cargas con Docker y nginx en una instancia de AWS, en la capa de aplicación del Moodle.
Implementación de un servidor de base de datos con Docker en una instancia de AWS, conectado al Moodle.
Implementación de un servidor para archivos con Docker en una instancia de AWS, conectado al Moodle.


## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Realizar una aplicación monolítica no escalable desplegada en DCA, con nombre de dominio y certificado SSL válido.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.


Se utilizaron contenedores en Docker para la ejecución del proyecto, nginx y MariaDB.

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

#Servidor de base de datos
1. Para crear el servidor de base de datos se conecta a la instancia de AWS de la maquina asignada.
2. Para comenzar se ejecutan los siguientes comandos:

```
sudo apt update
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```
3. Clonamos el repositorio donde se encuentran los scripts.
```
git clone REPOSITORIOOOOCAREMONDA
```
4. Se crea un repositorio para el docker container y accedemos a el.
```
sudo mkdir /home/ubuntu/mysql
```
5. Copiamos en este directorio los archivos del github.
```
cd ST0263-P2/mysql
sudo cp docker-compose.yml /home/ubuntu/mysql

```

6. Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker ubuntu
```
7. Corremos el contenedor docker y accedemos a MySQL:

```
cd /home/ubuntu/mysql
sudo docker-compose up

```

# Servidores MOODLE

1. Para crear el servidor de moodle se conecta a la instancia de AWS de la maquina asignada.
2. Para comenzar se ejecutan los siguientes comandos:

```
sudo apt update
sudo apt install nfs-common -y
```
3. Ingresamos al archivo /etc/fstab:
```
sudo nano /etc/fstab
```
Agregamos el siguiente comando al archivo, teniendo en cuenta que la dirección IP es la correspondiente a la instancia asignada al servidor NFS:
```
IP.IP.IP:/mnt/nfs_share /var/www/html nfs auto 0 0
```
4. Se conecta al servidor con el NFS
```
sudo mount
```
5. Se instala docker.io, docker-compose y git
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```
6. Se clona el repositorio
```
git clone https://github.com/dxninob/ST0263-P2.git

```
7. Se crea un repositorio para el docker container y accedemos a el.

```
sudo mkdir /home/ubuntu/moodle

```
8. Copiamos en este directorio los archivos del github.

```
cd ST0263-P2/moodle
sudo cp docker-compose.yml /home/ubuntu/moodle

```
9. Ponemos a funcionar docker:

```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker ubuntu
```
10. Corremos el contenedor docker y accedemos a MySQL:
```
cd /home/ubuntu/moodle
sudo docker-compose up 

```

#4. Balanceador de cargas

1. Para crear el balanceador de cargas se conecta a la instancia de AWS dando click en la opción SSH de la máquina asignada a este mismo.

2. Se instala certbot, letsencrypt y nginx. Para esto, se ejecutan los siguientes comandos:

```
sudo apt update  
sudo apt install snapd  
sudo snap install certbot --classic  
sudo apt install letsencrypt -y  
sudo apt install nginx -y

```
3. Se ingresa al archivo nginx.conf y se configura:

```
sudo nano /etc/nginx/nginx.conf

```
4. Se reemplaza todo el contenido por lo siguiente:


```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
    worker_connections  1024;  ## Default: 1024
}
http {
    server {
        listen  80 default_server;
        server_name _;
        location ~ /\.well-known/acme-challenge/ {
            allow all;
            root /var/www/letsencrypt;
            try_files $uri = 404;
            break;
        }
    }
}

```
5. Se guarda la configuración de nginx con los siguientes comandos:


```
sudo mkdir -p /var/www/letsencrypt
sudo nginx -t
sudo service nginx reload

```

6. Para pedir los certificados SSL se ejecutan los siguientes comandos:

```
sudo letsencrypt certonly -a webroot --webroot-path=/var/www/letsencrypt -m asarangog@eafit.edu.co --agree-tos -d lab4.asarangog.tk
sudo certbot --server https://acme-v02.api.letsencrypt.org/directory -d *.asarangog.tk --manual --preferred-challenges dns-01 certonly

```

7. Este último comando nos va a generar el código que debemos ingresar en el registro TXT del archivo de zona en AWS.

Creamos carpetas para los certificados:

```
mkdir /home/asarangog/nginx
mkdir /home/asarangog/nginx/ssl

```
8. Para hacer los registros se ejecutan los siguientes comandos:

```
sudo su
cp /etc/letsencrypt/live/lab4.asarangog.tk/* /home/asarangog/nginx/ssl/
cp /etc/letsencrypt/live/asarangog.tk/* /home/asarangog/nginx/ssl/
exit

```
9. Se instala docker, docker-compose y git con los siguientes comandos:

```
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y

```
10. Ponemos a funcionar docker:

```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker asarangog
sudo reboot

```
11. Clonamos el repositorio del curso de donde usaremos un archivo de configuración:

```
git clone https://github.com/st0263eafit/st0263-2022-2.git
cd st0263-2022-2/docker-nginx-wordpress-ssl-letsencrypt
sudo cp ssl.conf /home/asarangog/wordpress
cd

```
12. Ingresamos a la carpeta y creamos los siguientes archivos:

```
cd nginx
sudo touch docker-compose.yml
sudo touch nginx.conf

```
13. Entramos al archivo nginx.conf con el siguiente comando:

```
sudo nano nginx.conf

```
14. Añadimos el siguiente contenido, teniendo en cuenta que las direcciones IP de las líneas 10 y 11 corresponden a las instancias del moodle 1 y 2:

```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
  worker_connections  1024;  ## Default: 1024
}
http {
  upstream loadbalancer{
    server 10.128.0.56:80 weight=5;
    server 10.128.0.57:80 weight=5;
  }
  server {
    listen 80;
    listen [::]:80;
    server_name _;
    rewrite ^ https://$host$request_uri permanent;
  }
  server {
    listen 443 ssl http2 default_server;
    listen [::]:443 ssl http2 default_server;
    server_name _;
    # enable subfolder method reverse proxy confs
    #include /config/nginx/proxy-confs/*.subfolder.conf;
    # all ssl related config moved to ssl.conf
    include /etc/nginx/ssl.conf;
    client_max_body_size 0;
    location / {
      proxy_pass http://loadbalancer;
      proxy_redirect off;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Host $host;
      proxy_set_header X-Forwarded-Server $host;
      proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
}
```
13. Ingresamos al archivo docker-compose.yml con el siguiente comando:
```
sudo nano docker-compose.yml
```
14. Añadimos el siguiente contenido:
```
version: '3.1'
services:
  nginx:
    container_name: nginx
    image: nginx
    volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl
    - ./ssl.conf:/etc/nginx/ssl.conf
    ports:
    - 80:80
    - 443:443
```
15. Detenemos nginx con los siguientes comandos:
```
ps ax | grep nginx
netstat -an | grep 80
sudo systemctl disable nginx
sudo systemctl stop nginx
```
16. Por último, iniciamos Docker:
```
cd /home/asarangog/nginx
docker-compose up
```
## detalles técnicos

Se usó AWS para desplegar las máquinas virtuales.
Se usaron contenedores de Docker.
Se usó Cerbot y Let's Encrypt para asignar un certificado SSL válido.
Se usó Nginx como servidor web HTTP.
Se usó NFS kernel server para hacer el servidor NFS.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
## opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
## 
## opcionalmente - si quiere mostrar resultados o pantallazos 

# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.
Docker, Nginx, MariaDB y AWS.
# IP o nombres de dominio en nube o en la máquina servidor.

## descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)

## como se lanza el servidor.

## una mini guia de como un usuario utilizaría el software o la aplicación

## opcionalmente - si quiere mostrar resultados o pantallazos 

# 5. otra información que considere relevante para esta actividad.

# referencias:
<debemos siempre reconocer los créditos de partes del código que reutilizaremos, así como referencias a youtube, o referencias bibliográficas utilizadas para desarrollar el proyecto o la actividad>
## sitio1-url 
## sitio2-url
## url de donde tomo info para desarrollar este proyecto

#### versión README.md -> 1.0 (2022-agosto)