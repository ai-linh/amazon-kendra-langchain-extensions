import sys
import time

from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
import json
import os


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
        model_kwargs={"parameters": {"temperature": 0.8, "max_new_tokens": 100, "details": True}},
        content_handler=content_handler
    )

    retriever = AmazonKendraRetriever(index_id=kendra_index_id)

    prompt_template = """
      The following is a conversation between a Telstra AI chatbot and a customer. 
      The Telstra AI chatbot is helpful and provides lots of specific details from its context.
      If the Telstra AI chatbot does not know the answer to a question, it truthfully says it 
      does not know.
      {context}
      Instruction: Based on the above documents, provide a detailed answer for, {question} Answer "don't know" 
      if not present in the document. 
      Solution:"""
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
