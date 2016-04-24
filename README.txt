To run the neural network:
--------------------------
-Running the network will require the data collection of mp3 and wav files with appropriate ID3v2 genre tags
-First, cd into the root of the source directory
-Then, set the environment variable for the directory of the song files:
    -export SONG_DIR='/path/to/mp3/and/wav/files'
-Next, generate the mfcc values for training data.  This can be skipped if using the same data as in the original copy of the source.  This will be very time consuming:
    -python generateSongDataFiles.py
-Finally, run the neural network model:
    -python neuralNetwork.py