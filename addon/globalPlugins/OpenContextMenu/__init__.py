import globalPluginHandler
import addonHandler
import mouseHandler
import inputCore
from keyboardHandler import KeyboardInputGesture
import gui
from gui import SettingsPanel, guiHelper, nvdaControls
import wx
addonHandler.initTranslation()
# import languageHandler
import config
import api

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
		if hasattr(gesture, "_keyNamesInDisplayOrder") and gesture._keyNamesInDisplayOrder == key_combination:
			try:
				# If the click occurs in the document, then you need to get a focusable element under the cursor and set the focus on it so that the context menu is called to this object
				obj = api.getCaretObject().currentFocusableNVDAObject
				api.moveMouseToNVDAObject(obj)
				api.setMouseObject(obj)
				mouseHandler.doSecondaryClick()
			except: 
				obj = api.getFocusObject()
				KeyboardInputGesture.fromName("applications").send()
		self._executeGesture(gesture)


class Settings(gui.SettingsPanel):
	title = _("Open context menu")

	key_combinations = {
		"control+rightShift": "control+rightShift",
		"rightControl": "rightControl",
		"control+rightControl": "control+rightControl",
		"alt+rightControl": "alt+rightControl",
		"windows+rightControl": "windows+rightControl",
		"windows+leftShift": "windows+leftShift",
		"windows+rightShift": "windows+rightShift",
		# "windows+leftAlt": "windows+leftAlt",
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
