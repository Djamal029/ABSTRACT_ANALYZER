# Mesures de similarite lexicale en complement de la similarite semantique.
import re
import bm25s
from backend.app.domain.models.abstract import Abstract

# PAS FINIIIIII


class LexicalSimilarity:
    """
    We define class methods to tokenize the text and compute the similarity score
    between two texts using the BM25 algorithm. The similarity score is normalized
    to a range of [0, 1] for easier interpretation.
    """

    def __init__(self, abstract_a: Abstract, abstract_b: Abstract):
        self.abstract_a = abstract_a
        self.abstract_b = abstract_b

    # Find all alphanumeric tokens in the text, ignoring punctuation and case.
    # The < \w > metacharacter matches word characters : A word character is a character a-z, A-Z, 0-9, including _ (underscore).
    @staticmethod
    def _tokens(text: str | None) -> list[str]:
        return re.findall(r"[\w]+", text.lower() if text else "")

    # We define a method to create a document string from an Abstract object,
    # which includes : the title, text, and keywords.
    @staticmethod
    def _document(abstract: Abstract) -> str:
        keywords = " ".join(abstract.keywords or [])
        return " ".join(
            part for part in (abstract.abstractTitle, abstract.abstractText, keywords)
            if part
        )

    # Compute the similarity score between two texts using the BM25 algorithm.
    def _score(self, first: str, second: str) -> float:
        corpus_tokens = [self._tokens(first), self._tokens(second)]
        retriever = bm25s.BM25(
            k1=1.5,  # Default value for k1 is 1.5, which controls the term frequency saturation.
            b=0.75  # Default value for b is 0.75, which controls the length normalization of documents.
        )
        retriever.index(corpus_tokens)

        # Compute the BM25 scores for each document in the corpus against the other document.
        first_scores = retriever.get_scores(self._tokens(first))  # two scores are returned, one for each document in the corpus but we only need the score for the second document, which is at index 1.
        second_scores = retriever.get_scores(self._tokens(second))

        first_score = max(float(first_scores[1]), 0.0)
        second_score = max(float(second_scores[0]), 0.0)

        # Normalize the score to a range of [0, 1] using the formula : 2 * min(first_score, second_score) / (first_score + second_score)
        denominator = first_score + second_score
        return 2 * min(first_score, second_score) / denominator if denominator else 0.0

    def abstract_similarity(self) -> float:
        """Return the lexical similarity between the two abstracts in [0, 1]."""
        return self._score(
            self._document(self.abstract_a),
            self._document(self.abstract_b),
        )

    def theme_similarity(self, theme: str, choice: int) -> float:
        """Return the lexical similarity between abstract that we choose and an edition theme."""
        if choice == 1:
            return self._score(self._document(self.abstract_a), theme)
        elif choice == 2:
            return self._score(self._document(self.abstract_b), theme)
        else:
            raise ValueError("Choice must be 1 or 2.")
