import os
import telebot
import requests
import json
import csv

# TODO: 1.1 Get your environment variables 
yourkey = "60b64a7f"
bot_id = "5724015164:AAEnlp-L2TJlTtLUe1k1O8pMzNhgcaxu1Xg"

bot = telebot.TeleBot(bot_id)
global final
final=[]
@bot.message_handler(commands=['start', 'hello'])
def greet(message):
    global botRunning
    botRunning = True
    bot.reply_to(
        message, 'Hello there! I am a bot that will show movie information for you and export it in a CSV file.\n\n')
    
@bot.message_handler(commands=['stop', 'bye'])
def goodbye(message):
    global botRunning
    botRunning = False
    os.remove("data.csv")
    bot.reply_to(message, 'Bye!\nHave a good time')
    


@bot.message_handler(func=lambda message: botRunning, commands=['help'])
def helpProvider(message):
    bot.reply_to(message, '1.0 You can use \"/movie MOVIE_NAME\" command to get the details of a particular movie. For eg: \"/movie The Shawshank Redemption\"\n\n2.0. You can use \"/export\" command to export all the movie data in CSV format.\n\n3.0. You can use \"/stop\" or the command \"/bye\" to stop the bot.')


@bot.message_handler(func=lambda message: botRunning, commands=['movie'])
def getMovie(message):
    global final
    tex=message.text
    response = requests.get(f"http://www.omdbapi.com/?apikey=60b64a7f&t={tex[7:]}")
    data=response.json()
    l=[data['Title'],data['Year'],data['Released'],data['imdbRating']]
    final.append(l)
    final_test=final
    bot.reply_to(message, 'Getting movie info..')
    bot.send_message(message.chat.id,'Movie Found!')
    s='Movie Name: ' +data['Title']+'\nYear: '+data['Year']+'\nReleased: '+data['Released']+'\nimdbRating: '+data['imdbRating']
    bot.send_photo(message.chat.id,data['Poster'],s)
    header=['Title','Year','Released','imdbRating']
    with open('data.csv','w',encoding='UTF8',newline='') as f:
       writer=csv.writer(f)
      
       writer.writerow(header)
       writer.writerows(final)
    
   
    # TODO: 1.2 Get movie information from the API
    # TODO: 1.3 Show the movie information in the chat window
    # TODO: 2.1 Create a CSV file and dump the movie information in it

  
@bot.message_handler(func=lambda message: botRunning, commands=['export'])
def getList(message):
    global final_test
    bot.reply_to(message, 'Generating file...')    
    bot.send_document(message.chat.id, open('data.csv', 'rb'))
    
    
    #TODO: 2.2 Send downlodable CSV file to telegram chat

@bot.message_handler(func=lambda message: botRunning)
def default(message):
    bot.reply_to(message, 'I did not understand '+'\N{confused face}')
    
bot.infinity_polling()

