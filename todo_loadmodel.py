import gensim

model_path = "cc.ja.300.vec"
model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)

model.save("cc_ja_300.model")