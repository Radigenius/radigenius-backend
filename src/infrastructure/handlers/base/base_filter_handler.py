class BaseFiltersHandler:
    search_synonyms = {"لپ تاپ": ["لپتاپ", "لپتا"]}

    stop_words = {
        "از",
        "به",
        "با",
        "در",
        "برای",
        "که",
        "این",
        "آن",
        "و",
        "یا",
        "نه",
        "باشد",
        "است",
        "بود",
        "می",
        "کنید",
        "کنیم",
        "کرد",
        "کرده",
        "داریم",
        "دارید",
        "دارد",
        "دارند",
        "باید",
        "هم",
        "همچنین",
        "چون",
        "اگر",
        "تا",
        "روی",
        "به",
        "هر",
        "شده",
        "های",
        "های",
        "او",
        "ما",
        "تو",
        "شما",
        "ایشان",
        "ای",
        "ما",
        "من",
        "می‌شود",
        "می‌تواند",
        "هست",
        "هستند",
        "بودند",
        "باشد",
        "باشند",
        "داشت",
        "داشته",
        "داشته‌اند",
        "نمی",
        "هر",
        "هنوز",
        "بسیار",
        "مگر",
        "حتی",
        "خود",
        "خویش",
        "همین",
        "درست",
        "اما",
        "زیرا",
        "آیا",
        "بیشتر",
        "کمتر",
        "جایی",
        "چند",
        "همه",
        "خود",
        "آنجا",
        "همینطور",
        "هرچند",
        "بهترین",
        "اول",
        "دوم",
        "سوم",
    }

    @classmethod
    def _tokenize_sentence(cls, sentence: str) -> list[str]:
        """Tokenize the sentence into words."""
        return sentence.split(" ")

    @classmethod
    def _filter_stop_words(cls, words: list[str]) -> list[str]:
        """Filter out stop words from the list of words."""
        return [word for word in words if word not in cls.stop_words]

    @classmethod
    def _replace_with_synonyms(cls, words: list[str]) -> list[str]:
        """Replace words with their synonyms."""
        synonym_map = {
            syn: key for key, syns in cls.search_synonyms.items() for syn in syns
        }
        return [synonym_map.get(word, word) for word in words]

    @classmethod
    def query_normalizer(cls, query: bool | int | str) -> bool | int | str:
        """Normalize the sentence by tokenizing, filtering stop words, and replacing with synonyms."""

        if type(query) != str:  # guard for boolean or integer filters
            return query

        words = cls._tokenize_sentence(query)
        filtered_words = cls._filter_stop_words(words)
        normalized_words = cls._replace_with_synonyms(filtered_words)
        return " ".join(normalized_words)
