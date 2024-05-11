import openai

client = openai.OpenAI(api_key="sk-proj-0tNstEib3aEWL7SLXOstT3BlbkFJtZnSh46sYvBofD6d17bY")

train_file = client.files.create(file=open("train.jsonl", "rb"), purpose="fine-tune")
validation_file = client.files.create(file=open("validation.jsonl", "rb"), purpose="fine-tune")

fine_tuning_job = client.fine_tuning.jobs.create(training_file=train_file.id, validation_file=validation_file.id, model="gpt-3.5-turbo-0125")