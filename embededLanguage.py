from gensim.models import Word2Vec
from sklearn.decomposition import PCA
from matplotlib import pyplot
#Define the training data
# Scanner Tokens
# train model
sentences = [['this', 'is', 'the', 'first', 'sentence', 'for', 'word2vec'],
			['this', 'is', 'the', 'second', 'sentence'],
			['yet', 'another', 'sentence'],
			['one', 'more', 'sentence'],
			['and', 'the', 'final', 'sentence']]

Gramatica = [['if', 'else', 'print','putc', 'while','programa','switch','case','break'],
            ['{', '}', '(', ')', '+', '-','*', '%',';', ',','?']]

Lenguaje =[['Programa','{','PI = 3;' 'circ = 5 * PI;','switch ( a == 0) case 1 ', ' if( circ == 12 ){ circ = 15 ;}','? circ;','break','}'],
		   ['']
		   ]


model = Word2Vec(Gramatica, min_count=1)
# summarize the loaded model
print(model)
# summarize vocabulary
words = list(model.wv.vocab)
print(words)
# access vector for one word
#print(model['sentence'])
# save model
model.save('model.bin')
# load model
new_model = Word2Vec.load('model.bin')
print(new_model)

X = model[model.wv.vocab]
pca = PCA(n_components=2)
result = pca.fit_transform(X)
# create a scatter plot of the projection
pyplot.scatter(result[:, 0], result[:, 1])
words = list(model.wv.vocab)
for i, word in enumerate(words):
	pyplot.annotate(word, xy=(result[i, 0], result[i, 1]))
pyplot.show()

similar_words = model.wv.most_similar('{')

print(similar_words)