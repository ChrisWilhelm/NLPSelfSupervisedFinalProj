import os
import spacy
import random
import json
from tqdm import tqdm
from spacy.training import Example
from spacy.util import minibatch, compounding
import concurrent.futures

# Initialize spaCy model
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

# Process JSON data from all files in the folder in parallel
folder_path = "./LabeledDocuments"
train_data = []

def process_file(filename):
    file_path = os.path.join(folder_path, filename)
    with open(file_path, "r", encoding='utf-8') as file:
        data = json.load(file)
        local_train_data = []
        for item in data:
            text = item['text']
            entities = item['entities']
            annotated_entities = []
            for entity in entities:
                if entity['type'] == 'Skill':
                    annotated_entities.append((entity['start_idx'], entity['end_idx'], entity['type']))
            local_train_data.append((text, {'entities': annotated_entities}))
        return local_train_data

# Using ThreadPoolExecutor to parallelize reading and processing of files
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(process_file, filename) for filename in os.listdir(folder_path) if filename.endswith(".json")]
    for future in concurrent.futures.as_completed(futures):
        train_data.extend(future.result())

print("Data read and processed.")

# Add labels to the NER model
for _, annotations in train_data:
    for ent in annotations['entities']:
        ner.add_label(ent[2])

# Disable other pipeline components for training efficiency
pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

# Train NER model
with nlp.disable_pipes(*unaffected_pipes):
    optimizer = nlp.begin_training()
    batch_sizes = compounding(4.0, 32.0, 1.001)  # Dynamically compounding batch sizes
    for itn in (range(35)):
        random.shuffle(train_data)
        losses = {}
        batches = minibatch(train_data, size=batch_sizes)
        for batch in tqdm(batches):
            try:
                texts, annotations = zip(*batch)
                docs = list(nlp.pipe(texts))  # Efficiently process texts in batch
                examples = [Example.from_dict(doc, annotation) for doc, annotation in zip(docs, annotations)]
                nlp.update(examples, drop=0.5, losses=losses, sgd=optimizer)
            except ValueError as e:
                #print(f"Skipping due to error: {e}")
                continue
            
        print(f"Iteration {itn}, Losses: {losses}")

# Save model to disk
nlp.to_disk("resumeModels/ner_model_skills_35")
print("Model saved to disk.")
