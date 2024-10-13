extends Control


const VU_COUNT := 30
const FREQ_MAX := 11050.0
const MIN_DB = 80
const ANIMATION_SPEED = 0.1
const HEIGHT_SCALE = 8.0

@onready var volume_bar = $Content/HBoxContainer/VolumeMonitor/VolumeBar
@onready var volume_value = $Content/HBoxContainer/VolumeMonitor/VolumeValue
@onready var leds = $Content/HBoxContainer/SpectrumMonitor/LEDS

var capture_bus_idx : int 
var capture : AudioEffectCapture
var spectrum : AudioEffectSpectrumAnalyzerInstance

var min_values : Array[float] = []
var max_values : Array[float] = []

@export var chunk := 512
@export var threshold_amp := 0.005

signal frames_captured(frames)

func _ready():
	capture_bus_idx = AudioServer.get_bus_index("Capture")
	capture = AudioServer.get_bus_effect(capture_bus_idx, 0)
	spectrum = AudioServer.get_bus_effect_instance(capture_bus_idx, 2)
	min_values.resize(VU_COUNT); min_values.fill(0.0)
	max_values.resize(VU_COUNT); max_values.fill(0.0)


func _process(delta):
	capture_audio()
	update_samples_strength()
	update_spectrum_monitor()


func update_samples_strength() -> void:
	var volume_samples = []
	var sample = db_to_linear(AudioServer.get_bus_peak_volume_left_db(capture_bus_idx, 0))
	volume_samples.push_front(sample)

	while volume_samples.size() > 20:
		volume_samples.pop_back()

	var sample_avg = average_array(volume_samples)
	volume_value.text = '%s db' % round(linear_to_db(sample_avg))
	volume_bar.value = sample_avg


func update_spectrum_monitor() -> void:
	var prev_freq = 0
	var data = []; data.resize(VU_COUNT)

	for i in VU_COUNT:
		var freq = (i + 1) * FREQ_MAX / VU_COUNT
		var magnitude = spectrum.get_magnitude_for_frequency_range(
			prev_freq, freq,
			AudioEffectSpectrumAnalyzerInstance.MAGNITUDE_AVERAGE
		).length()
		# Boost the signal and normalize
		var energy = clamp((MIN_DB + linear_to_db(magnitude)) / MIN_DB, 0.0, 1.0)
		data[i] = energy * HEIGHT_SCALE
		prev_freq = freq
	leds.get_material().set_shader_parameter("freq_data", smooth_fft(data))


# Function to take average of an array
func average_array(arr: Array) -> float:
	var avg = 0.0
	for i in range(arr.size()):
		avg += arr[i]
	avg /= arr.size()
	return avg


# Apply linear interpolation for smooth animation
func smooth_fft(data: Array) -> Array:
	var fft : Array[float] = []
	for i in VU_COUNT:
		if data[i] > max_values[i]:
			max_values[i] = data[i]
		else:
			max_values[i] = lerp(max_values[i], data[i], ANIMATION_SPEED)
		if data[i] <= 0.0:
			min_values[i] = lerp(min_values[i], 0.0, ANIMATION_SPEED)
		fft.append(lerp(min_values[i], max_values[i], ANIMATION_SPEED))
	return fft


func capture_audio() -> void:
	if (capture.can_get_buffer(chunk)):
		# This will return audio frames of 2-tuple signed float32 PCM
		var frames = capture.get_buffer(chunk)
		var max_amp := 0.0
		for i in chunk:
			var amp = (frames[i].x + frames[i].y) / 2
			max_amp = max(amp, max_amp)
		if max_amp < threshold_amp:
			frames.fill(Vector2(0.0, 0.0))
		# Convert to array of signed int16
		frames = frames_to_packed_s16_bytes(frames)
		frames_captured.emit(frames)
	capture.clear_buffer()


func frames_to_packed_s16_bytes(frames) -> PackedByteArray:
	var converted: PackedByteArray = []
	for f in frames:
		var bytes = PackedByteArray([0, 0]) # 2 bytes for int16
		bytes.encode_s16(0, 32768 * (f.x + f.y) / 2) # Convert from float32 to int16
		converted.append_array(bytes)
	return converted


func _on_spin_box_value_changed(value):
	threshold_amp = value
