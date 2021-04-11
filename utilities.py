from pynput.keyboard import Key, Controller,Listener , KeyCode
from pynput import keyboard
from sclip import Sclip


def HotkeyChecker(transfer_binds:list , paste_binds:list ):
    s = Sclip()
    HotkeyDict = {'<ctrl>+<alt>+s': lambda:print("Restored")}
    failed = False
    def OnTransfer():
        print('Transfered')
        s.SendtoSecondaryClipboard()

    def OnPaste():
        print('Pasted')
        s.PasteFromSclip()

    def Restore():
    	print("Restored")
    	win.show()


    for i in transfer_binds:
    	if(i in paste_binds):
    		failed = True
    		break
    	HotkeyDict[HotkeyParser(i)] = OnTransfer
    for i in paste_binds:
    	if(i in transfer_binds):
    		failed = True
    		break
    	HotkeyDict[HotkeyParser(i)] = OnPaste
    print(HotkeyDict)
    if(not failed):
	    with keyboard.GlobalHotKeys(HotkeyDict) as h:
	        h.join()
    else:
        return False


def HotkeyParser(s:str):

	binds = list(s.split("+"))
	otpt = ""
	for i in binds:
		if(len(i) > 1):
			otpt = otpt+f"<{i.lower()}>+"
		else:
			otpt = otpt + i.lower() + "+"
	otpt = otpt[:-1]
	return otpt



if __name__ == "__main__":
	HotkeyChecker(["Ctrl+T"] , ["Ctrl+B"])