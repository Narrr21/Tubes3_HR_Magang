from typing import List


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

def run_search_algorithm(algorithm: str, query: str, limit: int = 10) -> List[ResultData]:
    """
    Runs the specified search algorithm with the given query.

    Args:
        algorithm (str): The name of the search algorithm to run.
        query (str): The search query.
        limit (int, optional): The maximum number of results to return. Defaults to 10.

    Returns:
        List[ResultData]: A list of data matching the search criteria.
    """

    # Placeholder dummy results simulating keyword matches
    results = [
        ResultData(id=1, name="John Doe", keywords={"Python": 5, "Data Analysis": 3}),
        ResultData(id=2, name="Jane Smith", keywords={"Machine Learning": 4, "Python": 2}),
        ResultData(id=3, name="Alice Johnson", keywords={"Data Science": 5, "Python": 1}),
        ResultData(id=4, name="Bob Brown", keywords={"Software Engineering": 3, "Python": 2}),
    ]
    return results[:limit]  # Return only up to the specified limit