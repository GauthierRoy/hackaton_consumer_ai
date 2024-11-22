from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from faker import Faker

def anonymize(text, language):
    fake = Faker()

    # Create configuration containing engine name and models
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": language, "model_name": f"{language}_core_news_md"}],
    }

    # Create NLP engine based on configuration
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine_with_spanish = provider.create_engine()
    analyzer = AnalyzerEngine(
        nlp_engine=nlp_engine_with_spanish,
        supported_languages=[language]
    )

    #analyse personal data
    results_french = analyzer.analyze(text=text, language=language)

    #replace with random data
    anonymizer = AnonymizerEngine()
    anonymized_text = anonymizer.anonymize(text=text,analyzer_results=results_french, operators={"PERSON": OperatorConfig("replace", {"new_value": fake.name()}), "PHONE_NUMBER": OperatorConfig("replace", {"new_value": fake.phone_number()}), "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": fake.email()}), "LOCATION": OperatorConfig("replace", {"new_value": fake.address()})})
    return anonymized_text.text



if __name__ == '__main__':
    text = "Mon nom est Morris et mon numéro est 0625555555. Je vis au 60 rue Louis Braille et voici mon mail : Quentin.ja@gmail.fr"
    print(anonymize(text = text, language = "fr"))
