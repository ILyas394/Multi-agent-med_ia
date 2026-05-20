QUESTIONS = [
    "Depuis quand les symptomes ont-ils commence ?",
    "Quels sont les symptomes principaux ressentis ?",
    "Avez-vous de la fievre, une douleur intense ou une gene respiratoire ?",
    "Avez-vous des antecedents medicaux ou prenez-vous un traitement ?",
    "Les symptomes s'aggravent-ils ou existe-t-il un signe inhabituel ?",
]


def ask_patient(question_count: int) -> str:
    """Return the next patient question."""
    if question_count < 0 or question_count >= len(QUESTIONS):
        return ""
    return QUESTIONS[question_count]


def build_patient_summary(initial_case: str, answers: list[dict[str, str]]) -> str:
    lines = [f"Cas initial: {initial_case.strip()}"]
    for index, item in enumerate(answers, start=1):
        lines.append(f"Question {index}: {item['question']}")
        lines.append(f"Reponse {index}: {item['answer']}")
    return "\n".join(lines)
