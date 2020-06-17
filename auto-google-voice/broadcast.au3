#include <AutoItConstants.au3>
#include <File.au3>

Global $scriptPaused = False

HotKeySet("{PAUSE}", "TogglePause")
HotKeySet("{BS}", "Terminate")

; We don't want to trigger Google's security features
Global $mouseSpeed = 1
Global $STR_STRIPENDS = $STR_STRIPLEADING + $STR_STRIPTRAILING
; Text file with all of the phone numbers
Local $phoneNumbers = FileOpen("numbers.txt")
; Text file with the automated message to send
Local $autoMessage = FileReadLine(FileOpen("message.txt"))

While True
    Local $line = FileReadLine($phoneNumbers)
    Local $matches = StringRegExp($line, "(\w+)[\w\s]*,\s*(\d+)", $STR_REGEXPARRAYMATCH)
    If @error Then ExitLoop

    SendTextMessage($matches[1], StringReplace($autoMessage, "$NAME", $matches[0]))
WEnd

MsgBox($MB_SYSTEMMODAL + $MB_OK, "Script finished!", "Click OK to exit.")

Func SendTextMessage($number, $message)
    ; Click "Send new message"
    MouseClick($MOUSE_CLICK_PRIMARY, 1230, 210, $mouseSpeed)
    Sleep(700)
    ; Save the number to the clipboard so fewer keys are sent
    ClipPut($number)
    ; Send the keys for the phone number
    Send("^v")
    Sleep(100)
    ; Click "Send to" in the list
    MouseClick($MOUSE_CLICK_PRIMARY, 1520, 270, $mouseSpeed)
    Sleep(1000)
    Send("{ESC}")
    Sleep(700)
    ; Click on "Type a message"
    MouseClick($MOUSE_CLICK_PRIMARY, 1440, 1050, $mouseSpeed)
    Sleep(700)
    ; Save the message to the clipboard so fewer keys are sent
    ClipPut($message)
    ; Send the characters of the message to the input
    Send("^v")
    ; Click on the send button
    MouseClick($MOUSE_CLICK_PRIMARY, 1890, 1030, $mouseSpeed)
    Sleep(2000)
EndFunc

Func TogglePause()
    $scriptPaused = Not $scriptPaused
    While $scriptPaused
        Sleep(100)
        MsgBox($MB_SYSTEMMODAL + $MB_OK, "Script paused!", "Click OK to continue executing.")
        $scriptPaused = Not $scriptPaused
    WEnd
EndFunc

Func Terminate()
    Exit
EndFunc
