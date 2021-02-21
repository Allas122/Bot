import json
import telebot as tb
import random as ran
d={}
with open('data.json','r') as f:
    d=json.load(f)
bot=tb.TeleBot(d['token'])

a=''
kb1=tb.types.ReplyKeyboardMarkup(True,True).row("Начать")
def request_geo():
    cb=tb.types.KeyboardButton('Отправить геопозицию',request_geo= True)
    kb3=tb.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard= True).row("Отказаться",cb)
    return kb3
def kb2():
    kb2=tb.types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard= True).row("Закончить")
    return kb2
kb3=tb.types.ReplyKeyboardMarkup(True,True).row("Да","Перезаписать","Отмена")

contacts = {}
contacts_name=[]
name_host=''

def compil_contact(message):
    if message.text == "Перезаписать":
        peple_send(message)
    elif message.text == "Да":
        #for i in contacts.keys():
        print(message.chat.first_name,message.chat.last_name)
def add_contact(message):
    print(message.contact)
    if message.text != 'Закончить':
        try:
            if message.contact.user_id != None:
                contacts[message.contact.user_id]=''
            else:
                bot.send_message(text='У этого пользователя нет Telegram',chat_id=message.chat.id)
            if message.contact.first_name != None and message.contact.last_name != None:
                contacts_name.append(message.contact.first_name+' '+message.contact.last_name)
            elif message.contact.first_name == None:
                contacts_name.append(message.contact.first_name+'')
            elif message.contact.last_name == None:
                contacts_name.append(message.contact.last_name+'')
            bot.register_next_step_handler(message,add_contact)
        except:
            bot.register_next_step_handler(message,add_contact)
    else:
        bot.send_message(chat_id=message.chat.id,text=f'Ты опросил {str(len(contacts_name))} а именно :{contacts_name}',reply_markup=kb3)
        bot.register_next_step_handler(message,compil_contact)
def peple_send(message):
    if message.text =="Начать" or message.text =="Перезаписать":
        bot.send_message(text="Добавьте из контактов всех, кто согласен с Вами на объём геолокацией закрепите контакты, по окончанию нажав закончить",chat_id=message.chat.id,reply_markup=kb2())
        bot.register_next_step_handler(message,add_contact)
@bot.message_handler()
def start(message):
    if message.text == 'Привет':
        bot.send_message(chat_id=message.chat.id,reply_markup=kb1,text='Узнавайте о друзьях поблизости ')
        bot.register_next_step_handler(message,peple_send)
bot.polling()