#!/usr/bin/env python
# -*- coding:Utf-8 -*-

###########
# Modules #
###########

import time

import Constantes

import logging
logger = logging.getLogger( __name__ )

###########
# Classes #
###########

## Classe image
class Image( object ):
	
	## Constructeur
	# @param nom      Nom de l'image
	# @param donnees  Donnees de l'image
	# @param date     Date de derniere utilisation de l'image
	def __init__( self, nom, donnees = "", date = int( time.time() ) ):
		self.nom     = nom
		self.donnees = donnees
		self.date    = date # timestamp
		
	## Surcharge de la methode ==
	# @param autre L'autre image a comparer
	# @return      Si les 2 images sont egales
	def __eq__( self, autre ):
		if( not isinstance( autre, Image ) ):
			return False
		else:
			return( self.nom == autre.nom )
	
	## Surcharge de la methode !=
	# @param autre L'autre image a comparer
	# @return      Si les 2 images sont differentes
	def __ne__( self, autre ):
		return not self.__eq__( autre )
		

## Classe permettant de gerer les images
class Gestionnaire( object ):
	
	# Instance de la classe (singleton)
	instance = None
	
	## Surcharge de la methode de construction standard (pour mettre en place le singleton)
	def __new__( self, *args, **kwargs ):
		if( self.instance is None ):
			self.instance = super( Gestionnaire, self ).__new__( self )
		return self.instance
	
	## Constructeur
	def __init__( self ):
		self.cache       = {}
		self.nombreAcces = 0
		
	## Vide le cache
	def viderCache( self ):
		self.cache.clear()
		
	## Nettoie le cache
	# Supprime les entrees les plus vieilles du cache
	def nettoieCache( self ):
		if( len( self.cache ) > Constantes.TAILLE_CACHE_IMAGE ):
			logger.info( "netttoieCache : le cache des images est trop important ; nettoyage" )
			lienDate = []
			for( lien, image ) in self.cache.items():
				lienDate.append( ( image.date, lien ) )
			lienDate.sort()
			for i in range( len( self.cache ) - Constantes.TAILLE_CACHE_IMAGE ):
				del self.cache[ lienDate[ i ][ 1 ] ]
	
	## Recupere une image
	# @param url URL de l'image
	# @return    L'image demandee
	def getImage( self, url ):
		if( self.cache.has_key( url ) ):
			image = self.cache[ url ]
			image.date = int( time.time() )
		else:
			# Telecharge l'image puis la met en cache
			pass
		
		# Nettoie le cache apres un nombre d'acces important au cache
		self.nombreAcces += 1
		if( self.nombreAcces > Constantes.TAILLE_CACHE_IMAGE ):
			self.nettoieCache()
			self.nombreAcces = 0
		
		return image
