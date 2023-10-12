
import sqlite3
import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from config import getFont

class CandidatureApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestion des candidatures")
        self.setMinimumSize(QSize(900, 650))

        self.initUI()
        self.load_data()

    def initUI(self):
        # Widgets
        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(["Type", "État", "Date", "Entreprise", "Poste", "Annonce", "Notes"])

        self.add_button = QPushButton("Ajouter Candidature")
        self.add_button.clicked.connect(self.add_candidature)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.table_widget)
        layout.addWidget(self.add_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_data(self):
        # Charger les données depuis la base de données SQLite et afficher dans le tableau
        conn = sqlite3.connect("candidatures.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS candidatures (id INTEGER PRIMARY KEY, type TEXT, etat TEXT, date DATE, entreprise TEXT, poste TEXT, annonce TEXT, notes TEXT)")
        cursor.execute("SELECT * FROM candidatures")
        data = cursor.fetchall()
        conn.close()

        self.table_widget.setRowCount(len(data))
        for row, candidature in enumerate(data):
            for col, value in enumerate(candidature[1:]):
                item = QTableWidgetItem(str(value))
                self.table_widget.setItem(row, col, item)

    def add_candidature(self):
        dialog = CandidatureDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            candidature = dialog.get_candidature()
            self.insert_candidature(candidature)
            self.load_data()

    def insert_candidature(self, candidature):
        conn = sqlite3.connect("candidatures.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO candidatures (type, etat, date, entreprise, poste, annonce, notes) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (candidature['type'], candidature['etat'], candidature['date'].toString("yyyy-MM-dd"),
                        candidature['entreprise'], candidature['poste'], candidature['annonce'], candidature['notes']))
        conn.commit()
        conn.close()

class CandidatureDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setWindowTitle("Ajouter une Candidature")
        self.setGeometry(200, 200, 400, 400)

        self.initUI()

    def initUI(self):
        # Widgets
        self.type_input = QComboBox()
        self.type_input.addItems(["Stage", "Alternance", "Emploi"])
        self.etat_input = QComboBox()
        self.etat_input.addItems(["Oui", "Non", "En attente"])
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.entreprise_input = QLineEdit()
        self.poste_input = QLineEdit()
        self.annonce_input = QLineEdit()
        self.notes_input = QTextEdit()

        self.save_button = QPushButton("Enregistrer")
        self.save_button.clicked.connect(self.accept)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.type_input)
        layout.addWidget(self.etat_input)
        layout.addWidget(self.date_input)
        layout.addWidget(self.entreprise_input)
        layout.addWidget(self.poste_input)
        layout.addWidget(self.annonce_input)
        layout.addWidget(self.notes_input)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def get_candidature(self):
        candidature = {
            "type": self.type_input.currentText(),
            "etat": self.etat_input.currentText(),
            "date": self.date_input.date(),
            "entreprise": self.entreprise_input.text(),
            "poste": self.poste_input.text(),
            "annonce": self.annonce_input.text(),
            "notes": self.notes_input.toPlainText()
        }

        return candidature

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CandidatureApp()
    window.show()
    sys.exit(app.exec_())
