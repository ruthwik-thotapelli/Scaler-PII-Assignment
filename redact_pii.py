from docx import Document
from presidio_analyzer import AnalyzerEngine
from faker import Faker

faker = Faker()
analyzer = AnalyzerEngine()
ENTITY_MAP = {}

def get_fake_value(entity_type, real_value):
    if real_value in ENTITY_MAP:
        return ENTITY_MAP[real_value]
    if entity_type == 'PERSON':
        val = faker.name()
    elif entity_type == 'EMAIL_ADDRESS':
        val = faker.email()
    else:
        val = f'[{entity_type}]'
    ENTITY_MAP[real_value] = val
    return val
