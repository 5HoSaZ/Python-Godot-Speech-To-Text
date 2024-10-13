extends AudioStreamPlayer
class_name AudioCapture


@onready var capture_bus_idx : int = AudioServer.get_bus_index("Capture")
@onready var capture_effect : AudioEffectCapture = AudioServer.get_bus_effect(capture_bus_idx, 0)
@onready var record_effect : AudioEffectRecord = AudioServer.get_bus_effect(capture_bus_idx, 1)


func _on_amp_spin_box_value_changed(new_amp: float) -> void:
	volume_db = linear_to_db(new_amp)


func _on_mute_button_toggled(toggled_on: bool):
	playing = toggled_on
