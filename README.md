# intent-detection-component
Purpose: This is a server that gets as POST request a sentence and send a POST request after identifying:
* What is the required action?
* On what object the action should be applied?
* The value that the action should apply to the object?

Dependency:

* python 3.7 or higher
* Flask
* Spacy
* Installed en_core_web_sm model (needs to first install Spacy)
