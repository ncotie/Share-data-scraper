# PRA1: Web Scraping Stock Index Data
#### Neil Cotie (trabajo individual)
## Descripción del proyecto
Esta práctica se ha realizado por la asignatura *Tipología y ciclo de vida de los datos*, dentro del curso del *Máster en Ciencia de Datos* de la Universitat Oberta de Catalunya.

El código implementa un web scraper para recoger un conjunto predefinido de datos diarios de los componentes de un índice bursátil especificado por el usuario, dentro de un rango limitado de índices suizos, disponibles en las páginas del mercado suizo, https://www.six-group.com/en/products-services/the-swiss-stock-exchange.html.  De momento es posible usarlo con los índices SMI, SMI-MID, SLI, SPI-20, y el SXI-Switzerland-Sustainability-25.

Cuando se ejecuta por un índice en concreto, el código busca las acciones componentes del índice, y colecciona los datos para cada acción.

Este pensado ser utilizado de forma diaria, programado a ejecutar regularmente de forma automática, así coleccionando datos a lo largo del tiempo.  Esos datos podrían ser útiles para hacer análisis de series temporales, y/o monitorizar cambios temporales en los índices y sus componentes, tras una colección adecuada de datos.

Los datos recogidos se guardan en formato CSV, con una primera línea cabecera con nombres de columnas, y en formato JSON. 

El código ha sido escrito siguiendo los principios de programación orientada a objetos, en Python.
## Ficheros del código
* main.py: programa principal, llamado al ejecutar el código, controlador de la ejecución 
* Classes/StockIndex.py: implementa la clase *StockIndex*, representando un índice bursátil.
* Classes/Stock.py: implementa la clase *Stock*, representando una acción en particular, miembro/componente de un índice bursátil.
* Classes/CSV.py: implementa la clase *CSV*, representando un fichero guardando datos de las acciones componentes del índice, en formato *CSV*.
* Classes/JSON.py: parecido a CSV.py pero en formato *JSON*.
## Otros Ficheros
* doc/Class diagram.dia: diagrama UML del diseño del código
* doc/PRA1_ncotie.pdf: documento más detallado sobre la práctica 
* Logfiles/SMI_scraped_data.csv:  muestra de datos CSV
* Logfiles/SMI_scraped_data.json: muestra de datos JSON




## Entorno
El código utiliza Firefox como navegador, y necesita un *driver* “geckodriver” instalado en el sistema operativo, disponible en https://github.com/mozilla/geckodriver/releases/, con más información en https://www.selenium.dev/selenium/docs/api/javascript/module/selenium-webdriver/firefox.html.
## Uso del Scraper
La llamada *command-line* al programa tiene que ser seguido por dos argumentos, el primero el nombre del índice, el segundo “True” o “False” para indicar si está permitido coleccionar datos mientras el mercado sigue abierto.  El caso normal estaría “False”, por querer esperar hasta que el día se ha terminado.
## Zenodo
El fichero de muestra en formato CSV también se encuentra en https://doi.org/10.5281/zenodo.5654517.

