from typing import List
from algorithms.KMP import KMP
from algorithms.BM import BM
from algorithms.AhoCorasick import AhoCorasick
from algorithms.Levenshtein import Levenshtein
import time
import os

# DATA STRUCTURES
class SummaryData():
    def __init__(self, nama: str, email: str, phone: str, address: str, skills: List[str], experience: List[str], education: List[str], summary: str):
        self.nama = nama
        self.email = email
        self.phone = phone
        self.address = address
        self.skills = skills
        self.experience = experience
        self.education = education
        self.summary = summary
    
    def to_string(self) -> str:
        return f"[SUMMARY] Nama: {self.nama}\nEmail: {self.email}\nPhone: {self.phone}\nAddress: {self.address}\nSkills: {', '.join(self.skills)}\nExperience: {', '.join(self.experience)}\nEducation: {', '.join(self.education)}\nSummary: {self.summary}"

class ResultData():
    def __init__(self, id: int, name: str, keywords: dict[str, int]):
        self.id = id
        self.name = name
        self.keywords = keywords
    
    def to_string(self) -> str:
        keywords_str = ', '.join([f"{key}: {value}" for key, value in self.keywords.items()])
        return f"[RESULT] ID: {self.id}\nName: {self.name}\nKeywords: {keywords_str}"

class SearchData():
    def __init__(self, id: int, name: str, text: str):
        self.id = id
        self.name = name
        self.text = text

    def to_string(self) -> str:
        return f"[SEARCH] ID: {self.id}\nName: {self.name}\nText: {self.text}"


# FUNCTION DEFINITIONS
def get_summary_data(id:int) -> SummaryData:
    """
    Returns a summary of the data in the database.
    Returns(SummaryData):
    # nama, email, phone, address, skills, experience, education, summary = get_summary_data(id)

    # Example:
    summary = "This is a summary of the CV or result being displayed."
    nama = "John Doe"
    email = "John@email.com"
    phone = "123-456-7890"
    address = "123 Main St, City, Country"
    skills = ["Python", "Data Analysis", "Machine Learning"]
    experience = ["Company A - Data Scientist (2020-2022)", "Company B - Software Engineer (2018-2020)"]
    education = ["B.Sc. in Computer Science - University X (2014-2018)", "M.Sc. in Data Science - University Y (2018-2020)"]
    """
    # TODO: Implement the logic to fetch data from the database

    # placeholder dummy data
    data = SummaryData(
        nama=f"John Doe {id}",
        email="tes@gmail.com",
        phone="123-456-7890",
        address="123 Main St, City, Country",
        skills=["Python11111111111111111111111111111111111111111111111111111111111111111111111", "Data Analysis is aadjajdjajdjsajdjasjdsjjsdjsajdjasjdjasjdjasjdasdasdasd", "Machine Learning"],
        experience=["Company A - Data Scientist (2020-2022)", "Company B - Software Engineer (2018-2020)"],
        education=["B.Sc. in Computer Science - University X (2014-2018)", "M.Sc. in Data Science - University Y (2018-2020)"],
        summary="This is a summary of the CV or result being displayed."
    )
    return data.nama, data.email, data.phone, data.address, data.skills, data.experience, data.education, data.summary

def get_file_path(id: int) -> str:
    """
    Returns the file path of the CV or result being displayed.
    Args:
        id (int): The ID of the CV or result.
    Returns:
        str: The file path of the CV or result.
    """

    # placeholder dummy file path
    file_path = "./data/tes_pdf.pdf"
    return file_path

def fuzzy_match(keyword: str, text: str) -> int:
    """
    Performs a fuzzy match for the given keyword.
    Args:
        keyword (str): The keyword to be matched.
        text (str): The text in which to search for the keyword.
    Returns:
        int: The number of matches found.
    """
    lv = Levenshtein()
    return lv.count_occurrence(text, keyword)

def run_search_algorithm(algorithm: str, keyword: list[str], limit: int = 10) -> tuple[List[ResultData], int, int]:
    """
    Runs the specified search algorithm with the given query.

    Args:
        algorithm (str): The name of the search algorithm to run.
        keyword (list of string): Keywords that need to be searched.
        limit (int, optional): The maximum number of results to return. Defaults to 10.

    Returns:
        List[ResultData]: A list of data matching the search criteria.
        int : Exact Match Time
        int : Fuzzy Match Time
    """

    # TODO: Take Search Data from Database

    # placeholder
    search = [
        SearchData(
            id=1,
            name="John Doe",
            text="In a world where everything changes constantly, finding consistency in values and vision remains paramount to achieving lasting success."
        ),
        SearchData(
            id=2,
            name="Jane Smith",
            text="From the farthest corners of forgotten libraries to the cutting edge of neural networks, knowledge flows unceasingly like a river carving its legacy through stone."
        ),
        SearchData(
            id=3,
            name="Carlos Nguyen",
            text="Despite the cacophony of opinions in digital forums, the quiet truth of well-reasoned evidence continues to resonate with those who seek clarity amidst confusion."
        ),
        SearchData(
            id=4,
            name="Aisha Ibrahim",
            text="It was not the brightest star that guided the explorers, but the one that held steady through storms and silence, whispering of lands uncharted yet deeply yearned for."
        ),
        SearchData(
            id=5,
            name="Liam Tanaka",
            text="Quantum possibilities dance beneath the surface of everyday decisions, subtly influencing outcomes in ways no deterministic algorithm can entirely predict or explain."
        )
    ]
    exact_time = 0
    fuzzy_time = 0
    fuzzy_search = False
    results = []
    
    for data in search:
        start_time = time.time()
        res = ResultData(id=data.id, name=data.name, keywords={})
        for key in keyword:
            res.keywords[key] = 0

        if (algorithm == "KMP"):
            res.keywords = KMP.search_multi_pattern(data.text, keyword)
        elif (algorithm == "BM"):
            res.keywords = BM.search_multi_pattern(data.text, keyword)
        elif (algorithm == "AhoCorasick"):
             res.keywords = AhoCorasick.search_multi_pattern(data.text, keyword)
        exact_time += (time.time() - start_time) * 1000
        for key in keyword:
            if res.keywords[key] == 0:
                start_time = time.time()
                res.keywords = Levenshtein.search_multi_pattern(data.text, keyword)
                fuzzy_time += (time.time() - start_time) * 1000
        results.append(res)
    
    
    # TODO: sorting results based on keyword occurences

    return results[:limit], round(exact_time, 6), round(fuzzy_time, 6)
    # Placeholder dummy results simulating keyword matches
    # results = [
    #     ResultData(id=1, name="John Doe", keywords={"Python": 5, "Data Analysis": 3}),
    #     ResultData(id=2, name="Jane Smith", keywords={"Machine Learning": 4, "Python": 2}),
    #     ResultData(id=3, name="Alice Johnson", keywords={"Data Science": 5, "Python": 1}),
    #     ResultData(id=4, name="Bob Brown", keywords={"Software Engineering": 3, "Python": 2}),
    # ]
    # return results[:limit], 123, 456

def add_file(path_to_file:str, id_applicant: int) -> bool:
    """
    Adds a file to the database.
    Args:
        path_to_file (str): The path to the file to be added.
        id_applicant (int): The ID of the applicant to whom the file belongs.
    Returns:
        bool: True if the file was added successfully, False otherwise.
    """
    try:
        if not os.path.exists(path_to_file):
            raise FileNotFoundError(f"File {path_to_file} does not exist.")
        
        # TODO: Implement the logic to add the file to the database
        
        print(f"File {path_to_file} added to the database.")
    except Exception as e:
        print(f"Error adding file: {e}")
        return False
    return True

def add_folder(path_to_folder:str, uploaded_cvs:list[dict]) -> bool:
    """
    Adds all files in a folder to the database.
    Args:
        path_to_folder (str): The path to the folder containing files to be added.
    Returns:
        bool: True if the files were added successfully, False otherwise.
    """
    try :
        if not os.path.exists(path_to_folder):
            raise FileNotFoundError(f"Folder {path_to_folder} does not exist.")
        
        # TODO: Implement the logic to add all files in the folder to the database

        print(f"All files in folder {path_to_folder} added to the database.")
        # Update Frontend
        for file in os.listdir(path_to_folder):
            if file.endswith(".pdf"):
                filename = os.path.join(path_to_folder, file)
                now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                uploaded_cvs.append({
                    "filename": filename,
                    "upload_time": now
                })
        return True
    except Exception as e:
        print(f"Error adding folder: {e}")
        return False

def clear_database() -> bool:
    """
    Clears the database.
    Returns:
        bool: True if the database was cleared successfully, False otherwise.
    """
    try:
        # TODO: Implement the logic to clear the database

        return True
    except Exception as e:
        print(f"Error clearing database: {e}")
        return False

def load_database() -> bool:
    """
    Loads the database.
    Returns:
        bool: True if the database was loaded successfully, False otherwise.
    """
    try:
        # TODO: Implement the logic to load the database

        print("Database loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading database: {e}")
        return False