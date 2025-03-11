import csv

def load_prof_data(file_name='professors.csv'):
    reader = csv.DictReader(open(file_name, 'r', encoding='utf-8-sig'))
    headers = reader.fieldnames
    questions = headers[2:]
    prof_pmf = {}
    question_data = {}
    for question in questions:
        question_data[question] = {}
    for row in reader:
        prof = row['Professor Name']
        probability = float(row['Probability'])
        prof_pmf[prof] = probability
        for question in questions:
            answer_raw = row[question]
            
            answer = True if answer_raw == 'Yes' else False
            question_data[question][prof] = answer

    # next we add in a question: "Is it a {animal}?"
    for prof in prof_pmf:
        question_data[f"Is it {prof}?"] = {prof: True}
        for other in prof_pmf:
            if other != prof:
                question_data[f"Is it {prof}?"][other] = False

    return prof_pmf, question_data