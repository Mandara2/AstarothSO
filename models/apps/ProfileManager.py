from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QLineEdit, QCheckBox, QMessageBox, QFormLayout, QApplication
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
import json
import os
import sys

class ProfileManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("👤 Crear Perfil de Usuario")
        self.setGeometry(100, 100, 500, 450)
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

        # Ruta para guardar perfiles
        self.perfiles_path = 'InfoUsers/perfiles.json'
        self.perfiles = self.load_profiles()

        # Crear interfaz
        self.initUI()

    def initUI(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)

        # Crear formulario
        form_layout = QFormLayout()

        # Campo de nombre
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Ingrese su nombre")
        form_layout.addRow("📛 Nombre:", self.nombre_input)

        # Contraseña
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        self.pass_input.setPlaceholderText("Ingrese su contraseña")
        form_layout.addRow("🔒 Contraseña:", self.pass_input)

        # Confirmación de contraseña
        self.pass_confirm_input = QLineEdit()
        self.pass_confirm_input.setEchoMode(QLineEdit.Password)
        self.pass_confirm_input.setPlaceholderText("Confirme su contraseña")
        form_layout.addRow("🔒 Confirmar:", self.pass_confirm_input)

        # Botón para cargar imagen
        self.imagen_button = QPushButton("📂 Cargar Imagen")
        self.imagen_button.setIcon(QIcon("icons/upload_icon.png"))
        self.imagen_button.clicked.connect(self.cargar_imagen)
        form_layout.addRow(self.imagen_button)

        # Mostrar imagen seleccionada
        self.imagen_label = QLabel("No se ha cargado ninguna imagen")
        self.imagen_label.setAlignment(Qt.AlignCenter)
        self.imagen_label.setStyleSheet("border: 1px solid #555; padding: 10px;")
        form_layout.addRow(self.imagen_label)

        # Administrador
        self.admin_checkbox = QCheckBox("¿Es Administrador?")
        form_layout.addRow(self.admin_checkbox)

        # Botón para guardar
        self.guardar_button = QPushButton("💾 Guardar Perfil")
        self.guardar_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.guardar_button.setStyleSheet("background-color: #1E88E5; color: white; padding: 10px;")
        self.guardar_button.clicked.connect(self.guardar_perfil)

        layout.addLayout(form_layout)
        layout.addWidget(self.guardar_button)

    def cargar_imagen(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Seleccionar Imagen", "", "Archivos de imagen (*.png *.jpg *.jpeg)", options=options
        )
        if file_name:
            pixmap = QPixmap(file_name).scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.imagen_label.setPixmap(pixmap)
            self.imagen_label.setText("")
            self.imagen_path = file_name
        else:
            self.imagen_label.setText("No se ha cargado ninguna imagen")

    def guardar_perfil(self):
        nombre = self.nombre_input.text().strip()
        contrasena = self.pass_input.text().strip()
        contrasena_confirmada = self.pass_confirm_input.text().strip()

        if not nombre or not contrasena or not contrasena_confirmada:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        if contrasena != contrasena_confirmada:
            QMessageBox.warning(self, "Error", "Las contraseñas no coinciden.")
            return

        if not hasattr(self, 'imagen_path'):
            self.imagen_path = 'imagenes/iconos/usuarios/usuario_default.png'

        is_admin = 1 if self.admin_checkbox.isChecked() else 0

        perfil = {
            "icon": self.imagen_path,
            "password": contrasena,
            "is_admin": is_admin
        }

        self.perfiles[nombre] = perfil
        self.save_profiles()

        QMessageBox.information(self, "Éxito", f"Perfil de {nombre} guardado correctamente.")
        self.crear_carpetas_usuario(nombre)

        # Resetear campos
        self.nombre_input.clear()
        self.pass_input.clear()
        self.pass_confirm_input.clear()
        self.imagen_label.setText("No se ha cargado ninguna imagen")
        self.admin_checkbox.setChecked(False)

    def load_profiles(self):
        if os.path.exists(self.perfiles_path):
            with open(self.perfiles_path, 'r') as file:
                return json.load(file)
        return {}

    def save_profiles(self):
        with open(self.perfiles_path, 'w') as file:
            json.dump(self.perfiles, file, indent=4)

    def crear_carpetas_usuario(self, nombre_usuario):
        directorio_usuario = os.path.join('UsersData', nombre_usuario)
        carpetas = ['Videos', 'Musica', 'Descargas', 'Escritorio', 'Imagenes']

        if not os.path.exists(directorio_usuario):
            os.makedirs(directorio_usuario)

        for carpeta in carpetas:
            carpeta_path = os.path.join(directorio_usuario, carpeta)
            if not os.path.exists(carpeta_path):
                os.makedirs(carpeta_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ProfileManager()
    window.show()
    sys.exit(app.exec_())
