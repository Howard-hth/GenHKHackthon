# How to run the test
0. **Review project_environment.py**
   ```bash
   - Replace API_URL and API_KEY
   - Check DB config mode [0: test, 1: production]
   ```

1. **Activate the Virtual Environment (RECOMMENDED WITH ANACONDA):**
   ```bash
   venv\Scripts\activate  # For Windows
   # or
   source venv/bin/activate  # For macOS/Linux
   ```

2. **Install New Packages:**
   ```bash
   pip install package_name  # Replace with the desired package
   ```

3. **Generate `requirements.txt`:**
   ```bash
   pip freeze > requirements.txt
   ```

4. **Install Packages from `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Flask Application:**
   ```bash
   python app.py
   ```
6. **Open https://reqbin.com/**
   ```bash
   # Follow the testcases format as below, 
   # The Google Form: "https://forms.gle/N7TPt3jNn1jCk4sj9" can help
   
   [POST] http://127.0.0.1:5000/api/classification 
   {
      "content": ""
   }

   [POST] http://127.0.0.1:5000/api/questionaire
   {
        "list": ["To be provided by /api/classification"],
        "questionaire_response":  {
            "diabetes": 0,
            "pregnancy": 0,
            "duration": 0,
            "frequency": 0,
            "phlegm": 0,
            "phlegm_color": 0,
            "phlegm_thickness": 0
        }
   }
    WHEREAS the questionaire represents the following:
    1. Do you have diabetes? (0: N; 1: Y)
    2. Do you have pregnacy? (0: N; 1: Y)
    3. How long is the symptom? (0: Within 1 week; 1: 1-6 weeks; 2: 1.5 months and above)
    4. How frequent is the symptom?
     (1: more than 6 times per week;
     2-6: 5-1 time(s) per week respectively;
     7-9: 3-1 time(s) per  month respectively;
     10: less than once a month)
    5. Do you have phlegm? (0: Y; 1: N)
    6. What's the color? (0: Yellow or No Phlegm; 1: White or colorless)
    7. What's thickness? (0: Thick or No Phlegm; 1: Thin)

   [POST] http://127.0.0.1:5000/api/questionaire2
   {
      "list": ["To be provided by /api/questionaire, WHILE RESPONSE KEY MUST CONTAIN 'list'],
      "answer":  integer 0-5
   }
   WHEREAS answer represent the most favourite flavor as below:
   0."原味"
   1."金桔"
   2."薄荷"
   3."烏梅"
   4."蘋果"
   5."檸檬草"

   [POST] http://127.0.0.1:5000/api/classification 
   {
    "success": ["To be provided by /api/questionaire or /api/questionaire2, WHILE RESPONSE KEY MUST CONTAIN 'success'"]
   }
   ```
