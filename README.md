# Halite Notebook

Visualize Halite game information in Jupyter Notebook! 

	import halite as hlt
	replay = hlt.Replay("replays/2065277-3109204898.hlt")  # Works on .hlt.gz files too
	board = replay.map_at(0)
	hlt.show_map(board)
	hlt.show_map(board, board['strength']])

![Map output](http://leancoder-share.s3.amazonaws.com/paste/shedeimu.png)

## Contributing

Pull requests welcome!

