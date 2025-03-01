from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QListWidget, QApplication
)
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt
import pygame
import sys
import os
import shutil

class ReproductorMusica(QMainWindow):
    def __init__(self, usuario_activo="Rafa"):
        super().__init__()
        self.setWindowTitle('🎵 Reproductor de Música')
        self.setGeometry(100, 100, 500, 400)
        self.setMinimumSize(500, 400)

        # Inicialización de pygame
        pygame.mixer.init()

        # Lista de canciones y el índice actual
        self.lista_canciones = []
        self.cancion_actual = 0

        # Estilo del fondo
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        self.setPalette(palette)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)

        # Etiqueta de la canción actual
        self.etiqueta_cancion = QLabel("🎶 No hay canción cargada")
        self.etiqueta_cancion.setFont(QFont('Arial', 16, QFont.Bold))
        self.etiqueta_cancion.setStyleSheet("color: white; padding: 10px;")
        self.etiqueta_cancion.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.etiqueta_cancion)

        # Lista de canciones
        self.lista_widget = QListWidget()
        self.lista_widget.setStyleSheet("""
            QListWidget {
                background: #212121;
                color: white;
                font-size: 14px;
                border: none;
                padding: 5px;
            }
            QListWidget::item:selected {
                background: #1E88E5;
            }
        """)
        self.lista_widget.clicked.connect(self.reproducir_cancion_desde_lista)
        layout.addWidget(self.lista_widget)

        # Controles
        controles_layout = QHBoxLayout()

        # Botón Cargar
        self.boton_cargar = QPushButton("📂 Cargar")
        self.boton_cargar.setFont(QFont('Arial', 12))
        self.boton_cargar.setStyleSheet("background: #43A047; color: white; padding: 8px;")
        self.boton_cargar.clicked.connect(self.abrir_explorador_archivos)
        controles_layout.addWidget(self.boton_cargar)

        # Botón Reproducir/Pausar
        self.boton_reproducir = QPushButton("⏯️ Reproducir")
        self.boton_reproducir.setFont(QFont('Arial', 12))
        self.boton_reproducir.setStyleSheet("background: #1E88E5; color: white; padding: 8px;")
        self.boton_reproducir.clicked.connect(self.reproducir_pausar)
        controles_layout.addWidget(self.boton_reproducir)

        # Botón Siguiente
        self.boton_siguiente = QPushButton("⏭️ Siguiente")
        self.boton_siguiente.setFont(QFont('Arial', 12))
        self.boton_siguiente.setStyleSheet("background: #E53935; color: white; padding: 8px;")
        self.boton_siguiente.clicked.connect(self.siguiente_cancion)
        controles_layout.addWidget(self.boton_siguiente)

        # Botón Anterior
        self.boton_anterior = QPushButton("⏮️ Anterior")
        self.boton_anterior.setFont(QFont('Arial', 12))
        self.boton_anterior.setStyleSheet("background: #FDD835; color: black; padding: 8px;")
        self.boton_anterior.clicked.connect(self.anterior_cancion)
        controles_layout.addWidget(self.boton_anterior)

        layout.addLayout(controles_layout)

        # Cargar canciones automáticamente
        self.cargar_canciones_automaticamente(usuario_activo)

    def cargar_canciones_automaticamente(self, usuario_activo):
        ruta_canciones = f"UsersData/{usuario_activo}/Musica"
        if os.path.exists(ruta_canciones):
            self.lista_canciones = [
                os.path.join(ruta_canciones, archivo)
                for archivo in os.listdir(ruta_canciones) if archivo.endswith(".mp3")
            ]
            if self.lista_canciones:
                self.lista_widget.clear()
                for cancion in self.lista_canciones:
                    self.lista_widget.addItem(os.path.basename(cancion))
                self.cancion_actual = 0
                self.reproducir_cancion()
            else:
                self.etiqueta_cancion.setText("❌ No se encontraron canciones MP3")
        else:
            self.etiqueta_cancion.setText("❌ La carpeta de música no existe")

    def abrir_explorador_archivos(self):
        opciones = QFileDialog.Options()
        archivos, _ = QFileDialog.getOpenFileNames(
            self, "Selecciona una canción", "", "Archivos MP3 (*.mp3)", options=opciones
        )
        if archivos:
            for archivo in archivos:
                self.mover_cancion_a_carpeta(archivo)

    def mover_cancion_a_carpeta(self, archivo):
        ruta_canciones = "UsersData/Rafa/Musica"
        if not os.path.exists(ruta_canciones):
            os.makedirs(ruta_canciones)

        nombre_archivo = os.path.basename(archivo)
        ruta_destino = os.path.join(ruta_canciones, nombre_archivo)
        if not os.path.exists(ruta_destino):
            shutil.move(archivo, ruta_destino)
            self.lista_canciones.append(ruta_destino)
            self.lista_widget.addItem(nombre_archivo)
        else:
            print(f"La canción {nombre_archivo} ya existe en la carpeta")

    def reproducir_pausar(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.boton_reproducir.setText("⏯️ Reproducir")
        else:
            pygame.mixer.music.unpause()
            self.boton_reproducir.setText("⏸️ Pausar")

    def siguiente_cancion(self):
        if self.lista_canciones:
            self.cancion_actual = (self.cancion_actual + 1) % len(self.lista_canciones)
            self.reproducir_cancion()

    def anterior_cancion(self):
        if self.lista_canciones:
            self.cancion_actual = (self.cancion_actual - 1) % len(self.lista_canciones)
            self.reproducir_cancion()

    def reproducir_cancion(self):
        if self.lista_canciones:
            cancion = self.lista_canciones[self.cancion_actual]
            pygame.mixer.music.load(cancion)
            pygame.mixer.music.play()
            self.etiqueta_cancion.setText(f"🎶 Reproduciendo: {os.path.basename(cancion)}")

    def reproducir_cancion_desde_lista(self):
        item = self.lista_widget.currentItem()
        if item:
            index = self.lista_widget.row(item)
            self.cancion_actual = index
            self.reproducir_cancion()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ReproductorMusica()
    window.show()
    sys.exit(app.exec_())
