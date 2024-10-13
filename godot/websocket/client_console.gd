extends MarginContainer


@onready var client = $WebSocketClient
@onready var logs = $Content/Logs
@onready var line_edit = $Content/TextField/LineEdit
@onready var connect_button = $Content/HostField/ConnectButton
@onready var host = $Content/HostField/Host


func info(msg) -> void:
	print(msg)
	logs.add_text(str(msg) + "\n")


func _on_client_connected_to_server() -> void:
	info("Connected with protocol: %s" % client.socket.get_selected_protocol())


func _on_client_connection_closed() -> void:
	var ws = client.socket
	info(
	"Disconnected with code: %s, reason: %s" 
	% [ws.get_close_code(), ws.get_close_reason()]
	)


func _on_client_message_received(message) -> void:
	info("%s" % message)


func _on_connect_button_toggled(toggled_on) -> void:
	if toggled_on:
		if host.text == "":
			connect_button.button_pressed = false
			info("Host url cannot be empty")
			return
		info("Connecting to host: %s." % [host.text])
		var err = client.connect_to_url(host.text)
		if err != OK:
			info("Error connecting to host: %s" % [host.text])
			connect_button.button_pressed = false
			return
		connect_button.text = "Close"

	if not toggled_on:
		connect_button.text = "Connect"
		client.close()


func _on_audio_processor_frames_captured(frames):
	if client.last_state == WebSocketPeer.STATE_OPEN:
		client.send(frames)
