## Project Setup: Setting up using replicate
### Step 1: Setting Replicate

Visit
(https://replicate.com/)

Create your API Token
```
https://replicate.com/account/api-tokens
```
Select your Model
```
https://replicate.com/models
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