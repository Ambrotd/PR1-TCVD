# PR1-TCVD
## Descripción
Práctica realiza como parte del ;áster en Ciencia de Datos de la UOC, en la que se ha realizado un scraper para obtener los anuncios de venta en el portal inmobiliario idealista.

## Instalación 
Instalamos los paquetes
``pip3 install -r requiremtents.txt``

El código ha sido creado para usar nordvpn para rotar entre vpns cuando idealista nos bloquea por bot.
En caso de no querer usar nordvpn cambiar USENORDVPN a false. 

Para que funcione hay que usar el driver correspondiente a nuestra versión de chrome para 
que funcione selenium. En este caso el que se incluye es el de chrome 95 para windows.


## Miembros del equipo
La práctica ha sido realizada por Daniel Sánchez Ambite

## Descripción de ficheros

- main.py: contiene el código base del programa con el que se realiza el proceso de scraping. Hay 3 funciones principales una que obtiene las zonas, otra que saca los ID de los anuncios
en cada una de las zonas y por último otra que obtiene los datos de cada anuncio.
- helpers.py: contiene funciones secundarias, para obtener los headers, uso de proxies (aunque hace falta una lista de proxies buena y no gratuita por lo que al final se optó por el uso de VPN)
y las funciones para guardar el csv.
- csv/madrid.csv: es el dataset resultante con la lista de inmuebles a la venta en la Comunidad de Madrid
- driver/chromedriver.exe: es el driver de windows para chrome 95 para que funcione selenium.

## Dataset

El fichero madrid.csv ha sido subido a zenodo con DOI 10.5281/zenodo.5635678 acesible en https://zenodo.org/record/5635678