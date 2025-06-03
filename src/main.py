import sys
import os
import fitz  
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QMessageBox, 
    QFileDialog, 
    QDialog, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QScrollArea,
    QPushButton
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from ui.home import Ui_MainWindow
from ui.summary import Ui_SummaryWindow  # Assuming you have a separate summary UI file
from ui.cv import Ui_CVViewerWindow  # Assuming yrou have a separate CV UI file
# from db import get_connection  # Uncomment and implement when ready

class CVWindow(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF Viewer")
        self.resize(700, 900)

        if not os.path.exists(file_path):
            return

        self.doc = fitz.open(file_path)
        self.zoom_factor = 1.0  # Start with 100%

        # Scroll Area setup
        self.scroll = QScrollArea(self)
        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)

        self.labels = []
        for page in self.doc:
            pix = page.get_pixmap()
            image = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)
            label = QLabel()
            pixmap = QPixmap.fromImage(image)
            label.setPixmap(pixmap)
            label.original_pixmap = pixmap  # Save original pixmap for scaling
            self.layout.addWidget(label)
            self.labels.append(label)

        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)

        # Zoom buttons
        zoom_in_btn = QPushButton("Zoom In +")
        zoom_out_btn = QPushButton("Zoom Out -")

        zoom_in_btn.clicked.connect(self.zoom_in)
        zoom_out_btn.clicked.connect(self.zoom_out)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(zoom_in_btn)
        btn_layout.addWidget(zoom_out_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.scroll)
        self.setLayout(main_layout)

    def zoom_in(self):
        self.zoom_factor *= 1.25
        self.apply_zoom()

    def zoom_out(self):
        self.zoom_factor /= 1.25
        self.apply_zoom()

    def apply_zoom(self):
        for label in self.labels:
            original_pixmap = label.original_pixmap
            size = original_pixmap.size()
            new_size = size * self.zoom_factor
            scaled_pixmap = original_pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)

class SummaryWindow(QDialog):
    def __init__(self, parent=None, id=None):
        super().__init__(parent)
        self.ui = Ui_SummaryWindow()
        self.ui.setupUi(self)

        # TODO: find nama, email, phone, address, skills, experience, education from database using id

        #placeholder data
        summary_daya = "This is a summary of the CV or result being displayed."
        nama = "John Doe"
        email = "John@email.com"
        # phone = "123-456-7890"
        address = "123 Main St, City, Country"
        skills = ["Python", "Data Analysis", "Machine Learning"]
        experience = ["Company A - Data Scientist (2020-2022)", "Company B - Software Engineer (2018-2020)"]
        education = ["B.Sc. in Computer Science - University X (2014-2018)", "M.Sc. in Data Science - University Y (2018-2020)"]
        self.set_summary_data(summary_daya)
        self.set_name(nama)
        self.set_personal_info(email=email,address=address) # Try phone none
        self.set_skills(skills)
        self.set_experience(experience)
        self.set_education(education)
        self.ui.btnViewFullCV.clicked.connect(self.handle_view_cv)
    
    def handle_view_cv(self):
        """
        Handle the action to view the full CV.
        Opens a new CV viewer window.
        """
        # TODO: Get the file path of the CV associated with the selected result

        # placeholder file path
        file_path = "./data/tes_pdf.pdf"  # Replace with actual file path from database
        # Open a new CV viewer window
        cv_window = CVWindow(file_path, self)
        cv_window.show()


    
    def set_summary_data(self, summary_data):
        """
        Set the summary data to be displayed in the summary window.
        :param data: Dictionary containing summary information.
        """
        # Example of setting data, adjust according to your UI design
        self.ui.textSummary.setText(summary_data)
    
    def set_name(self, name):
        """
        Set the name of the CV or result being summarized.
        :param name: Name of the CV or result.
        """
        self.setWindowTitle(f"Summary for {name}")
        self.ui.lblApplicantName.setText(name)
    
    def set_personal_info(self, email = None, phone = None, address = None):
        """
        Set personal information to be displayed in the summary.
        :param info: Dictionary containing personal information.
        """
        if email:
            self.ui.lblEmail.setText("Email: " + email)
        else:
            self.ui.lblEmail.setText("Email: -")
        if phone:
            self.ui.lblPhone.setText("Phone: " + phone)
        else:
            self.ui.lblPhone.setText("Phone: -")
        if address:
            self.ui.lblAddress.setText("Address: " + address)
        else:
            self.ui.lblAddress.setText("Address: -")
    
    def set_skills(self, skills):
        """
        Set the skills to be displayed in the summary.
        :param skills: List of skills.
        """
        if skills:
            self.ui.listSkill.clear()
            for skill in skills:
                self.ui.listSkill.addItem(skill)
        else:
            self.ui.listSkill.addItem("No skills listed")
    
    def set_experience(self, experience):
        """
        Set the work experience to be displayed in the summary.
        :param experience: List of work experience entries.
        """
        if experience:
            self.ui.listExperience.clear()
            for exp in experience:
                self.ui.listExperience.addItem(exp)
        else:
            self.ui.listExperience.addItem("No work experience listed")
    
    def set_education(self, education):
        """
        Set the education details to be displayed in the summary.
        :param education: List of education entries.
        """
        if education:
            self.ui.listEducation.clear()
            for edu in education:
                self.ui.listEducation.addItem(edu)
        else:
            self.ui.listEducation.addItem("No education listed")

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

        # Initialize UI state
        self.ui.btnViewSummary.setEnabled(False)
        self.ui.btnViewCV.setEnabled(False)

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

        # DEBUG
        print(f"[SEARCH] Searching with {algorithm} for keywords: {', '.join(keywords)} (Limit: {limit})")

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

    def handle_clear_button(self):
        self.ui.inputKeywords.clear()
        self.ui.listResults.clear()
        self.ui.lblExactMatchTime.setText("🎯 Exact Match : -ms")
        self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : -ms")
        self.ui.lblTotalResults.setText("📊 Total Results: -")

        self.ui.btnViewSummary.setEnabled(False)
        self.ui.btnViewCV.setEnabled(False)
    
    ## <----------------RESULT HANDLERS-------------------------------------------------------------------------------->
    # Placeholder: View detailed summary of selected result
    def handle_view_summary(self):
        selected = self.get_selected_result()
        if selected:
            print(f"[VIEW SUMMARY] Selected result: {selected}")

            # Open a new summary window
            summary_window = SummaryWindow(self)
            summary_window.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a result first.")

    # Placeholder: View CV of selected result
    def handle_view_cv(self):
        selected = self.get_selected_result()
        if selected:
            print(f"[VIEW CV] Selected result: {selected}")

            # TODO: Get the file path of the CV associated with the selected result

            # placeholder file path
            file_path = "./data/tes_pdf.pdf"  # Replace with actual file path from database
            # Open a new CV viewer window
            cv_window = CVWindow(file_path, self)
            cv_window.show()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a result first.")

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