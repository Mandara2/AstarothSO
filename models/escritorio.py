import subprocess
import threading
import sys
from time import perf_counter

import psutil
from PyQt5.QtWidgets import (
    QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QGridLayout, QFrame, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QIcon, QMovie
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, QTimeZone

from models.APIClient import APIClient
from models.apps.EditorDeTexto import EditorDeTexto
from models.apps.ExploradorArchivos import ExploradorArchivos
from models.apps.ProfileManager import ProfileManager
from models.apps.ReproductorMusica import ReproductorMusica
from models.apps.VisualizadorMultimedia import VisualizadorMultimedia
from models.apps.calculadora import Calculadora
from models.apps.Administradortareas import AdministradorTareas
import os
import time


class DesktopWindow(QMainWindow):
    def __init__(self, perfil_datos):
        super().__init__()
        #print("Estos son los perfiles de los datos")
        #print(perfil_datos)
        self.setWindowTitle('Escritorio Principal')
        self.setGeometry(0, 0, 1024, 768)

        self.active_apps = {}

        self.usuario_activo = perfil_datos
        self.directorio_usuario = f"./{self.usuario_activo}"  # Directorio simulado del usuario

        self.fondo = QLabel(self)
        self.loading_label = QLabel(self)


        self.mostrar_gif_carga()


        self.cargar_imagen_en_hilo('imagenes\\DesktopWallpaper.jpg')


        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)


        icons_layout = QGridLayout()
        icons_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        icons_layout.setSpacing(20)
        main_layout.addLayout(icons_layout, stretch=1)

        app_icons = [
            ('imagenes/iconos/aplicaciones/brave-icon.png', 'Brave'),
            ('imagenes/iconos/aplicaciones/musica.png', 'Musica'),
            ('imagenes/iconos/aplicaciones/carpeta.png', 'Archivos'),
            ('imagenes/iconos/aplicaciones/rendimiento.png', 'A. Tareas'),
            ('imagenes/iconos/aplicaciones/calculadora.jpg', 'Calculadora'),
            ('imagenes/iconos/aplicaciones/editorTextos.png', 'Editor de textos'),
            ('imagenes/iconos/aplicaciones/steam.png', 'Steam'),
            ('imagenes/iconos/aplicaciones/video.png', 'Visualizador'),
            ('imagenes/iconos/aplicaciones/api.png', 'API'),
          ('imagenes/iconos/aplicaciones/creacionUsuario.png', 'Creacion de usuario')
        ]


        row, col = 0, 0
        for icon_path, name in app_icons:
            icon_frame = QFrame()
            icon_frame.setFixedSize(100, 150)
            icon_layout = QVBoxLayout(icon_frame)
            icon_layout.setAlignment(Qt.AlignCenter)
            icon_layout.setContentsMargins(0, 0, 0, 0)

            button = QPushButton()
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                button.setIcon(QIcon(pixmap))
                button.setIconSize(QSize(80, 80))
            button.setFixedSize(80, 80)
            button.setStyleSheet("border: none;")

            app_label = QLabel(name)
            app_label.setAlignment(Qt.AlignCenter)
            app_label.setStyleSheet("color: white;")

            icon_layout.addWidget(button)
            icon_layout.addWidget(app_label)

            if name == 'Calculadora':
                button.clicked.connect(self.abrir_calculadora)
            elif name == 'Brave':
                button.clicked.connect(self.abrir_brave)
            elif name == 'Archivos':
                button.clicked.connect(self.abrir_explorador_archivos)
            elif name == "A. Tareas":
                button.clicked.connect(self.abrir_administrador_tareas)
            elif name == "Steam":
              button.clicked.connect(self.abrir_steam)
            elif name == "Musica":
              button.clicked.connect(self.abrir_reproductor_musica)
            elif name == "Editor de textos":
              button.clicked.connect(self.abrir_editor_textos)
            elif name == "Visualizador":
              button.clicked.connect(self.abrir_visualizador)
            elif name == "API":
              button.clicked.connect(self.abrir_api)
            elif name == "Creacion de usuario":
              button.clicked.connect(self.abrir_creador_usuarios)


            icons_layout.addWidget(icon_frame, row, col)
            col += 1
            if col == 2:
                col = 0
                row += 1


        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(10, 10, 10, 10)


        self.create_top_right_controls(top_layout)
        main_layout.addLayout(top_layout)


        self.create_taskbar()

        self.showFullScreen()

    def mostrar_gif_carga(self):
        # Crear un QMovie para el GIF de carga
        self.loading_gif = QMovie("gifts/carga.gif")
        self.loading_label.setMovie(self.loading_gif)
        self.loading_label.setGeometry(self.rect())
        self.loading_label.setScaledContents(True)
        self.loading_gif.start()

    def cargar_imagen_en_hilo(self, ruta_imagen):

        hilo = threading.Thread(target=self.cargar_imagen_fondo, args=(ruta_imagen,))
        hilo.start()

    def cargar_imagen_fondo(self, ruta_imagen):

        pixmap = QPixmap(ruta_imagen)

        if pixmap.isNull():
            print("Error: No se pudo cargar la imagen.")
        else:

            self.mostrar_imagen_fondo(pixmap)

    def mostrar_imagen_fondo(self, pixmap):

        self.loading_gif.stop()
        self.loading_label.hide()

        self.fondo.setPixmap(pixmap)
        self.fondo.setScaledContents(True)
        self.fondo.setGeometry(self.rect())

    def resizeEvent(self, event):
        self.fondo.setGeometry(self.rect())
        self.loading_label.setGeometry(self.rect())
        super().resizeEvent(event)

    def create_taskbar(self):

        self.taskbar_frame = QFrame(self)
        self.taskbar_frame.setStyleSheet("background-color: rgba(38, 35, 34, 80);")


        self.taskbar_frame.setFixedHeight(110)
        self.taskbar_frame.setFixedWidth(2600)


        self.taskbar_frame.move(0, 970)


        self.taskbar_layout = QHBoxLayout(self.taskbar_frame)
        self.taskbar_layout.setContentsMargins(10, 10, 10, 10)
        self.taskbar_layout.setAlignment(Qt.AlignLeft)

    def create_top_right_controls(self, top_layout):
        top_right_frame = QFrame()
        top_right_frame.setFixedHeight(100)
        top_right_layout = QHBoxLayout(top_right_frame)
        top_right_layout.setContentsMargins(0, 0, 10, 0)

        # Agregar reloj
        self.clock_label = QLabel()
        self.clock_label.setStyleSheet("color: white; font-size: 18px;")
        top_right_layout.addWidget(self.clock_label)

        # Agregar porcentaje de batería
        self.battery_label = QLabel()
        self.battery_label.setStyleSheet("color: white; font-size: 14px;")
        top_right_layout.addWidget(self.battery_label, alignment=Qt.AlignRight)

        # Agregar botón de apagado
        shutdown_button = QPushButton()
        shutdown_button.setIcon(QIcon('imagenes/iconos/aplicaciones/iconoApagado.png'))
        shutdown_button.setIconSize(QSize(50, 50))
        shutdown_button.clicked.connect(self.shutdown_system)
        shutdown_button.setStyleSheet("border: none;")
        top_right_layout.addWidget(shutdown_button, alignment=Qt.AlignRight)
        top_layout.addWidget(top_right_frame, alignment=Qt.AlignRight)

        # Iniciar hilos para actualizar reloj y batería
        self.update_clock_thread = threading.Thread(target=self.update_clock, daemon=True)
        self.update_battery_thread = threading.Thread(target=self.update_battery, daemon=True)
        self.update_clock_thread.start()
        self.update_battery_thread.start()

    def abrir_administrador_tareas(self):
        self.admin_tareas = AdministradorTareas(self)
        self.admin_tareas.setWindowIcon(QIcon('imagenes/iconos/aplicaciones/rendimiento.png'))
        self.admin_tareas.show()
        self.add_to_taskbar('A. Tareas', 'imagenes/iconos/aplicaciones/rendimiento.png', self.admin_tareas)

    def abrir_editor_textos(self):
      if 'Editor de textos' not in self.active_apps:
        self.editor_textos = EditorDeTexto(self.usuario_activo)  # Pasar el parámetro
        self.editor_textos.setWindowIcon(QIcon('imagenes\\iconos\\aplicaciones\\editorTextos.png'))
        self.editor_textos.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.editor_textos.show()
        self.add_to_taskbar('Editor de textos', 'imagenes\\iconos\\aplicaciones\\editorTextos.png', self.editor_textos)

      else:
        self.editor_textos.showNormal()
        self.editor_textos.activateWindow()

    def abrir_explorador_archivos(self):
        # Crear una ventana separada para el explorador de archivos
        self.explorador_archivos = ExploradorArchivos(self.directorio_usuario)
        self.explorador_archivos.setWindowIcon(QIcon('imagenes\\iconos\\aplicaciones\\carpeta.png'))
        self.explorador_archivos.show()

        self.add_to_taskbar('Archivos', 'imagenes/iconos/aplicaciones/carpeta.png', self.explorador_archivos)

    def abrir_calculadora(self):
        # Mostrar calculadora
        if 'Calculadora' not in self.active_apps:
            self.calculadora = Calculadora()
            self.calculadora.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            self.calculadora.setWindowIcon(QIcon('imagenes\\iconos\\aplicaciones\\calculadora.jpg'))
            self.calculadora.show()
            self.add_to_taskbar('Calculadora', 'imagenes\\iconos\\aplicaciones\\calculadora.jpg', self.calculadora)
        else:
            self.calculadora.showNormal()
            self.calculadora.activateWindow()

    def abrir_reproductor_musica(self):
      # Mostrar calculadora
      if 'Musica' not in self.active_apps:
        self.musica = ReproductorMusica(self.usuario_activo)
        self.musica.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.musica.setWindowIcon(QIcon('imagenes\\iconos\\aplicaciones\\musica.jpg'))
        self.musica.show()
        self.add_to_taskbar('Musica', 'imagenes/iconos/aplicaciones/musica.png', self.musica)
      else:
        self.musica.showNormal()
        self.musica.activateWindow()

    def abrir_api(self):
      # Mostrar calculadora
      if 'API' not in self.active_apps:
        self.api = APIClient()  # Crear la instancia de la ventana (APIClient)
        # Configuración de la ventana
        self.api.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.api.setWindowIcon(QIcon('imagenes/iconos/aplicaciones/api.png'))
        self.api.show()

        # Pasar la instancia de la ventana (self.api) a add_to_taskbar
        self.add_to_taskbar('API', 'imagenes/iconos/aplicaciones/api.png', self.api)

      else:
        # Si la ventana ya está abierta, simplemente la traemos al frente
        self.api.showNormal()
        self.api.activateWindow()

    def abrir_visualizador(self):
      # Mostrar calculadora
      if 'Visualizador' not in self.active_apps:
        self.visualizador = VisualizadorMultimedia(self.usuario_activo)
        self.visualizador.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.visualizador.setWindowIcon(QIcon('imagenes/iconos/aplicaciones/video.png'))
        self.visualizador.show()
        self.add_to_taskbar('Visualizador', 'imagenes/iconos/aplicaciones/video.png', self.visualizador)
      else:
        self.visualizador.showNormal()
        self.visualizador.activateWindow()

    def abrir_creador_usuarios(self):
      # Mostrar calculadora
      if 'Creacion de usuario' not in self.active_apps:
        self.creador = ProfileManager()
        self.creador.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
        self.creador.setWindowIcon(QIcon('imagenes/iconos/aplicaciones/creacionUsuario.png'))
        self.creador.show()
        self.add_to_taskbar('Creacion de usuario', 'imagenes/iconos/aplicaciones/creacionUsuario.png', self.creador)
      else:
        self.creador.showNormal()
        self.creador.activateWindow()

    def abrir_brave(self):
        # Comando para abrir Brave
        try:
            subprocess.Popen(["C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"])  # Ajusta el comando según la ruta de tu navegador
        except Exception as e:
            print(f"Error al abrir Brave: {e}")

    def abrir_steam(self):
        # Comando para abrir Brave
        try:
            subprocess.Popen(["C:/Program Files (x86)/Steam/steam.exe"])  # Ajusta el comando según la ruta de tu navegador
        except Exception as e:
            print(f"Error al abrir Steam: {e}")

    def add_to_taskbar(self, app_name, icon_path, app_window):
      if app_name not in self.active_apps:
        button = QPushButton()
        button.setIcon(QIcon(icon_path))
        button.setIconSize(QSize(40, 40))
        button.setStyleSheet("border: none;")

        # Ahora 'app_window' es una instancia de la ventana y tiene el método showNormal
        button.clicked.connect(app_window.showNormal)  # Mostrar la aplicación al hacer clic
        button.clicked.connect(app_window.activateWindow)  # Activar la ventana

        # Conectar el evento de cierre de la ventana al método que eliminará el icono
        app_window.closeEvent = self.remove_from_taskbar(app_name, button)  # Eliminar icono al cerrar

        self.taskbar_layout.addWidget(button)
        self.active_apps[app_name] = app_window  # Añadir la aplicación a las activas

    def remove_from_taskbar(self, app_name, button):
      """Elimina el icono de la barra de tareas al cerrar la aplicación"""

      def handler(event):
        # Eliminar el botón de la barra de tareas
        button.deleteLater()
        # Eliminar la aplicación del diccionario de aplicaciones activas
        if app_name in self.active_apps:
          del self.active_apps[app_name]
        event.accept()  # Aceptar el evento de cierre de la ventana

      return handler

    def update_clock(self):
        while True:
            current_time = time.strftime("%H:%M:%S")
            self.clock_label.setText(current_time)
            time.sleep(1)  # Actualiza cada segundo

    def update_battery(self):
        while True:
            battery = psutil.sensors_battery()
            percent = battery.percent if battery else "N/A"
            self.battery_label.setText(f"Batería: {percent}%")
            time.sleep(60)  # Actualiza cada minuto

    def update_top_right_info(self):
        # Actualizar reloj
        col_time_zone = QTimeZone(-18000)
        current_time = QDateTime.currentDateTime().toTimeZone(col_time_zone)
        self.clock_label.setText(current_time.toString('HH:mm:ss'))

        # Actualizar porcentaje de batería
        battery = psutil.sensors_battery()
        if battery:
            self.battery_label.setText(f" {battery.percent}%")

    def shutdown_system(self):
        # Apagar el sistema
        self.close()

    def resizeEvent(self, event):
        self.fondo.setGeometry(self.rect())
        super().resizeEvent(event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()
            else:
                self.showFullScreen()


def main():
    app = QApplication(sys.argv)
    desktop = DesktopWindow()
    desktop.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
