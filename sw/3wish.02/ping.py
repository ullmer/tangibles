############# get main window #############

def getMainWindow():
  "returns the main window"
  # using QtGui.qApp.activeWindow() isn't very reliable because if another
  # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
  # returned

  #toplevel = QtGui.qApp.topLevelWidgets()
  toplevel = QtGui.QApplication.topLevelWidgets()
  for i in toplevel:
    if i.metaObject().className() == "Gui::MainWindow": return i
  raise Exception("No main window found")
  
############# get combo view #############

def getComboView(mw):
  dw=mw.findChildren(QtGui.QDockWidget)
  for i in dw:
    if str(i.objectName()) == "Combo View":
      return i.findChild(QtGui.QTabWidget)
    elif str(i.objectName()) == "Python Console":
      return i.findChild(QtGui.QTabWidget)
  raise Exception ("No tab widget found")

############# build freecad user interface #############

def ping():

  mw  = getMainWindow()
  tab = getComboView(mw)
  print(dir(tab))

