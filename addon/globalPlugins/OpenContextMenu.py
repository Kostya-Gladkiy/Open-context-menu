import globalPluginHandler
import addonHandler
import inputCore
from keyboardHandler import KeyboardInputGesture
import gui
from gui import SettingsPanel, guiHelper, nvdaControls
import wx
addonHandler.initTranslation()
import languageHandler
import config

SPEC = {
	"key_combination": 'string(default="control+rightShift")',
}

# The current key combination to open the context menu
key_combination = None


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		config.conf.spec['Open_context_menu'] = SPEC
		global key_combination
		key_combination = tuple(config.conf["Open_context_menu"]["key_combination"].split("+"))
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(Settings)
		self._executeGesture = inputCore.manager.executeGesture
		inputCore.manager.executeGesture = self.executeGesture

	def executeGesture(self, gesture):
		if gesture._keyNamesInDisplayOrder == key_combination:
			KeyboardInputGesture.fromName("applications").send()
		else:
			self._executeGesture(gesture)


class Settings(gui.SettingsPanel):
	title = _("Open context menu")

	key_combinations = {
		"control+rightShift": "control+rightShift",
		"rightWindows": "rightWindows",
		"control+escape": "control+escape",
		"rightControl": "rightControl",
	}
	def makeSettings(self, settingsSizer):
		settingsSizerHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.keys = settingsSizerHelper.addLabeledControl(_("Key combination to open the context menu:"), wx.Choice, choices=list(self.key_combinations.values()))
		self.keys.SetStringSelection(config.conf["Open_context_menu"]["key_combination"])
		
	def onSave(self):
		config.conf["Open_context_menu"]["key_combination"] = self.keys.GetStringSelection()
		global key_combination
		key_combination = tuple(config.conf["Open_context_menu"]["key_combination"].split("+"))

	def onPanelActivated(self):
		self.originalProfileName = config.conf.profiles[-1].name
		config.conf.profiles[-1].name = None
		self.Show()

	def onPanelDeactivated(self):
		config.conf.profiles[-1].name = self.originalProfileName
		self.Hide()
