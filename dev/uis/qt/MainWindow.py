#!/usr/bin/env python
# -*- coding:Utf-8 -*-

#
# Modules
#

import operator
import threading

import sys
sys.path.append( ".." ) 

import tvdcore

from base.qt.QtFolderChooser import QtFolderChooser
from base.qt.qtString        import qstringToString
from base.qt.qtString        import stringToQstring

from PyQt4 import QtCore
from PyQt4 import QtGui

from uis.qt.QtIconsList   import QtIconsList
from uis.qt.QtTable       import QtTable
from uis.qt.QtTableView   import QtTableView

from uis.qt.models.FichiersTableModel import FichiersTableModel

#
# Classe
#

class MainWindow( QtGui.QMainWindow ):
	"""
	TVDownloader MainWindows
	"""
	
	def __init__( self, tvdVersion ):
		"""
		Constructeur
		"""
		# Appel au constructeur de la classe mere
		QtGui.QMainWindow.__init__( self )
		
		#
		# Fonts
		#
		
		# Font pour les titres
		self.titreFont = QtGui.QFont()
		self.titreFont.setPointSize( 11 )
		self.titreFont.setWeight( 75 )
		self.titreFont.setBold( True )
		
		#
		# Icones
		#
		
		self.tvdIco    = QtGui.QIcon( "uis/qt/ico/TVDownloader.png" )
		self.folderIco = QtGui.QIcon( "uis/qt/ico/gtk-folder.svg" )
		self.startIco  = QtGui.QIcon( "uis/qt/ico/gtk-media-play-ltr.svg" )
		self.stoprIco  = QtGui.QIcon( "uis/qt/ico/gtk-media-stop.svg" )
		# self.addIco    = QtGui.QIcon( "uis/qt/ico/gtk-add.svg" )
		# self.applyIco  = QtGui.QIcon( "uis/qt/ico/gtk-apply.svg" )
		# self.fileIco   = QtGui.QIcon( "uis/qt/ico/gtk-file.svg" )
		
		#
		# Signaux
		#
		
		# Liste des plugins a mettre en place
		self.listePluginsSignal = QtCore.SIGNAL( "listePlugins(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listePluginsSignal , self.ajouterPlugins )
		
		# Liste des chaines a mettre en place
		self.listeChainesSignal = QtCore.SIGNAL( "listeChaines(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listeChainesSignal , self.ajouterChaines )
		
		# Liste des emissions a mettre en place
		self.listeEmissionsSignal = QtCore.SIGNAL( "listeEmission(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listeEmissionsSignal , self.ajouterEmissions )

		# Liste des fichiers a mettre en place
		self.listeFichiersSignal = QtCore.SIGNAL( "listeFichiers(PyQt_PyObject)" )
		QtCore.QObject.connect( self, self.listeFichiersSignal , self.ajouterFichiers )
		
		#
		# Reglages de la fenetre
		#
		
		# Nom de la fenetre
		self.setWindowTitle( "TVDownloader %s" %( tvdVersion ) )
		# Mise en place de son icone
		self.setWindowIcon( self.tvdIco )
		
		#
		# Widget central de la fenetre
		#
		
		# Widget central qui contiendra tout
		self.centralWidget = QtGui.QWidget( self )
		self.setCentralWidget( self.centralWidget )
		
		# Layout de grille pour le widget central
		self.centralGridLayout = QtGui.QGridLayout( self.centralWidget )
		
		#
		# Onglets
		#
		
		# Gestionnaire onglets
		self.tabWidget = QtGui.QTabWidget( self.centralWidget )
		self.centralGridLayout.addWidget( self.tabWidget, 0, 0, 1, 2 )
		
		# Onglet Fichiers
		self.fichiersWidget = QtGui.QSplitter( QtCore.Qt.Vertical, self.centralWidget )
		self.tabWidget.addTab( self.fichiersWidget, u"Choix des fichiers" )
		
		# Onglet Telechargements
		self.telechargementsWidget = QtTable( self.centralWidget )
		self.tabWidget.addTab( self.telechargementsWidget, u"Téléchargements" )
		
		# Onglet Parametres
		self.parametresWidget = QtGui.QWidget( self.centralWidget )
		self.tabWidget.addTab( self.parametresWidget, u"Paramètres" )
		
		#
		# Onglet Fichiers
		#
		
		# Widget choix fichiers
		self.choixFichiersWidget = QtGui.QSplitter( QtCore.Qt.Horizontal, self.fichiersWidget )
		self.fichiersWidget.addWidget( self.choixFichiersWidget )
				
		# Widget choix de la chaine
		self.chaineWidget = QtGui.QWidget( self.choixFichiersWidget )
		self.choixFichiersWidget.addWidget( self.chaineWidget )
		
		# Layout chaine
		self.chaineLayout = QtGui.QVBoxLayout( self.chaineWidget )
		
		# Choix du plugin
		self.pluginComboBox = QtGui.QComboBox( self.chaineWidget )
		QtCore.QObject.connect( self.pluginComboBox,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerChaines )
		self.chaineLayout.addWidget( self.pluginComboBox )
		
		# Liste des chaines
		self.chaineIconsList = QtIconsList( self.chaineWidget )
		QtCore.QObject.connect( self.chaineIconsList,
								QtCore.SIGNAL( "buttonClicked(PyQt_PyObject)" ),
								self.listerEmissions )
		self.chaineLayout.addWidget( self.chaineIconsList )
		
		# Widget choix des fichiers
		self.fichierWidget = QtGui.QWidget( self.choixFichiersWidget )
		self.choixFichiersWidget.addWidget( self.fichierWidget )
		
		# Layout fichiers
		self.fichierLayout = QtGui.QVBoxLayout( self.fichierWidget )
		
		# Choix de l'emission
		self.emissionComboBox = QtGui.QComboBox( self.fichierWidget )
		QtCore.QObject.connect( self.emissionComboBox,
								QtCore.SIGNAL( "activated(QString)" ),
								self.listerFichiers )
		self.fichierLayout.addWidget( self.emissionComboBox )
		
		# Liste des fichiers
		self.fichierTableView = QtTableView( self.fichierWidget )
		fichierTableModel = FichiersTableModel()
		self.fichierTableView.setModel( fichierTableModel )
		self.fichierLayout.addWidget( self.fichierTableView )
		
		QtCore.QObject.connect( self.fichierTableView,
								QtCore.SIGNAL( "clicked(const QModelIndex &)" ),
								self.afficherDescriptionFichier )	
		
		# QtCore.QObject.connect( self.fichierTableView,
								# QtCore.SIGNAL( "doubleClicked(const QModelIndex &)" ),
								# self.gererTelechargement )	

		# Widget descriptif fichier
		self.descriptifFichierWidget = QtGui.QSplitter( QtCore.Qt.Horizontal, self.fichiersWidget )
		self.fichiersWidget.addWidget( self.descriptifFichierWidget )
		
		# Label du fichier
		self.fichierLabel = QtGui.QLabel( self.descriptifFichierWidget )
		self.descriptifFichierWidget.addWidget( self.fichierLabel )

		# Logo par defaut
		self.logoDefautPixmap = QtGui.QPixmap()
		self.logoDefautPixmap.load( "uis/qt/ico/gtk-dialog-question.svg" )
		self.afficherImageDescription( self.logoDefautPixmap )

		# Descriptif du fichier
		self.descriptionPlainTextEdit = QtGui.QPlainTextEdit( self.descriptifFichierWidget )
		self.descriptifFichierWidget.addWidget( self.descriptionPlainTextEdit )
		
		#
		# Onglet Telechargements
		#

		# Liste des telechargements
		self.telechargementsWidget.setColumnCount( 4 ) # 4 colonnes
		self.telechargementsWidget.setRowCount( 0 )    # 0 ligne
		self.telechargementsWidget.setHorizontalHeaderItem( 0, self.telechargementsWidget.createItem( "Nom" ) )
		self.telechargementsWidget.setHorizontalHeaderItem( 1, self.telechargementsWidget.createItem( "Avancement" ) )
		self.telechargementsWidget.setHorizontalHeaderItem( 2, self.telechargementsWidget.createItem( "Vitesse" ) )		
		self.telechargementsWidget.setHorizontalHeaderItem( 3, self.telechargementsWidget.createItem( "Stopper" ) )		
				
		#
		# Onglet Parametres
		#
		
		# Layout de forumlaire
		self.parametresLayout = QtGui.QFormLayout( self.parametresWidget )
		
		# Titre Repertoire
		self.titreRepertoireLabel = QtGui.QLabel( self.parametresWidget )
		self.titreRepertoireLabel.setFont( self.titreFont )
		self.titreRepertoireLabel.setText( u"Répertoires :" )
		self.parametresLayout.addRow( self.titreRepertoireLabel, None )		
		
		# Repertoire par defaut pour les videos
		self.choixRepertoire = QtFolderChooser( self.parametresWidget, self.folderIco )
		self.parametresLayout.addRow( u"Répertoire de téléchargement :", self.choixRepertoire )
		
		# Titre Internet
		self.titreInternetLabel = QtGui.QLabel( self.parametresWidget )
		self.titreInternetLabel.setFont( self.titreFont )
		self.titreInternetLabel.setText( u"Paramètres Internet :" )
		self.parametresLayout.addRow( self.titreInternetLabel, None )
		
		# Time out du navigateur
		self.timeOutSpinBox = QtGui.QSpinBox( self.parametresWidget )
		self.timeOutSpinBox.setMinimum( 1 )
		self.timeOutSpinBox.setMaximum( 60 )
		self.parametresLayout.addRow( u"Time out (en s) :", self.timeOutSpinBox )
		
		# Nombre de threads du navigateur
		self.threadSpinBox = QtGui.QSpinBox( self.parametresWidget )
		self.threadSpinBox.setMinimum( 1 )
		self.threadSpinBox.setMaximum( 100 )
		self.parametresLayout.addRow( u"Nombre de threads max :", self.threadSpinBox )
		
		#
		# Descriptif des fichiers
		#
		
		#
		# Barres de progression
		#
		
		self.dlFichierProgressBar = QtGui.QProgressBar( self.centralWidget )
		self.dlFichierProgressBar.setProperty( "value", 0 )
		self.centralGridLayout.addWidget( self.dlFichierProgressBar, 2, 0, 1, 2 )
		
		self.dlProgressBar = QtGui.QProgressBar( self.centralWidget )
		self.dlProgressBar.setProperty( "value", 0 )
		self.centralGridLayout.addWidget( self.dlProgressBar, 3, 0, 1, 2 )
		
		#
		# Bouton de téléchargement
		#
		
		self.lancerPushButton = QtGui.QPushButton( self.startIco, u"Lancer téléchargement", self.centralWidget )
		self.centralGridLayout.addWidget( self.lancerPushButton, 4, 0, 1, 2 )
		
		#
		# Signaux de TVDownloader
		#

		QtCore.QObject.connect( self,
								QtCore.SIGNAL( "nouvelleImageDescription(PyQt_PyObject)" ),
								self.afficherImageDescription )	
		
		#
		# Debut
		#
		
		self.actionsAuDebut()
		
	def closeEvent( self, evt ):
		"""
		Surcharge de la methode appele lors de la fermeture de la fenetre
		"""
		self.actionsAvantQuitter()
		evt.accept()
	
	def actionsAuDebut( self ):
		"""
		Actions a realiser au demarage du programe
		"""
		# Recupere l'instance de TVDContext
		self.tvdContext = tvdcore.TVDContext()
		# Recupere les instances des classes utiles
		self.pluginManager   = self.tvdContext.pluginManager
		self.downloadManager = self.tvdContext.downloadManager
		self.navigateur      = tvdcore.Navigateur()
		
		# Liste les plugins
		self.listerPlugins()
		
	def actionsAvantQuitter( self ):
		"""
		Actions a realiser avant de quitter le programme
		"""
		print "Bye bye"
		
	def listerPlugins( self ):
		"""
		Fonction qui demande la liste des plugins
		"""
		def threadListerPlugins( self ):
			listePlugins = self.pluginManager.getPluginListe()
			self.emit( self.listePluginsSignal, listePlugins )
		
		threading.Thread( target = threadListerPlugins, args = ( self, ) ).start()
	
	def listerChaines( self, plugin = None ):
		"""
		Fonction qui demande la liste des chaines d'un plugin donne
		Si plugin = None, alors elle demande la liste des chaines de tous les plugins
		"""
		def threadListerChaines( self, plugin ):
			listeChaines = map( lambda x : ( x, None ), self.pluginManager.getPluginListeChaines( plugin ) )
			self.emit( self.listeChainesSignal, listeChaines )
		
		if( plugin ):
			plugin = qstringToString( plugin )
		threading.Thread( target = threadListerChaines, args = ( self, plugin ) ).start()

	def listerEmissions( self, chaine ):
		"""
		Fonction qui demande la liste des emissions d'une chaine donnee
		"""
		def threadListerEmissions( self, plugin, chaine ):
			listeEmissions = self.pluginManager.getPluginListeEmissions( plugin, chaine )
			self.emit( self.listeEmissionsSignal, listeEmissions )
		
		plugin = qstringToString( self.pluginComboBox.currentText() )
		threading.Thread( target = threadListerEmissions, args = ( self, plugin, chaine ) ).start()

	def listerFichiers( self, emission ):
		"""
		Fonction qui demande la liste des fichiers d'une emission donnee
		"""		
		def threadListerFichiers( self, plugin, emission ):
			listeFichiers = self.pluginManager.getPluginListeFichiers( plugin, emission )
			self.emit( self.listeFichiersSignal, listeFichiers )
		
		plugin = qstringToString( self.pluginComboBox.currentText() )
		threading.Thread( target = threadListerFichiers, args = ( self, plugin, qstringToString( emission ) ) ).start()		
		
	def ajouterPlugins( self, listePlugins ):
		"""
		Met en place la liste des plugins donnee
		"""
		listePlugins.sort()
		self.pluginComboBox.clear()
		map( lambda x : self.pluginComboBox.addItem( stringToQstring( x ) ), listePlugins )
		# S'il n'y a qu'un seul plugin
		if( self.pluginComboBox.count() == 1 ):
			# Lance le listage des chaines
			self.listerChaines( self.pluginComboBox.currentText() )
		else:
			# Ne selectionne pas le plugin
			self.pluginComboBox.setCurrentIndex( -1 )	
	
	def ajouterChaines( self, listeChaines ):
		"""
		Met en place la liste des chaines donnee sous la forme ( nomChaine, logoChaine )
		"""
		listeChaines = sorted( listeChaines, key = operator.itemgetter( 0 ) )
		self.chaineIconsList.clear()
		map( lambda ( x, y ) : self.chaineIconsList.addIcon( x, y ), listeChaines )

	def ajouterEmissions( self, listeEmissions ):
		"""
		Met en place la liste des emissions
		"""
		listeEmissions.sort()
		self.emissionComboBox.clear()
		self.ajouterFichiers( [] )
		map( lambda x : self.emissionComboBox.addItem( stringToQstring( x ) ), listeEmissions )
		# S'il n'y a qu'une seule emission
		if( self.emissionComboBox.count() == 1 ):
			# Lance le listage des fichiers
			self.listerFichiers( self.emissionComboBox.currentText() )
		else:
			# Ne selectionne pas le plugin
			self.emissionComboBox.setCurrentIndex( -1 )	
	
	def ajouterFichiers( self, listeFichiers ):
		"""
		Met en place la liste des fichiers
		"""
		self.fichierTableView.model().changeFiles( listeFichiers )
		self.fichierTableView.resizeColumnsToContents()
	
	def ajouterTelechargement( self, fichier ):
		"""
		Met en place la liste des telechargements
		"""
		# Ajoute le fichier a la GUI
		ligneCourante = self.telechargementsWidget.rowCount()
		self.telechargementsWidget.insertRow( ligneCourante )
		tableRow = []
		tableRow.append( self.telechargementsWidget.createItem( fichier.nom ) )
		tableRow.append( self.telechargementsWidget.createItem( "0" ) )
		tableRow.append( self.telechargementsWidget.createItem( "0" ) )
		tableRow.append( self.telechargementsWidget.createItem( "Stop" ) )
		self.telechargementsWidget.setLigne( ligneCourante, tableRow )
		self.telechargementsWidget.resizeColumnsToContents()
		# Ajoute le fichier au downloadManager
		self.downloadManager.download( fichier )
	
	def afficherDescriptionFichier( self, index ):
		"""
		Affiche les informations du fichier selectionne
		"""
		def threadRecupererImageDescription( self, urlImage ):
			imageData = self.navigateur.getPicture( urlImage )
			image = QtGui.QPixmap()
			image.loadFromData( imageData )
			self.emit( QtCore.SIGNAL( "nouvelleImageDescription(PyQt_PyObject)" ), image )

		fichier = self.fichierTableView.model().listeFichiers[ index.row() ]
		# Affiche la description
		self.descriptionPlainTextEdit.clear()
		if( fichier.descriptif != "" ):
			self.descriptionPlainTextEdit.appendPlainText( stringToQstring( fichier.descriptif ) )
		else:
			self.plainTextEdit.appendPlainText( u"Aucune information disponible" )
		# Recupere l'image
		if( fichier.urlImage != "" ):
			threading.Thread( target = threadRecupererImageDescription, args = ( self, fichier.urlImage ) ).start()
		else:
			self.afficherImageDescription( self.logoDefautPixmap )

	def afficherImageDescription( self, image ):
		"""
		Affiche l'image de description du fichier selectionne
		"""
		self.fichierLabel.setPixmap( image.scaled( QtCore.QSize( 150, 150 ), QtCore.Qt.KeepAspectRatio ) )
