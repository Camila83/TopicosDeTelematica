# info de la materia: ST0263 Topicos especiales en telematica
#
# Estudiante(s): Camila Mejia Muñoz, cmejiam10@eafit.edu.co
#
# Profesor: Edwin Nelson Montoya Munera,  emontoya@eafit.edu.co

# Laboratorio 3
#
# 1. breve descripción de la actividad

Creacion de un dominio certificado SSL, desplegado en la app wordpress utilizando wordpress mediante Docker en una instancia GCP

## 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se cumplio con todos los aspecto de despliegue correctamente para el funcionamiento de la pagina web mediante wordpress, asignando el dominio con certificado SSL valido con Let's Encrypt

## 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Todos los aspectos se cumplieron correctamente.

# 2. información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Docker fue utilizado para la ejecucion del laboratorio.

# 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

## detalles del desarrollo.
1. Se crea una instancia en GCP
2. Se asigna una direccion IP elastica externa.
3. se asignaron el conjunto de registros GCP con sus respectivos nombres.
4. Instalacion de nginx, letsencrypt y cerbot.
6. se realizo la configuracion adecuada con el archivo "nginx.conf"
7. se clono el repositorio donde los archivos se usan y configuran.
8. Se inicializo el servidor de wordpress.


# 4. Descripción del ambiente de EJECUCIÓN (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

# IP o nombres de dominio en nube o en la máquina servidor.

IP elastica: 34.122.150.182
Nombre de dominio: cmejiam10.tk
Dominio con certificado SSL: https://www.cmejiam10.tk/

## una mini guia de como un usuario utilizaría el software o la aplicación
Para acceder solo debe copiar el siguiente link en el navegador https://www.cmejiam10.tk

# 5. otra información que considere relevante para esta actividad.

# referencias:
https://github.com/st0263eafit/st0263-2022-2/tree/main/docker-nginx-wordpress-ssl-letsencrypt

