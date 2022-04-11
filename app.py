import os, sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox, QProgressDialog, QToolBar, QAction, QStatusBar, QSizePolicy, QLineEdit, QMenu, QMenuBar, QInputDialog
from PyQt5.QtGui import QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
import ctypes
import argparse
import threading

ap = argparse.ArgumentParser(description="Daraz WebApp")
ap.add_argument("-U", "--url", required=True, type=str, default="no", help="url for web")
args = vars(ap.parse_args())

myappid = u"inventors.daraz.seller.0.0.1"
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class MyApp(QMainWindow):

	def __init__(self, url):
		super().__init__()

		self.url = url
		QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
		self.status = QStatusBar() 

		# setting status bar to the main window 
		self.setStatusBar(self.status)
		menuBar = QMenuBar(self)
		self.setMenuBar(menuBar)

		fileMenu = QMenu("&File", self)
		menuBar.addMenu(fileMenu)

		self.bookmark_bar = QToolBar('Bookmark')
		# self.bookmark_bar.setIconSize(QSize(12, 12))
		self.bookmark_bar.setMovable(False)
		self.addToolBar(self.bookmark_bar)

		 # similarly adding next button 
		next_btn = QAction("Forward", self) 
		next_btn.setStatusTip("Forward to next page") 
		next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward()) 
		self.bookmark_bar.addAction(next_btn) 

		self.initUI()

	def closeEvent(self, event):

		msg_box = QMessageBox()
		msg_box.setIcon(QMessageBox.Warning)
		msg_box.setWindowTitle("Alert")
		msg_box.setText("Are you sure you want to exit the program?")
		msg_box.setWindowIcon(QIcon("resources/icons/daraz.ico"))
		msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

		retval = msg_box.exec_()

		if retval == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def initUI(self):

		self.web = QWebEngineView()
		self.web.setWindowTitle("Daraz")
		self.web.setWindowIcon(QIcon("resources/icons/daraz.ico"))
		# self.web.load(QUrl("https://sellercenter.daraz.pk/"))
		# self.web.load(QUrl("https://junaidfiaz143.wordpress.com"))
		
		menuBar = QMenuBar(self)
		self.setMenuBar(menuBar)


		self.web.load(QUrl(self.url))
		self.web.showMaximized()
		self.web.show()
		self.web.loadStarted.connect(self.webPageLoadStarted)
		self.web.loadProgress.connect(self.webPageLoadProgress)
		self.web.loadFinished.connect(self.webpageLoaded)

		self.web.closeEvent = self.closeEvent

		self.progress = QProgressDialog("Progress", None, 0, 100, self)
		self.progress.setWindowIcon(QIcon("resources/icons/daraz.ico"))
		self.progress.setWindowModality(Qt.WindowModal) 
		self.progress.setWindowTitle("Loading")
		self.progress.setFixedSize(300, 60)
		self.progress.setSizeGripEnabled(False)
		self.progress.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		self.progress.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.Dialog)
		self.progress.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
		self.progress.setWindowFlag(Qt.WindowCloseButtonHint, False) 

		self.progress.hide()

	def mycontextMenuEvent(self, event):

		dlg = QInputDialog(self)
		dlg.setInputMode(QInputDialog.TextInput) 
		dlg.setWindowTitle("Open New Window")
		dlg.setLabelText("URL:")
		dlg.setTextValue("htps://")
		dlg.setWindowIcon(QIcon("resources/icons/daraz.ico"))
		dlg.resize(500, 100)
		# dlg.setStandardButtons("OK")
		ok = dlg.exec_()
		url = dlg.textValue()

		if ok:
			threading.Thread(target=self.openWindow, args=(url,)).start()
			print(url)
		else:
			print("no entry")

	def openWindow(self, url):
		os.system("python app.py -U " + url)

	def webPageLoadStarted(self):
		print("open link")
		# self.web.setContextMenuPolicy(Qt.NoContextMenu)
		self.progress.exec_()

	def webPageLoadProgress(self, prog):
		print("loading: ", prog)
		self.progress.setValue(prog)
		if prog == 100:		
			# self.web.setContextMenuPolicy(self.mycontextMenuEvent)

			self.web.contextMenuEvent = self.mycontextMenuEvent
			self.progress.hide()

	def webpageLoaded(self):
		print("loaded")
		QApplication.restoreOverrideCursor()

def hide_console():
		import win32gui, win32con

		cmd_terminal = win32gui.GetForegroundWindow()
		win32gui.ShowWindow(cmd_terminal , win32con.SW_HIDE)		

if __name__ == '__main__':
	# hide_console()

	app = QApplication(sys.argv)
	app.setApplicationName("Daraz")
	app.setOrganizationName("inventors")

	my_app = MyApp(args["url"])
	sys.exit(app.exec_())