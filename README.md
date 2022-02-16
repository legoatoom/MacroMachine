#  SimpleMacroMaker
Simple pynput hotkey ➔ commands, made for myself. You can look at the code if you like.

## Really want to use it?
No promises about the accuracy and reliability, if something goes wrong not my fault.

I used pyinstaller to install it with `pyinstaller --onefile main.py -n=macromachine`
make sure you have the modules/packages/ect.. installed (see `main.py` for what imports I used).

Then in you can run the macromachine file that was created via commandline.
`macromachine` starts
`macromachine stop` stops it.

It program uses a `config.json` file in `appdirs.user_config_dir('macromachine')`. Don't know where it is for every system.
And this is how the config.json looks.

```json
{
	"[pynput hotkey here]" : {
		"type" : "[toggle|button]",
		"on_commands" : ["[command1]", "[command2]"],
		"off_commands" : ["[command1]", "[command2]"]
	},
	"<alt>+7" : {
		"type" : "toggle",
		"on_commands" : ["echo hello", "echo world"],
		"off_commands" : ["echo foo","echo bar"]
	},
	"<alt>+7" : {
		"type" : "button",
		"commands" : ["echo hello", "echo world"]
	}
}
```
