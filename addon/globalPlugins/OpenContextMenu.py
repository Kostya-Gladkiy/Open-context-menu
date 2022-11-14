import globalPluginHandler
import inputCore
from keyboardHandler import KeyboardInputGesture


class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self._executeGesture = inputCore.manager.executeGesture
		inputCore.manager.executeGesture = self.executeGesture

	def executeGesture(self, gesture):
		if gesture._keyNamesInDisplayOrder == ('control', 'rightShift'):
			KeyboardInputGesture.fromName("shift+f10").send()
			gesture.send()
		else:
			self._executeGesture(gesture)