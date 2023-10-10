import sys
import time

import langchain
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
import json
import os

langchain.verbose = (os.environ["LC_VERBOSE"] == "True")

def build_chain():
    region = os.environ["AWS_REGION"]
    kendra_index_id = os.environ["KENDRA_INDEX_ID"]
    endpoint_name = os.environ["FALCON40B_ENDPOINT"]

    class ContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            input_str = json.dumps({"inputs": prompt, **model_kwargs})
            return input_str.encode('utf-8')

        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            return response_json[0]['generated_text']

    content_handler = ContentHandler()

    llm = SagemakerEndpoint(
        endpoint_name=endpoint_name,
        region_name=region,
        model_kwargs={"parameters": {"temperature": 0.001, "max_new_tokens": 500, "repetition_penalty": 1.03, "details": True}},
        content_handler=content_handler
    )

    retriever = AmazonKendraRetriever(index_id=kendra_index_id)

#     prompt_template = """You are an excellent phone customer service agent for Telstra. The customer is talking to you. You searched the knowledge base for help and that is summarized below. You must only use the summary below for your answer. If the answer can not be found in the information, or the question is not relevant to the abstract, you must only answer "I'm sorry, but I don't know the answer to that". Answer the following question in no more than four sentences:
#
# >>QUESTION<<
# {question}
#
# >>SUMMARY<<
# {context}
#
# >>ANSWER<<
# """

    prompt_template = """You are an excellent phone customer service agent for Telstra. The customer is talking to you directly on the telephone. You searched the knowledge base for help and that is summarized below. You must only use the summary for your answer. If the answer can not be found in the information, or the question is not relevant to the abstract, you must only answer "I don't know the answer to that". Do not refer to "the customer" but talk to them directly as "you". Answer the customer's question succinctly in no more than four sentences:

<Knowledge base>
{context}

<Customer>
{question}

<Phone Support>
"""

    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )

    chain_type_kwargs = {"prompt": PROMPT}
    qa = RetrievalQA.from_chain_type(
        llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs=chain_type_kwargs,
        return_source_documents=True
    )
    return qa


def run_chain(chain, prompt: str, history=[]):
    start = time.time()
    res = chain(prompt)
    end = time.time()
    # To make it compatible with chat samples
    return {
        "answer": res['result'],
        "source_documents": res['source_documents'],
        "metrics": f"{start},{end},{end-start}"
    }


if __name__ == "__main__":
    # read question from command line if there is one
    if len(sys.argv) > 1:
        question = sys.argv[1]
    else:
        question = "What's SageMaker?"
    chain = build_chain()
    print(f"Question: {question}")
    result = run_chain(chain, question)
    print(f"Answer: {result['answer']}")
    if 'source_documents' in result:
        print('Sources:')
        for d in result['source_documents']:
            print(d.metadata['source'])
    print(f"metrics: {result['metrics']}")
