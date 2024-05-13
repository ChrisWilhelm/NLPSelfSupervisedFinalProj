import spacy

nlp = spacy.load("./resumeModels/ner_model_skills_10")
# degree_nlp = spacy.load("./resumeModels/ner_model_degree_10")
# college_nlp = spacy.load("./resumeModels/ner_model_college")
# skill_nlp = spacy.load("./resumeModels/ner_model_skills_10")
# company_nlp = spacy.load("./resumeModels/ner_model_company_name")
# job_title_nlp = spacy.load("./resumeModels/ner_model_job_titles")

file = open("resume_579_skills_first.txt", encoding="utf-8")

lines = file.read()

labels = nlp(lines)


label_dict = {}
for ent in labels.ents:
    if ent.label_ in label_dict:
        label_dict[ent.label_] += 1
    else:
        label_dict[ent.label_] = 1
    print(ent.label_, ent.text)

# for key in label_dict.keys():
#     print(key, label_dict[key])