# Info de la materia: ST0263 Tópicos Especiales en Telemática
#
# Estudiante(s): Camila Mejia Muñoz, cmejiam10@eafit.edu.co

# Profesor: Edwin Nelson Montoya Munera, emontoya@eafit.edu.co
#
# Laboratorio 4
#
# 1. Breve descripción de la actividad
Desplegar un CMS wordpress utilizando contenedores, con un nombre de dominio y certificado SSL. Se utiliza un nginx tanto como frontend para el dominio y certificado y un balanceador de cargas para la capa de aplicación del wordpress. 

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Hacer la implementación el Google GCP.
Evolucionar la aplicación original (lab3) dockerizada monolítica en varios nodos que mejore la disponibilidad de esta aplicación.
Implementar un balanceador de cargas basado en nginx que reciba el tráfico web https de Internet con múltiples instancias de procesamiento.
Tener al menos 2 instancias de procesamiento detrás del balanceador de cargas.
Tener al menos 1 instancia de bases de datos mysql
Tener al menos 1 instancia de archivos distribuidos en NFS



## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)
No me corre con el dominio y realmente no encuntro solucion.
El usuario se supone que debe acceder a la URL https://lab4.cmejiam10.tk desde cualquier browser pero no ingresa.
Ingresa mediante la ip directa http://35.184.26.4/
el ingreso

# 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.
Se usaron contenedores Docker para la instalación de Wordpress, Nginx y MySQL en la máquina virtual.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, 

## IP o nombres de dominio

IP elástica: 35.208.215.54
Nombre de dominio: lab4.cmejiam10.tk
Dominio con certificación SSL: https://lab4.cmejiam10.tk

## detalles técnicos

GCP: se usó para desplegar una máquina virtual.
Docker: se usó un contenedor para desplegar un wordpress.
Cerbot: se usó para asiganar un certificado SSL válido.
Let's Encrypt: se usó para asiganar un certificado SSL válido.
Nginx: se usó como servidor web HTTP.
NFS kernel server: se usó para hacer el servidor NFS.
NFS common: se usó para vincular los wordpress con el servidor NFS.

## Descripcion y como se creo el proyecto.

Se crearon 5 VM en GCP. Asi:
![image](https://user-images.githubusercontent.com/37966987/197866220-da8e2f6a-634a-4075-820c-007b2ca41eb9.png)
Se configuro la IP elastica para cada una de las VM. Asi:
![image](https://user-images.githubusercontent.com/37966987/197867016-5987b2c9-da18-4baf-a81c-54fa58a39fef.png)
Se configuraron los registros DNS en GCP:
Ya la zona estaba creada solo se edito y organizo para este laboratorio.
![image](https://user-images.githubusercontent.com/37966987/197867248-670b6510-86d1-4533-95e6-c72ce16adcc9.png)

## Detalle del desarrolo

# Balanceador de cargas (lb)
Instalamos certbot, letsencrypt y nginx
```
sudo apt update
sudo apt install snapd
sudo snap install certbot --classic
sudo apt install letsencrypt -y
sudo apt install nginx -y

```
Configuramos el archivo nginx.conf.

```
sudo nano /etc/nginx/nginx.conf
```

Agregamos este contenido

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

```
Se guarda y se continua con lo siguiente
```
sudo mkdir -p /var/www/letsencrypt
sudo nginx -t
sudo service nginx reload
```

Solicitud de los certificados SSL:
```
sudo letsencrypt certonly -a webroot --webroot-path=/var/www/letsencrypt -m cmejiam10@eafit.edu.co --agree-tos -d lab4.cmejiam10.tk
sudo certbot --server https://acme-v02.api.letsencrypt.org/directory -d *.cmejiam10.tk --manual --preferred-challenges dns-01 certonly

```


Se crean las carpetas en el balanceador y los certificados.


```
mkdir /home/cmejiam10/nginx
mkdir /home/cmejiam10/nginx/ssl

```

Hacer los registros:

```
sudo su
cp /etc/letsencrypt/live/lab4.cmejiam10.tk/* /home/cmejiam10/nginx/ssl/
cp /etc/letsencrypt/live/cmejiam10.tk/* /home/cmejiam10/nginx/ssl/
exit

```

Instalacion de docker, docker-compose y git:
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
sudo apt install git -y
```
Corriendo docker:

```
git clone https://github.com/st0263eafit/st0263-2022-2.git
cd st0263-2022-2/docker-nginx-wordpress-ssl-letsencrypt
sudo cp ssl.conf /home/cmejiam10/wordpress
cd

```
Se crean 2 archivos:

```
cd nginx
sudo touch docker-compose.yml
sudo touch nginx.conf

```
Ingresamos al archivo y agregamos el contenido:
```
sudo nano nginx.conf
```
CONTENIDO:

```
worker_processes auto;
error_log /var/log/nginx/error.log;
pid /run/nginx.pid;

events {
  worker_connections  1024;  ## Default: 1024
}
http {
  upstream loadbalancer{
    server 10.128.0.16:80 weight=5;
    server 10.128.0.17:80 weight=5;
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

Ingresamos al docker-compose.yml:
```
sudo nano docker-compose.yml
```
Agregamos el siguiente contenido:
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

Detenemos nginx:

```
ps ax | grep nginx
netstat -an | grep 80
sudo systemctl disable nginx
sudo systemctl stop nginx
```

Inciamos Docker:
```
cd /home/cmejiam10/nginx
docker-compose up --build -d
```

# Servidor de Base de Datos (db)


Instalamos docker y docker-compose:
```
sudo apt install docker.io -y
sudo apt install docker-compose -y
```

Creamos un directorio para el docker container y accedemos a este:
```
mkdir docker
cd docker
```
Creamos dos archivos de configuración:

```
sudo touch Dockerfile
sudo touch docker-compose.yaml
```
Ingresamos al Dockerfile y le ponemos el CONTENIDO:
```
sudo nano Dockerfile
```
CONTENIDO
```
FROM mysql:8.0
```
Ingresamos al docker-compose.yaml Y le ponemos el CONTENIDO:
```
sudo nano docker-compose.yaml
```
CONTENIDO
```
version: "3.7"
services:
  mysql:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: dbserver
    restart: always
    ports:
      - 3306:3306
    environment:
      MYSQL_ROOT_PASSWORD: "1234"
      MYSQL_DATABASE: "wordpressdb"
    volumes:
      - ./schemas:/var/lib/mysql:rw
volumes:
  schemas: {}
```
Ponemos a funcionar docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker cmejiam10
sudo reboot
```

Corremos el contenedor docker y accedemos a MySQL:
```
cd docker
sudo docker-compose up --build -d
sudo docker exec -it dbserver mysql -p
```
Creamos la base de datos:
```
CREATE DATABASE wpdb;
```

```
CREATE USER 'cmejiam10' IDENTIFIED BY '1234';
GRANT ALL PRIVILEGES ON *.* TO 'cmejiam10'@'%';
exit
```
## Servidor NFS (nfs)

Instalamos nfs-kernel-server:
```
sudo apt update
sudo apt install nfs-kernel-server
sudo apt install ufw
```
Crear carpeta para compartir archivos en el servidor NFS:
```
sudo mkdir -p /mnt/nfs_share
```
Entramos al archivo /etc/exports:
```
sudo nano /etc/exports
```
Agregamos la siguiente linea al final :
```
/mnt/nfs_share 10.128.0.0/20(rw,sync,no_subtree_check)
```
Exportamos el nuevo NFS:
```
sudo exportfs
```
Actualizamos las reglas de firewall:
```
sudo systemctl restart nfs-kernel-server
```

## Servidores de Wordpress (w1 y w2)

El siguiente paso a paso se debe realizar para las dos instancias.
Instalamos nfs-common, docker y docker-compose:
```
sudo apt update
sudo apt install nfs-common -y
sudo apt install docker.io -y
sudo apt install docker-compose -y
```
Entramos al archivo /etc/fstab:
```
sudo nano /etc/fstab
```
Agregamos la siguiente línea:
```
10.128.0.32:/mnt/nfs_share /var/www/html nfs auto 0 0
```
Hacemos la conexión al servidor NFS:
```
sudo mount -a
```

Habilitamos docker:
```
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -a -G docker dxninob
sudo reboot
```
Creamos un directorio para el docker container:
```
mkdir docker
```
Creamos un archivo docker-compose.yaml e ingresamos:
```
sudo touch docker-compose.yaml
sudo nano docker-compose.yaml
```
Ingresamos el siguiente contenido:
```
version: '3.7'
services:
  wordpress:
    container_name: wordpress
    image: wordpress:latest
    restart: always
    environment:
      WORDPRESS_DB_HOST: 10.128.0.13:3306
      WORDPRESS_DB_USER: cmejiam10
      WORDPRESS_DB_PASSWORD: 1234
      WORDPRESS_DB_NAME: wpdb
    volumes:
      - /var/www/html:/var/www/html
    ports:
      - 80:80
volumes:
  wordpress:
```
Corremos el contenedor:
```
sudo docker-compose up --build -d
```
## USARLO
El usuario se supone que debe acceder a la URL https://lab4.cmejiam10.tk desde cualquier browser pero no ingresa.
Ingresa mediante la ip directa http://35.184.26.4/

## PANTALLAZOS DE LO REALIZADO

CERTFICADOS
![image](https://user-images.githubusercontent.com/37966987/197867526-433f2819-ac87-495e-9724-f935ce7e6630.png)

PAGINA
![image](https://user-images.githubusercontent.com/37966987/197867703-166d2d4e-75f5-46c6-bf4a-24eb3bef1d7c.png)

