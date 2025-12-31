image_index = 1

// Check button category

if (sprite_index == sButton_try){
		
	// check right
	for (var item=0; item<array_length(global.player_tries); item+=1){
		pos_color_right = global.computer_colors[item]
		player_try_id = global.player_tries[item]
		player_try_color = player_try_id.image_index
		correctness_slot = global.correctness_objects[item]
		
		if (player_try_color == pos_color_right){
			correctness_slot.image_index = 1
		}else{
			if (array_contains(global.computer_colors, player_try_color)){
				correctness_slot.image_index = 2
			}else{
				correctness_slot.image_index = 3
			}
		}
	}
}