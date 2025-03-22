import requests
import json

response = requests.get("http://localhost:8000/processor/tdp/Xeon%20Bronze%203508U")
print("Status code:", response.status_code)
print("Response content:", response.text)

# Fix the JSON response by adding a comma
fixed_json = response.text.replace('"tdp"', ',"tdp"')
print("Fixed JSON:", fixed_json)
print("Parsed JSON:", json.loads(fixed_json))
