import requests
import json, os
from html_to_json import convert
from PIL import Image
from io import BytesIO
import base64


def get_image(image_str):
    output_file_path = os.path.dirname(__file__) + "/response.png"
    
    image_data = base64.b64decode(image_str)
    # Create an image object
    image = Image.open(BytesIO(image_data))

    # Save the image to a file (optional)
    image.save(output_file_path)

def extract_data(rollNumber):
    
    dir = os.path.dirname(__file__)
    text_file_path = dir + "/response.txt"
    json_file_path = dir +  "/response.json"

    url = "https://oas.iitmandi.ac.in/student/Services/StdService.asmx/GetDetails"
    
    request_headers = {
        "Id": 6,
        "status": rollNumber,
        "EmpId": None
    }

    response = requests.post(url, json=request_headers)
  
    # Check the response status
    if response.status_code == 200:
        data = json.loads(response.text)
        html_data = data['d']
        json_data = convert(html_data)
        
        with open(text_file_path, 'w') as text_file:
            text_file.write(html_data)
        print("HTML data saved to response.txt")
        
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=2)
        print("JSON data saved to response.json")
        
        image_str = json_data["newdataset"][0].get("table17",[{}])[0].get("photocontent", [{}])[0].get("_value", "")
        get_image(image_str)
        name = json_data["newdataset"][0].get("table2",[{}])[0].get("firstname",[{}])[0].get("_value", None)
        fa = json_data["newdataset"][0].get("table2",[{}])[0].get("facultyadvisor", [{}])[0].get("_value",None)
        return name, fa
    else:
        # Print an error message
        print(f"Error: {response.status_code} - {response.text}")
        return None
