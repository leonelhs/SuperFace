import qtawesome as qta
from PySide6.QtCore import (QCoreApplication, QMetaObject, Qt, Signal)
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit,
                               QPushButton, QVBoxLayout, QWidget, QMessageBox)


class Tagging(QWidget):
    taggerHandler = Signal(object)

    def __init__(self, parent=None):
        super(Tagging, self).__init__(parent)
        self.face = None
        self.buttonCancel = None
        self.buttonOK = None
        self.buttonsLayout = None
        self.tagEdit = None
        self.photoLabel = None
        self.photoLayout = None
        self.layout = None
        self.setupUi()

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.photoLayout = QVBoxLayout()
        self.photoLabel = QLabel(self)
        self.photoLabel.setAlignment(Qt.AlignCenter)
        self.photoLabel.setMargin(10)
        self.photoLayout.addWidget(self.photoLabel)

        self.tagEdit = QLineEdit(self)
        self.photoLayout.addWidget(self.tagEdit)

        self.buttonsLayout = QHBoxLayout()
        self.buttonOK = QPushButton(self)

        icon_ok = qta.icon('mdi.check')
        self.buttonOK.setIcon(icon_ok)
        self.buttonsLayout.addWidget(self.buttonOK)

        self.buttonCancel = QPushButton(self)
        icon_close = qta.icon('mdi.close')
        self.buttonCancel.setIcon(icon_close)
        self.buttonsLayout.addWidget(self.buttonCancel)

        self.photoLayout.addLayout(self.buttonsLayout)

        self.layout.addLayout(self.photoLayout)

        self.buttonOK.clicked.connect(self.onClickOK)
        self.buttonCancel.clicked.connect(self.onClickCancel)

        self.retranslateUi(self)

        QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Tagging Face ", None))
        self.photoLabel.setText(QCoreApplication.translate("Form", u"Photo", None))
        self.buttonOK.setText(QCoreApplication.translate("Form", u"OK", None))
        self.buttonCancel.setText(QCoreApplication.translate("Form", u"Cancel", None))

    def showDialog(self, message):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Tagging Person")
        dialog.setText(message)
        dialog.exec()

    def onClickOK(self):
        tagName = self.tagEdit.text()
        if tagName:
            self.face.tags = tagName
            self.taggerHandler.emit(self.face)
            self.close()
        else:
            self.showDialog("Please enter a name for this person!")

    def onClickCancel(self):
        self.close()

    def onGalleryHandlerMessage(self, face):
        self.face = face
        self.photoLabel.setPixmap(self.face.pixmap)
        self.tagEdit.setText(self.face.match)
