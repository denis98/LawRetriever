# LawRetriever
This project includes a pipeline to interact with German laws via RAG in Langchain.

To run this, you can download any law from https://www.gesetze-im-internet.de/ in xml-format.
Put the file into the *data* folder and specify the name when calling the converter and indexer.

The retrieval-part is setup for interaction with models hosted on DeepInfra. If you want to use other LLM-providers, replace the initialization of *llm*, please see in the Langchain documentation for the usage.
