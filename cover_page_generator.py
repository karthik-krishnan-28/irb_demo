def generate_cover_page_from_protocol(protocol_text: str) -> str:
    import litellm

    prompt = f"""
You are generating the cover page for an IRB clinical trial protocol. Below is the full protocol document.

Your task is to extract or infer the following summary fields and return them in a clean format that follows IRB, NIH, FDA regulations. Search for examples on clinicaltrials.gov:

- Protocol Title
- Protocol Number (make up a plausible one if not specified)
- Compound
- Study Phase
- Acronym (a short name for the study, based on the title)
- Sponsor Name
- Sponsor Address (write 'N/A' if not available)
- Regulatory Identifier Number (use 'Pending' if not available)

Return only the cover page as a formatted block of text, clean and professionally.

--- Begin Protocol Document ---
{protocol_text}
--- End Protocol Document ---
"""

    response = litellm.completion(
        model="ollama/mistral",
        api_base="http://localhost:11434",
        api_provider="openai",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()
