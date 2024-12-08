## Project Setup
### Step 1: Create Google Gemini API Key
Create API Key
(https://ai.google.dev/gemini-api/docs/api-key)

Create
```
.env
```
Paste your API Key as
```
GOOGLE_API_KEY="API_KEY"
```

### Step 2: Integrating with Streamlit
Set Up a Virtual Environment
Install virtualenv:
```
pip install virtualenv
```
Create a Virtual Environment
Run the following command:
```
python -m venv venv
```
Activate the Virtual Environment
Navigate to the venv folder:
```
cd venv
cd Scripts
activate
```
Install Required Libraries
From within the virtual environment, install dependencies:
```
pip install -r requirements.txt
```
### Step 3: Running the Code
Navigate to the Project Directory
Go to the directory containing app.py.

Run the Streamlit App
Start the app with:
```
streamlit run app.py
```