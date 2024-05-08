import os
import psycopg2
import spacy
import re
from tqdm import tqdm

# Define a regular expression pattern to remove trailing special characters
pattern = re.compile(r'[^\w\s]+$')

degree_nlp = spacy.load("./resumeModels/ner_model_degree_10")
college_nlp = spacy.load("./resumeModels/ner_model_college")
skill_nlp = spacy.load("./resumeModels/ner_model_skills_10")
company_nlp = spacy.load("./resumeModels/ner_model_company_name")
job_title_nlp = spacy.load("./resumeModels/ner_model_job_titles")

def extract_entities_positions(nlp_model, text):
    labels = nlp_model(text)
    entities = [(ent.text.lower().strip(), ent.start, ent.end) for ent in labels.ents]
    return entities

def find_closest_position(entity_positions, target_position):
    closest_position = None
    min_distance = float('inf')
    for position in entity_positions:
        distance = abs(position[1] - target_position)
        if distance < min_distance:
            min_distance = distance
            closest_position = position
    return closest_position

DATABASE_URL = "postgres://tjzpfemc:Jqbyuxw_xlwyrqxHCPUjarS0RDYEonUz@fanny.db.elephantsql.com/tjzpfemc"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()



for filename in tqdm(os.listdir("./TestDocs")):
    file_path = os.path.join("./TestDocs", filename)
    # print(filename)
    with open(file_path, encoding="utf-8") as file:
        resume_text = file.read()

    degree_entities = extract_entities_positions(degree_nlp, resume_text)
    college_entities = extract_entities_positions(college_nlp, resume_text)
    skill_entities = extract_entities_positions(skill_nlp, resume_text)
    company_entities = extract_entities_positions(company_nlp, resume_text)
    job_title_entities = extract_entities_positions(job_title_nlp, resume_text)
    corpus = filename.split('_')[2].split('.')[0]
    resume_id = int(filename.split('_')[1])
    if corpus == "d2":
        resume_id += 20000

    cur.execute('INSERT INTO "public"."Resume" (resume_id, resume_text) VALUES (%s, %s) RETURNING resume_id', (resume_id, resume_text,))
    resume_id = cur.fetchone()[0]

    for degree_text, degree_start, degree_end in degree_entities:
        closest_college = find_closest_position(college_entities, degree_start)
        if closest_college:
            college_text = closest_college[0]
            cur.execute('SELECT degree_id FROM "public"."Degree" WHERE degree_name = %s', (degree_text,))
            existing_degree = cur.fetchone()
            cur.execute('SELECT college_id FROM "public"."College" WHERE college_name = %s', (college_text,))
            existing_college = cur.fetchone()
            if not existing_degree:
                cur.execute('INSERT INTO "public"."Degree" (degree_name) VALUES (%s) RETURNING degree_id', (degree_text,))
                degree_id = cur.fetchone()[0]
            else:
                degree_id = existing_degree[0]
            if not existing_college:
                cur.execute('INSERT INTO "public"."College" (college_name) VALUES (%s) RETURNING college_id', (college_text,))
                college_id = cur.fetchone()[0]
            else:
                college_id = existing_college[0]
            cur.execute('SELECT * FROM "public"."Resume_College" WHERE resume_id = %s AND college_id = %s AND degree_id = %s',
                        (resume_id, college_id, degree_id))
            existing_entry = cur.fetchone()
            if not existing_entry:
                cur.execute('INSERT INTO "public"."Resume_College" (resume_id, college_id, degree_id) VALUES (%s, %s, %s)',
                            (resume_id, college_id, degree_id))

    for skill_text, _, _ in skill_entities:
        skill_text = pattern.sub('', skill_text.strip())
        cur.execute('SELECT skill_id FROM "public"."Skills" WHERE skill_name = %s', (skill_text,))
        existing_skill = cur.fetchone()
        if not existing_skill:
            cur.execute('INSERT INTO "public"."Skills" (skill_name) VALUES (%s) RETURNING skill_id', (skill_text,))
            skill_id = cur.fetchone()[0]
        else:
            skill_id = existing_skill[0]
        cur.execute('SELECT * FROM "public"."Resume_Skill" WHERE resume_id = %s AND skill_id = %s', (resume_id, skill_id))
        existing_entry = cur.fetchone()
        if not existing_entry:
            cur.execute('INSERT INTO "public"."Resume_Skill" (resume_id, skill_id) VALUES (%s, %s)', (resume_id, skill_id))

    for company_text, _, _ in company_entities:
        if any(c.isalpha() for c in company_text):
            company_text = pattern.sub('', company_text.strip())
            cur.execute('SELECT company_id FROM "public"."Company" WHERE company_name = %s', (company_text,))
            existing_company = cur.fetchone()
            if not existing_company:
                cur.execute('INSERT INTO "public"."Company" (company_name) VALUES (%s) RETURNING company_id', (company_text,))
                company_id = cur.fetchone()[0]
            else:
                company_id = existing_company[0]

    for job_title_text, _, _ in job_title_entities:
        cur.execute('SELECT job_title_id FROM "public"."JobTitle" WHERE title_name = %s', (job_title_text,))
        existing_job_title = cur.fetchone()
        if not existing_job_title:
            cur.execute('INSERT INTO "public"."JobTitle" (title_name) VALUES (%s) RETURNING job_title_id', (job_title_text,))
            job_title_id = cur.fetchone()[0]
        else:
            job_title_id = existing_job_title[0]
        closest_company = None
        min_distance = float('inf')
        for company_text, company_start, _ in company_entities:
            if any(c.isalpha() for c in company_text):
                company_text = pattern.sub('', company_text.strip())
                for _, job_title_start, _ in job_title_entities:
                    distance = abs(job_title_start - company_start)
                    if distance < min_distance:
                        min_distance = distance
                        closest_company = company_text
        
        if closest_company:
            cur.execute('SELECT company_id FROM "public"."Company" WHERE company_name = %s', (closest_company,))
            existing_closest_company = cur.fetchone()
            if not existing_closest_company:
                cur.execute('INSERT INTO "public"."Company" (company_name) VALUES (%s) RETURNING company_id', (closest_company,))
                closest_company_id = cur.fetchone()[0]
            else:
                closest_company_id = existing_closest_company[0]
            cur.execute('INSERT INTO "public"."Experience" (job_title_id, company_id, resume_id) VALUES (%s, %s, %s)',
                        (job_title_id, closest_company_id, resume_id))

    conn.commit()
cur.close()
conn.close()
