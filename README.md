# Final Project

For running this project, first install the dependencies in the requirements.txt file.

Next, Docker is required in order to generate the database. Run

```
docker build .
```

to generate the Database.

Then run generateTestDocs.py to create the text files for the resumes.

## NER

You can then use ner_training.py to create NER models and test them on a specific resume with ner_test.py.

Once your models are trained, you can run db_setup.py for those models to generate the database entries.

## GPT

Next you can open the GPTFineTuningSet directory to finetune the GPT model.

Here, data.json contains the dataset. You can run train_validate.py to split the data.

Then, generate an OpenAI API key and run finetuning.py to finetune a model.

You can run this model using runModel.py for a specific query.

Ensure that you have pasted your API key into the scripts.
