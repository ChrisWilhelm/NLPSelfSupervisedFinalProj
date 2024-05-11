from openai import OpenAI
client = OpenAI(api_key="sk-proj-0tNstEib3aEWL7SLXOstT3BlbkFJtZnSh46sYvBofD6d17bY")

# List 10 fine-tuning jobs
client.fine_tuning.jobs.list(limit=10)