import requests

url="http://127.0.0.1:8000/api/upload/"
file_path = r"C:\Dev\FOSSEE_Intern_Task\test_data_3.csv"

with open (file_path,"rb") as f:
    files={"file": f}
    response = requests.post(url,files=files)

print("Status Code: ", response.status_code)
print("Response Text: ")
print(response.text)