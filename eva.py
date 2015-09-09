#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pynder
import cPickle as pickle
from time import sleep

# setup
FBTOKEN = # para conseguir o token visite https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token 
FBID = # ID do usuario do bot no Facebook
session = pynder.Session(FBID, FBTOKEN)
print 'Autorizado.'

from datetime import tzinfo, timedelta, datetime
ZERO = timedelta(0)           
class UTC(tzinfo):              # pedaco de codigo que 
    def utcoffset(self, dt):    # eu peguei so pra poder
        return ZERO             # comparar datas que
    def tzname(self, dt):       # nao tenham fuso horario 
        return "UTC"            # especificado (como as que
    def dst(self, dt):          # saem do datetime.now())
        return ZERO             # com as datas do Tinder   
utc = UTC()
last_check = pickle.load(open('last_check.p', 'rb'))

def like_everyone():
    try: users = session.nearby_users()
    except: users = [] 
    if users[0].name == 'Tinder Team': return
    print '\n\n'
    for user in users: 
        print '%s, %s: %s' % (user.name, user.age, user.bio)
        try: 
            if user.like(): print '(deu match!)'
        except: print 'something wrong'
    print 'Curti o pessoal'

def check_messages(): # retornas as mensagens recebidas depois da ultima checagem
    global last_check
    print 'Checando mensagens'
    new_messages = []
    for p in range(len(matches)):
        match = matches[p]
        oldest_unanswered = None
        for i in range(len(match.messages)-1,-1,-1): 
            try: sent = match.messages[i].sent # horario que a ultima mensagem foi mandada 
            except: continue
            if sent < last_check: # se mensagem for mais velha que a ultima checagem
                break
            oldest_unanswered = i # indice da ultima mensagem nao respondida
        new_messages.append((p,oldest_unanswered))
    last_check = datetime.now(utc)
    pickle.dump(last_check, open('last_check.p', 'wb'))
    return new_messages

def get_matches(): # As vezes a API dá uns problemas, por isso não uso session.matches() direto
    print 'Procurando matches...'
    matches = False
    while matches == False:
        try: matches = session.matches()
        except: 
            matches = False
            print 'stuck on a loop, captain',
    print 'Achei matches!'
    return matches

def write(new): # Manda as mensagens recebidas pros matches correspondentes
    print 'Escrevendo novas mensagens'
    for tupla in new:
        if tupla[1] == None: continue
        i = tupla[0] # match inicial
        c = (i/2)*2 + 1-(i % 2) # match correspondente
        new_messages = matches[i].messages[tupla[1]:]
        for msg in new_messages:
            print 'opa'
            if msg.sender.name != 'Eva':
                # antes tinha uma função de log aqui mas acabei tirando
                print '\n\n'
                msg = msg.body.encode('utf-8','replace')
                msg = str(msg).replace('linda','lindo')
                msg = msg.replace('Eva', str(matches[c]))
                msg = msg.replace(' eva', str(matches[c]))
                print matches[c]
                print msg
                matches[c].message(msg)

matches = get_matches()
print 'Iniciando.'
while True:
    print 'Loop!'
    if datetime.now().hour % 6 == 0: like_everyone()
    if datetime.now().minute % 10 == 0: matches = get_matches()
    new = check_messages()
    if new: write(new)
    sleep(5)
