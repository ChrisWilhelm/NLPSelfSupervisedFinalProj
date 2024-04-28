import spacy

# Load NER models for degree, college name, and skill
degree_nlp = spacy.load("./resumeModels/ner_model_degree")
college_nlp = spacy.load("./resumeModels/ner_model_college")
# skill_nlp = spacy.load("./resumeModels/ner_model_skill")

# Load the resume text
with open("resume_1274.txt", encoding="utf-8") as file:
    resume_text = file.read()

# Function to find the closest entity position
def find_closest_position(entity_positions, target_position):
    closest_position = None
    min_distance = float('inf')
    for position in entity_positions:
        distance = abs(position[0] - target_position)
        if distance < min_distance:
            min_distance = distance
            closest_position = position
    return closest_position

# Initialize dictionary to store degrees and their respective colleges
college_degrees_dict = {}

# Extract degree entities and their positions
degree_labels = degree_nlp(resume_text)
degrees = [(ent.text, (ent.start, ent.end)) for ent in degree_labels.ents]

# Extract college entities and their positions
college_labels = college_nlp(resume_text)
colleges = [(ent.text, (ent.start, ent.end)) for ent in college_labels.ents]

# Match degrees with the closest college based on position
for degree_text, degree_position in degrees:
    closest_college = None
    closest_college_position = None
    min_distance = float('inf')
    for college_text, college_position in colleges:
        distance = abs(college_position[0] - degree_position[0])
        if distance < min_distance:
            min_distance = distance
            closest_college = college_text
            closest_college_position = college_position
    if closest_college:
        if closest_college in college_degrees_dict:
            college_degrees_dict[closest_college].append(degree_text)
        else:
            college_degrees_dict[closest_college] = [degree_text]

# Print the combined degrees for each college
for college, degrees in college_degrees_dict.items():
    combined_degrees = ' '.join(degrees)
    print(f"College: {college}, Degrees: {combined_degrees}")
