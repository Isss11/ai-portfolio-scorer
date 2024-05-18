import os
import google.generativeai as genai
import re
import json

exampleJSON = {
    "readability": {
    "score": 8,
    "feedback": "The code is generally well-formatted and uses clear variable names. Docstrings are present, but type hints could improve readability further. Consider using a dictionary comprehension in getGeneralInfo for a more concise approach."
    },
    "oop": {
    "score": 7,
    "feedback": "The code demonstrates basic OOP concepts like encapsulation and abstraction. However, reusability can be improved by adding methods for retrieving more data or calculations."
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
    def getFileFeedback(self, codeStr):
        query = f"""Score the following code on code readability out of 10, in the format "Readability: a number/10". Than score the following code on object-oriented principles out of 10, in the format "OOP: a number/10". Than score the following code on maintainability out of 10, in the format "Maintainability: a number/10" Return it as a JSON response in the format and list that at the top of the response. Output any feedback as the value under a 'feedback' key under each score key. An example of the desired JSON output is below.\n {str(exampleJSON)}\n{codeStr}"""

        feedback = json.dumps(self.llm.generate_content(query).text)
        
        return feedback
        
if __name__ == "__main__":
    scorer = AIScorer()
    
    # Open up the example code file, read it in, and grade it
    fp = open("AnotherExample.vue", "r")
    fileStr = fp.read()
    fp.close()

    print(scorer.getFileFeedback(fileStr))
    