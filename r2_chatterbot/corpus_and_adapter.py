from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import chatterbot.comparisons
import chatterbot.response_selection

from r2_chatterbot.util import utils
utils.set_classpath()
import os

# Uncomment the following lines to enable verbose logging
#import logging
#logging.basicConfig(level=logging.INFO)

# Create a new instance of a ChatBot
os.environ['JAVA_HOME'] = "/home/sgp62/jdk-8u271-linux-aarch64/jdk1.8.0_271/"
bot = ChatBot(
    'Terminal',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'logic_adapters.weather_adapter.WeatherAdapter',
        'logic_adapters.restaurant_adapter.RestaurantAdapter',
        {
            "import_path": 'logic_adapters.bestmatch_2.BestMatch2',
            "statement_comparison_function": chatterbot.comparisons.levenshtein_distance,
            "response_selection_method": chatterbot.response_selection.get_most_frequent_response
        }
    ],
    database_uri='sqlite:///database.db',
    read_only = True
)

corpus_trainer = ChatterBotCorpusTrainer(bot)
corpus_trainer.train('chatterbot.corpus.english.greetings', "./r2_chatterbot/custom_corpus.yaml")

print('Type something to begin...')

# The following loop will execute each time the user enters input
# while True:
#     try:
#         user_input = input()
#         bot_response = bot.get_response(user_input)
#         print(bot_response)
#
#     # Press ctrl-c or ctrl-d on the keyboard to exit
#     except (KeyboardInterrupt, EOFError, SystemExit):
#         break

def response_from_chatbot(question):
    user_input = question
    bot_response = bot.get_response(question)
    #bot_response = "Eat a dick"
    return bot_response
