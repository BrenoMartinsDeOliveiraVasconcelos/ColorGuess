show_debug_message(string(is_toggleable))

if (image_index > 0 and !is_toggleable){
	global.selected_color = image_index
	global.selection.x = x
	global.selection.y = y
}else{
	if (is_toggleable){
		image_index = global.selected_color
	}
}
show_debug_message(string(global.selected_color))
