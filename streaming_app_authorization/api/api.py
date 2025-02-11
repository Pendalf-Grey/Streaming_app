from fastapi import FastAPI


def create_app():
    return FastAPI(
        title='Kafka Messanges',
        docs_url='/api/docs',
        description='A simple Kafka + DDD example.'
    )
