#!/usr/bin/python
# -*- coding: utf-8 -*-
#import sys
#nowe sciezki do modulow
#sys.path.append('/home/huczu/python')

import config
import ekg
from imaplib import IMAP4_SSL
from smtplib import SMTP_SSL
#import string
from time import strftime
from email.MIMEText import MIMEText
#RSS Reader
import feedparser

#cos w stylu pamieci?
ilosc_rss = {"rss":0, "rss_mem":0}
newsy = []
wyslijWiad = False

def rssReader(): #TODO: Formatowanie RSS
	wiadomosc = ''
	kanal = feedparser.parse(config.wykop_rss)
	ilosc_obecna = len(kanal.entries)
	ilosc_rss["rss_mem"] = ilosc_obecna
	if not ilosc_rss["rss"] == ilosc_obecna:
		for news in range(ilosc_obecna):
			newsy.append([kanal.entries[news].title, kanal.entries[news].description, kanal.entries[news].link])
			for i in range(len(newsy)):
				wiadomosc = wiadomosc + "\n\n".join(newsy[news][i]).encode('utf-8')

		ekg.command('gg:msg %s %s' % (config.admin, wiadomosc))
		ilosc_rss["wykop"] = ilosc_obecna
	else:
		ekg.command('gg:msg %s Brak.' % (config.admin))

"""def getMsgs(data):
	for num in data[0].split():
		typ, data = conn.fetch(num,'(RFC822)')
		msg = email.message_from_string(data[0][1])
		typ, data = conn.store(num,'-FLAGS','\\Seen')
		yield msg		"""

def czyJuzPora():
	if config.czas[0] <= int(strftime("%H")) <= config.czas[1]:
		return True
	else:
		return False

def sendSMS(tresc):
	text_subtype = 'plain' #plain, html, xml
	charset = 'utf-8' #utf-8 dla polskich znakow
	domena = ''
	usePrefix = False
	if config.siec == "plus":
		usePrefix = True
		domena = "@text.plusgsm.pl"
	elif config.siec == "orange":
		domena = "@sms.orange.pl" #TODO: Tworzenie maila do wyslania smsm, moze cos lepszego niz if/elif?
	else:
		domena = "@text.plusgsm.pl" #by nie bylo jakis nieporozumien

	try:
		msg = MIMEText(tresc, text_subtype, charset)
		msg['Subject'] = 'Info' #temat wiadomosci
		if usePrefix == True:
			msg['To'] += config.prefix

		msg['To']  += config.numer + domena #TODO: konfiguracja serwera sms
		msg['From'] = config.emails[config.server][1][0] #nawet nie dziala ale musi byc

		conn = SMTP_SSL('smtp.' + config.emails[config.server][0], config.smtp_port)
		conn.login(config.emails[config.server][1][0], config.emails[config.server][1][1])
		try:
			conn.sendmail(config.emails[config.server][1][0], msg['To'], msg.as_string())
		finally:
			conn.close()
	except Exception, exc:
		ekg.command("gg:msg %s SMS Failed: %s" % (config.admin, str(exc))) # give a error message

def checkMail():
	for email in config.emails:
		try:
			obj = IMAP4_SSL("imap." + email[0], config.imap_port)
			obj.login(email[1][0], email[1][1])
			try:
				obj.select()
				obj.search(None, 'UnSeen')
				ret, maile = obj.search(None, 'UnSeen')[1][0].split()
				ilosc_maili = len(maile)
				email[2]["mem"] = ilosc_maili
				"""if not fc == 0:
				for wiadomosc in maile:
					typ, informacje = obj.fetch(wiadomosc,'(RFC822.SIZE BODY[HEADER.FIELDS (SUBJECT)])')
					temat = data[0][1].lstrip('Subject: ').strip() + ' '"""
			finally:
				obj.close()
		except Exception, exc:
			ekg.command("gg:msg %s IMAP %s Failed: %s" % (config.admin, email[0], str(exc))) # give a error message

		jednaWiad = "Masz 1 nowa wiadomosc na koncie"
		doPiecWiad = "nowe wiadomosci na koncie"
		kilkaWiad = "nowych wiadomosci na koncie"
		sms = ""

		if not email[2]["email_memory"] == ilosc_maili:
			if email[2]["mem"] == 1:
				if wyslijWiad == True:
					ekg.command('gg:msg %s %s%s.' % (config.admin, jednaWiad, email[0]))
				elif wyslijWiad == False and czyJuzPora() == True:
					sms += jednaWiad + " " + email[0] + "\n"
			elif 1 < email[2]["mem"] < 5:
				if wyslijWiad == True:
					ekg.command('gg:msg %s Masz %d %s %s.' % (config.admin, email[2]["mem"], doPiecWiad, email[0]))
				elif wyslijWiad == False and czyJuzPora() == True:
					sms += "Masz " + email[2]["mem"] + " " + doPiecWiad + " " + email[0] + "\n"
			elif email[2]["mem"] > 5:
				if wyslijWiad == True:
					ekg.command('gg:msg %s Masz %d %s %s.' % (config.admin, email[2]["mem"], kilkaWiad, email[0]))
				elif wyslijWiad == False and czyJuzPora() == True:
					sms += "Masz " + email[2]["mem"] + " " + kilkaWiad + " " + email[0] + "\n"
			email[2]["email_memory"] = ilosc_maili

	if not sms:
		sendSMS(sms)

def init():
				ekg.printf("generic", "Skrypt odpalony")

def status_handler(session, uid, status, desc):
	global wyslijWiad
	if uid == config.admin:
		if not status == ekg.STATUS_NA:
			wyslijWiad = True
			return 1
		else:
			wyslijWiad = False
			return 0

def message_handler(session, uid, type, text, sent_time, ignore_level):
		if uid == config.admin:
			if text == "!checkmail":
				checkMail()
				return 1
			elif text == "!rss":
				rssReader()
				return 1
		elif text == "!wersja":
			ekg.command('gg:msg %s Moja wersja to %s' % (uid, config.version))
			return 1
		elif text == "!autorzy":
			ekg.command('gg:msg %s Stworzyl mnie %s i nadal rozwija.' % (uid, config.autor))
			return 1
		else:
			ekg.command('gg:msg %s Witaj! Nazywam sie %s i jestem botem GG stworzonym i rozwijanym przez %s .\nBot zostal wylacznie do uzytku autora. Nie masz co szukac :)' % (uid, config.nazwa_kodowa, config.autor))
			return 1

def connect_handler(session):
		ekg.echo("Sesja : " + session)
		sesja = ekg.session_get(session)
		if sesja.connected():
			ekg.echo('Połączony! Silnik i sto turbin poszło w ruch! :)')
		else:
			ekg.echo('W tym miejscu jeszcze nie połączony')

ekg.handler_bind('protocol-connected', connect_handler)
ekg.handler_bind('protocol-status', status_handler)
ekg.handler_bind('protocol-message-received', message_handler)
ekg.timer_bind(30, checkMail)
