# PRA1: Web Scraping Stock Index Data
#### Neil Cotie (trabajo individual)
## Descripci�n del proyecto
Esta pr�ctica se ha realizado por la asignatura *Tipolog�a y ciclo de vida de los datos*, dentro del curso del *M�ster en Ciencia de Datos* de la Universitat Oberta de Catalunya.

El c�digo implementa un web scraper para recoger un conjunto predefinido de datos diarios de los componentes de un �ndice burs�til especificado por el usuario, dentro de un rango limitado de �ndices suizos, disponibles en las p�ginas del mercado suizo, https://www.six-group.com/en/products-services/the-swiss-stock-exchange.html.  De momento es posible usarlo con los �ndices SMI, SMI-MID, SLI, SPI-20, y el SXI-Switzerland-Sustainability-25.

Cuando se ejecuta por un �ndice en concreto, el c�digo busca las acciones componentes del �ndice, y colecciona los datos para cada acci�n.

Este pensado ser utilizado de forma diaria, programado a ejecutar regularmente de forma autom�tica, as� coleccionando datos a lo largo del tiempo.  Esos datos podr�an ser �tiles para hacer an�lisis de series temporales, y/o monitorizar cambios temporales en los �ndices y sus componentes, tras una colecci�n adecuada de datos.

Los datos recogidos se guardan en formato CSV, con una primera l�nea cabecera con nombres de columnas. 

El c�digo ha sido escrito siguiendo los principios de programaci�n orientada a objetos, en Python.
## Ficheros del c�digo
* main.py: programa principal, llamado al ejecutar el c�digo, controlador de la ejecuci�n 
* Classes/StockIndex.py: implementa la clase *StockIndex*, representando un �ndice burs�til.
* Classes/Stock.py: implementa la clase *Stock*, representando una acci�n en particular, miembro/componente de un �ndice burs�til.
* Classes/CSV.py: implementa la clase *CSV*, representando un fichero guardando datos de las acciones componentes del �ndice, en formato *CSV*.
## Otros Ficheros
* doc/Class diagram.dia: diagrama UML del dise�o del c�digo
* doc/PRA1_ncotie.pdf: documento m�s detallado sobre la pr�ctica 
* Logfiles/SMI_scraped_data.csv:  muestra de datos CSV




## Entorno
El c�digo utiliza Firefox como navegador, y necesita un *driver* �geckodriver� instalado en el sistema operativo, disponible en https://github.com/mozilla/geckodriver/releases/, con m�s informaci�n en https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/firefox.html.
## Uso del Scraper
La llamada *command-line* al programa tiene que ser seguido por dos argumentos, el primero el nombre del �ndice, el segundo �True� o �False� para indicar si est� permitido coleccionar datos mientras el mercado sigue abierto.  El caso normal estar�a �False�, por querer esperar hasta que el d�a se ha terminado.
## Zenodo
El fichero de muestra en formato CSV tambi�n se encuentra en https://doi.org/10.5281/zenodo.5654517.

