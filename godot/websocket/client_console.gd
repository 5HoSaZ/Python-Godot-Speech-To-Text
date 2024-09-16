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


func _on_send_button_pressed() -> void:
	if line_edit.text == "":
		return
	info("Sending message: %s" % [line_edit.text])
	client.send(line_edit.text)
	line_edit.text = ""


func _on_connect_button_toggled(toggled_on) -> void:
	if not toggled_on:
		client.close()
		return
	if host.text == "":
		return
	info("Connecting to host: %s." % [host.text])
	var err = client.connect_to_url(host.text)
	if err != OK:
		info("Error connecting to host: %s" % [host.text])
		return
