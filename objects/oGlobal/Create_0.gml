window_set_size(600,  900)
gpu_set_tex_filter(false)


// Global variables
global.selection = instance_create_layer(-64, -64, "GUI", oSelected)
global.selected_color = 0
global.player_tries = []

// Color blocks spawning data

first_block_y =  16
block_spacing_pixels = 1
block_height =  16
block_width = 16
block_amount_x = 4
block_amount_y = 2

line_size = object_line_size(block_width, block_spacing_pixels, block_amount_x)
first_block_x = object_line_centered_x(line_size, room_width, block_width)

// Spawning blocks
posy = first_block_y
posx = first_block_x
block_color_index = 1
for (var line=0; line < block_amount_y; line+=1 ){
	posx = first_block_x 
	for (var col=0; col < block_amount_x; col+=1){	
		show_debug_message(string(posx)+","+string(posy))
		
		instance_create_layer(posx, posy, "Instances", oColor)
		color_instance =  instance_create_layer(posx, posy, "Lower", oColorBack)
		color_instance.image_index = block_color_index
		block_color_index += 1
		posx = calculate_next_pos(posx, block_width, 1, block_spacing_pixels)
	}
	posy = calculate_next_pos(posy, block_height, 1,block_spacing_pixels)
}

// Empty block spawn data
next_y_jump = 20
posy += next_y_jump
posx = first_block_x
block_amount_y = 1
for (var line=0; line < block_amount_y; line+=1 ){
	posx = first_block_x 
	for (var col=0; col < block_amount_x; col+=1){	
		show_debug_message(string(posx)+","+string(posy))
		
		instance_create_layer(posx, posy, "Instances", oEmpty)
		color_instance =  instance_create_layer(posx, posy, "Lower", oColorBack)
		color_instance.is_toggleable = true
		
		array_push(global.player_tries, color_instance)
		posx = calculate_next_pos(posx, block_width, 1, 1)
	}
	posy = calculate_next_pos(posy, block_height, 1, 1)
}


// Try utton location
room_middle_x = room_width/2
button_spacing_from_low_y =  20

global.try_btn = instance_create_layer(room_middle_x, room_height-button_spacing_from_low_y, "Instances", oButton)
global.try_btn.sprite_index = sButton_try
