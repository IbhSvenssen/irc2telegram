#!/usr/bin/python
# -*- coding: utf-8 -*-  

# Import some necessary libraries.
import socket, re, subprocess, os, time, threading, sys, telepot

# Variables                                                                                                                                                                                                        
telegram_token = '112657252:AAFPTAlHDLOfXdbftWIxq-tzKJuxz2jTQtL'                                                                                                                                                   

# Some basic variables used to configure the bot        
server = '127.0.0.1' # znc server
chname = u"#ロシア"
channel = chname.encode("utf8", "replace") # Channel
botnick = "Luna" # Your bots nick
password = "eingiN1mi8"                                                                                                                                                                                        
lines = 0                                                                                                                                                                                                          
telegram_chat_id = -202862520                                                                                                                                                                                      
                                                                                                                                                                                                                   
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                                                                                                                                                        
ircsock.connect((server, 9777)) # Here we connect to the server using the port 6667                                                                                                                                
ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\n") # user authentication                                                                                                            
ircsock.send("NICK "+ botnick +"\n") # assign the nick to the bot                                                                                                                                                  
ircsock.send("PASS :" + password + "\r\n")                                                                                                                                                                         
                                                                                                                                                                                                                   
def ping(): # respond to server Pings.                                                                                                                                                                             
  ircsock.send("PONG :pingis\n")                                                                                                                                                                                   

def sendmsg(msg): # sends messages to the channel.
  ircsock.send("PRIVMSG "+ channel +" :"+ msg +"\n") 

def sendaction(msg): # sends messages to the channel.
  ircsock.send("PRIVMSG "+ channel +" :\x01" + "ACTION " + msg +"\x01\n")

def joinchan(chan): # join channel(s).
  ircsock.send("JOIN "+ chan +"\n")

def handle(msg): # telegram input callback
    content_type, chat_type, chat_id = telepot.glance(msg)
    username = msg['from']['first_name']
    message = msg['text']
    print("Message from telegram to irc:")
    print(content_type, chat_type, chat_id)
    if content_type == 'text' and chat_id == telegram_chat_id:
        if message[:3] == '/me':
            text_t2i = "<" + username + "> " + message[3:]
            sendaction(text_t2i.encode("utf8", "replace"))
        else:
            text_t2i = "<" +username + "> " + message
            sendmsg(text_t2i.encode("utf8", "replace"))

bot = telepot.Bot(telegram_token)
bot.message_loop(callback=handle, source=None)

# main functions of the bot
def main():
  # start by joining the channel
  joinchan(channel)
  # start infinite loop to continually check for and receive new info from server
  while 1: 
    # clear ircmsg value every time
    ircmsg = ""
    # set ircmsg to new data received from server
    ircmsg = ircsock.recv(2048)
    # remove any line breaks
    ircmsg = ircmsg.strip('\n\r')
    #ircmsg = ircmsg.decode('utf8') # to UTF-8
    # print received message to stdout (mostly for debugging).
    print(ircmsg)

    # repsond to pings so server doesn't think we've disconnected
    if ircmsg.find("PING :") != -1: 
      ping()

    # look for PRIVMSG lines as these are messages in the channel or sent to the bot
    if ircmsg.find("PRIVMSG") != -1:
      # save user name into name variable
      name = ircmsg.split('!', 1)[0][1:]
      print('name: ' + name)
      # get the message to look for commands
      message = ircmsg.split('PRIVMSG', 1)[1].split(':', 1)[1]
      print(message)
      bot.sendMessage(telegram_chat_id, name + ": " + message)

#start main functioin
main()
