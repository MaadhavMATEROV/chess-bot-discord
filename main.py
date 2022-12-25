import discord
from discord.ext import commands
import chess
import chess.pgn
import chess.svg
import chess.engine
import chess.uci
import tkinter as tk
import asyncio

# Replace YOUR_BOT_TOKEN with the token for your Discord bot
TOKEN = 'MTAyNzcyODI3OTY1NTk0NDIzMw.GZzpi7.3Fe6Z0ZTHoRcYiKutF7DYFAYrW9fgrp5s-o4dg'

# Initialize the Discord client and the bot
client = discord.Client()
bot = commands.Bot(command_prefix='!')

# Set up the chess board and engine
board = chess.Board()
engine = chess.uci.popen_engine("stockfish")
engine.uci()

# Set up the GUI
class ChessWidget(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.initUI()
    
    def initUI(self):
        # Generate an SVG image of the chess board
        self.board_svg = chess.svg.board(board=board, size=400)

        # Set up the chess board and pieces
        self.board = tk.Label(self, image=self.board_svg)
        self.board.pack()

        self.pieces = []
        for i in range(64):
            label = tk.Label(self, image='')
            self.pieces.append(label)

        # Set up the drag and drop functionality
        for piece in self.pieces:
            piece.bind("<Button-1>", self.on_drag_start)
            piece.bind("<B1-Motion>", self.on_drag_move)
            piece.bind("<ButtonRelease-1>", self.on_drag_release)


def update_board(self):
    # Update the chess board image
    self.board.configure(image=self.board_svg)

    # Update the positions of the pieces on the board
    for i, piece in enumerate(self.pieces):
        row, col = divmod(i, 8)
        x = col * 50
        y = row * 50
        piece.place(x=x, y=y)

        # Get the piece at the current position on the chess board
        pos = chess.square(i)
        square = board.piece_at(pos)
        if square is None:
            piece.configure(image='')
        else:
            piece.configure(image=f"{square.symbol()}.png")

def on_drag_start(self, event):
        # Get the source square for the move
        self.source_square = event.widget
        self.source_square.lift()
        self.drag_x = event.x
        self.drag_y = event.y
    
def on_drag_move(self, event):
        # Move the piece along with the mouse cursor
        self.source_square.place(x=event.x_root - self.drag_x, y=event.y_root - self.drag_y)

    
def on_drag_release(self, event):
        # Get the destination square for the move
        self.dest_square = event.widget

# Set up the Discord bot commands
@commands.command(name='newgame', help='Start a new game of chess')
def newgame(bot, ctx):
    # Start a new game
    board.reset()
    widget.update_board()

@commands.command(name='move', help='Make a move on the chess board')
async def move(bot, ctx, source, dest):
    # Make a move on the chess board
    move = chess.Move.from_uci(f"{source}{dest}")
    if move in board.legal_moves:
        # Use asyncio to run the chess engine in the background
        async def make_move():
            board.push(move)
            widget.update_board()
            engine.position(board)
            result = engine.go(movetime=2000)
            board.push(result.bestmove)
            widget.update_board()

        asyncio.create_task(make_move())
    else:
        await ctx.send("Invalid move")

# Run the Discord bot
bot.run(TOKEN)
#your mom
# Set up the tkinter GUI and run the main loop
root = tk.Tk()
widget = ChessWidget(master=root)
root.mainloop()
