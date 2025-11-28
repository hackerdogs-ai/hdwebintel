class doc_similarities:
  

    def __init__(self, spacy=None, hamming=None, levenshtein=None, jaro=None, character_ngrams=None, jaccard=None, sorensen_dice=None, tversky=None, cosine=None, bag=None, matching_subsequences_ratio=None, token_sort_ratio=None, monge_elkan=None):
        self.spacy = spacy
        self.hamming = hamming
        self.levenshtein = levenshtein
        self.jaro = jaro
        self.character_ngrams = character_ngrams
        self.jaccard = jaccard
        self.sorensen_dice = sorensen_dice
        self.tversky = tversky
        self.cosine = cosine
        self.bag = bag
        self.matching_subsequences_ratio = matching_subsequences_ratio
        self.token_sort_ratio = token_sort_ratio
        self.monge_elkan = monge_elkan
        