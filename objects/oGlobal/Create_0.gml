window_set_size(600,  900)
gpu_set_tex_filter(false)


// Global variables
global.selection = instance_create_layer(-64, -64, "GUI", oSelected)
global.selected_color = 0
global.player_tries = []

// Color blocks spawning data
first_block_x = 24
first_block_y =  16
block_spacing_pixels = 1
block_height =  16
block_width = 16
block_amount_x = 4
block_amount_y = 2

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
		posx = calculate_next_pos(posx, block_width, 1, 1)
	}
	posy = calculate_next_pos(posy, block_height, 1, 1)
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
