# Barcode Batch Extractor & ASCII Decoder

## Contexto del Proyecto
Herramienta de extracción forense y automatización desarrollada para la resolución de un reto de Blue Team Labs.

### El Escenario y la Trampa (El Problema)
El incidente presentaba un directorio contaminado con 9374 imágenes etiquetadas numéricamente (ej. 1333.png, 1334.png).
La trampa cognitiva del reto es inducir al analista a intentar "coser" (stitch) visualmente estos recortes asumiendo que forman un único código de barras gigante (lo cual generaría un lienzo inútil de más de 1.5 millones de píxeles).

La realidad del artefacto: Cada imagen es un código de barras 1D independiente que esconde un valor numérico específico. El objetivo no es la manipulación de imágenes, sino la extracción masiva en lote (Batch Decoding).

### Arquitectura de la Solución
El script (ensamblador.py) está diseñado para ignorar el ruido y operar de forma secuencial y determinista en tres fases:

- Filtrado Estricto y Ordenamiento Lógico: Utiliza Expresiones Regulares (re) para ignorar archivos que no pertenezcan a la secuencia numérica. Ordena los archivos matemáticamente (del 1 al 9374) para evitar la corrupción de datos que generaría el ordenamiento alfabético del sistema operativo.

- Extracción con Contingencia (Fallback Forense): Itera sobre cada imagen utilizando pyzbar. Si la lectura nativa falla por artefactos o falta de contraste, el script no se detiene; aplica una binarización estricta (blanco y negro puro) en memoria mediante Pillow y fuerza una segunda lectura.

- Desofuscación (Decimal a ASCII): Los datos extraídos forman una cadena gigante de valores en ASCII Decimal. El script divide matemáticamente estos bloques, los convierte a caracteres de texto plano, y utiliza una nueva regla Regex para cazar automáticamente el formato de la flag (SBT{...}) dentro del muro de texto resultante.

### Autopsia del Error: La Corrupción de la Muestra Cruda
Durante la primera iteración del desarrollo, se cometió un error crítico de manipulación de evidencia: se inyectó un espacio artificial (+ " ") en el código tras leer cada imagen, asumiendo que los valores necesitaban separación.

- El impacto: Los códigos de barras ya contenían sus propios caracteres de espacio codificados. Al inyectar ruido adicional, el script rompió números íntegros (ej. el Decimal 65, que equivale a la letra 'A') transformándolos en dígitos aislados ("6 5"). Esto provocó que la traducción ASCII arrojara símbolos de la tabla extendida (♠♣♥☻) en lugar de texto plano.

Nunca inyectar datos arbitrarios en una extracción cruda a menos que se comprenda absoluta y milimétricamente el esquema de codificación subyacente.

## Requisitos y Uso
### Dependencias
Asegúrate de tener Python 3.x instalado en una arquitectura de 64 bits. Las librerías necesarias son:

```pip install Pillow pyzbar```

Coloca el script en el mismo directorio (o especifica la ruta) donde se alojan las imágenes a procesar.

```python ensamblador.py [ruta_al_directorio]```

Si no se pasa ningún argumento, el script asumirá el directorio actual .
