import random
from collections import defaultdict

class MarkovModel:
    def _init_(self, n):
        self.n = n
        self.start_tokens = []
        self.transitions = defaultdict(list)

    def train(self, corpus):
        for sentence in corpus:
            tokens = ['<start>'] * (self.n - 1) + sentence + ['<end>']
            self.start_tokens.append(tuple(tokens[:self.n - 1]))

            for i in range(len(tokens) - self.n):
                prefix = tuple(tokens[i:i + self.n - 1])
                next_word = tokens[i + self.n - 1]
                self.transitions[prefix].append(next_word)

    def generate_sentence(self, prefix, max_length=20):
        current_prefix = tuple(prefix[-(self.n - 1):]) if len(prefix) >= (self.n - 1) else tuple(['<start>'] * (self.n - 1))
        generated_sentence = list(prefix)

        while len(generated_sentence) < max_length:
            if current_prefix not in self.transitions:
                break

            next_word = random.choice(self.transitions[current_prefix])
            if next_word == '<end>':
                break
            generated_sentence.append(next_word)
            current_prefix = tuple(list(current_prefix) + [next_word])[1:]

        return generated_sentence
corpus = [
    ['The', 'quick', 'brown', 'fox', 'jumps', 'over', 'the', 'lazy', 'dog'],
    ['A', 'journey', 'of', 'a', 'thousand', 'miles', 'begins', 'with', 'a', 'single', 'step'],
    ['To', 'be', 'or', 'not', 'to', 'be', 'that', 'is', 'the', 'question'],
    ['In', 'the', 'beginning', 'God', 'created', 'the', 'heavens', 'and', 'the', 'earth'],
    ['All', 'that', 'glitters', 'is', 'not', 'gold'],
    ['To', 'err', 'is', 'human', 'to', 'forgive', 'divine'],
    ['Where', 'there', 'is', 'love', 'there', 'is', 'life'],
    ['Two', 'roads', 'diverged', 'in', 'a', 'wood', 'and', 'I', 'took', 'the', 'one', 'less', 'traveled'],
    ['It', 'was', 'the', 'best', 'of', 'times', 'it', 'was', 'the', 'worst', 'of', 'times']
]

markov_model = MarkovModel(n=3)
markov_model.train(corpus)

user_input = input("Enter a partial sentence: ").split()
completed_sentence = markov_model.generate_sentence(user_input)
print(' '.join(completed_sentence))