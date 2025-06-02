import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from ui.home import Ui_MainWindow
# from db import get_connection  # Uncomment and implement when ready

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect actions to menu items
        self.ui.actionUploadCV.triggered.connect(self.handle_action_upload_cvs)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionRefreshDatabase.triggered.connect(self.load_database_info)
        self.ui.actionClearDatabase.triggered.connect(self.clear_database)

        # Connect buttons to handlers
        self.ui.btnBrowse.clicked.connect(self.handle_browse_button)
        self.ui.btnUpload.clicked.connect(self.handle_upload_button)
        self.ui.btnSearch.clicked.connect(self.handle_search_button)
        self.ui.btnClear.clicked.connect(self.handle_clear_button)
        self.ui.btnViewSummary.clicked.connect(self.handle_view_summary)
        self.ui.btnViewCV.clicked.connect(self.handle_view_cv)
        self.ui.btnExportResults.clicked.connect(self.handle_export_results)

        # Initialize UI state
        self.ui.btnViewSummary.setEnabled(False)
        self.ui.btnViewCV.setEnabled(False)
        self.ui.btnExportResults.setEnabled(False)

        # Simulated in-memory "database" of uploaded CVs
        self.uploaded_cvs = []  # Each item: dict with keys 'filename' and 'upload_time' (datetime)

        # Load initial DB info
        self.load_database_info()

    ## <-----------DATABASE HANDLING----------------------------------------------------------------------------------->
    def clear_database(self):
        """
        Clears the in-memory uploaded_cvs list and updates the UI.
        """
        # TODO: Implement actual database clearing logic when connected

        # For now, just clear the in-memory list
        self.uploaded_cvs.clear()
        self.ui.lblTotalCVs.setText("Total CVs: 0")
        self.ui.lblLastUpload.setText("Last Upload: N/A")
        self.ui.listRecentCVs.clear()
        self.load_database_info()  # Refresh UI after clearing

    def load_database_info(self):
        """
        Loads the database info from the in-memory uploaded_cvs list.
        Updates UI labels and recent uploads list.
        """
        total_cvs = len(self.uploaded_cvs)
        last_upload = (
            max(self.uploaded_cvs, key=lambda x: x["upload_time"])["upload_time"].strftime("%Y-%m-%d %H:%M:%S")
            if self.uploaded_cvs else "N/A"
        )

        recent_uploads = [
            f"{cv['filename']} - {cv['upload_time'].strftime('%Y-%m-%d %H:%M')}"
            for cv in sorted(self.uploaded_cvs, key=lambda x: x["upload_time"], reverse=True)[:5]
        ]

        # Update UI labels
        self.ui.lblTotalCVs.setText(f"Total CVs: {total_cvs}")
        self.ui.lblLastUpload.setText(f"Last Upload: {last_upload}")

        # Clear and update recent CV list widget
        self.ui.listRecentCVs.clear()
        if recent_uploads:
            for item in recent_uploads:
                self.ui.listRecentCVs.addItem(item)
        else:
            self.ui.listRecentCVs.addItem("No recent uploads")

    ## <----------------UPLOAD HANDLERS-------------------------------------------------------------------------------->
    def handle_browse_button(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.ui.lineEditFilePath.setText(file_path)
        else:
            QMessageBox.warning(self, "Warning", "No file selected.")

    def get_file_path(self):
        return self.ui.lineEditFilePath.text().strip()
    
    def handle_upload_button(self):
        file_path = os.path.basename(self.get_file_path())
        if not file_path:
            QMessageBox.warning(self, "Warning", "Please select a file to upload.")
            return

        try:
            # TODO: Parse the file (CSV, JSON, etc.)
            # TODO: Store parsed data into database via get_connection()

            # Simulate adding this file to "database"
            now = datetime.now()
            filename = file_path.split("/")[-1]  # Extract filename from path
            print(f"[UPLOAD] Uploading file: {filename} at {now}")
            self.uploaded_cvs.append({
                "filename": filename,
                "upload_time": now
            })

            # QMessageBox.information(self, "Upload Info", f"File '{filename}' uploaded successfully.")
            self.ui.lineEditFilePath.clear()  # Clear file path input
            self.load_database_info()  # Refresh DB info after upload

        except Exception as e:
            QMessageBox.critical(self, "Upload Error", f"Failed to upload file:\n{e}")
    
    def handle_action_upload_cvs(self):
        self.handle_browse_button()  # Trigger browse action
        if self.get_file_path():
            self.handle_upload_button()  # Trigger upload action
    
    ## <----------------SEARCH HANDLERS-------------------------------------------------------------------------------->
    def get_selected_algorithm(self):
        if self.ui.radioKMP.isChecked():
            return "KMP"
        elif self.ui.radioBoyerMoore.isChecked():
            return "Boyer-Moore"
        elif self.ui.radioAhoCorasick.isChecked():
            return "Aho-Corasick"
        return None

    def get_result_limit(self):
        return self.ui.spinResultLimit.value()

    def get_keywords(self):
        text = self.ui.inputKeywords.text().strip()
        if text:
            return [text]
        return []

    def handle_search_button(self):
        algorithm = self.get_selected_algorithm()
        keywords = self.get_keywords()
        limit = self.get_result_limit()

        if not keywords:
            QMessageBox.warning(self, "Input Error", "Please enter keyword(s) to search.")
            return

        # TODO: Run selected search algorithm on keywords here
        # Placeholder: simulate search results
        dummy_results = [f"Result {i+1} for '{keywords[0]}'" for i in range(limit)]

        # Populate the results list
        self.ui.listResults.clear()
        for res in dummy_results:
            self.ui.listResults.addItem(res)

        # Update performance labels (placeholders)
        self.ui.lblExactMatchTime.setText("🎯 Exact Match : 0.123 ms")  # placeholder
        self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : 0.456 ms")  # placeholder
        self.ui.lblTotalResults.setText(f"📊 Total Results: {len(dummy_results)}")
        self.ui.btnViewSummary.setEnabled(len(dummy_results) > 0)
        self.ui.btnViewCV.setEnabled(len(dummy_results) > 0)
        self.ui.btnExportResults.setEnabled(len(dummy_results) > 0)

    def handle_clear_button(self):
        self.ui.inputKeywords.clear()
        self.ui.listResults.clear()
        self.ui.lblExactMatchTime.setText("🎯 Exact Match : -ms")
        self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : -ms")
        self.ui.lblTotalResults.setText("📊 Total Results: -")

        self.ui.btnViewSummary.setEnabled(False)
        self.ui.btnViewCV.setEnabled(False)
        self.ui.btnExportResults.setEnabled(False)
    
    ## <----------------RESULT HANDLERS-------------------------------------------------------------------------------->
    # Placeholder: View detailed summary of selected result
    def handle_view_summary(self):
        selected = self.get_selected_result()
        if selected:
            QMessageBox.information(self, "Summary", f"Showing summary for:\n{selected}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a result first.")

    # Placeholder: View CV of selected result
    def handle_view_cv(self):
        selected = self.get_selected_result()
        if selected:
            QMessageBox.information(self, "CV View", f"Showing CV for:\n{selected}")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a result first.")

    # Placeholder: Export all search results to file
    def handle_export_results(self):
        # TODO: Implement export (CSV, Excel, etc.)
        QMessageBox.information(self, "Export", "Exporting all results (placeholder).")

    def get_selected_result(self):
        selected_items = self.ui.listResults.selectedItems()
        if selected_items:
            return selected_items[0].text()
        return None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())