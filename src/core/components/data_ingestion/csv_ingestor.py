from pydantic import BaseModel


class InputCSVIngestorDto(BaseModel):
    file: any
    label: str


class CSVIngestor:
    
    def __init__(self):
        pass
    
    
    def ingest(input):
        pass