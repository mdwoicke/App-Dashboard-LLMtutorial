import streamlit as st
from pymongo import MongoClient
import urllib,io,json
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm=ChatOpenAI(model="gpt-4o",temperature=0.0)
#mongo client
#mongo client
username="ronidas"
pwd="t2HKvnxjL38QGV3D"
client=MongoClient("mongodb+srv://"+urllib.parse.quote(username)+":"+urllib.parse.quote(pwd)+"@cluster0.lymvb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db=client["invoice"]
collection=db["invoice"]


with io.open("sample.txt","r",encoding="utf-8")as f1:
    sample=f1.read()
    f1.close()
with io.open("sample1.txt","r",encoding="utf-8")as f1:
    sample1=f1.read()
    f1.close()

prompt="""
 you are a very intelligent AI assitasnt who is expert in identifying relevant questions from user
        and converting into nosql mongodb agggregation pipeline query.
        Note: You have to just return the query as to use in agggregation pipeline nothing else. Don't return any other thing
        Please use the below schema to write the mongodb queries , dont use any other queries.
       schema:
       the mentioned mogbodb collection talks about invoivces for a company. The schema for this document represents the structure of the data, describing various informations related to the _id, invoice_number, invoice_date, customer_name, product.brand, product.item, product.unit, product.single_unit_price, product.all_unit_price, total_price, mode_of_payment 
       your job is to get python code for the user question
       Here’s a breakdown of its schema with descriptions for each field:


1. _id: Unique identifier for the document, represented as an ObjectId.
2. invoice_number: A unique number assigned to the invoice.
3. invoice_date: The date when the invoice was issued.
4. customer_name: The name of the customer to whom the invoice is issued.
5. product: A list of products included in the invoice.
    - brand: The brand of the product.
    - item: The name or model of the product.
    - unit: The number of units of the product being invoiced, represented as an integer.
    - single_unit_price: The price of a single unit of the product, represented as an integer.
    - all_unit_price: The total price for all units of this product, represented as an integer.Will be used for brand or product specific revenue
6. total_price: The total price of all products included in the invoice, represented as an integer.
7. mode_of_payment: The mode of payment used for the invoice.
Here is the example provided with explanations:
example:{sample1}
This schema provides a comprehensive view of the data structure for multiple invoices in MongoDB, 
use the below sample_examples to generate your queries perfectly
sample_example:

Below are several sample user questions related to the MongoDB document provided, 
and the corresponding MongoDB aggregation pipeline queries that can be used to fetch the desired data.
Use them wisely.

sample_question: {sample}
As an expert you must use them whenever required.
Note: You have to just return the query nothing else. Don't return any additional text with the query.Please follow this strictly
input:{input}
output:
"""
def genresponse(input):
    query_with_prompt=PromptTemplate(
        template=prompt,
        input_variables=["input","sample","sample1"]
    )
    llmchain=LLMChain(llm=llm,prompt=query_with_prompt,verbose=True)
    response=llmchain.invoke({
                "input":input,
                "sample":sample,
                "sample1":sample1
            })
    data=response["text"]
    data=data.replace("json","")
    data=data.replace("`","")
    data=data.replace(".$numberInt","")
    query=json.loads(data)
    results=collection.aggregate(query)
    return results
            