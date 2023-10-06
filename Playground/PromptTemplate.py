"""Prompt template generic code"""
from langchain.llms.bedrock import Bedrock
import boto3
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import json
from botocore.exceptions import ClientError


def get_secret():
    secret_name = "kendraRagApp"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    return secret


def qa(query):
    secrets = json.loads(get_secret())
    kendra_index_id = secrets['kendra_index_id']

    llm = Bedrock(model_id="amazon.titan-tg1-large", region_name='us-east-1', credentials_profile_name='default')
    llm.model_kwargs = {"maxTokenCount": 4096}

    retriever = AmazonKendraRetriever(index_id=kendra_index_id)

    prompt_template = """
    {context}
    {question} If you are unable to find the relevant article, respond 'I can't generate the needed content based on the context provided.'
    """

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"])

    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        verbose=True,
        chain_type_kwargs={
            "prompt": PROMPT
        }
    )

    return chain(query)


def handler(event, context):
    query = event['query']
    response = qa(query)
    if response.get("result"):
        return {
            'statusCode': 200,
            'body': response["result"]
        }
    else:
        return {
            'statusCode': 400,
            'body': "Could not answer the query based on the context available"
        }
