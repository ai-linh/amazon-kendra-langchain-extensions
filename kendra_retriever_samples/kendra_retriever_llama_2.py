import sys
import time

import langchain
from langchain.retrievers import AmazonKendraRetriever
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.llms import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
import json
import os

langchain.verbose = (os.environ.get("LC_VERBOSE") == "True")

def build_chain():
    region = os.environ["AWS_REGION"]
    kendra_index_id = os.environ["KENDRA_INDEX_ID"]
    endpoint_name = os.environ["LLAMA_2_ENDPOINT"]

    class ContentHandler(LLMContentHandler):
        content_type = "application/json"
        accepts = "application/json"

        def transform_input(self, prompt: str, model_kwargs: dict) -> bytes:
            input_str = json.dumps({"inputs": [[{"role": "user", "content": prompt},]],
                                    "parameters" : model_kwargs
                                    })
            return input_str.encode('utf-8')
        
        def transform_output(self, output: bytes) -> str:
            response_json = json.loads(output.read().decode("utf-8"))
            print(response_json)
            return response_json[0]['generation']['content']

    content_handler = ContentHandler()

    llm=SagemakerEndpoint(
            endpoint_name=endpoint_name, 
            region_name=region,
            model_kwargs={"max_new_tokens": 1500, "top_p": 0.8,"temperature":0.6},
            endpoint_kwargs={"CustomAttributes":"accept_eula=true"},
            content_handler=content_handler
        )
    retriever = AmazonKendraRetriever(index_id=kendra_index_id,region_name=region)

    prompt_template = """
    The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context.
    If the AI does not know the answer to a question, it truthfully says it 
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
    result = chain(prompt)
    end = time.time()
    # To make it compatible with chat samples
    return {
        "answer": result['result'],
        "source_documents": result['source_documents'],
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
