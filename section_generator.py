from storm_wrapper import generate_storm_protocol

def generate_full_protocol(study_title: str, study_summary: str) -> str:
    """
    Generates a full IRB protocol using STORM from a study title and summary.
    Returns the polished article text.
    """
    return generate_storm_protocol(study_title, study_summary)