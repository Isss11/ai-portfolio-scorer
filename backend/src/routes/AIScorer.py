import os
import google.generativeai as genai
import re
import json

exampleJSON = {
    "readability": {
    "score": 8,
    "feedback": "test.py is generally well-formatted and uses clear variable names. Docstrings are present, but type hints could improve readability further. Consider using a dictionary comprehension in getGeneralInfo for a more concise approach."
    },
    "bestProgrammingPractices": {
    "score": 7,
    "feedback": "myapp.java demonstrates basic OOP concepts like encapsulation and abstraction. However, reusability can be improved by adding methods for retrieving more data or calculations. Test.vue has doesn't not use OOP concepts, but that is fine since OOP is not as important in JavaScript programming. Some additional best coding pracitices were followed, such as modularity."
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
    def getFeedback(self, stringifiedFiles):
        query = f"""Score the following code from different files on code readability out of 10, in the format "Readability: a number/10". Than score the following code on best programming practices for the given programming language (such as object-oriented programming if the programming language used is Java, Kotlin, or another OOP language) out of 10, in the format "bestCodingPractices: a number/10". Than score the following code on maintainability out of 10, in the format "Maintainability: a number/10".  Return it as a JSON object (with the feedback included) in the format and list that at the top of the response. Do not include "```json" in the response. Output any feedback as the value under a 'feedback' key under each score key and list any filenames (e.g. 'test.py') for code examples. Feedback values should be a minimum of 2 sentences and should not include any apostrophes. An example of the desired JSON output is below. Score all the files with a single score.\n {str(exampleJSON)}\n{stringifiedFiles}"""

        feedback = self.llm.generate_content(query).text
        
        print(feedback)
        print(feedback[4])
        
        # Removing initial part of response
        if feedback[3] == 'j':
            feedback = feedback[9:-4]
        elif feedback[3] == '`':
            feedback = feedback[4:-4]
            
        # TODO: Find a better solutions for this to replace (regular expression)
        feedback = feedback.replace("'", '"')
        
        feedback = self.extract_json(feedback)[0]
        
        return feedback
    
    # Reference for JSON fix: https://learnwithhasan.com/consistent-json-gemini-python/
    def extract_json(self, text_response):
        # This pattern matches a string that starts with '{' and ends with '}'
        pattern = r'\{[^{}]*\}'

        matches = re.finditer(pattern, text_response)
        json_objects = []

        for match in matches:
            json_str = match.group(0)
            try:
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
            if text[i] == '{':
                nest_count += 1
            elif text[i] == '}':
                nest_count -= 1
                if nest_count == 0:
                    return text[start:i+1]
        return text[start:end]
    
    # Creates string of files to be used in the prompt, given the file paths.
    def getStringifiedFiles(self, fileContent):
        stringifiedFiles = ""
    
        for language in fileContent:
            files = fileContent[language]['files']
            
            for file in files:
                stringifiedFiles += file['name']
                stringifiedFiles += "\n\n"
                stringifiedFiles += file['content']
                stringifiedFiles += "\n\n"
            
        return stringifiedFiles
    
    # Takes a list of file paths and obtains a score and feedback from Gemini on a series of criteria
    def gradeFiles(self, filePaths):
        stringifiedFiles = self.getStringifiedFiles(filePaths)
        feedback = self.getFeedback(stringifiedFiles, filePaths[0])
        
        return feedback