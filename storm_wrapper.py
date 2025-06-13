import os
import json
from datetime import datetime
from knowledge_storm import STORMWikiRunnerArguments, STORMWikiRunner, STORMWikiLMConfigs
from knowledge_storm.lm import LitellmModel
from vector_loader import build_vector_store


class LocalStormRetriever:
    def __init__(self, retriever, k=3):
        self.retriever = retriever
        self.k = k

    def retrieve(self, query: str):
        # Ensure query is a string (not a list)
        if isinstance(query, list):
            query = " ".join(query)
        docs = self.retriever.get_relevant_documents(query)
        results = []
        for doc in docs:
            results.append({
                "title": doc.metadata.get("source", "Local Document"),
                "url": "file://" + doc.metadata.get("source", "local.txt"),
                "description": "",
                "snippets": [doc.page_content]
            })
        return results

    def __call__(self, query_or_queries: str, **kwargs):
        return self.retrieve(query_or_queries)


def generate_storm_protocol(study_title: str, summary: str) -> str:
    """
    Generates a full IRB protocol using STORM from a study title and descriptive summary.
    Returns the polished protocol as a string.
    """
    topic = study_title
    desc = summary

    os.environ["LITELLM_CACHE"] = "False"

    # Initialize LLM 
    llm = LitellmModel(
        model="ollama/mistral",
        api_base="http://localhost:11434",
        api_provider="openai",
        temperature=0.7,
        max_tokens=20000,
        litellm_cache=False
    )

    # Configure LLM roles for each STORM component
    lm_configs = STORMWikiLMConfigs()
    for setter in [
        lm_configs.set_conv_simulator_lm,
        lm_configs.set_question_asker_lm,
        lm_configs.set_outline_gen_lm,
        lm_configs.set_article_gen_lm,
        lm_configs.set_article_polish_lm
    ]:
        setter(llm)

    # Set STORM parameters
    args = STORMWikiRunnerArguments(
        output_dir="",
        max_conv_turn=3,
        max_perspective=3,
        search_top_k=3,
        max_thread_num=3,
    )

    # Setup vector-based retriever on local corpus
    vector_store, embed_model = build_vector_store()
    retriever_obj = vector_store.as_retriever(search_kwargs={"k": args.search_top_k})
    retriever = LocalStormRetriever(retriever=retriever_obj, k=args.search_top_k)

    # Run STORM
    runner = STORMWikiRunner(args, lm_configs, retriever)
    runner.run(
        topic=topic + "\n" + desc,
        do_research=True,
        do_generate_outline=True,
        do_generate_article=True,
        do_polish_article=True
    )

    runner.post_run()
    runner.summary()

def log_generation(section_name: str, topic: str, response: str):
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "section": section_name,
        "topic": topic,
        "response": response
    }
    with open("logs/generation_log.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")