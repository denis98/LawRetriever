from transformers import AutoModel

class LawEmbeddings:
    def __init__(self, embed_type = "embed"):
        """Initialisiere das Hugging Face Modell und Tokenizer."""
        self.model = AutoModel.from_pretrained("jinaai/jina-embeddings-v3", trust_remote_code=True)
        self.embed_type = embed_type

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple documents using the Hugging Face model.

        Args:
            texts: List of text documents to embed.

        Returns:
            List of embeddings for each document.
        """
        embeddings = []
        for text in texts:
            embeddings.append(self._embed_text(text))
        return embeddings

    def embed_query(self, text: str) -> list[float]:
        """Embed a single query using the Hugging Face model.

        Args:
            text: Query text to embed.

        Returns:
            Embedding for the query.
        """
        return self._embed_text(text)

    def _embed_text(self, text: str) -> list[float]:
        """Internal helper method to embed a single text."""
        if self.embed_type == "embed":
            return self.model.encode(text, task="retrieval.passage")
        else:
            return self.model.encode(text, task="retrieval.query")