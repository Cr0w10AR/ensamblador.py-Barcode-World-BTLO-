import os
import sys
import re
from PIL import Image
from pyzbar.pyzbar import decode

def main(directory='.'):
    #Filtro estricto
    patron_archivo = re.compile(r'^(\d+)\.(png|jpg|jpeg|bmp)$', re.IGNORECASE)
    archivos_validos = []

    for f in os.listdir(directory):
        match = patron_archivo.match(f)
        if match:
            numero = int(match.group(1))
            archivos_validos.append((numero, f))

    if not archivos_validos:
        print("[-] ERROR: No hay imágenes válidas en el directorio.")
        return

    archivos_validos.sort(key=lambda x: x[0])
    print(f"[*] Procesando {len(archivos_validos)} códigos de barras individuales...")

    flag_extraida = ""
    fallos = 0

    # 2. Extracción Secuencial
    for _, fname in archivos_validos:
        ruta = os.path.join(directory, fname)
        try:
            with Image.open(ruta) as img:
                objetos = decode(img)
                
                if objetos:
                    flag_extraida += objetos[0].data.decode('utf-8')
                else:
                    # Intento de rescate en Blanco y Negro
                    img_bw = img.convert('L').point(lambda x: 0 if x < 128 else 255, '1')
                    objetos_reintento = decode(img_bw)
                    
                    if objetos_reintento:
                        flag_extraida += objetos_reintento[0].data.decode('utf-8')
                    else:
                        fallos += 1
                        
        except Exception as e:
            fallos += 1

    #Resultado Final y Decodificación ASCII
    print("\n" + "="*50)
    print(f"[+] PROCESO TERMINADO. Fallos de lectura: {fallos}")
    
    try:
        # Limpiamos espacios extra, dividimos y convertimos cada número a su carácter ASCII
        numeros = flag_extraida.strip().split()
        texto_decodificado = ''.join(chr(int(num)) for num in numeros)
        
        print("\n[+] TEXTO PLANO DECODIFICADO:")
        print(texto_decodificado)
        
        # Cazamos la flag automáticamente dentro del texto
        match_flag = re.search(r'(B4rc0d3_[A-Za-z0-9_-]+)', texto_decodificado)
        if match_flag:
            print("\n[!] FLAG DETECTADA CON ÉXITO:")
            print(f">>> {match_flag.group(0)} <<<")
            
    except Exception as e:
        print(f"[-] Error al intentar decodificar el ASCII: {e}")

    print("="*50 + "\n")

if __name__ == '__main__':
    ruta_dir = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(ruta_dir)  
