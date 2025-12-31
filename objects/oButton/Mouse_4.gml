image_index = 1

// Check button category

if (sprite_index == sButton_try){
	
	// check right
	global.right_bar.image_index = 0
	global.wrongpos_bar.image_index = 0
	global.wrong_bar.image_index = 0
	
	for (var item=0; item<array_length(global.player_tries); item+=1){
		pos_color_right = global.computer_colors[item]
		player_try_id = global.player_tries[item]
		player_try_color = player_try_id.image_index
		correctness_slot = global.correctness_objects[item]
		correctness_index = 0
		
		if (player_try_color == pos_color_right){
				correctness_index = 1
				global.right_bar.image_index += 1
		}else{
				if (array_contains(global.computer_colors, player_try_color)){
					correctness_index = 2
					global.wrongpos_bar.image_index += 1
				}else{
					correctness_index = 3
					global.wrong_bar.image_index += 1 
				}
		}
			
		if (global.mode_switch.image_index == 0){
			correctness_slot.image_index = correctness_index
		}else{
			correctness_slot.image_index = 0
		}
	}
}