import sys
import os
import fitz  
import re
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
    QPushButton,
    QListWidgetItem,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QStringListModel, QTimer
from ui.home import Ui_MainWindow
from ui.summary import Ui_SummaryWindow  # Assuming you have a separate summary UI file
# from db import get_connection  # Uncomment and implement when ready
from ui.toast import Toast  # Assuming you have a Toast class for notifications
from ui.wrapper import Wrapper  # Assuming you have a custom item delegate for list widgets
from interface import (
    get_summary_data,       # get summary data from database by id
    get_file_path,          # get file path of CV from database by id
    run_search_algorithm,   # run search algorithm on keywords
    add_file,               # add file to database
    add_folder,             # add files in folder to database
    clear_database,          # clear database
    load_database          # load database info
)

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
        """
        Handle the action to view the full CV.
        Opens a new CV viewer window.
        """
        file_path = get_file_path(self.id)

        cv_window = CVWindow(file_path, self)
        cv_window.show()


    
    def set_summary_data(self, summary_data):
        """
        Set the summary data to be displayed in the summary window.
        :param data: Long string containing the summary information.
        """
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
        :param email: Email address of the applicant.
        :param phone: Phone number of the applicant.
        :param address: Address of the applicant.
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
        :param skills: List of skills (strings) to be displayed.
        """
        print(f"[Skills] : {skills}\n")  # DEBUG
        model = QStringListModel()
        if skills:
            model.setStringList(skills)
        else:
            model.setStringList(["No skills listed"])
        self.ui.listSkill.setItemDelegate(Wrapper())
        self.ui.listSkill.setModel(model)

    def set_experience(self, experience):
        """
        Set the work experience to be displayed in the summary.
        :param experience: List of work experience (strings) to be displayed.
        """
        print(f"[Experience] : {experience}\n")  # DEBUG
        # experience = ["Company Name August 2006 to May 2017 Reading Teacher City , State Reading Endorsed Helped students develop and improve study methods and habits. Used a variety of teaching methods such as lectures, discussions and demonstrations. Improved 97% reading scores to satisfy graduation requirements Met with parents and guardians to discuss students' progress at least once per semester. Established positive relationships with students, parents, colleagues and administrators. Encouraged discussion of class material to promote critical thinking and academic success Implemented remedial programs for students requiring extra help Participated in regular professional development training to keep up-to-date with new teaching. Company Name August 2013 to June 2016 Sunshine Social Chairperson City , State Collected faculty and staff dues Planned and organized all school events, i.e. Parent Conference Night meals, Birthdays, Retirement Celebration, End of the year luncheon Morale Booster Company Name August 2010 to September 2012 On-Site Professional Developer City , State Led 110 students to improve test scores by more than 37% during the first semester of the 2015-2016 academic year. Offered specific training programs to help teachers maintain and improve in classroom management and student success Used a variety of teaching methods such as lectures, discussions and demonstrations to promote student success Provided onsite training for teachers and staff Planned and executed book studies and faculty trainings Company Name August 2006 to June 2009 Girls JV Basketball Coach City , State Motivated and encouraged student athletes to do their best during practices and games ' Met with prospective student-athletes to discuss their experience and goals Created and ran up-to-date and relevant drills Monitored the academic performance of student-athletes in addition to their athletic progress Helped develop each participant's physical and psychological fitness Maintained and updated attendance forms and insurance records Company Name July 2002 to May 2006 VE Teacher City , State Employed a variety of assessment tools and strategies to improve instruction in the classroom Attended a variety of professional development workshops centered on learning goals, classroom management, student motivation and engaging learning activities. Served on various committees and projects including Sunshine Committee as the on-site Chairperson Facilitated activities that developed students' physical, emotional and social growth. Encouraged students to be understanding with others. Used the positive reinforcement method to redirect poor behavior. Conducted small group and individual classroom activities with students based on differentiated learning needs. Worked with an average of 20 students per class. Participated in ongoing staff training sessions. Company Name August 2002 to May 2006 Sunshine Social Chairperson City , State Collected faculty and staff dues Planned and organized all school events, i.e. Parent Conference Night meals, Birthdays, Retirement Celebration, End of the year luncheon Morale Booster Company Name August 2002 to May 2006 Girls Basketball Coach City , State Motivated and encouraged student athletes to do their best during practices and games Met with prospective student-athletes to discuss their experience and goals Created and ran up-to-date and relevant drills Monitored the academic performance of student-athletes in addition to their athletic progress Helped develop each participant's physical and psychological fitness Maintained and updated attendance forms and insurance records"]
        experience = ["Company Name August 2006 to May 2017 Reading Teacher City"]
        model = QStringListModel()
        if experience:
            model.setStringList(experience)
        else:
            model.setStringList(["No work experience listed"])
        self.ui.listExperience.setItemDelegate(Wrapper())
        self.ui.listExperience.setModel(model)

    def set_education(self, education):
        """
        Set the education details to be displayed in the summary.
        :param education: List of education (strings) to be displayed.
        """
        print(f"[Education] : {education}\n")  # DEBUG
        model = QStringListModel()
        if education:
            model.setStringList(education)
        else:
            model.setStringList(["No education listed"])
        self.ui.listEducation.setItemDelegate(Wrapper())
        self.ui.listEducation.setModel(model)

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
        self.uploaded_cvs = []

        # Load initial DB info
        clear_database()
        self.load_database_info()

    ## <-----------DATABASE HANDLING----------------------------------------------------------------------------------->
    def clear_database(self):
        """
        Clears the in-memory uploaded_cvs list and updates the UI.
        """
        response = clear_database()  # Call to clear the database in the backend
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
        self.load_database_info()  # Refresh UI after clearing

    def load_database_info(self):
        """
        Loads the database info from the in-memory uploaded_cvs list.
        Updates UI labels and recent uploads list.
        """
        response = load_database()
        if not response:
            toast = Toast("Failed to load database info", duration=3000, parent=self)
            toast.show_above(self)
            return
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
        if self.ui.checkFolderMode.isChecked():  # Folder mode
            folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", "")
            if folder_path:
                self.ui.lineEditFilePath.setText(folder_path)
            else:
                toast = Toast("No folder selected.", duration=3000, parent=self)
                toast.show_above(self)
        else:  # File mode
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
        interval = 200  # ms
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
            # Valid input
            self.ui.inputIDApplicants.setStyleSheet("")
            return text

    
    def handle_upload_button(self):
        clear_database()
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
            # Simulate adding this file to "database"
            now = datetime.now()
            filename = file_path.split("/")[-1]  # Extract filename from path
            id_applicant = self.get_id_applicant()  # Placeholder for ID applicant retrieval logic

            # TODO: Validate id_applicant before proceeding
            
            if not filename.lower().endswith('.pdf'):
                toast = Toast("Only PDF files are allowed", duration=3000, parent=self)
                toast.show_above(self)
                self.fade_border(self.ui.lineEditFilePath)
                self.ui.lineEditFilePath.clear()  # Clear file path input
                self.ui.inputIDApplicants.clear()  # Clear ID input
                return
            
            if not id_applicant:
                return
            
            response = add_file(file_path, id_applicant)

            if response:
                toast = Toast("File uploaded successfully", duration=3000, parent=self)
                toast.show_above(self)
            else:
                toast = Toast("Failed to upload file", duration=3000, parent=self)
                toast.show_above(self)
                return

            print(f"[UPLOAD] Uploading file: {filename} at {now} by id applicant {id_applicant}")  # DEBUG
            self.uploaded_cvs.append({
                "filename": filename,
                "upload_time": now
            })

            self.ui.lineEditFilePath.clear()  # Clear file path input
            self.ui.inputIDApplicants.clear()  # Clear ID input
            print(f"[UPLOAD] File {filename} uploaded successfully at {now}.")  # DEBUG
            self.load_database_info()  # Refresh DB info after upload

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
            folderName = os.path.basename(folder_path)  # Extract folder name from path
            response = add_folder(folder_path, self.uploaded_cvs)

            if response:
                toast = Toast("Folder uploaded successfully", duration=3000, parent=self)
                toast.show_above(self)
            else:
                toast = Toast("Failed to upload file", duration=3000, parent=self)
                toast.show_above(self)
                return
            self.ui.lineEditFilePath.clear()  # Clear file path input
            print(f"[UPLOAD] Folder {folderName} uploaded successfully.")  # DEBUG
        except Exception as e:
            toast = Toast("Failed to upload folder:\n" + str(e), duration=3000, parent=self)
            toast.show_above(self)

    def handle_action_upload_cvs(self):
        clear_database()
        self.handle_browse_button()  # Trigger browse
        if self.get_file_path():
            self.handle_upload_button()  # Trigger upload
    
    ## <----------------SEARCH HANDLERS-------------------------------------------------------------------------------->
    def get_selected_algorithm(self):
        if self.ui.radioKMP.isChecked():
            return "KMP"
        elif self.ui.radioBoyerMoore.isChecked():
            return "BM"
        elif self.ui.radioAhoCorasick.isChecked():
            return "Aho-Corasick"
        return None

    def get_result_limit(self):
        return self.ui.spinResultLimit.value()

    def get_keywords(self):
        raw_text = self.ui.inputKeywords.text()
        words = re.split(r'[,\s]+', raw_text.strip())
        keywords = [word for word in words if word]
        print(f"[KEYWORDS] Parsed keywords: {keywords}")  # DEBUG

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

        results, exact_time, fuzzy_time = run_search_algorithm(algorithm, keywords, limit)

        self.ui.listResults.clear()
        for res in results:
            display_text = f"{res.name} (ID: {res.id})"
            if res.keywords:
                display_text += " - Keywords: " + ", ".join(f"{k} ({v})" for k, v in res.keywords.items())
            else:
                display_text += " - No keywords found"
            item = QListWidgetItem(display_text)
            item.setData(Qt.UserRole, res)
            self.ui.listResults.addItem(item)

        if exact_time != None:
            self.ui.lblExactMatchTime.setText("🎯 Exact Match : " + str(exact_time) + " ms")  # placeholder
        else:
            self.ui.lblExactMatchTime.setText("🎯 Exact Match : -ms")

        if fuzzy_time != None:
            self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : " + str(fuzzy_time) + " ms")  # placeholder
        else:
            self.ui.lblFuzzyMatchTime.setText("🔍 Fuzzy Match : -ms")
        
        if len(results) > 0:
            self.ui.lblTotalResults.setText(f"📊 Total Results: {len(results)}")
        else:
            self.ui.lblTotalResults.setText("📊 Total Results: -")
        
        self.ui.btnViewSummary.setEnabled(len(results) > 0)
        self.ui.btnViewCV.setEnabled(len(results) > 0)

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