import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import json 

class Embedding:
        vocab_size = 0
        path = ""
        EMBEDDING_DIM = 5 

        x_train = None
        y_train = None

        embeddedWords = None 
        int2word = {}
        word2int = {} 

        def  __init__(self,path_ds,vocab_size,emb_dim = 5):
                self.vocab_size = vocab_size
                self.path = path_ds
                self.EMBEDDING_DIM = emb_dim
                self.load_data(self.path)

        def load_data(self,path):
                self.x_train = np.load(path + "/x_train.npy")
                self.y_train = np.load(path + "y_train.npy")
                with open(path + "/dict.json") as dicts:
                        diz = json.load(dicts)
                        #splitting dictts  W 

        def embedding_words(self):
                #INPUT LAYER 
                x = tf.placeholder(tf.float32, shape=(None, self.vocab_size))
                y_label = tf.placeholder(tf.float32, shape=(None, self.vocab_size))

                #len embedded-vector
                #HIDDEN LAYER
                # you can choose your own number
                W1 = tf.Variable(tf.random_normal([self.vocab_size, self.EMBEDDING_DIM]))
                b1 = tf.Variable(tf.random_normal([self.EMBEDDING_DIM])) #bias
                hidden_representation = tf.add(tf.matmul(x,W1), b1)
                
                #OUTPUT LAYER 
                W2 = tf.Variable(tf.random_normal([self.EMBEDDING_DIM, self.vocab_size]))
                b2 = tf.Variable(tf.random_normal([self.vocab_size]))
                prediction = tf.nn.softmax(tf.add( tf.matmul(hidden_representation, W2), b2))


                sess = tf.Session()
                init = tf.global_variables_initializer()
                sess.run(init) #make sure you do this!
                # define the loss function:
                cross_entropy_loss = tf.reduce_mean(-tf.reduce_sum(y_label * tf.log(prediction), reduction_indices=[1]))
                # define the training step:
                train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy_loss)
                n_iters = 7000 # REF 
                # train for n_iter iterations
                for _ in range(n_iters):
                        sess.run(train_step, feed_dict={x: self.x_train, y_label: self.y_train})
                        print('loss is : ', sess.run(cross_entropy_loss, feed_dict={x: self.x_train, y_label: self.y_train}))
                self.embeddedWords =  sess.run(W1,b1)
                sess.close()
                return self.embeddedWords

        def print_embeddedMatrix(self):
                for i in range(0,self.vocab_size):
                        print(self.int2word[i] + " : " + str(self.embeddedWords[i]))
'''
TESTING 
print("\n\n\n\n")
for i in range(0,vocab_size):
    print(int2word[i] + " : " + str(vectors[i]))



print(int2word[find_closest(word2int['re'], vectors)])
print(int2word[find_closest(word2int['regina'], vectors)])
print(int2word[find_closest(word2int['reame'], vectors)])
'''

'''
#da parola al vettore one-hot 


def to_one_hot(data_point_index, vocab_size):
    temp = np.zeros(vocab_size)
    temp[data_point_index] = 1
    return temp

def euclidean_dist(vec1, vec2):
    return np.sqrt(np.sum((vec1-vec2)**2))

def find_closest(word_index, vectors): #distanza minima tra due vettori [parole]
    min_dist = 10000 # to act like positive infinity
    min_index = -1
    query_vector = vectors[word_index]
    for index, vector in enumerate(vectors):
        if euclidean_dist(vector, query_vector) < min_dist and not np.array_equal(vector, query_vector):
            min_dist = euclidean_dist(vector, query_vector)
            min_index = index
    return min_index



corpus_raw = 'Lui è il re.Il re ha reame . La regina ha il reame '

corpus_raw = corpus_raw.lower()

words = []
for word in corpus_raw.split():
    if word != '.': # because we don't want to treat . as a word
        words.append(word)
words = set(words)



word2int = {}
int2word = {}
vocab_size = len(words) # gives the total number of unique words
#print(vocab_size)


for i,word in enumerate(words):
    word2int[word] = i
    int2word[i] = word
raw_sentences = corpus_raw.split('.')
sentences = []
for sentence in raw_sentences:
    sentences.append(sentence.split())
#print(word2int)
#print(int2word)
#print("\n\n\n\n\n")


data = []
WINDOW_SIZE = 2
for sentence in sentences:
    for word_index, word in enumerate(sentence):
        for nb_word in sentence[max(word_index - WINDOW_SIZE, 0) : min(word_index + WINDOW_SIZE, len(sentence)) + 1] :
            if nb_word != word:
                data.append([word, nb_word])


x_train = [] # input word
y_train = [] # output word
for data_word in data:
    x_train.append(to_one_hot(word2int[ data_word[0] ], vocab_size))
    y_train.append(to_one_hot(word2int[ data_word[1] ], vocab_size))
# convert them to numpy arrays
x_train = np.asarray(x_train)
y_train = np.asarray(y_train)

#print(x_train)
np.save("test",x_train)

xload = np.load("test.npy")
print(xload)
'''