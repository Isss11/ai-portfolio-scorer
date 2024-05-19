import google.generativeai as genai
import re
import json

from src.config import GOOGLE_API_KEY

jsonQueryExample = {
    "readability": 5,
    "bestProgrammingPractices": 7,
    "maintainability": 3,
    "feedback": "Feedback is written here.",
}

llm: genai.GenerativeModel = None  # type: ignore


class AIQuery:
    def __init__(self) -> None:
        global llm
        llm = llm or self.getGemini()

    # Sets up API key for Gemini, ready to query
    def getGemini(self):
        genai.configure(api_key=GOOGLE_API_KEY)

        return genai.GenerativeModel("gemini-pro")

    def getNote(self, category, score):
        # category = "impact"
        objectFormat = {
            "note": "A note is here.",
        }

        query = f"Can you give a message about my score of {score} out of 100 for my overall '{category}' on GitHub in 8 words or less. It should not have any apostrophes. The response should be in the format:\n {objectFormat}"

        note = llm.generate_content(query).text

        note = self.extract_json(note)

        return note[0]["note"]

    # Obtains a JSON response on a variety of grades from Gemini
    def getFeedback(self, stringifiedFiles):
        query = f"""
Score the following code from different files on code readability with an integer, with the maximum value being 10.
Then score the following code on best programming practices for the given programming language (such as object-oriented programming if the programming language used is Java, Kotlin, or another OOP language) with an integer, with the maximum value being 10.
Than score the following code on maintainability with an integer, with the maximum value being 10.
Also provide some general feedback on the code itself in a 'feedback' object -- it should be a maximum of 25 words.
Return it as a JSON object exactly as in this example:
{jsonQueryExample}
The code to score is:
{stringifiedFiles}""".strip()

        feedback = llm.generate_content(query)
        feedback = feedback.text

        feedback = self.extract_json(feedback)

        return feedback[0]

    # Reference for JSON fix: https://learnwithhasan.com/consistent-json-gemini-python/
    def extract_json(self, text_response):
        # This pattern matches a string that starts with '{' and ends with '}'
        pattern = r"\{[^{}]*\}"
        text = text_response.replace("'", '"')

        matches = re.finditer(pattern, text)
        json_objects = []

        for match in matches:
            json_str = match.group(0)
            try:

                print(json_str)
                # Validate if the extracted string is valid JSON
                json_obj = json.loads(json_str)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                # Extend the search for nested structures
                extended_json_str = self.extend_search(text_response, match.span())
                try:
                    json_obj = json.loads(extended_json_str)
                    json_objects.append(json_obj)
                except json.JSONDecodeError:
                    # Handle cases where the extraction is not valid JSON
                    continue

        if json_objects:
            return json_objects
        else:
            return None  # Or handle this case as you prefer

    # Reference for JSON fix: https://learnwithhasan.com/consistent-json-gemini-python/
    def extend_search(self, text, span):
        # Extend the search to try to capture nested structures
        start, end = span
        nest_count = 0
        for i in range(start, len(text)):
            if text[i] == "{":
                nest_count += 1
            elif text[i] == "}":
                nest_count -= 1
                if nest_count == 0:
                    return text[start : i + 1]
        return text[start:end]

    # Creates string of files to be used in the prompt, given the file paths.
    def getStringifiedFiles(self, fileContent):
        stringifiedFiles = ""

        for language in fileContent:
            files = fileContent[language]["files"]

            for file in files:
                stringifiedFiles += file["content"]
                stringifiedFiles += "\n\n"

        return stringifiedFiles

    # Takes a list of file paths and obtains a score and feedback from Gemini on a series of criteria
    def gradeFiles(self, filePaths):
        stringifiedFiles = self.getStringifiedFiles(filePaths)
        feedback = self.getFeedback(stringifiedFiles, filePaths[0])

        return feedback
