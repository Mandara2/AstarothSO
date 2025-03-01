import os
import json
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QPropertyAnimation, QEasingCurve, QRect


class ExploradorArchivos(QDialog):
    def __init__(self, usuario, parent=None):
        super().__init__(parent)
        self.usuario = self.limpiar_nombre_usuario(usuario)
        self.setWindowTitle('Gestor de Archivos')
        self.setGeometry(300, 300, 600, 400)
        self.setStyleSheet("background-color: black; color: white;")

        self.layout = QVBoxLayout(self)
        self.carpetas = ['Videos', 'Musica', 'Descargas', 'Escritorio', 'Imagenes']
        self.iconos = {
            'Videos': 'imagenes/iconos/aplicaciones/ExploradorArchivos/videos.png',
            'Musica': 'imagenes/iconos/aplicaciones/musica.png',
            'Descargas': 'imagenes/iconos/aplicaciones/ExploradorArchivos/descargas.png',
            'Escritorio': 'imagenes/iconos/aplicaciones/ExploradorArchivos/Escritorio.png',
            'Imagenes': 'imagenes/iconos/aplicaciones/ExploradorArchivos/imagenes.png'
        }

        # Configurar el diseño de iconos
        self.iconos_layout = QGridLayout()
        self.layout.addLayout(self.iconos_layout)

        for i, carpeta in enumerate(self.carpetas):
            button = QPushButton(carpeta)
            button.setIcon(QIcon(self.iconos[carpeta]))
            button.setIconSize(QSize(40, 40))
            button.setStyleSheet("""
                QPushButton {
                    background-color: #555555;
                    color: white;
                    font-size: 16px;
                    font-weight: bold;
                    padding: 10px;
                    border: 2px solid #777777;
                    border-radius: 8px;
                }
                QPushButton:hover {
                    background-color: #777777;
                }
            """)
            button.clicked.connect(self.crear_manejador_click(carpeta))
            self.animar_boton(button)
            self.iconos_layout.addWidget(button, i // 2, i % 2)

        self.list_widget = QListWidget(self)
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: #222222;
                color: white;
                font-size: 14px;
                border: 1px solid #555555;
                padding: 5px;
            }
        """)
        self.layout.addWidget(self.list_widget)

        self.is_admin = self.verificar_admin()
        self.setLayout(self.layout)

    def limpiar_nombre_usuario(self, nombre_usuario):
        return nombre_usuario.lstrip('./')

    def verificar_admin(self):
        ruta_json = 'InfoUsers/perfiles.json'
        if not os.path.exists(ruta_json):
            print(f"Error: La ruta {ruta_json} no existe.")
            return False

        try:
            with open(ruta_json, 'r') as archivo_json:
                datos = json.load(archivo_json)
                usuario_data = datos.get(self.usuario)
                return usuario_data and usuario_data.get('is_admin', 0) == 1
        except Exception as e:
            print(f"Error al leer el archivo JSON: {e}")
            return False

    def crear_manejador_click(self, carpeta):
        def manejador():
            self.mostrar_archivos(carpeta)
        return manejador

    def mostrar_archivos(self, carpeta):
        self.list_widget.clear()

        if self.is_admin:
            ruta_base = 'UsersData'
            for usuario in os.listdir(ruta_base):
                ruta_carpeta = os.path.join(ruta_base, usuario, carpeta)
                self.listar_archivos(ruta_carpeta, f'{usuario}/{carpeta}')
        else:
            ruta_carpeta = os.path.join('UsersData', self.usuario, carpeta)
            self.listar_archivos(ruta_carpeta, carpeta)

    def listar_archivos(self, ruta_carpeta, etiqueta):
        if os.path.exists(ruta_carpeta):
            archivos = os.listdir(ruta_carpeta)
            if archivos:
                for archivo in archivos:
                    self.list_widget.addItem(f'{etiqueta}: {archivo}')
            else:
                self.list_widget.addItem(f'{etiqueta}: No hay archivos')
        else:
            self.list_widget.addItem(f'{etiqueta}: Carpeta no encontrada')

    def animar_boton(self, boton):
        """Aplica una animación al pasar el ratón sobre el botón."""
        animacion = QPropertyAnimation(boton, b"geometry")
        animacion.setDuration(500)
        animacion.setStartValue(QRect(boton.x(), boton.y(), boton.width(), boton.height()))
        animacion.setEndValue(QRect(boton.x(), boton.y() - 10, boton.width(), boton.height()))
        animacion.setEasingCurve(QEasingCurve.InOutQuad)
        animacion.start()
