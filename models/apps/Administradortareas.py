import psutil
import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout, QListWidget, QDialog, QLabel, QGroupBox, QWidget, QHBoxLayout
import os
from PyQt5.QtCore import QTimer
import multiprocessing

def worker(conn):
    """Función que obtiene las estadísticas del sistema"""
    while True:
        # Obtener estadísticas del sistema
        cpu_usage = psutil.cpu_percent(interval=1)
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            battery_status = f"{percent}% {'(Cargando)' if plugged else '(No cargando)'}"
        else:
            battery_status = "Batería: N/A"

        disk_usage = psutil.disk_usage('/')
        free_space = disk_usage.free / (1024 * 1024 * 1024)  # Convertir a GB
        total_space = disk_usage.total / (1024 * 1024 * 1024)  # Convertir a GB
        ssd_status = f"{free_space:.2f} GB libres de {total_space:.2f} GB totales"

        # Enviar datos al proceso principal
        stats = {
            "cpu_usage": cpu_usage,
            "battery_status": battery_status,
            "ssd_status": ssd_status
        }
        conn.send(stats)

class AdministradorTareas(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Administrador de Tareas')

        # Ajustar el tamaño de la ventana
        self.resize(800, 600)

        self.layout = QVBoxLayout(self)

        # Crear lista de procesos
        self.procesos_lista = QListWidget(self)
        self.layout.addWidget(self.procesos_lista)

        # Crear un grupo para estadísticas del sistema
        self.estadisticas_box = QGroupBox("Estadísticas del Sistema", self)
        self.estadisticas_layout = QVBoxLayout(self.estadisticas_box)
        self.layout.addWidget(self.estadisticas_box)

        # Etiquetas para mostrar el estado de la CPU, batería y SSD
        self.cpu_label = QLabel(self)
        self.battery_label = QLabel(self)
        self.ssd_label = QLabel(self)

        self.estadisticas_layout.addWidget(self.cpu_label)
        self.estadisticas_layout.addWidget(self.battery_label)
        self.estadisticas_layout.addWidget(self.ssd_label)

        # Crear y arrancar un proceso hijo para obtener las estadísticas del sistema
        self.parent_conn, self.child_conn = multiprocessing.Pipe()
        self.proceso = multiprocessing.Process(target=worker, args=(self.child_conn,))
        self.proceso.daemon = True
        self.proceso.start()

        # Crear gráficos para CPU y memoria
        self.graph_widget_cpu = pg.PlotWidget(self)
        self.graph_widget_cpu.setBackground('w')  # Fondo blanco
        self.cpu_curve = self.graph_widget_cpu.plot(pen='r')
        self.layout.addWidget(self.create_group_box("Uso de CPU (%)", self.graph_widget_cpu))

        self.graph_widget_memory = pg.PlotWidget(self)
        self.graph_widget_memory.setBackground('w')  # Fondo blanco
        self.memory_curve = self.graph_widget_memory.plot(pen='b')
        self.layout.addWidget(self.create_group_box("Uso de Memoria (MB)", self.graph_widget_memory))

        # Inicialización
        self.cargar_procesos()

        # Timer para actualizar las estadísticas y las gráficas
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_estadisticas)
        self.timer.timeout.connect(self.actualizar_graficas)
        self.timer.start(1000)  # Actualizar cada 1 segundo

        self.cpu_data = []
        self.memory_data = []

    def cargar_procesos(self):
        self.procesos_lista.clear()
        pid_actual = os.getpid()

        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
            try:
                if proc.info['pid'] == pid_actual or proc.info['name'] == "python.exe":
                    info = f"PID: {proc.info['pid']} - Nombre: {proc.info['name']} - CPU: {proc.info['cpu_percent']}% - Memoria: {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB"
                    self.procesos_lista.addItem(info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def actualizar_estadisticas(self):
        if self.parent_conn.poll():  # Verificar si hay nuevos datos
            stats = self.parent_conn.recv()
            cpu_usage = stats["cpu_usage"]
            battery_status = stats["battery_status"]
            ssd_status = stats["ssd_status"]
            self.cpu_label.setText(f"Uso de CPU: {cpu_usage}%")
            self.battery_label.setText(f"Batería: {battery_status}")
            self.ssd_label.setText(f"Espacio SSD: {ssd_status}")

    def actualizar_graficas(self):
        # Obtener uso de CPU y memoria para las gráficas
        cpu_usage = psutil.cpu_percent(interval=None)
        memory_usage = psutil.virtual_memory().percent

        # Limitar la cantidad de datos mostrados en la gráfica
        self.cpu_data.append(cpu_usage)
        self.memory_data.append(memory_usage)

        if len(self.cpu_data) > 100:  # Mostrar solo los últimos 100 puntos de datos
            self.cpu_data.pop(0)
            self.memory_data.pop(0)

        # Actualizar las gráficas
        self.cpu_curve.setData(self.cpu_data)
        self.memory_curve.setData(self.memory_data)

        # Actualizar las etiquetas de los ejes
        self.graph_widget_cpu.setLabel('left', 'Uso de CPU (%)', color='r', size=12)
        self.graph_widget_cpu.setLabel('bottom', 'Tiempo (s)', color='r', size=12)

        self.graph_widget_memory.setLabel('left', 'Uso de Memoria (MB)', color='b', size=12)
        self.graph_widget_memory.setLabel('bottom', 'Tiempo (s)', color='b', size=12)

    def create_group_box(self, title, widget):
        """Crea un QGroupBox con un título y un widget"""
        group_box = QGroupBox(title, self)
        layout = QVBoxLayout()
        layout.addWidget(widget)
        group_box.setLayout(layout)
        return group_box

    def closeEvent(self, event):
        self.proceso.terminate()  # Asegurar que el proceso hijo termine correctamente
        self.proceso.join()  # Esperar a que el proceso hijo termine
        event.accept()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    multiprocessing.set_start_method('spawn')  # Asegurar que el inicio sea 'spawn'

    app = QApplication(sys.argv)
    dialog = AdministradorTareas()
    dialog.show()
    sys.exit(app.exec_())
