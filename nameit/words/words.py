"""words - a simple database for storing and randomly-selecting words by part-of-speech.
"""
import sqlite3
import logging
import secrets
import re

def get_log(name):
    """Get a logger under the nameit aegis"""
    return logging.getLogger("nameit.{}".format(name))

def get_word(table_name, cur):
    log = get_log(__name__)
    word_count = cur.execute("SELECT COUNT(word) FROM {}".format(table_name)).fetchone()[0]
    word_id = secrets.randbelow(word_count) + 1

    cmd = "SELECT word FROM {} WHERE id = ?".format(table_name)

    log.debug(word_id)
    return cur.execute(cmd, (word_id,)).fetchone()[0]

class words:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = sqlite3.connect(self.db_path)
        pass

    def initialize(self, adjectives, adverbs, nouns, verbs):
        """Initialize the words DB with words from the supplied files."""

        log = get_log(__name__)
        cur = self.db.cursor()

        def create_table(table_name):
            cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
            cur.execute("CREATE TABLE {} (id INTEGER NOT NULL PRIMARY KEY, word)".format(table_name))

        create_table("adjectives")
        create_table("adverbs")
        create_table("nouns")
        create_table("verbs")

        def load_words(table_name, words_file):
            with words_file.open() as words:
                for word in words:
                    cmd = "INSERT INTO {} (word) VALUES (?)".format(table_name)
                    log.debug("{} : {}".format(cmd, word))
                    cur.execute(cmd, (word.strip(),))
            pass

        load_words("adjectives", adjectives)
        load_words("adverbs", adverbs)
        load_words("nouns", nouns)
        load_words("verbs", verbs)

        self.db.commit()
        pass

    def adjective(self):
        """Return a single randomly-selected adjective."""

        return get_word("adjectives", self.db.cursor())
        pass

    def adverb(self):
        """Return a single randomly-selected adverb."""

        return get_word("adverbs", self.db.cursor())
        pass

    def noun(self):
        """Return a single randomly-selected noun."""

        return get_word("nouns", self.db.cursor())
        pass

    def verb(self):
        """Return a single randomly-selected verb."""

        def ss(word, suffix):
            return re.sub("{}$".format(suffix), "", word)

        def clean_suffixes(word, suffixes):
            for suffix in suffixes:
                word = ss(word, suffix)
            return word

        word = clean_suffixes(get_word("verbs", self.db.cursor()), ["ings", "ing", "es", "ed", "e", "s"])
        return word
        pass

    def name(self, form="{adverb} {verb}ing {adjective} {noun}"):
        """Return a name according to the form.

        For a form, you may use one of the following named fields:

        {adjective}

        {adverb}

        {noun}

        {verb}

        For example, the default form is: "{adverb} {verb}ing {adjective} {noun}".
        """

        adjective = self.adjective()
        adverb = self.adverb()
        noun = self.noun()
        verb = self.verb()

        return form.format(adjective=adjective, adverb=adverb, noun=noun, verb=verb)
    pass
