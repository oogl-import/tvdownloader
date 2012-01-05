#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#########################################
# Licence : GPL2 ; voir fichier LICENSE #
#########################################

#~ Ce programme est libre, vous pouvez le redistribuer et/ou le modifier selon les termes de la Licence Publique Générale GNU publiée par la Free Software Foundation (version 2 ou bien toute autre version ultérieure choisie par vous).
#~ Ce programme est distribué car potentiellement utile, mais SANS AUCUNE GARANTIE, ni explicite ni implicite, y compris les garanties de commercialisation ou d'adaptation dans un but spécifique. Reportez-vous à la Licence Publique Générale GNU pour plus de détails.
#~ Vous devez avoir reçu une copie de la Licence Publique Générale GNU en même temps que ce programme ; si ce n'est pas le cas, écrivez à la Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307, États-Unis.

###########
# Modules #
###########
import httplib,re
from random import choice
from APIPrive  import APIPrive
from urlparse import urlparse

##########
# Classe #
##########

## Classe rassemblant des méthodes utils et nécessaire aux plugins.
#
# Cette classe fournis des méthodes permattant de facilité la création d'un plugin. Elle est pour l'instant peu fournis mais a pour but d'être étoffé avec le temps et la possible augmentation de fonctionnalité possible des plugins.
# Elle contient aussi des méthodes permettant de dialoguer avec le programme.
class API(APIPrive):
	## Instance utilisé par le programme
	INSTANCE = None
	
	## Constructeur.
	# Ne pas utiliser.
	# @param self l'objet courant
	def __init__( self ):
		APIPrive.__init__( self )
		
		if API.INSTANCE != None:
			raise Exception("API est déjà instancier")
	
	## Renvoie l'instance d'API
	# @return l'instance d'API
	@staticmethod
	def getInstance():
		"""Renvoie l'instance de l'API"""
		return API.INSTANCE
	
	## Récupère une page web sur internet et remplace les caractères spéciaux (code HTML ou ISO).
	# @param self le plugin courant
	# @param url l'url de la page web
	# @return la page web sous forme d'une chaîne ou la chaîne vide en cas d'échec
	def getPage(self, url):
		#Vérification de l'url
		match = re.match(API.PATTERN_URL, url)
		if match == None:
			print "API.getPage(): url invalide."
			return ""
		
		#Téléchargement et décompression si néscessaire
		connexion = httplib.HTTPConnection(match.group(1), timeout=APIPrive.HTTP_TIMEOUT)
		
		heads = {"Accept-Encoding":"deflate,gzip",
			"User-Agent":choice(APIPrive.USER_AGENT)}
		connexion.request("GET", match.group(2), headers=heads)
		reponse = connexion.getresponse()
		if reponse == None:
			print "API.getPage(): erreur de téléchargement."
			return ""
		return self.reponseHttpToUTF8(reponse)
	
	## Récupère des pages webs sur internet et remplace les caractères spéciaux (code HTML ou ISO). Cette méthode reste connecté au serveur si il y a plusieurs page à y télécharger, elle est plus rapide que plusieurs appel à #getPage.
	# @param self le plugin courant
	# @param urls une liste d'url des pages à télécharger
	# @return un dictionnaire avec comme clé les urls et comme valeur les pages sous forme de chaîne
	def getPages(self, urls):
		reponses = {}
		connexions = {}
		for url in urls:
			parse = urlparse(url)
			query = parse.query
			if query != "":
				query = "?"+query
			path = parse.path
			if path == "":
				path = "/"
				
			requette = path+query
			serveur= parse.netloc
			
			connexion = None
			if not connexions.has_key(serveur):
				connexion = httplib.HTTPConnection(serveur, timeout=APIPrive.HTTP_TIMEOUT)
				connexion.connect()
				connexions[serveur] = connexion
			else:
				connexion = connexions[serveur]
			connexion.putrequest("GET", requette)
			connexion.putheader("Connexion", "Keep-alive")
			connexion.endheaders()
			
			reponse = connexion.getresponse()
			if reponse == None:
				print "API.getPages(): erreur de téléchargement de",url
				reponses[url] = ""
			else:
				reponses[url] = self.reponseHttpToUTF8(reponse)
		for serveur in connexions.keys():
			connexions[serveur].close()
		return reponses

API.INSTANCE = API()

