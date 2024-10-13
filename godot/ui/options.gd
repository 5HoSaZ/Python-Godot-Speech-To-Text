extends MarginContainer


@onready var mic_option_button = $Content/MicOption/MicOptionButton
@onready var mute_button = $Content/MuteOption/MuteButton
@onready var devices := AudioServer.get_input_device_list() # All available microphones


func _ready() -> void:
	# Add all devices to option list
	for i in range(devices.size()):
		var device = devices[i]
		mic_option_button.add_item(device)
		if device == AudioServer.get_input_device():
			mic_option_button.select(i)


func _on_mic_option_button_item_selected(index):
	AudioServer.set_input_device(devices[index])


func _on_mute_button_toggled(toggled_on: bool):
	mute_button.text = "On" if toggled_on else "Off"
	
