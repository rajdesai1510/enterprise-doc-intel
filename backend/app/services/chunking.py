try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError as exc:
    raise ImportError(
        "langchain_text_splitters is required. Install it: `pip install -U langchain-text-splitters`"
    ) from exc


def get_chunking_config(doc_type: str, purpose: str):
    """
    Returns chunk_size and overlap based on document type and end purpose
    """

    # Defaults
    chunk_size = 1000
    overlap = 200

    if doc_type == "legal":
        chunk_size = 1500
        overlap = 300

    elif doc_type == "technical":
        chunk_size = 1200
        overlap = 200

    elif doc_type == "notes":
        chunk_size = 700
        overlap = 100

    # Purpose-based tuning
    if purpose == "qa":
        chunk_size = min(chunk_size, 900)

    elif purpose == "summary":
        chunk_size = max(chunk_size, 1500)
        overlap = 300

    return chunk_size, overlap


def chunk_text(text: str, doc_type: str, purpose: str):
    chunk_size, overlap = get_chunking_config(doc_type, purpose)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_text(text)
