import spacy

nlp = spacy.load("./resumeModels/ner_model_YOE_10")

file = open("resume_579.txt", encoding="utf-8")

lines = file.read()

labels = nlp(lines)


label_dict = {}
for ent in labels.ents:
    if ent.label_ in label_dict:
        label_dict[ent.label_] += 1
    else:
        label_dict[ent.label_] = 1
    print(ent.label_, ent.text)
    print('')

# for key in label_dict.keys():
#     print(key, label_dict[key])