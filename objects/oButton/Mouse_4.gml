image_index = 1

// Check button category

if (sprite_index == sButton_try){
	for (var item=0; item<array_length(global.player_tries); item+=1){
		show_debug_message(string(global.player_tries[item].image_index))
	}
}