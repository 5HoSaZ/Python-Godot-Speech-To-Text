extends AudioStreamPlayer
class_name AudioCapture


@export var buffer_frames := 512
@onready var capture_bus_idx : int = AudioServer.get_bus_index("Capture")
@onready var capture_effect : AudioEffectCapture = AudioServer.get_bus_effect(capture_bus_idx, 0)
@onready var record_effect : AudioEffectRecord = AudioServer.get_bus_effect(capture_bus_idx, 1)


func _ready() -> void:
	pass

func _process(_delta) -> void:
	var sample = AudioServer.get_bus_peak_volume_left_db(capture_bus_idx, 0)
	if (capture_effect.can_get_buffer(buffer_frames)):
		var frames = capture_effect.get_buffer(buffer_frames)
	capture_effect.clear_buffer()


func _on_amp_spin_box_value_changed(new_amp: float) -> void:
	volume_db = linear_to_db(new_amp)
