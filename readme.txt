Improving Biomedical Word Embeddings with Subowrd Information and MeSH Ontology 
================================================================================

This sourcecode is a demo implementation described in the paper "Improving Biomedical Word Embeddings with Subowrd Information and MeSH Ontology."

This is research software, provided as is without express or implied warranties etc. see licence.txt for more details. We have tried to make it reasonably usable and provided help options, but adapting the system to new environments or transforming a corpus to the format used by the system may require significant effort. 

The details of related files are described as follows:

Data: Mesh_dic.pkl.gz contains the files which are used to align the MeSH heading ids with mention words. Due to the limitation of the github, the PubMed corpus and MeSH RDF data can be download from NCBI. We provide two sample files graph_mesh_sample.edgelist and pubmed_sample by which you can quickly test the method.
 

Prerequisites
* python 3.5
* networkx 1.11
* gensim 2.3


Usage
User can use jointly_learn_wordembedding.py to automatically learn the word embedding based on text corpus and network data.


