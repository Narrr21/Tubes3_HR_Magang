from typing import List
from KMP import KMP
import time

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

class ResultData():
    def __init__(self, id: int, name: str, keywords: dict[str, int]):
        self.id = id
        self.name = name
        self.keywords = keywords

class SearchData():
    def __init__(self, id: int, name: str, text: str):
        self.id = id
        self.name = name
        self.text = text


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
        skills=["Python", "Data Analysis", "Machine Learning"],
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
    fuzzy = True
    exact_time = None
    fuzzy_time = None
    results = []
    ## KMP
    if (algorithm == "KMP"):
        start_time = time.time()
        for data in search:
            res = ResultData(id=data.id, name=data.name, keywords={})
            kmp = KMP("")
            res.keywords = kmp.search_multi_pattern(data.text, keyword)
            if not res.keywords == {}:
                fuzzy = False
            results.append(res)
        exact_time = time.time() - start_time
    elif (algorithm == "BM"):
        ...
    else:
        ...
    
    if fuzzy:
        # TODO: fuzzy match here
        ...
    
    return results[:limit], exact_time, fuzzy_time
    # Placeholder dummy results simulating keyword matches
    # results = [
    #     ResultData(id=1, name="John Doe", keywords={"Python": 5, "Data Analysis": 3}),
    #     ResultData(id=2, name="Jane Smith", keywords={"Machine Learning": 4, "Python": 2}),
    #     ResultData(id=3, name="Alice Johnson", keywords={"Data Science": 5, "Python": 1}),
    #     ResultData(id=4, name="Bob Brown", keywords={"Software Engineering": 3, "Python": 2}),
    # ]
    # return results[:limit], 123, 456