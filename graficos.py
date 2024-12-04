import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
# Función para generar el gráfico del MRU
def generarGraficoPosFinal_MRU(x0, v, t_max, archivo_salida="grafico.png"):
    """
    Genera una imagen con el gráfico del MRU y la guarda como un archivo PNG.
    :param x0: Posición inicial en el tiempo t=0.
    :param v: Velocidad constante.
    :param t_max: Tiempo máximo para graficar.
    :param archivo_salida: Nombre del archivo de salida donde se guardará la imagen.
    """
    # Aseguramos que t_max sea un entero
    t_max = int(t_max)

    # Crear un rango de tiempos
    t = np.linspace(0, t_max, num=t_max + 1)  # Rango de tiempos de 0 a t_max

    # Calcular las posiciones correspondientes
    x = x0 + v * t  # Posición en función de t
    # Crear la figura con tamaño ajustado (por ejemplo, 6x4 pulgadas)
    plt.figure(figsize=(5,4))  # Ajusta el tamaño aquí (anchura, altura) en pulgadas

    # Graficar
    plt.plot(t, x, label='Posición vs Tiempo', color='red', linewidth=2)

    # Etiquetas y título
    plt.title("Gráfico de MRU")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Posición (x)")

    # Etiquetas en los ejes
    plt.xticks(np.arange(0, t_max + 1, step=(t_max/5)))  # Ajustamos las etiquetas del eje x
    plt.yticks(np.arange(min(x), max(x)+1, step=(max(x)/10)))  # Ajustamos las etiquetas del eje y

    # Guardar la imagen generada
    plt.savefig(archivo_salida, format='png')

    # Cerrar el gráfico
    plt.close()

def generarGraficoPosFinal_MRUA(x0, v0, t_max, a,  archivo_salida="graficoPosFinalmrua.png"):
    """
    Genera una imagen con el gráfico del MRUA y la guarda como un archivo PNG.
    :param x0: Posición inicial en el tiempo t=0.
    :param v0: Velocidad inicial.
    :param a: Aceleración constante.
    :param t_max: Tiempo máximo para graficar.
    :param archivo_salida: Nombre del archivo de salida donde se guardará la imagen.
    """
    t_max = int(t_max)
    t = np.linspace(0, t_max, num=t_max + 1)  # Rango de tiempos de 0 a t_max
    x = x0 + v0 * t + 0.5 * a * t**2  # Posición en función de t
    
    # Crear la figura con tamaño ajustado
    plt.figure(figsize=(5, 4))  
    plt.plot(t, x, label="Posición vs Tiempo", color="blue", linewidth=2)

    plt.title("Gráfico de MRUA")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Posición (x)")

    plt.xticks(np.arange(0, t_max + 1, step=(t_max/5)))  # Ajustamos las etiquetas del eje x
    plt.yticks(np.arange(min(x), max(x)+1, step=(max(x)/10)))  # Ajustamos las etiquetas del eje y

    # Guardar la imagen generada
    plt.savefig(archivo_salida, format="png")
    plt.close()

def generarGraficoVelocidadFinal_MRUA(v0, a, t_max, archivo_salida="graficovelocidadmrua.png"):
    """
    Genera una imagen con el gráfico de la Velocidad Final en MRUA y la guarda como un archivo PNG.
    :param v0: Velocidad inicial.
    :param a: Aceleración constante.
    :param t_max: Tiempo máximo para graficar.
    :param archivo_salida: Nombre del archivo de salida donde se guardará la imagen.
    """
    t_max = int(t_max)
    t = np.linspace(0, t_max, num=t_max + 1)  # Rango de tiempos de 0 a t_max
    vf = v0 + a * t  # Velocidad final en función del tiempo
    
    # Crear la figura con tamaño ajustado
    plt.figure(figsize=(5, 4))  
    plt.plot(t, vf, label="Velocidad Final vs Tiempo", color="blue", linewidth=2)

    plt.title("Gráfico de Velocidad Final en MRUA")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Velocidad Final (vf)")

    plt.xticks(np.arange(0, t_max + 1, step=(t_max/5)))  # Ajustamos las etiquetas del eje x
    plt.yticks(np.arange(min(vf), max(vf)+1, step=(max(vf)/10)))  # Ajustamos las etiquetas del eje y

    # Guardar la imagen generada
    plt.savefig(archivo_salida, format="png")
    plt.close()

def generarGraficoVelocidadFinal_CaidaLibre(v0, g, t_max, archivo_salida="graficovelocidadcaidalibre.png"):
    """
    Genera una imagen con el gráfico de la Velocidad Final en Caída Libre y la guarda como un archivo PNG.
    :param v0: Velocidad inicial.
    :param g: Aceleración debida a la gravedad (9.81 m/s² en la Tierra).
    :param t_max: Tiempo máximo para graficar.
    :param archivo_salida: Nombre del archivo de salida donde se guardará la imagen.
    """
    t_max = int(t_max)
    t = np.linspace(0, t_max, num=t_max + 1)  # Rango de tiempos de 0 a t_max
    vf = v0 + g * t  # Velocidad final en función del tiempo
    
    # Crear la figura con tamaño ajustado
    plt.figure(figsize=(5, 4))  
    plt.plot(t, vf, label="Velocidad Final vs Tiempo", color="green", linewidth=2)

    plt.title("Gráfico de Velocidad Final en Caída Libre")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Velocidad Final (vf)")

    plt.xticks(np.arange(0, t_max + 1, step=(t_max/5)))  # Ajustamos las etiquetas del eje x
    plt.yticks(np.arange(min(vf), max(vf)+1, step=(max(vf)/10)))  # Ajustamos las etiquetas del eje y

    # Guardar la imagen generada
    plt.savefig(archivo_salida, format="png")
    plt.close()

def generarImagenFuerzaNeta_Dinamica(m, a, archivo_salida="graficofuerzaneta.png"):
    """
    Genera una imagen con la fórmula y el resultado de la fuerza neta dinámica.
    :param m: Masa del objeto (en kg).
    :param a: Aceleración constante (en m/s²).
    :param t: Tiempo en segundos.
    :param archivo_salida: Nombre del archivo donde se guardará la imagen.
    """
    F = m * a  # Fuerza neta dinámica
    formula = f"F = m * a = {m} * {a} = {F}"  # Fórmula de la fuerza neta

    # Crear una nueva imagen en blanco
    imagen = Image.new('RGB', (400, 100), (255, 255, 255))  # Ancho, Alto y color de fondo blanco
    draw = ImageDraw.Draw(imagen)

    # Usar una fuente por defecto (puedes cambiarla por otra si tienes alguna específica)
    font = ImageFont.load_default()

    # Escribir la fórmula y el resultado en la imagen
    draw.text((10, 10), formula, font=font, fill=(0, 0, 0))  # Coloca el texto en color negro

    # Guardar la imagen generada
    imagen.save(archivo_salida)

def generarImagenPeso_Dinamica(m, g, archivo_salida="graficoPeso.png"):
    W = m * g  
    formula = f"W = m * g = {m} * {g} = {W}" 

    # Crear una nueva imagen en blanco
    imagen = Image.new('RGB', (400, 100), (255, 255, 255))  # Ancho, Alto y color de fondo blanco
    draw = ImageDraw.Draw(imagen)

    # Usar una fuente por defecto (puedes cambiarla por otra si tienes alguna específica)
    font = ImageFont.load_default()

    # Escribir la fórmula y el resultado en la imagen
    draw.text((10, 10), formula, font=font, fill=(0, 0, 0))  # Coloca el texto en color negro

    # Guardar la imagen generada
    imagen.save(archivo_salida)

def generarFriccion_Dinamica(μ, N ,archivo_salida="graficofriccion.png"):
    f = μ * N
    formula = f"f = mu * N = {μ} * {N} = {f}" 

    # Crear una nueva imagen en blanco
    imagen = Image.new('RGB', (400, 100), (255, 255, 255))  # Ancho, Alto y color de fondo blanco
    draw = ImageDraw.Draw(imagen)

    # Usar una fuente por defecto (puedes cambiarla por otra si tienes alguna específica)
    font = ImageFont.load_default()

    # Escribir la fórmula y el resultado en la imagen
    draw.text((10, 10), formula, font=font, fill=(0, 0, 0))  # Coloca el texto en color negro

    # Guardar la imagen generada
    imagen.save(archivo_salida)

def generarGraficoVelocidadAngularFinal_MCUA(ω0, α, t_max, archivo_salida="graficovelocidadangularmcua.png"):
    """
    Genera una imagen con el gráfico de la Velocidad Angular Final en MCUA y la guarda como un archivo PNG.
    :param ω0: Velocidad angular inicial (en radianes por segundo).
    :param α: Aceleración angular (en radianes por segundo al cuadrado).
    :param t_max: Tiempo máximo para graficar.
    :param archivo_salida: Nombre del archivo de salida donde se guardará la imagen.
    """
    t_max = int(t_max)
    t = np.linspace(0, t_max, num=t_max + 1)  # Rango de tiempos de 0 a t_max
    ωf = ω0 + α * t  # Velocidad angular final en función del tiempo
    
    # Crear la figura con tamaño ajustado
    plt.figure(figsize=(5, 4))  
    plt.plot(t, ωf, label="Velocidad Angular Final vs Tiempo", color="blue", linewidth=2)

    plt.title("Gráfico de Velocidad Angular Final en MCUA")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Velocidad Angular Final (ωf)")

    plt.xticks(np.arange(0, t_max + 1, step=(t_max/5)))  # Ajustamos las etiquetas del eje x
    plt.yticks(np.arange(min(ωf), max(ωf)+1, step=(max(ωf)/10)))  # Ajustamos las etiquetas del eje y

    # Guardar la imagen generada
    plt.savefig(archivo_salida, format="png")
    plt.close()

def generarGraficoDesplazamientoAngular_MCUA(ω0, α, t_max, archivo_salida="graficodesplazamientoangularmcua.png"):
    """
    Genera una imagen con el gráfico de desplazamiento angular en MCUA y la guarda como un archivo PNG.
    :param ω0: Velocidad angular inicial (en radianes por segundo).
    :param α: Aceleración angular (en radianes por segundo al cuadrado).
    :param t_max: Tiempo máximo para graficar.
    :param archivo_salida: Nombre del archivo de salida donde se guardará la imagen.
    """
    t_max = int(t_max)
    t = np.linspace(0, t_max, num=t_max + 1)  # Rango de tiempos de 0 a t_max
    θ = ω0 * t + 0.5 * α * t**2  # Desplazamiento angular en función del tiempo
    
    # Crear la figura con tamaño ajustado
    plt.figure(figsize=(5, 4))  
    plt.plot(t, θ, label="Desplazamiento Angular vs Tiempo", color="green", linewidth=2)

    plt.title("Gráfico de Desplazamiento Angular en MCUA")
    plt.xlabel("Tiempo (t)")
    plt.ylabel("Desplazamiento Angular (θ)")

    plt.xticks(np.arange(0, t_max + 1, step=(t_max/5)))  # Ajustamos las etiquetas del eje x
    plt.yticks(np.arange(min(θ), max(θ)+1, step=(max(θ)/10)))  # Ajustamos las etiquetas del eje y

    # Guardar la imagen generada
    plt.savefig(archivo_salida, format="png")
    plt.close()

