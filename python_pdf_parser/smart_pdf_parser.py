from tabula import read_pdf
import re
import pandas as pd


AUTO_EXTRACT_META_DATA = ['Case ID', 'Collected', 'Received', 'Clinic No', 'Owner', 'Lab Number', 'Species', 'Reported', 'Sex', 'Age', 'Animal ID']

def get_obj_with_text(json_obj, text):
    for i in json_obj:
        objs = i['data']
        for obj in objs:
            for o in obj:
                if o['text'] == text:
                    return o


def get_obj_with_text_contains(json_obj, text):
    for i in json_obj:
        objs = i['data']
        for obj in objs:
            for o in obj:
                if text in o['text']:
                    return o


def extract_label_data(label, target_string):
    m = re.search(f'{label}:( *\S+)', target_string)
    if m:
        found = m.group(1)
        return found
    else:
        return None


def extract_metadata(json_obj):
    output = {}
    for key in AUTO_EXTRACT_META_DATA:
        text = get_obj_with_text_contains(json_obj, f'{key}:')['text']
        if key == 'Animal ID':
            output[key] = text.replace("Animal ID:", "").strip()
        else:
            output[key] = extract_label_data(key, text).strip()
    return output


def parse_value(val):
    try:
        return float(val)
    except ValueError:
        text = val.split(' ')
        try:
            return float(text[0])
        except ValueError:
            return val


def process_pdf(pdf_filename):
    parsed_pdf = {}
    try:
        json_obj = read_pdf(pdf_filename, output_format='json', guess=False, silent=True)
        output = extract_metadata(json_obj)
        meta_df = pd.DataFrame(output, index=[0])

        o = get_obj_with_text(json_obj, 'Range')
        table_start = o['top'] + o['height']

        for i in json_obj:
            objs = i['data']
            for j, _ in enumerate(objs):
                if j < len(i['data']) - 1:
                    prev = objs[j][0]
                    after = objs[j+1][0]

                    diff = after['top'] - prev['top']
                    if diff > 20 and after['top'] > table_start and 'RBC' not in after['text']:
                        table_end = after['top']
                        break

        df = read_pdf(
            pdf_filename, output_format='dataframe',
            guess=False, area=(table_start, 0, table_end, 1000),
            pandas_options={'header': None}, silent=True)

        df = df.loc[:, 0:1]
        df[1] = df[1].apply(parse_value)
        df_meta = meta_df.T.reset_index()
        df_meta.columns = [0, 1]
        df = df_meta.append(df).reset_index(drop=True)
        blood_smear_index = df.index[df[0] == 'BLOOD SMEAR'].tolist()[0]
        blood_smear_str = ', '.join(df.iloc[blood_smear_index:len(df)][1].tolist())
        df = df.drop(df.index[[i for i in range(blood_smear_index, len(df))]])
        df = df.append({0: 'BLOOD SMEAR EXAMINATION', 1: blood_smear_str}, ignore_index=True)

        df_T = df.T
        df_T.columns = df_T.iloc[0, :]
        df_T = df_T.drop(df_T.index[[0]])
        df_T = df_T.reset_index(drop=True)

        parsed_pdf = df_T.to_dict('records')[0]
        parsed_pdf['pdf_parse_failed'] = 0
    except Exception as e:
        parsed_pdf['pdf_parse_failed'] = 1
        pass
    finally:
        parsed_pdf['filename'] = pdf_filename.split('/')[-1]
        return parsed_pdf