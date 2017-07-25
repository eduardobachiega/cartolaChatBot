#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import datetime
import cartolafc
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

api = cartolafc.Api(email='allan75silva@yahoo.com.br', password='sevirabrother', attempts=10)

def start(bot, update):
    update.message.reply_text('Ola! Eu sou um bot para dar informacoes do cartola!')

def help(bot, update):
    update.message.reply_text(getHelp(), parse_mode='HTML')

def team(bot, update, args):
	update.message.reply_text(text=getTeamByName(' '.join(args)), parse_mode='HTML')

def teamSlug(bot, update, args):
	update.message.reply_text(text=getTeamBySlug(args[0]), parse_mode='HTML')

def league(bot, update, args):
	update.message.reply_text(text=getLeagueByName(' '.join(args)), parse_mode='HTML')

def leagueSlug(bot, update, args):
	update.message.reply_text(text=getLeagueBySlug(args[0]), parse_mode='HTML')

def round(bot, update, args):
	update.message.reply_text(text=getRoundByName(' '.join(args)), parse_mode='HTML')

def roundSlug(bot, update, args):
	update.message.reply_text(text=getRoundBySlug(args[0]), parse_mode='HTML')

def games(bot, update, args):
	if len(args) > 0:
		update.message.reply_text(getGames(args[0]), parse_mode='HTML')
	else:
		update.message.reply_text(getGames(None), parse_mode='HTML')

def echo(bot, update):
    update.message.reply_text(update.message.text)
    
def teamSearch(bot, update, args):
	update.message.reply_text(text=getTeamSearch(' '.join(args)), parse_mode='HTML')

def leagueSearch(bot, update, args):
	update.message.reply_text(text=getLeagueSearch(' '.join(args)), parse_mode='HTML')

def market(bot, update):
	update.message.reply_text(text=getMarketInfo(), parse_mode='HTML')

def best(bot, update):
	getBest(update)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def getBest(update):
	try:
		destaque = api.pos_rodada_destaques()
		message = "Destaques da rodada\n\n"
		message += "<b>Média de cartoletas:</b> %s\n" %(str("%.2f" %(destaque.media_cartoletas)))
		message += "<b>Média de pontos:</b> %s\n\n" %(str("%.2f" %(destaque.media_pontos)))
		time = destaque.mito_rodada
		update.message.reply_text(text=message, parse_mode='HTML')
		update.message.reply_text(text="Mito da rodada\n\n" + getTeamBySlug(time.slug), parse_mode='HTML')
	except Exception as e:
		return str(e)

def getMarketInfo():
	try:
		mercado = api.mercado()
		message = "Informações do mercado\n\n"
		message += "<b>Rodada atual:</b> %s\n" %(str(mercado.rodada_atual))
		message += "<b>Status:</b> %s\n" %(mercado.status.nome)
		message += "<b>Times escalados:</b> %s\n" %(str(mercado.times_escalados))
		aviso = mercado.aviso
		if len(aviso) == 0:
			aviso = "Sem aviso"
		message += "<b>Aviso:</b> %s\n" %(aviso)
		fechamentoDate = mercado.fechamento
		fechamento = fechamentoDate.strftime("%d/%m/%Y %H:%M")
		message += "<b>Fechamento:</b> %s\n" %(fechamento)
		return message
	except Exception as e:
		return str(e)

def getTeamSearch(query):
	try:
		times = api.times(query=query)
		message = "Times encontrados \n\n"
		for time in times:
			message += "<b>%s</b>, time de <b>%s</b> (Slug: <b>%s</b>)\n\n" %(time.nome, time.nome_cartola, time.slug)
		return message
	except Exception as e:
		return str(e)

def getLeagueSearch(query):
	try:
		ligas = api.ligas(query=query)
		message = "Ligas encontradas \n\n"
		for liga in ligas:
			message += "Liga: <b>%s</b> Slug: <b>%s</b>\n\n" %(liga.nome, liga.slug)
		return message
	except Exception as e:
		return str(e)

def getHelp():
	text = "Comandos Cartola Bot: \n\n"
	text += "/start <b>-></b> inicia o bot \n"
	text += "/help <b>-></b> ajuda \n"
	text += "/time {nome} <b>-></b> informações do time \n"
	text += "/timeSlug {slug} <b>-></b> informações do time \n"
	text += "/liga {nome} <b>-></b> informações da liga \n"
	text += "/ligaSlug {slug} <b>-></b> informações da liga \n"
	text += "/jogos <b>-></b> jogos da rodada atual \n"
	text += "/jogos {numero_rodada} <b>-></b> jogos de uma rodada específica \n"
	text += "/rodada {nomeLiga} <b>-></b> pontuação dos times da liga na rodada atual \n"
	text += "/rodadaSlug {slugLiga} <b>-></b> pontuação dos times da liga na rodada atual \n"
	text += "/buscaTime {busca} <b>-></b> time ou donos correspondentes a busca \n"
	text += "/buscaLiga {busca} <b>-></b> ligas correspondentes a busca \n"
	text += "/mercado -> informações do mercado \n"
	text += "/destaque -> o mito da rodada"
	text += "\n* Para melhor resultado é recomendado utilizar slugs de times e ligas\n"
	return text

def getRoundBySlug(leagueSlug):
	try:
		liga = api.liga(slug=leagueSlug, order_by=cartolafc.RODADA)
		times = liga.times
		league = "<b>" + liga.nome + "</b>\n\n"
		for time in times:
			timeReq = api.time(slug=time.slug)
			league += "<b>" + time.nome + "</b> (" + time.nome_cartola + "): <b>%.2f</b>\n" %(timeReq.ultima_pontuacao) 
		return league
	except Exception as e:
		return str(e)

def getRoundByName(leagueName):
	try:
		liga = api.liga(nome=leagueName, order_by=cartolafc.RODADA)
		times = liga.times
		league = "<b>" + liga.nome + "</b>\n\n"
		for time in times:
			timeReq = api.time(slug=time.slug)
			league += "<b>" + time.nome + "</b> (" + time.nome_cartola + "): <b>%.2f</b>\n" %(timeReq.ultima_pontuacao) 
		return league
	except Exception as e:
		return str(e)

def getGames(round):
	if round is None:
		mercado = api.mercado()
		round = str(mercado.rodada_atual)

	r = requests.get('https://api.cartolafc.globo.com/partidas/' + round)
	json = r.json()
	message = "Partidas da rodada %s\n\n" %(round)
	if "mensagem" in json:
		message = json['mensagem']
	else:
		clubes = json['clubes']
		partidas = json['partidas']
		for partida in partidas:
			homeId = str(partida['clube_casa_id'])
			awayId = str(partida['clube_visitante_id'])
			homeTeam = clubes[homeId]
			awayTeam = clubes[awayId]
			homeScore = partida['placar_oficial_mandante']
			awayScore = partida['placar_oficial_visitante']
			if homeScore == None:
				homeScore = 0
				awayScore = 0
			message += "<b>%s</b> (%s) X (%s) <b>%s</b>\n" %(homeTeam['nome'], homeScore, awayScore, awayTeam['nome'])
	return message

def getTeamBySlug(teamSlug):
	try:
		time = api.time(slug=teamSlug)
		team = "<b>" + time.info.nome + "</b>, time de <b>" + time.info.nome_cartola + "</b>\n\n"
		team += "Ultima pontuacao: <b>%.2f</b>\n\n" %(time.ultima_pontuacao)
		atletas = time.atletas
		for atleta in atletas:
			team += atleta.apelido + " (" + atleta.clube.nome + "): <b>%.2f</b>\n" %(atleta.pontos)
		return team
	except Exception as e:
		return str(e)

def getTeamByName(teamName):
	try:
		time = api.time(nome=teamName)
		team = "<b>" + time.info.nome + "</b>, time de <b>" + time.info.nome_cartola + "</b>\n\n"
		team += "Ultima pontuacao: <b>%.2f</b>\n\n" %(time.ultima_pontuacao)
		atletas = time.atletas
		for atleta in atletas:
			team += atleta.apelido + " (" + atleta.clube.nome + "): <b>%.2f</b>\n" %(atleta.pontos)
		return team
	except Exception as e:
		return str(e)

def getLeagueBySlug(leagueSlug):
	try:
		liga = api.liga(slug=leagueSlug)
		times = liga.times
		league = "<b>" + liga.nome + "</b>\n\n"
		for time in times:
			league += "<b>" + time.nome + "</b> (" + time.nome_cartola + "): <b>%.2f</b>\n" %(time.pontos) 
		return league
	except Exception as e:
		return str(e)

def getLeagueByName(leagueName):
	try:
		liga = api.liga(nome=leagueName)
		times = liga.times
		league = "<b>" + liga.nome + "</b>\n\n"
		for time in times:
			league += "<b>" + time.nome + "</b> (" + time.nome_cartola + "): <b>%.2f</b>\n" %(time.pontos) 
		return league
	except Exception as e:
		return str(e)
		
def main():
    updater = Updater("379341428:AAFb9lsdw7ISbRYENaiXqV3w7J4aaTJ8LDo")

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("time", team, pass_args=True))
    dp.add_handler(CommandHandler("liga", league, pass_args=True))
    dp.add_handler(CommandHandler("jogos", games, pass_args=True))
    dp.add_handler(CommandHandler("rodada", round, pass_args=True))
    dp.add_handler(CommandHandler("timeSlug", teamSlug, pass_args=True))
    dp.add_handler(CommandHandler("ligaSlug", leagueSlug, pass_args=True))
    dp.add_handler(CommandHandler("rodadaSlug", roundSlug, pass_args=True))
    dp.add_handler(CommandHandler("buscaTime", teamSearch, pass_args=True))
    dp.add_handler(CommandHandler("buscaLiga", leagueSearch, pass_args=True))
    dp.add_handler(CommandHandler("mercado", market))
    dp.add_handler(CommandHandler("destaque", best))
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
	main()