# Smart Maps



## Setup instructions
```
python3 -m venv ENV
source ENV/bin/activate
pip install -r requirements.txt
```
Along with this you also have to install Java 7 or 8.

## Running instructions

### Batch processing locally
```
python -m python_read_data --file-dir='sample-data'
```

This will take all the pdfs from a specified directory and output a 'output.csv' file.

### Test Flask app locally

Run below code to start up the flask server locally.
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Run below code to test the flask server.
```
curl -F "data=@sample-data/B1705_2000560947.pdf" http://127.0.0.1:5000/api/process-pdf
```

Example output:
```
{
    "response": {
        "Age": "1Y",
        "Animal ID": "1635",
        "BASOPHILS": 0.0,
        "BASOPHILS%": 0.0,
        "BLOOD SMEAR EXAMINATION": "Occasional activated lymphocytes, Red cell morphology normal.",
        "Case ID": "C1595073",
        "Clinic No": "B1705",
        "Collected": "15/01/2018",
        "EOSINOPHILS": 0.0,
        "EOSINOPHILS%": 0.0,
        "FIBRINOGEN": 1.0,
        "HAEMATOCRIT": 0.4,
        "HAEMOGLOBIN": 129.0,
        "LYMPHOCYTES": 4.3,
        "LYMPHOCYTES%": 48.0,
        "Lab Number": "2000560947",
        "MCH": 12.0,
        "MCHC": 323.0,
        "MCV": 37.0,
        "MONOCYTES": 0.4,
        "MONOCYTES%": 5.0,
        "NEUTROPHILS": 4.2,
        "NEUTROPHILS%": 47.0,
        "Owner": "CCRG",
        "PLASMA APPEARANCE": "Normal",
        "PLATELET COUNT": 363.0,
        "PLATELETS": "Normal",
        "PROTEIN  PLASMA": 69.0,
        "RBC": 10.9,
        "Received": "15/01/2018",
        "Reported": "15/01/2018",
        "Sex": "Female",
        "Species": "OVINE",
        "WBC": 8.9,
        "filename": "B1705_2000560947.pdf",
        "pdf_parse_failed": 0
    }
}
```