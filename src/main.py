import sys
import os
import re
import pymupdf as fitz
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QFileDialog, 
    QDialog, 
    QWidget, 
    QVBoxLayout, 
    QHBoxLayout, 
    QLabel, 
    QScrollArea,
    QPushButton,
    QListWidgetItem,
    QListWidget
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QStringListModel, QTimer
from ui.home import Ui_MainWindow
from ui.summary import Ui_SummaryWindow
from ui.toast import Toast
from ui.wrapper import Wrapper
from interface import *

class CVWindow(QDialog):
    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("PDF Viewer")
        self.resize(700, 900)

        if not os.path.exists(file_path):
            return

        self.doc = fitz.open(file_path)
        self.zoom_factor = 1.0

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
            label.original_pixmap = pixmap
            self.layout.addWidget(label)
            self.labels.append(label)

        self.scroll.setWidget(self.container)
        self.scroll.setWidgetResizable(True)

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

        self.id = id
        nama, email, phone, address, skills, experience, education, summary = get_summary_data(id)
        
        self.set_summary_data(summary)
        self.set_name(nama)
        self.set_personal_info(email, phone, address)
        self.set_skills(skills)
        self.set_experience(experience)
        self.set_education(education)
        self.ui.btnViewFullCV.clicked.connect(self.handle_view_cv)
    
    def handle_view_cv(self):
        file_path = get_file_path(self.id)

        cv_window = CVWindow(file_path, self)
        cv_window.show()


    
    def set_summary_data(self, summary_data):
        self.ui.textSummary.setText(summary_data)
    
    def set_name(self, name):
        self.setWindowTitle(f"Summary for {name}")
        self.ui.lblApplicantName.setText(name)
    
    def set_personal_info(self, email = None, phone = None, address = None):
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
        print(f"[Skills] : {skills}\n")
        self.ui.listSkill.clear()
        self.ui.listSkill.setItemDelegate(Wrapper(self.ui.listSkill))  # Pass parent to delegate
        self.ui.listSkill.setWordWrap(True)
        self.ui.listSkill.setUniformItemSizes(False)
        self.ui.listSkill.setSelectionMode(QListWidget.NoSelection)
        if skills:
            for skill in skills:
                list_item = QListWidgetItem(skill)
                self.ui.listSkill.addItem(list_item)
        else:
            self.ui.listSkill.addItem("No skills listed")

    def set_experience(self, experience):
        print(f"[Experience] : {experience}\n") # DEBUG

        self.ui.listExperience.clear() 
        
        self.ui.listExperience.setItemDelegate(Wrapper(self.ui.listExperience)) # Pass parent to delegate

        self.ui.listExperience.setWordWrap(True)
        self.ui.listExperience.setUniformItemSizes(False)
        self.ui.listExperience.setSelectionMode(QListWidget.NoSelection)

        if experience:
            for item_text in experience:
                list_item = QListWidgetItem(item_text)
                self.ui.listExperience.addItem(list_item)
        else:
            self.ui.listExperience.addItem("No work experience listed")

    def set_education(self, education):
        print(f"[Education] : {education}\n")
        self.ui.listEducation.clear()
        self.ui.listEducation.setItemDelegate(Wrapper(self.ui.listEducation))  # Pass parent to delegate
        self.ui.listEducation.setWordWrap(True)
        self.ui.listEducation.setUniformItemSizes(False)
        self.ui.listEducation.setSelectionMode(QListWidget.NoSelection)
        if education:
            for item_text in education:
                list_item = QListWidgetItem(item_text)
                self.ui.listEducation.addItem(list_item)
        else:
            self.ui.listEducation.addItem("No education history listed")

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

        self.uploaded_cvs = []
        clear_database()
        conn = get_connection()  # Initialize database connection
        seed_database()
        conn.close()

        # Load initial DB info
        self.load_database_info()

    ## <-----------DATABASE HANDLING----------------------------------------------------------------------------------->
    def clear_database(self):
        response = clear_database()
        if not response:
            toast = Toast("Failed to clear database", duration=3000, parent=self)
            toast.show_above(self)
            return
        else:
            toast = Toast("Database cleared successfully", duration=3000, parent=self)
            toast.show_above(self)
        self.uploaded_cvs.clear()
        self.ui.lblTotalCVs.setText("Total CVs: 0")
        self.ui.lblLastUpload.setText("Last Upload: N/A")
        self.ui.listRecentCVs.clear()
        self.load_database_info()

    def load_database_info(self):
        response, count = load_database()
        if not response:
            toast = Toast("Failed to load database info", duration=3000, parent=self)
            toast.show_above(self)
            return

        total_cvs = count
        last_upload = (
            max(self.uploaded_cvs, key=lambda x: x["upload_time"])["upload_time"].strftime("%Y-%m-%d %H:%M:%S")
            if self.uploaded_cvs else "N/A"
        )

        recent_uploads = [
            f"{cv['filename']} - {cv['upload_time'].strftime('%Y-%m-%d %H:%M')}"
            for cv in sorted(self.uploaded_cvs, key=lambda x: x["upload_time"], reverse=True)[:5]
        ]

        self.ui.lblTotalCVs.setText(f"Total CVs: {total_cvs}")
        self.ui.lblLastUpload.setText(f"Last Upload: {last_upload}")

        self.ui.listRecentCVs.clear()
        if recent_uploads:
            for item in recent_uploads:
                self.ui.listRecentCVs.addItem(item)
        else:
            self.ui.listRecentCVs.addItem("No recent uploads")

    ## <----------------UPLOAD HANDLERS-------------------------------------------------------------------------------->
    def handle_browse_button(self):
        if self.ui.checkFolderMode.isChecked():
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")
            if folder_path:
                self.ui.lineEditFilePath.setText(folder_path)
            else:
                toast = Toast("No folder selected.", duration=3000, parent=self)
                toast.show_above(self)
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
            if file_path:
                self.ui.lineEditFilePath.setText(file_path)
            else:
                toast = Toast("No file selected.", duration=3000, parent=self)
                toast.show_above(self)



    def get_file_path(self):
        return self.ui.lineEditFilePath.text().strip()
    
    def fade_border(self, widget=None):
        steps = 10
        interval = 200
        for i in range(steps):
            opacity = 1 - i / steps
            red_value = int(255 * opacity)
            style = f"border: 2px solid rgba({red_value}, 0, 0, 150);"
            QTimer.singleShot(i * interval, lambda s=style: widget.setStyleSheet(s))
        QTimer.singleShot(steps * interval, lambda: widget.setStyleSheet(""))

    def get_id_applicant(self):
        text = self.ui.inputIDApplicants.text().strip()
        if not text.isdigit():
            self.fade_border(self.ui.inputIDApplicants)
            toast = Toast("Please enter a valid ID applicant", duration=3000, parent=self)
            toast.show_above(self)
            return None
        else:
            self.ui.inputIDApplicants.setStyleSheet("")
            return text

    
    def handle_upload_button(self):        
        file_path = os.path.basename(self.get_file_path())
        if self.ui.checkFolderMode.isChecked():
            self.handle_upload_folder()
            return
        if not file_path:
            toast = Toast("Please select a file to upload", duration=3000, parent=self)
            toast.show_above(self)
            self.fade_border(self.ui.lineEditFilePath)
            return

        try:
            now = datetime.now()
            filename = file_path.split("/")[-1]
            id_applicant = self.get_id_applicant()

            # TODO: Validate id_applicant before proceeding
            if not id_applicant:
                return
            
            if not filename.lower().endswith('.pdf'):
                toast = Toast("Only PDF files are allowed", duration=3000, parent=self)
                toast.show_above(self)
                self.fade_border(self.ui.lineEditFilePath)
                self.ui.lineEditFilePath.clear()
                return
            
            response = add_file(self.get_file_path(), id_applicant)

            if response:
                pass
            else:
                toast = Toast("Failed to upload file", duration=3000, parent=self)
                toast.show_above(self)
                return

            print(f"[UPLOAD] Uploading file: {filename} at {now} by id applicant {id_applicant}")  # DEBUG
            self.uploaded_cvs.append({
                "filename": filename,
                "upload_time": now
            })

            self.ui.lineEditFilePath.clear()
            self.ui.inputIDApplicants.clear()
            print(f"[UPLOAD] File {filename} uploaded successfully at {now}.")  # DEBUG
            toast = Toast("File uploaded successfully", duration=3000, parent=self)
            toast.show_above(self)
            self.load_database_info()

        except Exception as e:
            toast = Toast("Failed to upload file:\n" + str(e), duration=3000, parent=self)
            toast.show_above(self)
    
    def handle_upload_folder(self):
        folder_path = self.get_file_path()
        if not folder_path:
            toast = Toast("Please select a folder to upload", duration=3000, parent=self)
            toast.show_above(self)
            self.fade_border(self.ui.lineEditFilePath)
            return

        try:
            folderName = os.path.basename(folder_path)
            response = add_folder(folder_path, self.uploaded_cvs)

            if response:
                toast = Toast("Folder uploaded successfully", duration=3000, parent=self)
                toast.show_above(self)
            else:
                toast = Toast("Failed to upload file", duration=3000, parent=self)
                toast.show_above(self)
                return
            self.ui.lineEditFilePath.clear()
            print(f"[UPLOAD] Folder {folderName} uploaded successfully.")
            self.load_database_info()
        except Exception as e:
            toast = Toast("Failed to upload folder:\n" + str(e), duration=3000, parent=self)
            toast.show_above(self)

    def handle_action_upload_cvs(self):
        self.handle_browse_button()
        if self.get_file_path():
            self.handle_upload_button()
    
    ## <----------------SEARCH HANDLERS-------------------------------------------------------------------------------->
    def get_selected_algorithm(self):
        if self.ui.radioKMP.isChecked():
            return "KMP"
        elif self.ui.radioBoyerMoore.isChecked():
            return "BM"
        elif self.ui.radioAhoCorasick.isChecked():
            return "AhoCorasick"
        return None

    def get_result_limit(self):
        return self.ui.spinResultLimit.value()

    def get_keywords(self):
        raw_text = self.ui.inputKeywords.text()
        words = re.split(r'[,\s]+', raw_text.strip())
        keywords = [word for word in words if word]
        print(f"[KEYWORDS] Parsed keywords: {keywords}")

        if keywords:
            return keywords
        else:
            return []


    def handle_search_button(self):
        algorithm = self.get_selected_algorithm()
        keywords = self.get_keywords()
        limit = self.get_result_limit()

        # DEBUG
        print(f"[SEARCH] Searching with {algorithm} for keywords: {', '.join(keywords)} (Limit: {limit})")

        if not keywords:
            self.fade_border(self.ui.inputKeywords)
            toast = Toast("Please enter keyword to search", duration=3000, parent=self)
            toast.show_above(self)
            return
        toast = Toast("Searching...", duration=3000, parent=self)
        toast.show_above(self)
        results, exact_time, fuzzy_time = run_search_algorithm(algorithm, keywords, limit)

        self.ui.listResults.clear()
        if len(results) == 0:
            toast = Toast("No results found", duration=3000, parent=self)
            toast.show_above(self)
            self.ui.listResults.addItem("No results found")

        for res in results:
            display_text = f"{res.name} (ID: {res.id})"
            if len(res.keywords) > 0:
                display_text += " - Keywords: " + ", ".join(f"{k} ({v})" for k, v in res.keywords.items())
            else:
                display_text += " - No keywords found"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, res)
            self.ui.listResults.addItem(item)

        if exact_time != None:
            self.ui.lblExactMatchTime.setText("🎯 Exact Match : " + str(exact_time) + " ms")
        else:
            self.ui.lblExactMatchTime.setText("🎯 Exact Match : -ms")

        if fuzzy_time != None:
            self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : " + str(fuzzy_time) + " ms")
        else:
            self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : -ms")
        
        if len(results) > 0:
            self.ui.lblTotalResults.setText(f"📊 Total Results: {len(results)}")
        else:
            self.ui.lblTotalResults.setText("📊 Total Results: -")
        
        self.ui.btnViewSummary.setEnabled(len(results) > 0)
        self.ui.btnViewCV.setEnabled(len(results) > 0)
        toast = Toast("Searching Done!!", duration=3000, parent=self)
        toast.show_above(self)

    def handle_clear_button(self):
        self.ui.inputKeywords.clear()
        self.ui.listResults.clear()
        self.ui.lblExactMatchTime.setText("🎯 Exact Match : -ms")
        self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : -ms")
        self.ui.lblTotalResults.setText("📊 Total Results: -")

        self.ui.btnViewSummary.setEnabled(False)
        self.ui.btnViewCV.setEnabled(False)

    ## <----------------RESULT HANDLERS-------------------------------------------------------------------------------->
    def handle_view_summary(self):
        selected = self.get_selected_result()
        if selected:
            print(f"[VIEW SUMMARY] Selected result: name={selected.name}, id={selected.id}")

            summary_window = SummaryWindow(self, id=selected.id)
            summary_window.show()
        else:
            toast = Toast("Please select a result first.", duration=3000, parent=self)
            toast.show_above(self)

    def handle_view_cv(self):
        selected = self.get_selected_result()
        if selected:
            print(f"[VIEW CV] Selected result: name={selected.name}, id={selected.id}")

            file_path = get_file_path(selected.id)

            cv_window = CVWindow(file_path, self)
            cv_window.show()
        else:
            toast = Toast("Please select a result first.", duration=3000, parent=self)
            toast.show_above(self)

    def get_selected_result(self):
        selected_items = self.ui.listResults.selectedItems()
        if selected_items:
            res = selected_items[0].data(Qt.UserRole)
            return res
        return None

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())