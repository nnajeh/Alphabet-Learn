#Load needed libraries
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.utils import np_utils
from keras.preprocessing.sequence import pad_sequences

# fix random seed for reproducibility
numpy.random.seed(7)

# define the raw dataset
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# create mapping of characters to integers (0-25) and the reverse
char_to_int = dict((c, i) for i, c in enumerate(alphabet))
int_to_char = dict((i, c) for i, c in enumerate(alphabet))


# prepare the dataset of input to output pairs encoded as integers
seq_length = 1
# input
dataX = []
# output
dataY = []

for i in range(0, len(alphabet) - seq_length, 1):
  #Selected rows to be used in input
  seq_in = alphabet[i:i + seq_length]
  #Selected rows to be used in output
  seq_out = alphabet[i + seq_length]
  #append/add to the input caracters converted to numbers 
  dataX.append([char_to_int[char] for char in seq_in])
  dataY.append(char_to_int[seq_out])
  #print(seq_out)
  print (seq_in, '->', seq_out)
  
# convert list of lists to array and pad sequences if needed
X = pad_sequences(dataX, maxlen=max_len, dtype= float32 )

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (len(dataX), seq_length, 1))

# normalize
X = X/float(len(alphabet))

# one hot encode the output variable
y = np_utils.to_categorical(dataY)

# create the model
model = Sequential()
model.add(LSTM(32, input_shape=(X.shape[1], X.shape[2])))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#Fit the model
model.fit(X, y, nb_epoch=5000, batch_size=len(dataX), verbose=2, shuffle=False)

# summarize performance of the model
scores = model.evaluate(X, y, verbose=0)
print("Model Accuracy: %.2f%%" % (scores[1]*100))

# Make predictions
for i in range(20):
  pattern_index = numpy.random.randint(len(dataX))
  pattern = dataX[pattern_index]
  x = pad_sequences([pattern], maxlen=max_len, dtype= float32 )
  x = numpy.reshape(x, (1, max_len, 1))
  x = x / float(len(alphabet))
  prediction = model.predict(x, verbose=0)
  index = numpy.argmax(prediction)
  result = int_to_char[index]
  seq_in = [int_to_char[value] for value in pattern]
  print seq_in, "->", result
