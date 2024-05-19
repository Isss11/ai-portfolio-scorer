import google.generativeai as genai
import re
import json

from src.config import GOOGLE_API_KEY

jsonQueryExample = {
    "score": 50,
    "feedback": ["<Constructive feedback>"],
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
Provide a score and feedback on the following code
based on code readability, best practices, and maintainability.

Use the following JSON format in your response:
{json.dumps(jsonQueryExample)}

The score represents how well the code follows these principles and is an integer between 0 and 100.
The feedback is 1-3 sentences of broad but constructive feedback as a list of strings.

The code is as follows:

{stringifiedFiles}""".strip()

        generated_content = llm.generate_content(query)
        generated_text = generated_content.text
        print("AIQuery.getFeedback response", generated_text)

        score = 55
        feedback = []

        try:
            json_feedback = json.loads(generated_text)
            score = json_feedback.get("score", score)
            feedback = json_feedback.get("feedback", feedback)
        except json.JSONDecodeError:
            pass

        return {"score": score, "feedback": feedback}

    # Reference for JSON fix: https://learnwithhasan.com/consistent-json-gemini-python/
    def extract_json(self, text_response):
        # This pattern matches a string that starts with '{' and ends with '}'
        pattern = r"\{[^{}]*\}"
        text = text_response.replace("'", '"')
        text = text.replace("`", "")

        print("Feedback after adjustments.")
        print(text)

        matches = re.finditer(pattern, text)
        json_objects = []

        for match in matches:
            json_str = match.group(0)
            try:
                # Validate if the extracted string is valid JSON
                json_obj = json.loads(json_str)
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                # Extend the search for nested structures
                text = text_response.replace("'", '"')
                text = text.replace("`", "")

                print("First exception.")

                extended_json_str = self.extend_search(text, match.span())
                try:
                    json_obj = json.loads(extended_json_str)
                    json_objects.append(json_obj)
                except json.JSONDecodeError:
                    # Handle cases where the extraction is not valid JSON
                    print("Second exception.")
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
