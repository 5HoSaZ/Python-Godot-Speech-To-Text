extends AudioStreamPlayer
class_name AudioCapture


@export_range(10, 512, 1) var chunk := 512
@onready var capture_bus_idx : int = AudioServer.get_bus_index("Capture")
@onready var capture_effect : AudioEffectCapture = AudioServer.get_bus_effect(capture_bus_idx, 0)
@onready var record_effect : AudioEffectRecord = AudioServer.get_bus_effect(capture_bus_idx, 1)

signal frames_captured(frames)


func _ready() -> void:
	pass


func _process(_delta) -> void:
	if playing: capture_audio()


func capture_audio() -> void:
	var sample = AudioServer.get_bus_peak_volume_left_db(capture_bus_idx, 0)
	if (capture_effect.can_get_buffer(chunk)):
		# This will return audio frames of 2-tuple signed float32 PCM
		var frames = capture_effect.get_buffer(chunk)
		# Convert to array of float32
		frames = frames_to_packed_float32(frames)
		frames_captured.emit(frames)
	capture_effect.clear_buffer()


func frames_to_packed_float32(frames) -> PackedFloat32Array:
	var converted: PackedFloat32Array = []
	for f in frames:
		converted.append(f.x)
	return converted


func _on_amp_spin_box_value_changed(new_amp: float) -> void:
	volume_db = linear_to_db(new_amp)


func _on_process_button_toggled(toggled_on: bool) -> void:
	playing = toggled_on
