import sys
import requests
import json
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QTextEdit, QPushButton, QWidget, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class APIClient(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consumidor de API")
        self.setGeometry(300, 300, 600, 400)

        # Crear área de texto
        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet("""
            QTextEdit {
                background: #212121;
                color: white;
                font-size: 14px;
                padding: 10px;
                border: none;
            }
        """)

        # Configuración general
        self.setStyleSheet("background-color: #2E2E2E; color: white;")
        self.layout = QVBoxLayout()
        self.init_ui()

    def init_ui(self):
        button_container = QWidget(self)
        button_layout = QVBoxLayout(button_container)

        botones = {
            "Obtener clientes": self.obtener_datos1,
            "Obtener rutas": self.obtener_datos2,
            "Obtener conductores": self.obtener_datos3,
            "Obtener direcciones": self.obtener_datos4,
            "Obtener facturas": self.obtener_datos5,
        }

        for texto, funcion in botones.items():
            btn = QPushButton(texto, self)
            btn.setFont(QFont('Arial', 12))
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #1E88E5;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #1565C0;
                }
            """)
            btn.clicked.connect(funcion)
            button_layout.addWidget(btn)

        self.layout.addWidget(button_container)
        self.layout.addWidget(self.text_area)

        main_widget = QWidget(self)
        main_widget.setLayout(self.layout)
        self.setCentralWidget(main_widget)

    def realizar_peticion(self, url):
        try:
            self.text_area.setText("⏳ Realizando solicitud, por favor espera...")
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            QMessageBox.critical(self, 'Error HTTP', f'Error HTTP: {e.response.status_code}\n{e}')
            return None
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, 'Error de Conexión', 'No se pudo conectar al servidor.')
            return None
        except requests.exceptions.Timeout:
            QMessageBox.critical(self, 'Tiempo de Espera Excedido', 'La solicitud ha tardado demasiado.')
            return None
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', f'Error desconocido: {e}')
            return None

    def mostrar_resultado(self, datos):
        if datos:
            texto_formateado = json.dumps(datos, indent=4, ensure_ascii=False)
            self.text_area.setText(texto_formateado)
        else:
            self.text_area.setText("❌ No se pudo obtener datos.")

    def obtener_datos1(self):
        url = "http://127.0.0.1:3333/clientes"
        datos = self.realizar_peticion(url)
        self.mostrar_resultado(datos)

    def obtener_datos2(self):
        url = "http://127.0.0.1:3333/rutas"
        datos = self.realizar_peticion(url)
        self.mostrar_resultado(datos)

    def obtener_datos3(self):
        url = "http://127.0.0.1:3333/conductores"
        datos = self.realizar_peticion(url)
        self.mostrar_resultado(datos)

    def obtener_datos4(self):
        url = "http://127.0.0.1:3333/direcciones"
        datos = self.realizar_peticion(url)
        self.mostrar_resultado(datos)

    def obtener_datos5(self):
        url = "http://127.0.0.1:3333/facturas"
        datos = self.realizar_peticion(url)
        self.mostrar_resultado(datos)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = APIClient()
    ventana.show()
    sys.exit(app.exec_())
