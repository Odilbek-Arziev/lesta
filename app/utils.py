import string
import re
import math


def simple_stem(word):
    suffixes = ["у", "ю", "е", "и", "ов", "ами", "ям", "ем", "ах", "ых", "ой", "ого"]
    for suffix in suffixes:
        if word.endswith(suffix):
            return word[: -len(suffix)]
    return word


def clean_text(text):
    text = text.lower()
    for char in string.punctuation + "«»—…":
        text = text.replace(char, " ")

    words = text.split()

    stop_words = {
        "и",
        "в",
        "во",
        "не",
        "что",
        "он",
        "на",
        "я",
        "с",
        "со",
        "как",
        "а",
        "то",
        "все",
        "она",
        "так",
        "его",
    }

    words = [word for word in words if word not in stop_words]

    return [simple_stem(word) for word in words]


def compute_tf(documents):
    """Вычисляет TF для каждого слова (усредняя по документам)."""
    tf_values = {}
    total_documents = len(documents)

    for doc in documents:
        word_counts = {}
        for word in doc:
            word_counts[word] = word_counts.get(word, 0) + 1

        total_words = len(doc)
        for word, count in word_counts.items():
            tf_values.setdefault(word, []).append(count / total_words)

    return {
        word: round(sum(tf_list) / total_documents, 6)
        for word, tf_list in tf_values.items()
    }


def compute_idf(documents):
    """Вычисляет IDF по документам."""
    num_documents = len(documents)
    word_doc_count = {}

    for doc in documents:
        for word in set(doc):
            word_doc_count[word] = word_doc_count.get(word, 0) + 1

    return {
        word: round(math.log(num_documents / (count + 1)), 6)
        for word, count in word_doc_count.items()
    }


def process_text(text):
    """Обрабатывает текст: чистит, делит на документы, считает TF и IDF."""
    documents = list(filter(None, re.split(r"[.!?]", text.lower())))
    cleaned_documents = [clean_text(doc) for doc in documents if doc.strip()]

    tf = compute_tf(cleaned_documents)
    idf = compute_idf(cleaned_documents)

    sorted_words = sorted(idf, key=idf.get, reverse=True)
    return [(word, tf[word], idf[word]) for word in sorted_words]
