from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QListWidget, QSplitter, QWidget, \
  QListWidgetItem
from PyQt5.QtGui import QImage, QPixmap, QFont, QIcon
from PyQt5.QtCore import QTimer, Qt
import sys
import cv2
import os


class VisualizadorMultimedia(QMainWindow):
  def __init__(self, nombre_usuario):
    super().__init__()
    self.setWindowTitle('🎥 Visualizador Multimedia 📸')
    self.setGeometry(300, 300, 1000, 600)
    self.setStyleSheet("background-color: #121212; color: #FFFFFF;")

    self.nombre_usuario = nombre_usuario
    self.imagenes = []
    self.videos = []

    # Configurar la interfaz
    self.init_ui()

    # Variables para el video
    self.timer = QTimer(self)
    self.cap = None

  def init_ui(self):
    # Configuración principal
    splitter = QSplitter(Qt.Horizontal, self)
    self.setCentralWidget(splitter)

    # Crear barra lateral
    barra_lateral = QWidget(self)
    layout_lateral = QVBoxLayout(barra_lateral)

    # Listas de imágenes y videos
    self.lista_imagenes = QListWidget(self)
    self.lista_imagenes.itemClicked.connect(self.abrir_multimedia)
    self.lista_imagenes.setStyleSheet("background-color: #1F1F1F; color: #FFFFFF;")

    self.lista_videos = QListWidget(self)
    self.lista_videos.itemClicked.connect(self.abrir_multimedia)
    self.lista_videos.setStyleSheet("background-color: #1F1F1F; color: #FFFFFF;")

    # Títulos estilizados
    titulo_imagenes = QLabel("📷 Imágenes")
    titulo_imagenes.setFont(QFont("Arial", 16, QFont.Bold))
    titulo_videos = QLabel("🎬 Videos")
    titulo_videos.setFont(QFont("Arial", 16, QFont.Bold))

    layout_lateral.addWidget(titulo_imagenes)
    layout_lateral.addWidget(self.lista_imagenes)
    layout_lateral.addWidget(titulo_videos)
    layout_lateral.addWidget(self.lista_videos)

    # Área principal
    area_principal = QWidget(self)
    layout_principal = QVBoxLayout(area_principal)
    self.label_multimedia = QLabel("Selecciona un archivo multimedia")
    self.label_multimedia.setAlignment(Qt.AlignCenter)
    self.label_multimedia.setFont(QFont("Arial", 18))
    layout_principal.addWidget(self.label_multimedia)

    splitter.addWidget(barra_lateral)
    splitter.addWidget(area_principal)
    splitter.setSizes([300, 700])

    # Cargar archivos
    self.cargar_multimedia()

  def cargar_multimedia(self):
    ruta_imagenes = f'UsersData/{self.nombre_usuario}/Imagenes'
    ruta_videos = f'UsersData/{self.nombre_usuario}/Videos'

    if os.path.exists(ruta_imagenes):
      for archivo in os.listdir(ruta_imagenes):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff')):
          item = QListWidgetItem(QIcon("icons/image_icon.png"), archivo)
          self.imagenes.append(os.path.join(ruta_imagenes, archivo))
          self.lista_imagenes.addItem(item)

    if os.path.exists(ruta_videos):
      for archivo in os.listdir(ruta_videos):
        if archivo.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv')):
          item = QListWidgetItem(QIcon("icons/video_icon.png"), archivo)
          self.videos.append(os.path.join(ruta_videos, archivo))
          self.lista_videos.addItem(item)

  def abrir_multimedia(self, item):
    if item in self.lista_imagenes.selectedItems():
      ruta_imagen = self.imagenes[self.lista_imagenes.row(item)]
      self.mostrar_imagen(ruta_imagen)
    elif item in self.lista_videos.selectedItems():
      ruta_video = self.videos[self.lista_videos.row(item)]
      self.mostrar_video(ruta_video)

  def mostrar_imagen(self, ruta_imagen):
    pixmap = QPixmap(ruta_imagen)
    self.label_multimedia.setPixmap(
      pixmap.scaled(self.label_multimedia.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )

  def mostrar_video(self, ruta_video):
    self.cap = cv2.VideoCapture(ruta_video)
    self.timer.timeout.connect(self.mostrar_frame)
    self.timer.start(30)
    self.label_multimedia.setText('Reproduciendo video...')

  def mostrar_frame(self):
    if self.cap and self.cap.isOpened():
      ret, frame = self.cap.read()
      if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)

        self.label_multimedia.setPixmap(
          QPixmap.fromImage(qimg).scaled(self.label_multimedia.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )
      else:
        self.timer.stop()
        self.cap.release()


if __name__ == '__main__':
  nombre_usuario = 'Mandara'
  app = QApplication(sys.argv)
  visualizador = VisualizadorMultimedia(nombre_usuario)
  visualizador.show()
  sys.exit(app.exec_())
