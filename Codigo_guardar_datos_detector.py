import serial # Importa la librería pyserial, que permite comunicarse con dispositivos por puerto serie (USB)

puerto = 'COM3' # Puerto donde está conectado el detector (en Windows suele ser COM3, COM4, etc.)
baud_rate = 9600 # Velocidad de comunicación en baudios; debe coincidir con la del detector
archivo_salida = 'datos_detector.txt' # Nombre del archivo donde se guardarán los datos

try:
    # Abre la conexión serie con el detector
    ser = serial.Serial(puerto, baud_rate, timeout=1)

    # Mensaje informativo para el usuario
    print(f'Conectado a {puerto} a {baud_rate} baudios')

    # Abre el archivo de salida en modo escritura ('w' = write)
    with open(archivo_salida, 'w') as f:
        print(f'Archivo {archivo_salida} abierto para escribir.')
        print('Guardando datos. Presiona Ctrl+C para detener.')

        # Bucle infinito para leer continuamente datos del detector
        while True:

            # Comprueba si hay datos disponibles en el buffer del puerto serie
            if ser.in_waiting > 0:

                # Lee una línea del puerto serie
                linea = ser.readline() # lee hasta encontrar salto de línea

                # Convierte los bytes recibidos a texto UTF-8
                linea = linea.decode('utf-8', errors='ignore').strip()

                # Muestra los datos en la terminal
                print(f'{linea}')

                # Escribe la línea en el archivo de salida
                f.write(linea + '\n')

                # Fuerza a guardar inmediatamente en el archivo
                # (importante para no perder datos si el programa se cierra)
                f.flush()

# Este bloque se ejecuta cuando el usuario pulsa Ctrl+C
except KeyboardInterrupt:
    print('Guardado detenido por el usuario.')

# Este bloque captura cualquier otro error (puerto incorrecto, detector desconectado, etc.)
except Exception as e:
    print(f'Error: {e}')

# Este bloque siempre se ejecuta al final
finally:

    # Comprueba si la variable ser existe y si el puerto sigue abierto
    if 'ser' in locals() and ser.is_open:

        # Cierra el puerto serie correctamente
        ser.close()

        # Mensaje final informando de que la conexión se cerró
        print('Puerto serie cerrado.')
