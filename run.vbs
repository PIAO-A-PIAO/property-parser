Set objShell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Get the directory where this script is located
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)

' Change to the project directory
objShell.CurrentDirectory = scriptDir

' First, check for updates silently (hidden window, wait for completion)
On Error Resume Next
objShell.Run "pythonw src/update.py", 0, True
On Error Goto 0

' Now run the main application (hide console window)
objShell.Run "pythonw src/main.py", 0, False