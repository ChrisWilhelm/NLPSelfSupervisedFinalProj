import openai

client = openai.OpenAI(api_key="YOUR_API_KEY")

# wait above is done
fine_tune_results = client.fine_tuning.jobs.retrieve("ftjob-RwB0NjAhSXGIW7HiDzThdiQ2")
ft_model = fine_tune_results.fine_tuned_model

context = "You are a chat bot tasked with converting natural language queries into SQL queries given the following schema: \n\n" + open("../databaseFiles/schema.sql").read()


res = client.chat.completions.create(model=ft_model, messages=[
    {"role": "system", "content": context},
    {"role": "user", "content": "Find all resumes with javascript as a skill."}
], temperature=0)
print(res.choices[0].message.content)
