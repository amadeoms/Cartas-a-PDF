# Cartas-a-PDF
Utiliza imágenes frontales y posteriores para crear cartas, añadiéndolas en varios archivos PNG o un único PDF para simplificar la impresión.

Input:
- Carpeta cards_front para almacenar todas las imágenes que se usarán como parte frontal de la carta.
- Carpeta cards_back para almacenar todas las imágenes que se usarán como reverso de la carta.
- Las imágenes frontales deben seguir el formato "start_type_number.format"
- Las imágenes posteriores deben seguir el formato "start_type_back.format"


variables necesarias que hay que alterar según tus parámetros:
-  dpi: indicar el DPI de tu impresora para obtener el tamaño de la imagen final en píxeles.
-  format: Formato de las imágenes, en String (en mi caso, ".png")
-  start: Inicio/nombre común que poseerán todas las cartas (en mi caso, "dq")
-  a3_width_in, a3_height_in: tamaño de la imagen en pulgadas (en el caso añadido, el tamaño de un A3: 11.69,16.54)

Output:
Carpeta llamada output_pages, que posee
- PNGs llamados "page_number_front", donde cada uno contiene el máximo de cartas frontales que caben dentro del tamaño indicado.
- PNGs llamados "page_number_back", donde cada uno contiene la carta posterior correspondiente con su frontal.
  A primera vista parece que está en orden inverso, pero hay que recordar que al estar "detrás" de la carta frontal, deben de estar al revés.
- PDF compuesto de todas los PNGs generados y en orden.
