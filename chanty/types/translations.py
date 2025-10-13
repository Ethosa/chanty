from typing import Dict, Optional

from ..utils import detect_project_name


class Translations:
    _entries: Dict[str, Dict[str, str]] = {}

    _project_name = detect_project_name().replace('-', '_')

    @classmethod
    def add(cls, key: str, translations: Dict[str, str]):
        cls._entries[key.format(project=cls._project_name)] = translations

    @classmethod
    def get(cls, key: str, lang: str = "en_us") -> str:
        return cls._entries.get(key, {}).get(lang, key)

    @classmethod
    def find_key(cls, text: str) -> Optional[str]:
        normalized = text.strip().lower()
        for key, langs in cls._entries.items():
            for lang_text in langs.values():
                if lang_text.strip().lower() == normalized:
                    return key
        return None

    @classmethod
    def has_key(cls, text: str) -> Optional[str]:
        key = cls.find_key(text)
        if key is None and text in cls._entries:
            key = text
        if key is not None:
            return True
        return False

    @classmethod
    def get_str(cls, text: str) -> Optional[str]:
        key = cls.find_key(text)
        if key is None and text in cls._entries:
            key = text
        if key is not None:
            return key
        return text

    @classmethod
    def translate(cls, text: str) -> Optional[str]:
        key = cls.find_key(text)
        if key is None and text in cls._entries:
            key = text
        if key is not None:
            return {"translate": key}
        return text
