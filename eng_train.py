from core import *
from chatterbot.trainers import ChatterBotCorpusTrainer

eng_trainer = ChatterBotCorpusTrainer(chatbot)
eng_trainer.train('chatterbot.corpus.english')

