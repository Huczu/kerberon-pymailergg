#!/usr/bin/python
# -*- coding: utf-8 -*-
#config do skryptu


#sms sender
numer = "+48601000000" # koniecznie +48
siec = "plus" # na razie obslugiwany tylko Plus
czas = (9,23) #dozwolony czas w ktorym moze wyslac sms niech nas kuhwa nie budzi o 3 nad ranem, ze nowe gacie -30% w croppie
server = 1 # Ktory e-mail ma odpowiadac za wyslanie wiadomosci na nasza komorke liczymy z krotki od 0, polecam gmail
#Mailer
imap_port = 993 # port od IMAP
smtp_port = 465 # port od SMTP
emails = ( #domain, (login, pass), {pamiec, pamiec2}
		("huczu.pl",("admin@huczu.pl","pass",),{"email_memory":0, "mem":0,})
		("gmail.com",("huczu93@gmail.com","pass",), {"email_memory":0, "mem":0}),
		("huk.mail.pl",("andrzej@huk.mal.pl","pass",), {"email_memory":0, "mem":0}),
)

#Other
admin = "gg:3667449" # moze to byc rownie dobrze inny protokol for ex. xmpp , irc
nazwa_kodowa = "Kerberon" #nazwa kodowa, piekna c'nie?
autor = "Huczu" # prosze mnie uszanowac i tego nie ruszac ;)
version = "1.0beta" #pierwsza beta ktora ujrzy swiat
wykop_rss = "http://www.wykop.pl/rss/5958707a595145454d513d3d/7a40f0460b0d6f220bbe57e6f8f7d21be35c1212/" #link do rss
