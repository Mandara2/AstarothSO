from PyQt5.QtWidgets import (
  QMainWindow, QLineEdit, QVBoxLayout, QWidget,
  QPushButton, QGridLayout, QApplication
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import math
import sys


class Calculadora(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle('Calculadora Científica')
    self.setGeometry(100, 100, 400, 600)
    self.setMinimumSize(400, 600)

    # Configuración de estilos
    self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLineEdit {
                background: #282a36;
                color: white;
                border: 2px solid #44475a;
                border-radius: 8px;
                padding: 10px;
                font-size: 24px;
            }
            QPushButton {
                background: #6272a4;
                color: white;
                border: none;
                font-size: 18px;
                border-radius: 8px;
                padding: 15px;
            }
            QPushButton:hover {
                background: #7088b1;
            }
            QPushButton:pressed {
                background: #44475a;
            }
            QPushButton.especial {
                background: #274b8f;
            }
            QPushButton.especial:hover {
                background: #3561b1;
            }
        """)

    # Configuración de la interfaz
    widget = QWidget(self)
    self.setCentralWidget(widget)
    layout = QVBoxLayout(widget)

    # Pantalla
    self.pantalla = QLineEdit()
    self.pantalla.setAlignment(Qt.AlignRight)
    self.pantalla.setReadOnly(True)
    self.pantalla.setFixedHeight(100)
    self.pantalla.setFont(QFont('Arial', 24))
    layout.addWidget(self.pantalla)

    # Botones
    botones_layout = QGridLayout()

    botones = [
      ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('log', 0, 3),
      ('root3', 1, 0), ('pi', 1, 1), ('e', 1, 2), ('!', 1, 3),
      ('(', 2, 1), (')', 2, 2), ('^', 2, 3), ('C', 2, 0, 'especial'),
      ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
      ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
      ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
      ('0', 6, 0), ('.', 6, 1), ('=', 6, 2, 'especial'), ('+', 6, 3)
    ]

    for texto, fila, columna, *estilo in botones:
      boton = QPushButton(texto)
      if estilo:
        boton.setProperty("class", estilo[0])  # Clase especial para "C" y "="
      boton.clicked.connect(lambda checked, t=texto: self.on_click(t))
      botones_layout.addWidget(boton, fila, columna)

    layout.addLayout(botones_layout)

  def on_click(self, texto):
    if texto == '=':
      try:
        expresion = self.pantalla.text()
        expresion = expresion.replace('sin(', 'math.sin(')
        expresion = expresion.replace('root3(', 'math.')
        expresion = expresion.replace('cos(', 'math.cos(')
        expresion = expresion.replace('tan(', 'math.tan(')
        expresion = expresion.replace('log(', 'math.log(')
        expresion = expresion.replace('root3(', 'math.cbrt(')
        expresion = expresion.replace('^', '**')
        resultado = str(eval(expresion))
        self.pantalla.setText(resultado)
      except Exception:
        self.pantalla.setText('Error')
    elif texto == 'C':
      self.pantalla.clear()
    elif texto in ['sin', 'cos', 'tan', 'log', 'root3']:
      self.pantalla.setText(self.pantalla.text() + f'{texto}(')
    elif texto == 'pi':
      self.pantalla.setText(self.pantalla.text() + str(math.pi))
    elif texto == 'e':
      self.pantalla.setText(self.pantalla.text() + str(math.e))
    elif texto == '!':
      try:
        num = int(self.pantalla.text())
        resultado = math.factorial(num)
        self.pantalla.setText(str(resultado))
      except ValueError:
        self.pantalla.setText('Error')
    else:
      self.pantalla.setText(self.pantalla.text() + texto)

  def keyPressEvent(self, event):
    key = event.key()
    if key in range(Qt.Key_0, Qt.Key_9 + 1):
      self.on_click(str(key - Qt.Key_0))
    elif key == Qt.Key_Plus:
      self.on_click('+')
    elif key == Qt.Key_Minus:
      self.on_click('-')
    elif key == Qt.Key_Asterisk:
      self.on_click('*')
    elif key == Qt.Key_Slash:
      self.on_click('/')
    elif key in (Qt.Key_Equal, Qt.Key_Return):
      self.on_click('=')
    elif key == Qt.Key_Backspace:
      self.pantalla.backspace()
    elif key == Qt.Key_Escape:
      self.pantalla.clear()


if __name__ == '__main__':
  app = QApplication(sys.argv)
  window = Calculadora()
  window.show()
  sys.exit(app.exec_())
