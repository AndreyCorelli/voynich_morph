# voynich_morph
### project

is a Python 3 **Django** project that was initially intended to detect the language of the famous  [Voynich Manuscript](https://en.wikipedia.org/wiki/Voynich_manuscript) or to find the closest one among known languages.

In short, the language detecting algorithm is the following:

1. we collect ~ 20 … 30 text files written in one language with about 10 000 words per file,
2. we transform each text file into a feature vector
3. we repeat steps 1 - 2 for other languages (presently - English, Greek, Latin, Polish and Russian)
4. we train a classifier on these feature vectors
5. and finally we use the trained classifier to “predict” (y) the language of the Voynich manuscript.

The specific feature of this application is that it doesn’t rely on alphabet (because it looks unique) or on punctuation (because there’s no punctuation there) or even correlation between symbols.

So at the step (1) we pre-process each text file to remove punctuation, abbreviations, extra spaces, linebreaks, numbers. Then a featurizer (one from [vman/apps/vnlp/training/featurizers](https://github.com/AndreyCorelli/voynich_morph/tree/master/vman/apps/vnlp/training/featurizers)) transforms the file into an array of floating point numbers. The featurization is the most important step - most calculation is being performed here.

The featurizer is rather a lightweight class that relies on “corpus” files ([vman/apps/vnlp/training/corpus_features.py](https://github.com/AndreyCorelli/voynich_morph/blob/master/vman/apps/vnlp/training/corpus_features.py)). Each “corpus” file is mostly a dictionary plus a collection of word N-grams with some simple statistics behind each word / ngram.

There are preprocessed text files [vman/corpus/raw](https://github.com/AndreyCorelli/voynich_morph/tree/master/vman/corpus/raw) already in the project’s folder. There are also “corpus” files in another folder, [vman/corpus/features](https://github.com/AndreyCorelli/voynich_morph/tree/master/vman/corpus/features) because building CorpusFeatures objects from all text files can take about an hour.

## How to run the code
First, create a virtual environment for **Python 3** in the repository folder (near the `vman` folder) by a command like `python3 -m venv venv`.
Then activate venv and install the requirements:
```
pip install -r requirements.txt
```
Then descend to the `vman` folder and there run Django migrations like this:
```
./manage.py migrate
```
Then run the application - web server - by the command
```
./manage.py runserver 127.0.0.1:8091
```
(IP and port may be anything). Then the server is up, navigate to http://127.0.0.1:8091/vgui/corpus/compare/.

## How to add more texts / more languages.
First, be sure each text file contains about 10 000 words. The project contains class  `RawCorpusDownloader` that preprocesses the text file, removing extra characters and making all letters lowercase. Processing and storing a file into the *vman/corpus/raw/<language>* subfolder is easy to perform in the  TestRawCorpusDownloader (vman/apps/vnlp/training/tests/test_raw_corpus_downloader.py) test set or in the command line.

### How to add new language
First, derive a new class from `Alphabet` (vman/apps/vnlp/training/alphabet.py). Add this class reference to the `alphabet_by_code` dictionary. Create a subfolder under *vman/corpus/raw/* path and import text files in another `TestRawCorpusDownloader` test method or in the command line.

## How to classify languages
There are two test classes:
- `TestRandomForestClassifier` trains a classifier on 80% of the source files and then test the classifier on the rest 20% of the files. The same class also can try classifying Voynich Manuscript (encoded in EVA-A) language (see `test_predict_voynich` class method).
- `TestTransliteratedText` trains a classifier, then transliterates one English text file into Greek and then tries to classify the resulted file’s language.
