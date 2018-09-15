import tabula, pandas, glob, os

# Read pdf into DataFrame
# df = tabula.read_pdf("test.pdf", options)

from tabula import wrapper
#df = wrapper.read_pdf('../sample-data/B1705_2000560947.pdf', output_format='dataframe', guess=False)
#df = wrapper.read_pdf('../sample-data/B1705_2000560948.pdf', output_format='dataframe', guess=False)
#df = wrapper.read_pdf('../sample-data/B1705_2000604352 (1).pdf', output_format='dataframe', guess=False)


collection_frame = []


for file in os.listdir("../sample-data/"):
    if file.endswith(".pdf"):
        #print(file)
        filepath = "../sample-data/{}".format(file)
        print(filepath)
        df = wrapper.read_pdf(filepath, output_format='dataframe', guess=False)
        list(df)
        RBC_Value= df['Unnamed: 0'][df['Unnamed: 0'].str.contains("RBC").__eq__(True)]
        Fibrinogen_Value= df['Unnamed: 0'][df['Unnamed: 0'].str.contains("FIBRINOGEN").__eq__(True)]

        #getting rows from start to finish
        test= df['Unnamed: 0'].str.split(' ', expand=True)[1][11:32]
        #print(test)
        test2 = df['Unnamed: 0'].str.split(' ', expand=True)[2][18]

        test3 = df['Unnamed: 0'].str.split(' ', expand=True)[3][30]
        #print(test3)

        platelet_appearance = df['Unnamed: 0'].str.split(' ', expand=True)[1][17]
        plasma_appearance = df['Unnamed: 0'].str.split(' ', expand=True)[2][32]


        # Remove rows with alphabetic characters
        test=test[~test.str.contains("[a-zA-Z]").fillna(False)]
        #print(test)
        columns = ['RBC', 'HAEMOGLOBIN', 'HAEMATOCRIT', 'MCV', 'MCH',            
        'MCHC',
        'PLATELET COUNT',
        'WBC',
        'NEUTROPHILS%',
        'NEUTROPHILS',
        'LYMPHOCYTES%',
        'LYMPHOCYTES',
        'MONOCYTES%',
        'MONOCYTES',
        'EOSINOPHILS%',
        'EOSINOPHILS',
        'BASOPHILS%',
        'BASOPHILS',
        'PROTEIN PLASMA',
        'FIBRINOGEN',
        'PLASMA APPEARANCE',
        'BLOOD SMEAR EXAMINATION']

        index = ""
        values = test


        values["RBC"] = test[11]
        values["HAEMOGLOBIN"] = test[12]
        values["HAEMATOCRIT"] =test[13]
        values["MCV"] = test[14]
        values["MCH"] = test[15]
        values["MCHC"] = test[16]
        values["PLATELET APPEARANCE"] = platelet_appearance
        values["PLATELET COUNT"] = test2
        values["WBC"] = test[19]
        values["NEUTROPHILS%"] = test[20]
        values["NEUTROPHILS"] = test[21]
        values["LYMPHOCYTES%"] = test[22]
        values['LYMPHOCYTES'] = test[23]
        values["MONOCYTES%"] = test[24]
        values["MONOCYTES"] = test[25]
        values["EOSINOPHILS%"] = test[26]
        values["EOSINOPHILS"]  = test[27]
        values["BASOPHILS%"] = test[28]
        values["BASOPHILS"] = test[29]
        values["PROTEIN PLASMA"] = test3
        values["FIBRINOGEN"] = test[31]
        values["PLASMA APPEARANCE"] = plasma_appearance

        blood_smear_examination = df['Unnamed: 0'][33:35]
        blood_smear_examination = blood_smear_examination.str.replace('BLOOD SMEAR', '')
        blood_smear_examination = blood_smear_examination.str.replace('EXAMINATION', '')
        blood_smear_examination= blood_smear_examination.str.cat(sep=',')
        values["BLOOD SMEAR EXAMINATION"] = blood_smear_examination
        values = values[19:]
        #print(values) 
        animal_id = df["Unnamed: 1"][5]

        #animal_id = animal_id.split('Animal ID:', expand=True)
        animal_id=animal_id.replace('Animal ID:','')
        values["Animal ID:"]=animal_id
        collection_date = df["Unnamed: 0"][7]
        #collection_date= collection_date.replace('Received:', "")
        collection_date = collection_date.split("Received:")[0]
        collection_date = collection_date.split("Collected:")[1]
        values["Collected:"] = collection_date
        #print(collection_date)
        #animal_id=animal_id.replace('Animal ID:','')
        #values["Animal ID:"]=animal_id
        #print(values)
        #print(collection_date)
        #print(df)
        received_date = df["Unnamed: 0"][7]
        received_date = received_date.split("Received:")[1]
        values["Received:"] = received_date
        #print(received_date)
        #print(values)
        collection_frame.append(values)
    

#print(collection_frame)
testing = pandas.DataFrame(collection_frame)
print(testing)

testing.to_csv("../sample-data/combined_results.csv", encoding='utf-8', index=False)


df = wrapper.read_pdf('../sample-data/B1705_2000560949.pdf', output_format='dataframe', guess=False)