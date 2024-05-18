import os
import google.generativeai as genai
import re
import json

exampleJSON = {
    "readability": {
    "score": 8,
    "feedback": "test.py is generally well-formatted and uses clear variable names. Docstrings are present, but type hints could improve readability further. Consider using a dictionary comprehension in getGeneralInfo for a more concise approach."
    },
    "oop": {
    "score": 7,
    "feedback": "myapp.vue demonstrates basic OOP concepts like encapsulation and abstraction. However, reusability can be improved by adding methods for retrieving more data or calculations."
    },
    "maintainability": {
    "score": 8,
    "feedback": "The code has good modularity due to the class structure. Error handling and unit tests would further enhance maintainability."
    }
}

class AIScorer:
    def __init__(self) -> None:
        self.llm = self.getGemini()
    
    # Sets up API key for Gemini, ready to query
    def getGemini(self):   
        self.GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        genai.configure(api_key=self.GOOGLE_API_KEY)
        
        return genai.GenerativeModel('gemini-pro')

        
    # Obtains a JSON response on a variety of grades from Gemini
    def getFeedback(self, stringifiedFiles, firstFileName):
        query = f"""Score the following code from different files (starting with {firstFileName}) on code readability out of 10, in the format "Readability: a number/10". Than score the following code on object-oriented principles out of 10, in the format "OOP: a number/10". Than score the following code on maintainability out of 10, in the format "Maintainability: a number/10".  Return it as a JSON response (with the feedback included) in the format and list that at the top of the response. Output any feedback as the value under a 'feedback' key under each score key and list any filenames (e.g. {firstFileName}) for code examples. An example of the desired JSON output is below. Score all the files with a single score.\n {str(exampleJSON)}\n{stringifiedFiles}"""

        print(query)

        feedback = json.dumps(self.llm.generate_content(query).text)
        
        return feedback
    
    # Creates string of files to be used in the prompt, given the file paths.
    def getStringifiedFiles(self, fileList):
        stringfiedFiles = ""
        
        for filePath in fileList:
            stringfiedFiles += f"\n{filePath}\n\n"
            
            fp = open(filePath)
            fileString = fp.read()
            stringfiedFiles += f"\n{fileString}\n\n"
            
        return stringfiedFiles
    
    # Takes a list of file paths and obtains a score and feedback from Gemini on a series of criteria
    def gradeFiles(self, filePaths):
        stringifiedFiles = self.getStringifiedFiles(filePaths)
        feedback = self.getFeedback(stringifiedFiles, filePaths[0])
        
        return feedback
        
if __name__ == "__main__":
    scorer = AIScorer()
    print(scorer.gradeFiles(['AnotherExample.vue', 'ExampleFile.py']))