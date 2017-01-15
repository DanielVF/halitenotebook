# Halite Notebook

Visualize Halite game information in Jupyter Notebook

Sample usage:

	import halite as hlt
	
	# Load a replay
	replay = hlt.Replay("replays/2065277-3109204898.hlt")
	
	# Get a board for a particular turn
	board = replay.map_at(0)
	
	# Show the board, with peices
	hlt.show_map(board)
	
	# Show the board, with values of your choice
	hlt.show_map(board, board['strength']])

![Map output](http://leancoder-share.s3.amazonaws.com/paste/shedeimu.png)

## Contributing

Pull requests welcome!

