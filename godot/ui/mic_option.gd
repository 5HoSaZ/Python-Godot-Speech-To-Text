extends HBoxContainer

@onready var option_button : OptionButton = get_child(1)
@onready var devices := AudioServer.get_input_device_list() # All available microphones

func _ready() -> void:
	# Add all devices to option list
	for i in range(devices.size()):
		var device = devices[i]
		option_button.add_item(device)
		if device == AudioServer.get_input_device():
			option_button.select(i)


func _on_option_button_item_selected(index):
	AudioServer.set_input_device(devices[index])
