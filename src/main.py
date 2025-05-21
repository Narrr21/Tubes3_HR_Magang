import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from ui.window import Ui_MainWindow
from db import get_connection

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnSearch.clicked.connect(self.search_name)

    def search_name(self):
        name = self.ui.inputName.text()
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM resumes WHERE name LIKE %s"
        cursor.execute(query, (f"%{name}%",))
        results = cursor.fetchall()

        output = ""
        for row in results:
            output += str(row) + "\n"

        self.ui.resultBox.setText(output)
        conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
