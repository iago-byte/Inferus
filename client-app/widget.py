import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MLOpsGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        # Cargar archivo .ui
        loader = QUiLoader()
        ui_file = QFile("form.ui")
        ui_file.open(QFile.ReadOnly)
        self.widget = loader.load(ui_file, None)  # NO usar self como parent
        ui_file.close()

        self.setCentralWidget(self.widget)
        self.setWindowTitle("Plataforma MLOps - Cliente")
        self.resize(1200, 800)

        # Aplicar estilo QSS moderno
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: white;
            }
            QLabel, QLineEdit, QComboBox, QCheckBox, QPushButton {
                color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #007acc;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #005f99;
            }
            QProgressBar {
                border: 1px solid grey;
                border-radius: 3px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #3daee9;
            }
            QTabWidget::pane {
                border: 1px solid #444;
            }
        """)

        self.widget.findChild(QWidget, "toggleAdvanced").toggled.connect(
            lambda checked: self.widget.findChild(QWidget, "groupAdvanced").setVisible(checked)
        )
        self.widget.findChild(QWidget, "groupAdvanced").setVisible(False)

        # Gráfica matplotlib
        self.canvas = FigureCanvas(Figure(figsize=(4, 3)))
        self.ax = self.canvas.figure.subplots()
        self.canvas.figure.patch.set_facecolor("#2e2e2e")
        self.ax.set_facecolor("#2e2e2e")
        self.ax.tick_params(colors="white")
        self.ax.set_title("Loss/Accuracy", color="white")
        self.ax.set_xlabel("Epoch", color="white")
        self.ax.set_ylabel("Value", color="white")

        # Agregar al layout corregido
        monitor_container = self.widget.findChild(QWidget, "Graph")
        if monitor_container:
            monitor_container.layout().addWidget(self.canvas)

        # Conexiones
        self.widget.findChild(QWidget, "btnEntrenar").clicked.connect(self.simular_entrenamiento)
        self.widget.findChild(QWidget, "btnRecomendado").clicked.connect(self.config_recomendada)
        self.widget.findChild(QWidget, "toggleAdvanced").toggled.connect(
            lambda checked: self.widget.findChild(QWidget, "groupAdvanced").setVisible(checked)
        )

    def simular_entrenamiento(self):
        self.widget.findChild(QWidget, "labelEstado").setText("Entrenando...")
        progress = self.widget.findChild(QWidget, "progressTraining")
        progress.setRange(0, 0)
        self.ax.clear()
        self.ax.set_facecolor("#2e2e2e")
        self.ax.tick_params(colors="white")
        self.ax.set_title("Loss/Accuracy", color="white")
        self.ax.set_xlabel("Epoch", color="white")
        self.ax.set_ylabel("Value", color="white")
        QTimer.singleShot(3000, self.finalizar_entrenamiento)

    def finalizar_entrenamiento(self):
        progress = self.widget.findChild(QWidget, "progressTraining")
        progress.setRange(0, 100)
        progress.setValue(100)
        self.widget.findChild(QWidget, "labelEstado").setText("Entrenamiento finalizado")
        self.ax.plot([1, 2, 3, 4], [0.9, 0.6, 0.4, 0.3], label="Loss")
        self.ax.plot([1, 2, 3, 4], [0.5, 0.7, 0.8, 0.9], label="Accuracy")
        self.ax.legend()
        self.canvas.draw()

    def config_recomendada(self):
        self.widget.findChild(QWidget, "comboTipoModelo").setCurrentIndex(1)  # Equilibrado
        self.widget.findChild(QWidget, "comboBackbone").setCurrentIndex(0)
        self.widget.findChild(QWidget, "comboOptimizer").setCurrentIndex(0)
        self.widget.findChild(QWidget, "lineBatch").setText("16")
        self.widget.findChild(QWidget, "lineLR").setText("0.001")
        self.widget.findChild(QWidget, "labelEstado").setText("Valores recomendados aplicados")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MLOpsGUI()
    window.show()
    sys.exit(app.exec())
