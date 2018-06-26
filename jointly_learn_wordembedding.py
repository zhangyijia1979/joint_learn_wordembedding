'''
Reference implementation for joint learning word vector based on bio text and mesh knowledge.
The implementation is based on Fasttext and Node2vec.
'''
#coding=utf-8

import argparse
import networkx as nx
import node2vec
from gensim.models import FastText
from gensim.models.fasttext import logger,FAST_VERSION
import random
import gzip
import pickle as pkl


def parse_args():

	parser = argparse.ArgumentParser()

	parser.add_argument('--input_corpus', nargs='?', default='./data/pubmed_sample',
	                    help='Input biomedical corpus')

	parser.add_argument('--input_mesh', nargs='?', default='./data/graph_mesh_sample.edgelist',
						help='Input mesh knowledge')

	parser.add_argument('--input_dic', nargs='?', default='./data/mesh_dic.pkl.gz',
						help='Input mesh dic')

	parser.add_argument('--output_model', nargs='?', default='./pubmed_mesh_test',
	                    help='output of word vector model')

	parser.add_argument('--output_bin', nargs='?', default='./pubmed_mesh_test.bin',
						help='output of word vector bin file')

	parser.add_argument('--dimensions', type=int, default=200,
	                    help='Number of dimensions. Default is 200.')

	parser.add_argument('--walk-length', type=int, default=50,
	                    help='Length of walk per source. Default is 50.')

	parser.add_argument('--num-walks', type=int, default=2,
	                    help='Number of walks per source. Default is 10.')

	parser.add_argument('--windows', type=int, default=5,
                    	help='Context size for optimization. Default is 5.')

	parser.add_argument('--iter', default=5, type=int,
                      help='Number of epochs in SGD')

	parser.add_argument('--min_count', default=5, type=int,
						help='Number of ignores min_count')

	parser.add_argument('--sg', default=1, type=int,
						help='if 1, skip-gram is used, otherwise, CBOW')

	parser.add_argument('--workers', type=int, default=8,
	                    help='Number of parallel workers. Default is 8.')

	parser.add_argument('--p', type=float, default=2,
	                    help='Return hyperparameter. Default is 2.')

	parser.add_argument('--q', type=float, default=1,
	                    help='Inout hyperparameter. Default is 1.')

	parser.add_argument('--directed', dest='directed', action='store_true',
	                    help='Graph is (un)directed. Default is undirected.')
	parser.add_argument('--undirected', dest='undirected', action='store_false')
	parser.set_defaults(directed=False)

	return parser.parse_args()

class MySentences(object):
	def __init__(self, pubmed_file):

		self.pubmed_file=pubmed_file

	def __iter__(self):

		for line in open(self.pubmed_file,'r'):
			yield str(line).split()



def main(args):

	f_pkl = gzip.open(args.input_dic, 'r')

	supplement_dict = pkl.load(f_pkl)
	f_pkl.close()
	print(FAST_VERSION)

	G = nx.read_edgelist(args.input_mesh, nodetype=str, create_using=nx.DiGraph())
	for edge in G.edges():
		G[edge[0]][edge[1]]['weight'] = 1

	G = G.to_undirected()

	G = node2vec.Graph(G, args.directed, args.p, args.q)

	G.preprocess_transition_probs()

	walks = G.simulate_walks(args.num_walks, args.walk_length)

	walks = [list(map(str, walk)) for walk in walks]

	new_walks=[]

	node_set=set([])

	for instance in walks:
		temp_list=[]
		for node in instance:
			node_set.add(node)
			if node in supplement_dict:
				temp_list.append(supplement_dict[node])

		new_walks.append(temp_list)


	sentences = list(MySentences(args.input_corpus))

	sentences.extend(new_walks)

	random.shuffle(sentences)

	model = FastText(size=args.dimensions, window=args.windows, min_count=args.min_count, workers=args.workers,
					 sg=args.sg, iter=args.iter)

	model.build_vocab(sentences)

	model.train(sentences, total_examples=model.corpus_count, epochs=model.iter)

	#model.save(args.output_model)

	print(model)

	model.wv.save_word2vec_format(args.output_bin, binary=True)


if __name__ == "__main__":
	args = parse_args()
	main(args)