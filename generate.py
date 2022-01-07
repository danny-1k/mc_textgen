import argparse
import numpy as np
from string import punctuation


class Markovgen:
    def __init__(self, files=[]):
        self.corpus = ' '.join(
            [open(f, encoding='utf-8', mode='r').read() for f in files])

        self.corpus = self.preprocess_corpus(self.corpus)
        self.word_count = self.create_word_count(self.corpus)

    def seed(self,seed=0):
        np.random.seed(seed)

    def preprocess_corpus(self, corpus):
        corpus = ''.join(c for c in corpus.lower() if c.isalnum(
        ) or c == ' ' or c in punctuation or c == '' or c == '\n')
        corpus = ''.join(' '+c+' ' if c in punctuation or c ==
                         '\n' else c for c in corpus)
        return corpus

    def create_word_count(self, corpus):
        word_count = {}
        corpus = corpus.split()
        for idx in range(len(corpus)-1):

            word = corpus[idx]
            next_word = corpus[idx+1]

            if word in word_count:
                if next_word in word_count[word]:
                    word_count[word][next_word] += 1
                else:
                    word_count[word][next_word] = 1
            else:
                word_count[word] = {}
                word_count[word][next_word] = 1

        return word_count

    def sample_from_word(self, word_dict):
        words = list(word_dict.keys())
        count = [word_dict[w] for w in list(word_dict.keys())]
        count_sum = sum([word_dict[w] for w in list(word_dict.keys())])
        probs = [i/count_sum for i in count]

        return np.random.choice(words, p=probs)

    def sample_n(self, num=15, start=None):
        if start == None:
            start = np.random.choice(list(self.word_count.keys()))

        current = start
        out = f'{start}'

        for n in range(num):
            sampled = self.sample_from_word(self.word_count[current])
            out += ' '+sampled
            current = sampled

        return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start',help='start token')
    parser.add_argument('--num',help='number of words to generate')
    parser.add_argument('--seed',help='random seed for reproducibility')

    args = parser.parse_args()

    start = str(args.start) if args.start!=None else None
    num = int(args.num) if args.num!=None else 15
    seed = int(args.seed) if args.seed!=None else None

    mc = Markovgen(files=['AliceInWonderland.txt','TheTimeMachine.txt'])
    mc.seed(seed)
    print(mc.sample_n(start=start,num=num))