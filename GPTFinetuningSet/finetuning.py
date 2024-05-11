import openai

client = openai.OpenAI(api_key="API_KEY")

train_file = client.files.create(file=open("train.json", "rb"), purpose="fine-tune")
validation_file = client.files.create(file=open("validate.json", "rb"), purpose="fine-tune")

fine_tuning_job = client.fine_tuning.jobs.create(training_file=train_file.id, validation_file=validation_file.id, model="gpt-3.5-turbo-0125")

# wait above is done
# fine_tune_results = client.fine_tuning.jobs.retrieve(fine_tuning_job.id)
# ft_model = fine_tune_results.fine_tuned_model

# res = client.completions.create(model=ft_model, prompt="input prompt", temperature=0)
# print(res.choices[0].text)
