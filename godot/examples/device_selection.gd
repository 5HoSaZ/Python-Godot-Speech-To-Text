extends OptionButton

var devices: Array

func _ready() -> void:
	devices = AudioServer.get_input_device_list()
	for i in range(devices.size()):
		var device = devices[i]
		add_item(device)
		if device == AudioServer.get_input_device():
			select(i)

func _on_device_selection_item_selected(index: int) -> void:
	AudioServer.set_input_device(devices[index])
