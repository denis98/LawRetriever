from langchain_chroma import Chroma
from LawEmbeddings import LawEmbeddings
from connection import client, collection_name
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain_community.query_constructors.chroma import ChromaTranslator
from langchain_core.structured_query import Comparator
from langchain.chains.query_constructor.base import (
    StructuredQueryOutputParser,
    get_query_constructor_prompt,
)


queryembeddings = LawEmbeddings(embed_type="query")
querystore = Chroma(
    client=client,
    collection_name=collection_name,
    embedding_function=queryembeddings,
)


def paragraph_retriever(llm):
    # Filtering
    metadata_fields = [
        AttributeInfo(
            name="paragraph",
            description="""
            Identifier of the paragraph (just the number).
            Examples: 13, 305a - Its important to match this field exactly.
            Ignore further characters that indicate subparagraph or similar additional information.
            """,
            type="string"
        ),
        AttributeInfo(
            name="law",
            description="Abbreviation of the law. Example: BGB",
            type="string"
        ),
    ]
    
    examples = [
        (
            "§ 14 BGB",
            {
                "query": "",
                "filter": 'and(eq("paragraph", "13"), eq("law", BGB))',
            }
        ),
        (
            "§§ 13 und 14 BGB",
            {
                "query": "",
                "filter": 'or(and(eq("paragraph", "13"), eq("law", "BGB")),and(eq("paragraph", "14"), eq("law", "BGB")))',
            }
        ),
    ]
    
    document_content_description = "Full-Text of german laws. Be precise while querying information."
    
    prompt = get_query_constructor_prompt(
        document_contents=document_content_description,
        attribute_info=metadata_fields,
        examples=examples,
        allowed_comparators=Comparator.EQ
    )
    output_parser = StructuredQueryOutputParser.from_components()
    query_constructor = prompt | llm | output_parser
    
    retriever = SelfQueryRetriever(
        llm=llm,
        vectorstore=querystore,
        document_contents=document_content_description,
        metadata_field_info=metadata_fields,
        query_constructor=query_constructor
    )
    return retriever