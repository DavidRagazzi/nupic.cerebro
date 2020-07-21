﻿import collections
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import ArrayTableModel
from nupic_studio.ui import Global
from nupic_studio.htm.encoding import Encoding, FieldDataType

class EncodingForm(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        QtWidgets.QDialog.__init__(self)

        self.initUI()

        self.encodingIdx = -1
        """Index of the encoding that is being edited. If index is -1 the user is creating a new encoding."""

        self.encodings = []
        """Temporary list of encodings that is being edited"""

    def initUI(self):

        # labelDataSourceFieldName
        self.labelDataSourceFieldName = QtWidgets.QLabel()
        self.labelDataSourceFieldName.setText("Datasource Field Name:")
        self.labelDataSourceFieldName.setAlignment(QtCore.Qt.AlignRight)

        # textBoxDataSourceFieldName
        self.textBoxDataSourceFieldName = QtWidgets.QLineEdit()
        self.textBoxDataSourceFieldName.setAlignment(QtCore.Qt.AlignLeft)

        # labelDataSourceFieldDataType
        self.labelDataSourceFieldDataType = QtWidgets.QLabel()
        self.labelDataSourceFieldDataType.setText("Field Data Type:")
        self.labelDataSourceFieldDataType.setAlignment(QtCore.Qt.AlignRight)

        # comboBoxDataSourceFieldDataType
        self.comboBoxDataSourceFieldDataType = QtWidgets.QComboBox()
        self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.boolean)
        self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.integer)
        self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.decimal)
        self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.dateTime)
        self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.string)

        # checkBoxEnableInference
        self.checkBoxEnableInference = QtWidgets.QCheckBox()
        self.checkBoxEnableInference.setText("Enable Inference")

        # labelEncoderModule
        self.labelEncoderModule = QtWidgets.QLabel()
        self.labelEncoderModule.setText("Module:")
        self.labelEncoderModule.setAlignment(QtCore.Qt.AlignRight)

        # textBoxEncoderModule
        self.textBoxEncoderModule = QtWidgets.QLineEdit()
        self.textBoxEncoderModule.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9._]+')))

        # labelEncoderClass
        self.labelEncoderClass = QtWidgets.QLabel()
        self.labelEncoderClass.setText("Class:")
        self.labelEncoderClass.setAlignment(QtCore.Qt.AlignRight)

        # textBoxEncoderClass
        self.textBoxEncoderClass = QtWidgets.QLineEdit()
        self.textBoxEncoderClass.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9_]+')))

        # labelEncoderParams
        self.labelEncoderParams = QtWidgets.QLabel()
        self.labelEncoderParams.setText("Params:")
        self.labelEncoderParams.setAlignment(QtCore.Qt.AlignRight)

        # dataGridEncoderParams
        data = []
        data.append(['', ''])
        data.append(['', ''])
        data.append(['', ''])
        data.append(['', ''])
        data.append(['', ''])
        data.append(['', ''])
        self.dataGridEncoderParams = QtWidgets.QTableView()
        self.dataGridEncoderParams.setModel(ArrayTableModel(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.dataGridEncoderParams.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.dataGridEncoderParams.verticalHeader().setDefaultSectionSize(18)
        self.dataGridEncoderParams.model().update(['Parameter', 'Value'], data)
        self.dataGridEncoderParams.resizeColumnsToContents()
        self.dataGridEncoderParams.setMinimumHeight(140)

        # labelEncoderFieldName
        self.labelEncoderFieldName = QtWidgets.QLabel()
        self.labelEncoderFieldName.setText("Field Name:")
        self.labelEncoderFieldName.setAlignment(QtCore.Qt.AlignRight)

        # textBoxEncoderFieldName
        self.textBoxEncoderFieldName = QtWidgets.QLineEdit()
        self.textBoxEncoderFieldName.setAlignment(QtCore.Qt.AlignLeft)

        # labelEncoderFieldDataType
        self.labelEncoderFieldDataType = QtWidgets.QLabel()
        self.labelEncoderFieldDataType.setText("Field Data Type:")
        self.labelEncoderFieldDataType.setAlignment(QtCore.Qt.AlignRight)

        # comboBoxEncoderFieldDataType
        self.comboBoxEncoderFieldDataType = QtWidgets.QComboBox()
        self.comboBoxEncoderFieldDataType.addItem(FieldDataType.boolean)
        self.comboBoxEncoderFieldDataType.addItem(FieldDataType.integer)
        self.comboBoxEncoderFieldDataType.addItem(FieldDataType.decimal)
        self.comboBoxEncoderFieldDataType.addItem(FieldDataType.dateTime)
        self.comboBoxEncoderFieldDataType.addItem(FieldDataType.string)

        # groupBoxEncoderLayout
        groupBoxEncoderLayout = QtWidgets.QGridLayout()
        groupBoxEncoderLayout.addWidget(self.labelEncoderModule, 0, 0)
        groupBoxEncoderLayout.addWidget(self.textBoxEncoderModule, 0, 1)
        groupBoxEncoderLayout.addWidget(self.labelEncoderClass, 1, 0)
        groupBoxEncoderLayout.addWidget(self.textBoxEncoderClass, 1, 1)
        groupBoxEncoderLayout.addWidget(self.labelEncoderParams, 2, 0)
        groupBoxEncoderLayout.addWidget(self.dataGridEncoderParams, 2, 1)
        groupBoxEncoderLayout.addWidget(self.labelEncoderFieldName, 3, 0)
        groupBoxEncoderLayout.addWidget(self.textBoxEncoderFieldName, 3, 1)
        groupBoxEncoderLayout.addWidget(self.labelEncoderFieldDataType, 4, 0)
        groupBoxEncoderLayout.addWidget(self.comboBoxEncoderFieldDataType, 4, 1)

        # groupBoxEncoder
        self.groupBoxEncoder = QtWidgets.QGroupBox()
        self.groupBoxEncoder.setLayout(groupBoxEncoderLayout)
        self.groupBoxEncoder.setTitle("Encoder")

        # groupBoxMainLayout
        groupBoxMainLayout = QtWidgets.QGridLayout()
        groupBoxMainLayout.addWidget(self.labelDataSourceFieldName, 0, 0)
        groupBoxMainLayout.addWidget(self.textBoxDataSourceFieldName, 0, 1)
        groupBoxMainLayout.addWidget(self.labelDataSourceFieldDataType, 1, 0)
        groupBoxMainLayout.addWidget(self.comboBoxDataSourceFieldDataType, 1, 1)
        groupBoxMainLayout.addWidget(self.checkBoxEnableInference, 2, 1)
        groupBoxMainLayout.addWidget(self.groupBoxEncoder, 3, 1)

        # groupBoxMain
        self.groupBoxMain = QtWidgets.QGroupBox()
        self.groupBoxMain.setLayout(groupBoxMainLayout)

        # buttonBox
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.__buttonOk_click)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(not Global.simulationInitialized)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.__buttonCancel_click)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.groupBoxMain)
        layout.addWidget(self.buttonBox)

        # SensorForm
        self.setLayout(layout)
        self.setModal(True)
        self.setWindowTitle("Sensor Properties")
        self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
        self.resize(400, 200)

    def setControlsValues(self):
        """
        Set controls values from a class instance.
        """

        # Set controls value with encoding params
        if self.encodingIdx >= 0:
            encoding = self.encodings[self.encodingIdx]
            self.checkBoxEnableInference.setChecked(encoding.enableInference)
            self.textBoxDataSourceFieldName.setText(encoding.dataSourceFieldName)
            self.comboBoxDataSourceFieldDataType.setCurrentIndex(self.comboBoxDataSourceFieldDataType.findText(encoding.dataSourceFieldDataType, QtCore.Qt.MatchFixedString))

            # Set encoding parameters
            self.textBoxEncoderModule.setText(encoding.encoderModule)
            self.textBoxEncoderClass.setText(encoding.encoderClass)
            encoderParams = json.loads(encoding.encoderParams.replace("'", "\""), object_pairs_hook=collections.OrderedDict)
            gridData = self.dataGridEncoderParams.model().data
            row = 0
            for key, value in encoderParams.iteritems():
                gridData[row][0] = key
                gridData[row][1] = value
                row += 1
            self.textBoxEncoderFieldName.setText(encoding.encoderFieldName)
            self.comboBoxEncoderFieldDataType.setCurrentIndex(self.comboBoxEncoderFieldDataType.findText(encoding.encoderFieldDataType, QtCore.Qt.MatchFixedString))

    def duplicatedFieldName(self, fieldName):
        """
        Check if exists an encoding with the same name.
        """
        duplicated = False

        if len(self.encodings) > 0:
            for i in range(len(self.encodings)):
                if self.encodings[i].encoderFieldName == fieldName and i != self.encodingIdx:
                    duplicated = True
                    break

        return duplicated

    def __buttonOk_click(self, event):
        """
        Check if values changed and save the,.
        """

        encoderParamsDict = collections.OrderedDict()
        if self.textBoxDataSourceFieldName.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Record field name was not specified.")
            return
        elif self.textBoxEncoderModule.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder module was not specified.")
            return
        elif self.textBoxEncoderClass.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder class was not specified.")
            return
        elif self.textBoxEncoderFieldName.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder field name was not specified.")
            return
        elif self.duplicatedFieldName(self.textBoxEncoderFieldName.text()):
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder field name already is used by other encoding.")
            return
        else:
            gridData = self.dataGridEncoderParams.model().data
            for row in range(len(gridData)):
                if gridData[row][0] != '':
                    # Valid parameter name
                    try:
                        gridData[row][0] = gridData[row][0].toString()
                    except:
                        pass
                    param = str(gridData[row][0])
                    validExpr = QtCore.QRegExp('[a-zA-Z0-9_]+')
                    if not validExpr.exactMatch(param):
                        QtWidgets.QMessageBox.warning(self, "Warning", "'" + param + "' is not a valid name.")
                        return

                    # Valid parameter value
                    try:
                        gridData[row][1] = gridData[row][1].toString()
                    except:
                        pass
                    value = str(gridData[row][1])
                    if len(value) == 0:
                        QtWidgets.QMessageBox.warning(self, "Warning", "'" + param + "' value is empty.")
                        return

                    # Add param name and its value to dictionary
                    encoderParamsDict[param] = value

        dataSourceFieldName = str(self.textBoxDataSourceFieldName.text())
        dataSourceFieldDataType = str(self.comboBoxDataSourceFieldDataType.currentText())
        enableInference = self.checkBoxEnableInference.isChecked()
        encoderModule = str(self.textBoxEncoderModule.text())
        encoderClass = str(self.textBoxEncoderClass.text())
        encoderParams = json.dumps(encoderParamsDict)
        encoderFieldName = str(self.textBoxEncoderFieldName.text())
        encoderFieldDataType = str(self.comboBoxEncoderFieldDataType.currentText())

        # Remove double quotes from param values
        encoderParams = encoderParams.replace("\"", "'")
        encoderParams = encoderParams.replace("True", "true")
        encoderParams = encoderParams.replace("False", "false")

        # If this is a new encoding get it from list else create a new one
        if self.encodingIdx >= 0:
            encoding = self.encodings[self.encodingIdx]
        else:
            encoding = Encoding()
            self.encodings.append(encoding)

        # If anything has changed
        if encoding.dataSourceFieldName != dataSourceFieldName or encoding.dataSourceFieldDataType != dataSourceFieldDataType or encoding.enableInference != enableInference or encoding.encoderModule != encoderModule or encoding.encoderClass != encoderClass or encoding.encoderParams != encoderParams or encoding.encoderFieldName != encoderFieldName or encoding.encoderFieldDataType != encoderFieldDataType:
            # Set encoding params with controls values
            encoding.dataSourceFieldName = dataSourceFieldName
            encoding.dataSourceFieldDataType = dataSourceFieldDataType
            encoding.enableInference = enableInference
            encoding.encoderModule = encoderModule
            encoding.encoderClass = encoderClass
            encoding.encoderParams = encoderParams
            encoding.encoderFieldName = encoderFieldName
            encoding.encoderFieldDataType = encoderFieldDataType

            self.accept()

        self.close()

    def __buttonCancel_click(self, event):
        self.reject()
        self.close()
