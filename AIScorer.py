import os
import google.generativeai as genai
import re

class AIScorer:
    def __init__(self) -> None:
        self.llm = self.getGemini()
    
    # Sets up API key for Gemini, ready to query
    def getGemini(self):   
        self.GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
        genai.configure(api_key=self.GOOGLE_API_KEY)
        
        return genai.GenerativeModel('gemini-pro')
    
    # Grades a file using Gemini, given a string representation of it.
    def getIndentationResponse(self, codeStr):
        query = f"Grade the following code (out of 10) based on indentation:\n{codeStr}"
        
        response = self.llm.generate_content(query)
        
        return response.text
        
    # Uses parallel computing to score the grade of a single file.
    def getFileGrades(self, codeStr):
        # Get responses from Gemini
        indentationResponse = self.getIndentationResponse(codeStr)
        
        # Search for grade in responses
        indentationGrade = self.extractGradeFromResponse(indentationResponse)
        
        return indentationGrade
    
    # Searches through string for the grade that Gemini provided (uses a regular expression)
    def extractGradeFromResponse(self, response):
        pattern1 = r"(?<!\d)(\d+)\/10(?!\d)"
        pattern2 = r"\d{1,2} out of 10"
        regexPatterns = [pattern1, pattern2]
        
        # String searching with regex
        try:
            for regex in regexPatterns:
                grade = re.search(regex, response)
                
                # Once a grade has been obtained, break out of the loop
                if grade != None:
                    break
                
            # Return grade (just first value, not full fraction), as long as it has been obtained
            if grade != None:
                return grade.group()[0]
        except Exception:
            grade = None
            
        
        return grade
        
if __name__ == "__main__":
    scorer = AIScorer()
    
    # Open up the example code file, read it in, and grade it
    fp = open("AnotherExample.vue", "r")
    fileStr = fp.read()
    fp.close()

    print(scorer.getFileGrades(fileStr))
    