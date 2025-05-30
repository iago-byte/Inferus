# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFormLayout,
    QGroupBox, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QProgressBar, QPushButton,
    QSizePolicy, QStackedWidget, QStatusBar, QTabWidget,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 613)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.trainTab = QWidget()
        self.trainTab.setObjectName(u"trainTab")
        self.trainLayout = QHBoxLayout(self.trainTab)
        self.trainLayout.setObjectName(u"trainLayout")
        self.leftLayout = QVBoxLayout()
        self.leftLayout.setObjectName(u"leftLayout")
        self.groupBasic = QGroupBox(self.trainTab)
        self.groupBasic.setObjectName(u"groupBasic")
        self.formBasic = QFormLayout(self.groupBasic)
        self.formBasic.setObjectName(u"formBasic")
        self.model = QLabel(self.groupBasic)
        self.model.setObjectName(u"model")

        self.formBasic.setWidget(0, QFormLayout.ItemRole.LabelRole, self.model)

        self.comboTipoModelo = QComboBox(self.groupBasic)
        self.comboTipoModelo.addItem("")
        self.comboTipoModelo.addItem("")
        self.comboTipoModelo.addItem("")
        self.comboTipoModelo.setObjectName(u"comboTipoModelo")

        self.formBasic.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboTipoModelo)

        self.classes = QLabel(self.groupBasic)
        self.classes.setObjectName(u"classes")

        self.formBasic.setWidget(1, QFormLayout.ItemRole.LabelRole, self.classes)

        self.lineNumClases = QLineEdit(self.groupBasic)
        self.lineNumClases.setObjectName(u"lineNumClases")

        self.formBasic.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineNumClases)

        self.dataset = QLabel(self.groupBasic)
        self.dataset.setObjectName(u"dataset")

        self.formBasic.setWidget(2, QFormLayout.ItemRole.LabelRole, self.dataset)

        self.lineDataset = QLineEdit(self.groupBasic)
        self.lineDataset.setObjectName(u"lineDataset")

        self.formBasic.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineDataset)


        self.leftLayout.addWidget(self.groupBasic)

        self.groupParams = QGroupBox(self.trainTab)
        self.groupParams.setObjectName(u"groupParams")
        self.formParams = QFormLayout(self.groupParams)
        self.formParams.setObjectName(u"formParams")
        self.Batch_size = QLabel(self.groupParams)
        self.Batch_size.setObjectName(u"Batch_size")

        self.formParams.setWidget(0, QFormLayout.ItemRole.LabelRole, self.Batch_size)

        self.lineBatch = QLineEdit(self.groupParams)
        self.lineBatch.setObjectName(u"lineBatch")

        self.formParams.setWidget(0, QFormLayout.ItemRole.FieldRole, self.lineBatch)

        self.Epochs = QLabel(self.groupParams)
        self.Epochs.setObjectName(u"Epochs")

        self.formParams.setWidget(1, QFormLayout.ItemRole.LabelRole, self.Epochs)

        self.lineEpochs = QLineEdit(self.groupParams)
        self.lineEpochs.setObjectName(u"lineEpochs")

        self.formParams.setWidget(1, QFormLayout.ItemRole.FieldRole, self.lineEpochs)


        self.leftLayout.addWidget(self.groupParams)

        self.toggleAdvanced = QCheckBox(self.trainTab)
        self.toggleAdvanced.setObjectName(u"toggleAdvanced")

        self.leftLayout.addWidget(self.toggleAdvanced)

        self.groupAdvanced = QGroupBox(self.trainTab)
        self.groupAdvanced.setObjectName(u"groupAdvanced")
        self.formAdvanced = QFormLayout(self.groupAdvanced)
        self.formAdvanced.setObjectName(u"formAdvanced")
        self.backbone = QLabel(self.groupAdvanced)
        self.backbone.setObjectName(u"backbone")

        self.formAdvanced.setWidget(0, QFormLayout.ItemRole.LabelRole, self.backbone)

        self.comboBackbone = QComboBox(self.groupAdvanced)
        self.comboBackbone.addItem("")
        self.comboBackbone.addItem("")
        self.comboBackbone.addItem("")
        self.comboBackbone.setObjectName(u"comboBackbone")

        self.formAdvanced.setWidget(0, QFormLayout.ItemRole.FieldRole, self.comboBackbone)

        self.Optimizador = QLabel(self.groupAdvanced)
        self.Optimizador.setObjectName(u"Optimizador")

        self.formAdvanced.setWidget(1, QFormLayout.ItemRole.LabelRole, self.Optimizador)

        self.comboOptimizer = QComboBox(self.groupAdvanced)
        self.comboOptimizer.addItem("")
        self.comboOptimizer.addItem("")
        self.comboOptimizer.setObjectName(u"comboOptimizer")

        self.formAdvanced.setWidget(1, QFormLayout.ItemRole.FieldRole, self.comboOptimizer)

        self.learning = QLabel(self.groupAdvanced)
        self.learning.setObjectName(u"learning")

        self.formAdvanced.setWidget(2, QFormLayout.ItemRole.LabelRole, self.learning)

        self.lineLR = QLineEdit(self.groupAdvanced)
        self.lineLR.setObjectName(u"lineLR")

        self.formAdvanced.setWidget(2, QFormLayout.ItemRole.FieldRole, self.lineLR)

        self.tile_size = QLabel(self.groupAdvanced)
        self.tile_size.setObjectName(u"tile_size")

        self.formAdvanced.setWidget(3, QFormLayout.ItemRole.LabelRole, self.tile_size)

        self.lineTile = QLineEdit(self.groupAdvanced)
        self.lineTile.setObjectName(u"lineTile")

        self.formAdvanced.setWidget(3, QFormLayout.ItemRole.FieldRole, self.lineTile)

        self.Stride = QLabel(self.groupAdvanced)
        self.Stride.setObjectName(u"Stride")

        self.formAdvanced.setWidget(4, QFormLayout.ItemRole.LabelRole, self.Stride)

        self.lineStride = QLineEdit(self.groupAdvanced)
        self.lineStride.setObjectName(u"lineStride")

        self.formAdvanced.setWidget(4, QFormLayout.ItemRole.FieldRole, self.lineStride)

        self.checkTileInfer = QCheckBox(self.groupAdvanced)
        self.checkTileInfer.setObjectName(u"checkTileInfer")

        self.formAdvanced.setWidget(5, QFormLayout.ItemRole.SpanningRole, self.checkTileInfer)


        self.leftLayout.addWidget(self.groupAdvanced)

        self.hboxLayout = QHBoxLayout()
        self.hboxLayout.setObjectName(u"hboxLayout")
        self.btnRecomendado = QPushButton(self.trainTab)
        self.btnRecomendado.setObjectName(u"btnRecomendado")

        self.hboxLayout.addWidget(self.btnRecomendado)

        self.btnEntrenar = QPushButton(self.trainTab)
        self.btnEntrenar.setObjectName(u"btnEntrenar")

        self.hboxLayout.addWidget(self.btnEntrenar)


        self.leftLayout.addLayout(self.hboxLayout)


        self.trainLayout.addLayout(self.leftLayout)

        self.monitorLayout = QVBoxLayout()
        self.monitorLayout.setObjectName(u"monitorLayout")
        self.labelEstado = QLabel(self.trainTab)
        self.labelEstado.setObjectName(u"labelEstado")

        self.monitorLayout.addWidget(self.labelEstado)

        self.progressTraining = QProgressBar(self.trainTab)
        self.progressTraining.setObjectName(u"progressTraining")

        self.monitorLayout.addWidget(self.progressTraining)

        self.Graph = QWidget(self.trainTab)
        self.Graph.setObjectName(u"Graph")
        self.graphLayout = QVBoxLayout(self.Graph)
        self.graphLayout.setObjectName(u"graphLayout")
        self.graphLayout.setContentsMargins(0, 0, 0, 0)

        self.monitorLayout.addWidget(self.Graph)


        self.trainLayout.addLayout(self.monitorLayout)

        self.tabWidget.addTab(self.trainTab, "")
        self.inferTab = QWidget()
        self.inferTab.setObjectName(u"inferTab")
        self.inferLayout = QVBoxLayout(self.inferTab)
        self.inferLayout.setObjectName(u"inferLayout")
        self.comboInferModel = QComboBox(self.inferTab)
        self.comboInferModel.addItem("")
        self.comboInferModel.addItem("")
        self.comboInferModel.addItem("")
        self.comboInferModel.setObjectName(u"comboInferModel")
        self.comboInferModel.setEditable(False)

        self.inferLayout.addWidget(self.comboInferModel)

        self.stackedInferOutput = QStackedWidget(self.inferTab)
        self.stackedInferOutput.setObjectName(u"stackedInferOutput")
        self.pageSegmentation = QWidget()
        self.pageSegmentation.setObjectName(u"pageSegmentation")
        self.segLayout = QVBoxLayout(self.pageSegmentation)
        self.segLayout.setObjectName(u"segLayout")
        self.btnCargarImagen = QPushButton(self.pageSegmentation)
        self.btnCargarImagen.setObjectName(u"btnCargarImagen")

        self.segLayout.addWidget(self.btnCargarImagen)

        self.imgResultado = QLabel(self.pageSegmentation)
        self.imgResultado.setObjectName(u"imgResultado")
        self.imgResultado.setAlignment(Qt.AlignCenter)

        self.segLayout.addWidget(self.imgResultado)

        self.stackedInferOutput.addWidget(self.pageSegmentation)
        self.pageClassification = QWidget()
        self.pageClassification.setObjectName(u"pageClassification")
        self.classLayout = QVBoxLayout(self.pageClassification)
        self.classLayout.setObjectName(u"classLayout")
        self.lblResultadoClase = QLabel(self.pageClassification)
        self.lblResultadoClase.setObjectName(u"lblResultadoClase")
        self.lblResultadoClase.setAlignment(Qt.AlignCenter)

        self.classLayout.addWidget(self.lblResultadoClase)

        self.stackedInferOutput.addWidget(self.pageClassification)
        self.pageText = QWidget()
        self.pageText.setObjectName(u"pageText")
        self.textLayout = QVBoxLayout(self.pageText)
        self.textLayout.setObjectName(u"textLayout")
        self.inputPrompt = QLineEdit(self.pageText)
        self.inputPrompt.setObjectName(u"inputPrompt")

        self.textLayout.addWidget(self.inputPrompt)

        self.outputTexto = QTextEdit(self.pageText)
        self.outputTexto.setObjectName(u"outputTexto")
        self.outputTexto.setReadOnly(True)

        self.textLayout.addWidget(self.outputTexto)

        self.stackedInferOutput.addWidget(self.pageText)

        self.inferLayout.addWidget(self.stackedInferOutput)

        self.tabWidget.addTab(self.inferTab, "")
        self.metricsTab = QWidget()
        self.metricsTab.setObjectName(u"metricsTab")
        self.tabWidget.addTab(self.metricsTab, "")
        self.deployTab = QWidget()
        self.deployTab.setObjectName(u"deployTab")
        self.tabWidget.addTab(self.deployTab, "")
        self.configTab = QWidget()
        self.configTab.setObjectName(u"configTab")
        self.tabWidget.addTab(self.configTab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1000, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Plataforma MLOps - Cliente", None))
        self.groupBasic.setTitle(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n b\u00e1sica", None))
        self.model.setText(QCoreApplication.translate("MainWindow", u"Tipo de modelo", None))
        self.comboTipoModelo.setItemText(0, QCoreApplication.translate("MainWindow", u"Ligero", None))
        self.comboTipoModelo.setItemText(1, QCoreApplication.translate("MainWindow", u"Equilibrado", None))
        self.comboTipoModelo.setItemText(2, QCoreApplication.translate("MainWindow", u"Robusto", None))

        self.classes.setText(QCoreApplication.translate("MainWindow", u"N\u00famero de clases", None))
        self.dataset.setText(QCoreApplication.translate("MainWindow", u"Ruta del dataset", None))
        self.groupParams.setTitle(QCoreApplication.translate("MainWindow", u"Par\u00e1metros generales", None))
        self.Batch_size.setText(QCoreApplication.translate("MainWindow", u"Batch size", None))
        self.Epochs.setText(QCoreApplication.translate("MainWindow", u"\u00c9pocas", None))
        self.toggleAdvanced.setText(QCoreApplication.translate("MainWindow", u"Mostrar configuraci\u00f3n avanzada", None))
        self.groupAdvanced.setTitle(QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n avanzada", None))
        self.backbone.setText(QCoreApplication.translate("MainWindow", u"Backbone espec\u00edfico", None))
        self.comboBackbone.setItemText(0, QCoreApplication.translate("MainWindow", u"resnet18", None))
        self.comboBackbone.setItemText(1, QCoreApplication.translate("MainWindow", u"resnet34", None))
        self.comboBackbone.setItemText(2, QCoreApplication.translate("MainWindow", u"efficientnet-b0", None))

        self.Optimizador.setText(QCoreApplication.translate("MainWindow", u"Optimizador", None))
        self.comboOptimizer.setItemText(0, QCoreApplication.translate("MainWindow", u"Adam", None))
        self.comboOptimizer.setItemText(1, QCoreApplication.translate("MainWindow", u"SGD", None))

        self.learning.setText(QCoreApplication.translate("MainWindow", u"Learning Rate", None))
        self.tile_size.setText(QCoreApplication.translate("MainWindow", u"Tile size", None))
        self.Stride.setText(QCoreApplication.translate("MainWindow", u"Stride", None))
        self.checkTileInfer.setText(QCoreApplication.translate("MainWindow", u"Inferencia con tiles", None))
        self.btnRecomendado.setText(QCoreApplication.translate("MainWindow", u"Config. recomendada", None))
        self.btnEntrenar.setText(QCoreApplication.translate("MainWindow", u"Entrenar", None))
        self.labelEstado.setText(QCoreApplication.translate("MainWindow", u"Estado: Idle", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.trainTab), QCoreApplication.translate("MainWindow", u"Entrenamiento", None))
        self.comboInferModel.setItemText(0, QCoreApplication.translate("MainWindow", u"Segmentaci\u00f3n", None))
        self.comboInferModel.setItemText(1, QCoreApplication.translate("MainWindow", u"Clasificaci\u00f3n", None))
        self.comboInferModel.setItemText(2, QCoreApplication.translate("MainWindow", u"Texto", None))

        self.btnCargarImagen.setText(QCoreApplication.translate("MainWindow", u"Cargar imagen", None))
        self.imgResultado.setText(QCoreApplication.translate("MainWindow", u"Resultado de segmentaci\u00f3n", None))
        self.lblResultadoClase.setText(QCoreApplication.translate("MainWindow", u"Resultado de clasificaci\u00f3n", None))
        self.inputPrompt.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Introduce tu prompt y pulsa Enter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.inferTab), QCoreApplication.translate("MainWindow", u"Page", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.metricsTab), QCoreApplication.translate("MainWindow", u"M\u00e9tricas", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.deployTab), QCoreApplication.translate("MainWindow", u"Despliegue", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.configTab), QCoreApplication.translate("MainWindow", u"Configuraci\u00f3n", None))
    # retranslateUi

