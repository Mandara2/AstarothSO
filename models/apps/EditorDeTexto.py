import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton,
    QInputDialog, QWidget, QMessageBox, QHBoxLayout, QListWidget, QLabel
)
from PyQt5.QtCore import QPropertyAnimation, QRect, QEasingCurve
from PyQt5.QtGui import QIcon, QColor

class EditorDeTexto(QMainWindow):
    def __init__(self, nombre_usuario):
        super().__init__()
        self.setWindowTitle('Editor de Texto')
        self.setGeometry(300, 300, 800, 600)

        # Establecer un icono para la ventana
        self.setWindowIcon(QIcon('icono.png'))  # Asegúrate de tener un archivo icono.png

        # Obtener la carpeta del usuario
        self.nombre_usuario = nombre_usuario
        self.ruta_documentos = os.path.join('UsersData', self.nombre_usuario, 'Documentos')

        # Asegurarse de que la carpeta de documentos exista
        if not os.path.exists(self.ruta_documentos):
            os.makedirs(self.ruta_documentos)

        # Crear el directorio donde se guardarán los archivos
        self.ruta_guardado = os.path.join(self.ruta_documentos, 'TextosEditor')
        if not os.path.exists(self.ruta_guardado):
            os.makedirs(self.ruta_guardado)

        # Configurar la interfaz
        self.init_ui()

    def init_ui(self):
        # Crear un widget principal
        widget_principal = QWidget(self)
        self.setCentralWidget(widget_principal)

        # Establecer el fondo de la ventana
        self.setStyleSheet("background-color: #f4f4f4;")  # Color de fondo claro

        # Crear el layout principal
        layout_principal = QVBoxLayout(widget_principal)

        # Título para la lista de documentos
        titulo_documentos = QLabel("Documentos", self)
        titulo_documentos.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(titulo_documentos)

        # Crear una lista para los documentos
        self.lista_documentos = QListWidget(self)
        self.lista_documentos.setStyleSheet("background-color: #ffffff; color: #2c3e50; border-radius: 5px; padding: 10px;")
        self.lista_documentos.itemClicked.connect(self.abrir_documento)
        layout_principal.addWidget(self.lista_documentos)

        # Título para el área de texto
        titulo_texto = QLabel("Área de texto", self)
        titulo_texto.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout_principal.addWidget(titulo_texto)

        # Crear área de texto
        self.text_area = QTextEdit(self)
        self.text_area.setStyleSheet("background-color: #ffffff; color: #2c3e50; border-radius: 5px; padding: 10px;")
        layout_principal.addWidget(self.text_area)

        # Crear un contenedor para los botones
        contenedor_botones = QWidget(self)
        layout_botones = QHBoxLayout(contenedor_botones)

        # Botón para guardar el archivo
        btn_guardar = QPushButton('Guardar', self)
        btn_guardar.setStyleSheet("background-color: #3498db; color: white; padding: 10px; border-radius: 5px;")
        btn_guardar.setIcon(QIcon('save_icon.png'))  # Asegúrate de tener un archivo save_icon.png
        btn_guardar.clicked.connect(self.guardar_archivo)
        layout_botones.addWidget(btn_guardar)

        # Agregar el contenedor de botones al layout principal
        layout_principal.addWidget(contenedor_botones)

        # Cargar documentos de la carpeta del usuario
        self.cargar_documentos()

        # Agregar una transición animada para los botones
        self.animar_boton(btn_guardar)

    def animar_boton(self, boton):
      # Agregar una animación suave para el botón "Guardar"
      animacion = QPropertyAnimation(boton, b"geometry")
      animacion.setDuration(1000)
      animacion.setStartValue(QRect(boton.x(), boton.y(), boton.width(), boton.height()))
      animacion.setEndValue(QRect(boton.x(), boton.y() - 10, boton.width(), boton.height()))

      # Establecer la curva de suavizado correcta
      animacion.setEasingCurve(QEasingCurve.InOutQuad)  # Usa una curva de suavizado válida
      animacion.start()

    def cargar_documentos(self):
        # Limpiar la lista antes de cargar los nuevos documentos
        self.lista_documentos.clear()

        # Buscar todos los archivos de texto en la carpeta de documentos
        if os.path.exists(self.ruta_documentos):
            for archivo in os.listdir(self.ruta_documentos):
                if archivo.lower().endswith('.txt'):  # Solo archivos de texto
                    self.lista_documentos.addItem(archivo)

    def guardar_archivo(self):
        # Pedir el nombre del archivo mediante un cuadro de entrada
        nombre_archivo, ok = QInputDialog.getText(
            self, 'Guardar archivo', 'Ingrese el nombre del archivo (sin extensión):'
        )

        # Si el usuario proporciona un nombre y presiona OK
        if ok and nombre_archivo:
            # Validar que el nombre no esté vacío y no tenga caracteres no permitidos
            if not nombre_archivo.strip():
                QMessageBox.warning(self, 'Advertencia', 'El nombre del archivo no puede estar vacío.')
                return

            if any(char in nombre_archivo for char in r'\/:*?"<>|'):
                QMessageBox.warning(self, 'Advertencia', 'El nombre del archivo contiene caracteres no permitidos.')
                return

            try:
                # Crear la ruta completa para guardar el archivo
                ruta_guardado = os.path.join(self.ruta_documentos, f'{nombre_archivo}.txt')

                # Guardar el contenido del área de texto en el archivo seleccionado
                with open(ruta_guardado, 'w', encoding='utf-8') as archivo:
                    contenido = self.text_area.toPlainText()
                    archivo.write(contenido)

                QMessageBox.information(self, 'Éxito', f'Archivo "{nombre_archivo}.txt" guardado exitosamente.')
                # Actualizar la lista de documentos
                self.cargar_documentos()

            except Exception as e:
                QMessageBox.critical(self, 'Error', f'No se pudo guardar el archivo: {e}')

    def abrir_documento(self, item):
        # Obtener la ruta del documento seleccionado
        ruta_documento = os.path.join(self.ruta_documentos, item.text())
        if os.path.exists(ruta_documento):
            try:
                with open(ruta_documento, 'r', encoding='utf-8') as archivo:
                    contenido = archivo.read()
                    self.text_area.setText(contenido)
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'No se pudo abrir el archivo: {e}')
        else:
            QMessageBox.warning(self, 'Advertencia', 'El archivo seleccionado no existe.')

if __name__ == '__main__':
    import sys

    nombre_usuario = input("Ingrese el nombre del usuario: ")  # Solicitar nombre de usuario al ejecutar
    app = QApplication(sys.argv)

    # Crear el editor de texto con el nombre de usuario
    editor = EditorDeTexto(nombre_usuario)

    # Mostrar la ventana después de la inicialización
    editor.show()

    sys.exit(app.exec_())
