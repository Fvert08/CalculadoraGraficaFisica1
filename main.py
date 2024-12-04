from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
    QComboBox, QTableWidget, QTableWidgetItem, QGridLayout, QFrame, QSizePolicy, QStackedWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QPixmap
from calculos import calcularPosFinal_MRU,calcularPosFinal_MRUA,calcularVelocidadFinal_MRUA,calcularVelocidadFinal_CaidaLibre,calcularFuerzaNeta_Dinamica,calcularPeso_Dinamica,calcularFuerzaFriccion_Dinamica,calcularVelocidadAngularFinal_MCUA,calcularDesplazamientoAngular_MCUA
from graficos import generarGraficoPosFinal_MRU,generarGraficoPosFinal_MRUA,generarGraficoVelocidadFinal_MRUA,generarGraficoVelocidadFinal_CaidaLibre,generarImagenFuerzaNeta_Dinamica,generarImagenPeso_Dinamica,generarFriccion_Dinamica,generarGraficoVelocidadAngularFinal_MCUA,generarGraficoDesplazamientoAngular_MCUA

class CalculadoraGrafica(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 500)
        # Configuración de la ventana
        self.setWindowTitle("Calculadora Gráfica")
        self.setGeometry(100, 100, 600, 500)
        
        # Layout principal
        layout_principal = QGridLayout()
        
        # Título
        titulo = QLabel("CALCULADORA GRAFICA")
        titulo.setAlignment(Qt.AlignCenter)
        layout_principal.addWidget(titulo, 0, 0, 1, 4)  # Ocupa 1 fila y 4 columnas
        
        # Sección de selección de cálculo
        layout_principal.addWidget(QLabel("Seleccione el tipo de calculo:"), 1, 0, 1, 1)  # Ocupa 1 fila y 1 columna
        
        self.tipo_calculo = QComboBox()
        self.tipo_calculo.addItem("MRU: Posicion final")
        self.tipo_calculo.addItem("MRUA: Posicion final")
        self.tipo_calculo.addItem("MRUA: Velocidad final")
        self.tipo_calculo.addItem("Caida libre: Velocidad Final")
        self.tipo_calculo.addItem("Dinamica: Fuerza")
        self.tipo_calculo.addItem("Dinamica: Peso")
        self.tipo_calculo.addItem("Dinamica: Friccion")
        self.tipo_calculo.addItem("MCUA: Velocidad angular final")
        self.tipo_calculo.addItem("MCUA: Desplazamiento angular")
        layout_principal.addWidget(self.tipo_calculo, 1, 1, 1, 2)  # Ocupa 1 fila y 2 columnas
        
        # Sección de datos de cálculo (QStackedWidget para cambiar el bloque dinámicamente)
        self.datos_stack = QStackedWidget()
        
        # Crear bloques de datos para cada opción del ComboBox
        self.bloquePosicionFinal_MRU()
        self.bloquePosicionFinal_MRUA()
        self.bloqueVelocidadFinal_MRUA()
        self.bloqueVelocidadFinal_CaidaLibre()
        self.bloqueFuerzaNeta_Dinamica()
        self.bloquePeso_Dinamica()
        self.bloqueFuerzaFriccion_Dinamica()
        self.bloqueVelocidadAngularFinal_MCUA()
        self.bloqueDesplazamientoAngular_MCUA()
        layout_principal.addWidget(self.datos_stack, 2, 0, 1, 2)  # Ocupa 1 fila y 2 columnas

        # Conectar el cambio en el ComboBox a una función para cambiar el bloque de datos
        self.tipo_calculo.currentIndexChanged.connect(self.cambiar_bloque_datos)
        
        # Sección de gráfico en un QFrame para mantener el borde
        frame_grafico = QFrame()
        frame_grafico.setFrameShape(QFrame.Box)
        frame_grafico.setFrameShadow(QFrame.Sunken)
        
        layout_grafico = QVBoxLayout()
        layout_grafico.addWidget(QLabel("Gráfico"), alignment=Qt.AlignCenter)
        
        # Crear un QLabel para mostrar la imagen generada
        self.graficoxy= QLabel(self)
        layout_grafico.addWidget(self.graficoxy)
        frame_grafico.setLayout(layout_grafico)
        
        layout_principal.addWidget(frame_grafico, 2, 2, 6, 2)  # Gráfico ocupa 6 filas y 2 columnas, desde la fila 2 y columna 2
        
        # Sección de tabla de datos
        layout_principal.addWidget(QLabel("Tabla de datos"), 8, 0, 1, 4)  # Ocupa 1 fila y 4 columnas
        
        self.tabla_datos = QTableWidget(10,2 )
        self.tabla_datos.setHorizontalHeaderLabels([])
        layout_principal.addWidget(self.tabla_datos, 9, 0, 1, 4)  # Ocupa 1 fila y 4 columnas
        
        # Ajustar espaciado y márgenes
        layout_principal.setHorizontalSpacing(10)
        layout_principal.setVerticalSpacing(10)
        layout_principal.setContentsMargins(20, 20, 20, 20)
        
        # Configuración final de la ventana
        self.setLayout(layout_principal)

    def bloquePosicionFinal_MRU(self):
        widget_opcion1 = QWidget()
        layout_opcion1 = QVBoxLayout()

        # Campo para "X0"
        hbox_x0 = QHBoxLayout()
        hbox_x0.addWidget(QLabel("X0 ="))
        x0_input = QLineEdit()
        x0_input.setMaximumWidth(300)
        x0_input.setPlaceholderText("Distancia inicial")
        x0_input.setAlignment(Qt.AlignLeft)
        hbox_x0.addWidget(x0_input)
        layout_opcion1.addLayout(hbox_x0)
        
        # Campo para "v"
        hbox_v = QHBoxLayout()
        hbox_v.addWidget(QLabel("v ="))
        v_input = QLineEdit()
        v_input.setMaximumWidth(300)
        v_input.setPlaceholderText("Velocidad")
        hbox_v.addWidget(v_input)
        layout_opcion1.addLayout(hbox_v)
        
        # Campo para "t"
        hbox_t = QHBoxLayout()
        hbox_t.addWidget(QLabel("t ="))
        t_input = QLineEdit()
        t_input.setMaximumWidth(300)
        t_input.setPlaceholderText("Tiempo")
        hbox_t.addWidget(t_input)
        layout_opcion1.addLayout(hbox_t)
        
        # Formula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Formula usada: x= x0 + v * t"))
        layout_opcion1.addLayout(hbox_formula)

        # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion1.addLayout(hbox_Resultado)
        
        # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion1.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularPosFinal_MRU(
                float(x0_input.text()), 
                float(v_input.text()), 
                float(t_input.text())
            ) + " m"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarGraficoPosFinal_MRU(
                float(x0_input.text()), 
                float(v_input.text()), 
                float(t_input.text()), 
                archivo_salida="GraficoPosFinal_MRU.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoMRU(
                float(x0_input.text()), 
                float(v_input.text()), 
                float(t_input.text())
            ),
        ])



        widget_opcion1.setLayout(layout_opcion1)
        self.datos_stack.addWidget(widget_opcion1)
    def actualizargraficoMRU(self,x0,v,t):
        pixmap = QPixmap("GraficoPosFinal_MRU.png")

        # Redimensionar el pixmap
        scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Establecer el pixmap redimensionado en el QLabel
        self.graficoxy.setPixmap(scaled_pixmap)
        # Actualizar tabla con los datos
        # Establecer los encabezados de las columnas
        self.tabla_datos.setHorizontalHeaderLabels(['Tiempo (x)', 'Posicion (y)'])
        # Definir el número de columnas
        self.tabla_datos.setColumnCount(2)  # 2 columnas
        self.tabla_datos.setRowCount(int(t)+1) 
        #Llenar tabla de datos
         # Opcional: Llenar la tabla con algunos datos nuevos
        for row in range(int(t)+1):
            for col in range(2):
                if col == 0:  # Columna 1: "t"
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(str(row)))  # Ponemos el valor de 't'
                elif col == 1:  # Columna 2: Resultado de la ecuación
                    resultado = x0 + v * row  # Esto calcula la posición en el tiempo t
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado

    def bloquePosicionFinal_MRUA(self):
        widget_opcion2 = QWidget()
        layout_opcion2 = QVBoxLayout()
        
        # Campo para "x0"
        hbox_x0 = QHBoxLayout()
        hbox_x0.addWidget(QLabel("x0 ="))
        x0_input = QLineEdit()
        x0_input.setMaximumWidth(300)
        x0_input.setPlaceholderText("Distancia inicial")
        hbox_x0.addWidget(x0_input)
        layout_opcion2.addLayout(hbox_x0)

        # Campo para "v0"
        hbox_v0 = QHBoxLayout()
        hbox_v0.addWidget(QLabel("v0 ="))
        v0_input = QLineEdit()
        v0_input.setMaximumWidth(300)
        v0_input.setPlaceholderText("Velocidad inicial")
        hbox_v0.addWidget(v0_input)
        layout_opcion2.addLayout(hbox_v0)
        
        # Campo para "t"
        hbox_t = QHBoxLayout()
        hbox_t.addWidget(QLabel("t ="))
        t_input = QLineEdit()
        t_input.setMaximumWidth(300)
        t_input.setPlaceholderText("Tiempo")
        hbox_t.addWidget(t_input)
        layout_opcion2.addLayout(hbox_t)

        # Campo para "a"
        hbox_a = QHBoxLayout()
        hbox_a.addWidget(QLabel("a ="))
        a_input = QLineEdit()
        a_input.setMaximumWidth(300)
        a_input.setPlaceholderText("Aceleracion")
        hbox_a.addWidget(a_input)
        layout_opcion2.addLayout(hbox_a)

        # Formula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Formula usada: x= x0 + v0 * t + (1/2) a * t^2"))
        layout_opcion2.addLayout(hbox_formula)

        # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion2.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion2.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularPosFinal_MRUA(
                float(x0_input.text()), 
                float(v0_input.text()), 
                float(t_input.text()),
                float(a_input.text())
            ) + " m"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarGraficoPosFinal_MRUA(
                float(x0_input.text()), 
                float(v0_input.text()), 
                float(t_input.text()),
                float(a_input.text()), 
                archivo_salida="graficoPosFinalmrua.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoPosFinalMRUA(
                float(x0_input.text()), 
                float(v0_input.text()), 
                float(t_input.text()),
                float(a_input.text()), 
            ),
        ])
        widget_opcion2.setLayout(layout_opcion2)
        self.datos_stack.addWidget(widget_opcion2)
    def actualizargraficoPosFinalMRUA(self,x0,v0,t,a):
        pixmap = QPixmap("graficoPosFinalmrua.png")

        # Redimensionar el pixmap
        scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Establecer el pixmap redimensionado en el QLabel
        self.graficoxy.setPixmap(scaled_pixmap)
        # Actualizar tabla con los datos
        # Establecer los encabezados de las columnas
        self.tabla_datos.setHorizontalHeaderLabels(['Tiempo (x)', 'Posicion (y)'])
        # Definir el número de columnas
        self.tabla_datos.setColumnCount(2)  # 2 columnas
        self.tabla_datos.setRowCount(int(t)+1) 
        #Llenar tabla de datos
         # Opcional: Llenar la tabla con algunos datos nuevos
        for row in range(int(t)+1):
            for col in range(2):
                if col == 0:  # Columna 1: "t"
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(str(row)))  # Ponemos el valor de 't'
                elif col == 1:  # Columna 2: Resultado de la ecuación
                    resultado =x0 + v0 * row + 0.5 * a * row**2   # Esto calcula la posición en el tiempo t
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado
    
    def bloqueVelocidadFinal_MRUA(self):
        widget_opcion_velocidad_final = QWidget()
        layout_opcion_velocidad_final = QVBoxLayout()
        
        # Campo para "v0"
        hbox_v0 = QHBoxLayout()
        hbox_v0.addWidget(QLabel("v0 ="))
        v0_input = QLineEdit()
        v0_input.setMaximumWidth(300)
        v0_input.setPlaceholderText("Velocidad inicial")
        hbox_v0.addWidget(v0_input)
        layout_opcion_velocidad_final.addLayout(hbox_v0)
        
        # Campo para "a"
        hbox_a = QHBoxLayout()
        hbox_a.addWidget(QLabel("a ="))
        a_input = QLineEdit()
        a_input.setMaximumWidth(300)
        a_input.setPlaceholderText("Aceleración")
        hbox_a.addWidget(a_input)
        layout_opcion_velocidad_final.addLayout(hbox_a)
        
        # Campo para "t"
        hbox_t = QHBoxLayout()
        hbox_t.addWidget(QLabel("t ="))
        t_input = QLineEdit()
        t_input.setMaximumWidth(300)
        t_input.setPlaceholderText("Tiempo")
        hbox_t.addWidget(t_input)
        layout_opcion_velocidad_final.addLayout(hbox_t)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: vf = v0 + a * t"))
        layout_opcion_velocidad_final.addLayout(hbox_formula)
         # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_velocidad_final.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_velocidad_final.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularVelocidadFinal_MRUA(
                float(v0_input.text()), 
                float(a_input.text()),
                float(t_input.text())
            ) + " m"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarGraficoVelocidadFinal_MRUA(
                float(v0_input.text()), 
                float(a_input.text()),
                float(t_input.text()), 
                archivo_salida="graficovelocidadmrua.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficovelFinalMRUA(
                float(v0_input.text()), 
                float(t_input.text()),
                float(a_input.text()), 
            ),
        ])
        widget_opcion_velocidad_final.setLayout(layout_opcion_velocidad_final)
        self.datos_stack.addWidget(widget_opcion_velocidad_final)
    def actualizargraficovelFinalMRUA(self,v0,t,a):
            pixmap = QPixmap("graficovelocidadmrua.png")

            # Redimensionar el pixmap
            scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Establecer el pixmap redimensionado en el QLabel
            self.graficoxy.setPixmap(scaled_pixmap)
            # Actualizar tabla con los datos
            # Establecer los encabezados de las columnas
            self.tabla_datos.setHorizontalHeaderLabels(['Tiempo (x)', 'velocidad (y)'])
            # Definir el número de columnas
            self.tabla_datos.setColumnCount(2)  # 2 columnas
            self.tabla_datos.setRowCount(int(t)+1) 
            #Llenar tabla de datos
            # Opcional: Llenar la tabla con algunos datos nuevos
            for row in range(int(t)+1):
                for col in range(2):
                    if col == 0:  # Columna 1: "t"
                        self.tabla_datos.setItem(row, col, QTableWidgetItem(str(row)))  # Ponemos el valor de 'row'
                    elif col == 1:  # Columna 2: Resultado de la ecuación
                        resultado =v0 + a * row  # Esto calcula la posición en el tiempo t
                        self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado
    
    def bloqueVelocidadFinal_CaidaLibre(self):
        widget_opcion_velocidad_final_caida_libre = QWidget()
        layout_opcion_velocidad_final_caida_libre = QVBoxLayout()
        
        # Campo para "v0"
        hbox_v0 = QHBoxLayout()
        hbox_v0.addWidget(QLabel("v0 ="))
        v0_input = QLineEdit()
        v0_input.setMaximumWidth(300)
        v0_input.setPlaceholderText("Velocidad inicial")
        hbox_v0.addWidget(v0_input)
        layout_opcion_velocidad_final_caida_libre.addLayout(hbox_v0)
        
        # Campo para "g" (gravedad)
        hbox_g = QHBoxLayout()
        hbox_g.addWidget(QLabel("g ="))
        g_input = QLineEdit()
        g_input.setMaximumWidth(300)
        g_input.setPlaceholderText("Gravdedad: 9.81")  # Puede ayudar a recordar el valor de g
        hbox_g.addWidget(g_input)
        layout_opcion_velocidad_final_caida_libre.addLayout(hbox_g)
        
        # Campo para "t"
        hbox_t = QHBoxLayout()
        hbox_t.addWidget(QLabel("t ="))
        t_input = QLineEdit()
        t_input.setMaximumWidth(300)
        t_input.setPlaceholderText("Tiempo")
        hbox_t.addWidget(t_input)
        layout_opcion_velocidad_final_caida_libre.addLayout(hbox_t)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: vf = v0 + g * t"))
        layout_opcion_velocidad_final_caida_libre.addLayout(hbox_formula)

         # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_velocidad_final_caida_libre.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_velocidad_final_caida_libre.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularVelocidadFinal_CaidaLibre(
                float(v0_input.text()), 
                float(g_input.text()),
                float(t_input.text())
            ) + " m"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarGraficoVelocidadFinal_CaidaLibre(
                float(v0_input.text()), 
                float(g_input.text()),
                float(t_input.text()), 
                archivo_salida="graficovelocidadcaidalibre.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoVelocidadFinal_CaidaLibre(
                float(v0_input.text()), 
                float(g_input.text()),
                float(t_input.text()), 
            ),
        ])
        widget_opcion_velocidad_final_caida_libre.setLayout(layout_opcion_velocidad_final_caida_libre)
        self.datos_stack.addWidget(widget_opcion_velocidad_final_caida_libre)
    def actualizargraficoVelocidadFinal_CaidaLibre(self,v0,g,t):
        pixmap = QPixmap("graficovelocidadcaidalibre.png")

        # Redimensionar el pixmap
        scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Establecer el pixmap redimensionado en el QLabel
        self.graficoxy.setPixmap(scaled_pixmap)
        # Actualizar tabla con los datos
        # Establecer los encabezados de las columnas
        self.tabla_datos.setHorizontalHeaderLabels(['Tiempo (x)', 'velocidad final (y)'])
        # Definir el número de columnas
        self.tabla_datos.setColumnCount(2)  # 2 columnas
        self.tabla_datos.setRowCount(int(t)+1) 
        #Llenar tabla de datos
        # Opcional: Llenar la tabla con algunos datos nuevos
        for row in range(int(t)+1):
            for col in range(2):
                if col == 0:  # Columna 1: "t"
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(str(row)))  # Ponemos el valor de 'row'
                elif col == 1:  # Columna 2: Resultado de la ecuación
                    resultado =v0 + g * row  # Esto calcula la posición en el tiempo t
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado

#------ Dinamica
    def bloqueFuerzaNeta_Dinamica(self):
        widget_opcion_fuerza_neta = QWidget()
        layout_opcion_fuerza_neta = QVBoxLayout()
        
        # Campo para "m" (masa)
        hbox_m = QHBoxLayout()
        hbox_m.addWidget(QLabel("m ="))
        m_input = QLineEdit()
        m_input.setMaximumWidth(300)
        m_input.setPlaceholderText("Masa")
        hbox_m.addWidget(m_input)
        layout_opcion_fuerza_neta.addLayout(hbox_m)
        
        # Campo para "a" (aceleración)
        hbox_a = QHBoxLayout()
        hbox_a.addWidget(QLabel("a ="))
        a_input = QLineEdit()
        a_input.setMaximumWidth(300)
        a_input.setPlaceholderText("Aceleración")
        hbox_a.addWidget(a_input)
        layout_opcion_fuerza_neta.addLayout(hbox_a)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: F = m * a"))
        layout_opcion_fuerza_neta.addLayout(hbox_formula)

         # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_fuerza_neta.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_fuerza_neta.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularFuerzaNeta_Dinamica(
                float(m_input.text()), 
                float(a_input.text()),
            ) + " N"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarImagenFuerzaNeta_Dinamica(
                float(m_input.text()), 
                float(a_input.text()),
                archivo_salida="graficofuerzaneta.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoFuerzaNeta(
                float(m_input.text()), 
                float(a_input.text()),
            ),
        ])

        widget_opcion_fuerza_neta.setLayout(layout_opcion_fuerza_neta)
        self.datos_stack.addWidget(widget_opcion_fuerza_neta)
    def actualizargraficoFuerzaNeta(self,m,a):
            pixmap = QPixmap("graficofuerzaneta.png")

            # Redimensionar el pixmap
            scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            # Establecer el pixmap redimensionado en el QLabel
            self.graficoxy.setPixmap(scaled_pixmap)
            # Actualizar tabla con los datos
            # Establecer los encabezados de las columnas
            self.tabla_datos.setHorizontalHeaderLabels(['m', 'Fuerza neta'])
            # Definir el número de columnas
            self.tabla_datos.setColumnCount(2)  # 2 columnas
            self.tabla_datos.setRowCount(1) 
            #Llenar tabla de datos
            # Opcional: Llenar la tabla con algunos datos nuevos
            for row in range(1):
                for col in range(2):
                    if col == 0:  # Columna 1: "t"
                        self.tabla_datos.setItem(row, col, QTableWidgetItem(str(m)))  # Ponemos el valor de 'row'
                    elif col == 1:  # Columna 2: Resultado de la ecuación
                        resultado =m * a  # Esto calcula la posición en el tiempo t
                        self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado

    def bloquePeso_Dinamica(self):
        widget_opcion_peso = QWidget()
        layout_opcion_peso = QVBoxLayout()
        # Campo para "m" (masa)
        hbox_m = QHBoxLayout()
        hbox_m.addWidget(QLabel("m ="))
        m_input = QLineEdit()
        m_input.setMaximumWidth(300)
        m_input.setPlaceholderText("Masa")
        hbox_m.addWidget(m_input)
        layout_opcion_peso.addLayout(hbox_m)
        
        # Campo para "g" (gravedad)
        hbox_g = QHBoxLayout()
        hbox_g.addWidget(QLabel("g ="))
        g_input = QLineEdit()
        g_input.setMaximumWidth(300)
        g_input.setPlaceholderText("Gravedad: 9.81")
        hbox_g.addWidget(g_input)
        layout_opcion_peso.addLayout(hbox_g)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: W = m * g"))
        layout_opcion_peso.addLayout(hbox_formula)

        # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_peso.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_peso.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularPeso_Dinamica(
                float(m_input.text()), 
                float(g_input.text()),
            ) + " N"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarImagenPeso_Dinamica(
                float(m_input.text()), 
                float(g_input.text()),
                archivo_salida="graficofuerzaneta.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoPeso(
                float(m_input.text()), 
                float(g_input.text()),
            ),
        ])
        widget_opcion_peso.setLayout(layout_opcion_peso)
        self.datos_stack.addWidget(widget_opcion_peso)
    def actualizargraficoPeso(self,m,g):
                pixmap = QPixmap("graficofuerzaneta.png")

                # Redimensionar el pixmap
                scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # Establecer el pixmap redimensionado en el QLabel
                self.graficoxy.setPixmap(scaled_pixmap)
                # Actualizar tabla con los datos
                # Establecer los encabezados de las columnas
                self.tabla_datos.setHorizontalHeaderLabels(['m', 'Peso'])
                # Definir el número de columnas
                self.tabla_datos.setColumnCount(2)  # 2 columnas
                self.tabla_datos.setRowCount(1) 
                #Llenar tabla de datos
                # Opcional: Llenar la tabla con algunos datos nuevos
                for row in range(1):
                    for col in range(2):
                        if col == 0:  # Columna 1: "t"
                            self.tabla_datos.setItem(row, col, QTableWidgetItem(str(m)))  # Ponemos el valor de 'row'
                        elif col == 1:  # Columna 2: Resultado de la ecuación
                            resultado =m * g  # Esto calcula la posición en el tiempo t
                            self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado

    def bloqueFuerzaFriccion_Dinamica(self):
        widget_opcion_fuerza_friccion = QWidget()
        layout_opcion_fuerza_friccion = QVBoxLayout()
        
        # Campo para "μ" (coeficiente de fricción)
        hbox_mu = QHBoxLayout()
        hbox_mu.addWidget(QLabel("μ ="))
        mu_input = QLineEdit()
        mu_input.setMaximumWidth(300)
        mu_input.setPlaceholderText("Coeficiente de fricción")
        hbox_mu.addWidget(mu_input)
        layout_opcion_fuerza_friccion.addLayout(hbox_mu)
        
        # Campo para "N" (normal)
        hbox_N = QHBoxLayout()
        hbox_N.addWidget(QLabel("N ="))
        N_input = QLineEdit()
        N_input.setMaximumWidth(300)
        N_input.setPlaceholderText("Fuerza normal")
        hbox_N.addWidget(N_input)
        layout_opcion_fuerza_friccion.addLayout(hbox_N)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: f = μ * N"))
        layout_opcion_fuerza_friccion.addLayout(hbox_formula)

        # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_fuerza_friccion.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_fuerza_friccion.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularFuerzaFriccion_Dinamica(
                float(mu_input.text()), 
                float(N_input.text()),
            ) + " μ"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarFriccion_Dinamica(
                float(mu_input.text()), 
                float(N_input.text()),
                archivo_salida="graficofriccion.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoPeso(
                float(mu_input.text()), 
                float(N_input.text()),
            ),
        ])
        widget_opcion_fuerza_friccion.setLayout(layout_opcion_fuerza_friccion)
        self.datos_stack.addWidget(widget_opcion_fuerza_friccion)
    def actualizargraficoPeso(self,mu,N):
        pixmap = QPixmap("graficofriccion.png")
        # Redimensionar el pixmap
        scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Establecer el pixmap redimensionado en el QLabel
        self.graficoxy.setPixmap(scaled_pixmap)
        # Actualizar tabla con los datos
        # Establecer los encabezados de las columnas
        self.tabla_datos.setHorizontalHeaderLabels(['coeficiente', 'Peso'])
        # Definir el número de columnas
        self.tabla_datos.setColumnCount(2)  # 2 columnas
        self.tabla_datos.setRowCount(1) 
        #Llenar tabla de datos
        # Opcional: Llenar la tabla con algunos datos nuevos
        for row in range(1):
            for col in range(2):
                if col == 0:  
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(str(mu)))  
                elif col == 1:  # Columna 2: Resultado de la ecuación
                    resultado =mu * N 
                    self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado
#---- MCUA
    def bloqueVelocidadAngularFinal_MCUA(self):
        widget_opcion_velocidad_angular_final = QWidget()
        layout_opcion_velocidad_angular_final = QVBoxLayout()
        
        # Campo para "ω0" (velocidad angular inicial)
        hbox_omega0 = QHBoxLayout()
        hbox_omega0.addWidget(QLabel("ω0 ="))
        omega0_input = QLineEdit()
        omega0_input.setMaximumWidth(300)
        omega0_input.setPlaceholderText("Velocidad angular inicial")
        hbox_omega0.addWidget(omega0_input)
        layout_opcion_velocidad_angular_final.addLayout(hbox_omega0)
        
        # Campo para "α" (aceleración angular)
        hbox_alpha = QHBoxLayout()
        hbox_alpha.addWidget(QLabel("α ="))
        alpha_input = QLineEdit()
        alpha_input.setMaximumWidth(300)
        alpha_input.setPlaceholderText("Aceleración angular")
        hbox_alpha.addWidget(alpha_input)
        layout_opcion_velocidad_angular_final.addLayout(hbox_alpha)
        
        # Campo para "t" (tiempo)
        hbox_t = QHBoxLayout()
        hbox_t.addWidget(QLabel("t ="))
        t_input = QLineEdit()
        t_input.setMaximumWidth(300)
        t_input.setPlaceholderText("Tiempo")
        hbox_t.addWidget(t_input)
        layout_opcion_velocidad_angular_final.addLayout(hbox_t)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: ωf = ω0 + α * t"))
        layout_opcion_velocidad_angular_final.addLayout(hbox_formula)
         # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_velocidad_angular_final.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_velocidad_angular_final.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularVelocidadAngularFinal_MCUA(
                float(omega0_input.text()), 
                float(alpha_input.text()),
                float(t_input.text())
            ) + " m"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarGraficoVelocidadAngularFinal_MCUA(
                float(omega0_input.text()), 
                float(alpha_input.text()),
                float(t_input.text()), 
                archivo_salida="graficovelocidadangularmcua.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoVelocidadAngularFinal(
                float(omega0_input.text()), 
                float(alpha_input.text()),
                float(t_input.text()), 
            ),
        ])
        widget_opcion_velocidad_angular_final.setLayout(layout_opcion_velocidad_angular_final)
        self.datos_stack.addWidget(widget_opcion_velocidad_angular_final)
    def actualizargraficoVelocidadAngularFinal(self,omega,alpha,t):
                pixmap = QPixmap("graficovelocidadangularmcua.png")

                # Redimensionar el pixmap
                scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                # Establecer el pixmap redimensionado en el QLabel
                self.graficoxy.setPixmap(scaled_pixmap)
                # Actualizar tabla con los datos
                # Establecer los encabezados de las columnas
                self.tabla_datos.setHorizontalHeaderLabels(['Tiempo (x)', 'velocidad angular final (y)'])
                # Definir el número de columnas
                self.tabla_datos.setColumnCount(2)  # 2 columnas
                self.tabla_datos.setRowCount(int(t)+1) 
                #Llenar tabla de datos
                # Opcional: Llenar la tabla con algunos datos nuevos
                for row in range(int(t)+1):
                    for col in range(2):
                        if col == 0:  # Columna 1: "t"
                            self.tabla_datos.setItem(row, col, QTableWidgetItem(str(row)))  # Ponemos el valor de 'row'
                        elif col == 1:  # Columna 2: Resultado de la ecuación
                            resultado =omega + alpha * row  # Esto calcula la posición en el tiempo t
                            self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resultado

    def bloqueDesplazamientoAngular_MCUA(self):
        widget_opcion_desplazamiento_angular = QWidget()
        layout_opcion_desplazamiento_angular = QVBoxLayout()
        
        # Campo para "ω0" (velocidad angular inicial)
        hbox_omega0 = QHBoxLayout()
        hbox_omega0.addWidget(QLabel("ω0 ="))
        omega0_input = QLineEdit()
        omega0_input.setMaximumWidth(300)
        omega0_input.setPlaceholderText("Velocidad angular inicial")
        hbox_omega0.addWidget(omega0_input)
        layout_opcion_desplazamiento_angular.addLayout(hbox_omega0)
        
        # Campo para "t" (tiempo)
        hbox_t = QHBoxLayout()
        hbox_t.addWidget(QLabel("t ="))
        t_input = QLineEdit()
        t_input.setMaximumWidth(300)
        t_input.setPlaceholderText("Tiempo")
        hbox_t.addWidget(t_input)
        layout_opcion_desplazamiento_angular.addLayout(hbox_t)
        
        # Campo para "α" (aceleración angular)
        hbox_alpha = QHBoxLayout()
        hbox_alpha.addWidget(QLabel("α ="))
        alpha_input = QLineEdit()
        alpha_input.setMaximumWidth(300)
        alpha_input.setPlaceholderText("Aceleración angular")
        hbox_alpha.addWidget(alpha_input)
        layout_opcion_desplazamiento_angular.addLayout(hbox_alpha)
        
        # Fórmula usada
        hbox_formula = QHBoxLayout()
        hbox_formula.addWidget(QLabel("Fórmula usada: θ = ω0 * t + 0.5 * α * t^2"))
        layout_opcion_desplazamiento_angular.addLayout(hbox_formula)

        # Resultado
        hbox_Resultado = QHBoxLayout()  
        label_resultado = QLabel("Resultado: ")
        hbox_Resultado.addWidget(label_resultado)
        layout_opcion_desplazamiento_angular.addLayout(hbox_Resultado)
         # Botón calcular
        boton_calcular = QPushButton("Calcular")
        layout_opcion_desplazamiento_angular.addWidget(boton_calcular)  # Ocupa 1 fila y 2 columnas
        boton_calcular.clicked.connect(lambda: [
            # Calcular el resultado y actualizar el label
            label_resultado.setText("Resultado: " + calcularDesplazamientoAngular_MCUA(
                float(omega0_input.text()), 
                float(t_input.text()),
                float(alpha_input.text())
            ) + " m"),
            
            # Actualizar el gráfico con los nuevos valores y guardarlo
            generarGraficoDesplazamientoAngular_MCUA(
                float(omega0_input.text()), 
                float(alpha_input.text()),
                float(t_input.text()), 
                archivo_salida="graficodesplazamientoangularmcua.png"
            ),
            
            # Actualizar el gráfico en el widget, pasando los valores necesarios
            self.actualizargraficoDesplazamientoAngular(
                float(omega0_input.text()), 
                float(alpha_input.text()),
                float(t_input.text()), 
            ),
        ])
        widget_opcion_desplazamiento_angular.setLayout(layout_opcion_desplazamiento_angular)
        self.datos_stack.addWidget(widget_opcion_desplazamiento_angular)
    def actualizargraficoDesplazamientoAngular(self,omega,alpha,t):
                    pixmap = QPixmap("graficodesplazamientoangularmcua.png")

                    # Redimensionar el pixmap
                    scaled_pixmap = pixmap.scaled(600, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)

                    # Establecer el pixmap redimensionado en el QLabel
                    self.graficoxy.setPixmap(scaled_pixmap)
                    # Actualizar tabla con los datos
                    # Establecer los encabezados de las columnas
                    self.tabla_datos.setHorizontalHeaderLabels(['Tiempo (x)', 'Desplazamiento Angular (y)'])
                    # Definir el número de columnas
                    self.tabla_datos.setColumnCount(2)  # 2 columnas
                    self.tabla_datos.setRowCount(int(t)+1) 
                    #Llenar tabla de datos
                    # Opcional: Llenar la tabla con algunos datos nuevos
                    for row in range(int(t)+1):
                        for col in range(2):
                            if col == 0:  # Columna 1: "t"
                                self.tabla_datos.setItem(row, col, QTableWidgetItem(str(row)))  # Ponemos el valor de 'row'
                            elif col == 1:  # Columna 2: Resultado de la ecuación
                                resultado =omega * t + 0.5 * alpha * t**2  # Esto calcula la posición en el tiempo t
                                self.tabla_datos.setItem(row, col, QTableWidgetItem(f'{resultado}'))  # Ponemos el resul
    
    def cambiar_bloque_datos(self, index):
        """Cambia el bloque de datos según la selección del ComboBox."""
        self.graficoxy.setPixmap(QPixmap())
        self.tabla_datos.clearContents()
        self.tabla_datos.setHorizontalHeaderLabels(['1', '2'])
        if index == 0:
            self.datos_stack.setCurrentIndex(0)  # Muestra Posicion final MRU
        elif index == 1:
            self.datos_stack.setCurrentIndex(1)  # Muestra Posicion final MRUA
        elif index == 2:
            self.datos_stack.setCurrentIndex(2)  # Muestra Velocidad final MRUA
        elif index == 3:
            self.datos_stack.setCurrentIndex(3)  # Muestra Velocidad final Caida libre
        elif index == 4:
            self.datos_stack.setCurrentIndex(4)  # Muestra Fuerza Dinamica
        elif index == 5:
            self.datos_stack.setCurrentIndex(5)  # Muestra Peso Dinamica
        elif index == 6:
            self.datos_stack.setCurrentIndex(6)  # Muestra Friccion Dinamica 
        elif index == 7:
            self.datos_stack.setCurrentIndex(7)  # Muestra Velocidad angular final MCUA
        elif index == 8:
            self.datos_stack.setCurrentIndex(8)  # Muestra Desplazamiento angular MCUA
        else:
            self.datos_stack.setCurrentIndex(-1)  # Muestra nada (si elige "Elija una opción")

if __name__ == "__main__":
    app = QApplication([])
    ventana = CalculadoraGrafica()
    ventana.show()
    app.exec_()

