#! python3
# -*- coding: utf-8 -*-

"""
Marquee Widget for Tk.
Written (or at least posted by) Bryan Oakley (stackoverflow.com/users/7432)
at StackOverflow (stackoverflow.com/questions/47224061).
I've updated the documentation and changed the code to meet PEP8 and PEP257
standards.
"""
import tkinter as tk


class Marquee(tk.Canvas):
    """Marquee widget written for Tk."""

    def __init__(self, parent, text, margin=2,
                 borderwidth=1, relief='flat', fps=30):
        """Marquee class __init__ method."""
        tk.Canvas.__init__(self, parent, borderwidth=borderwidth,
                           relief=relief, bg = '#252525')
        self.fps = fps

        # start by drawing the text off screen, then asking the canvas
        # how much space we need. Use that to compute the initial size
        # of the canvas.
        text = self.create_text(0, -1000, text=text, font = ("Garamond", 18, "bold"), fill = 'white',
                                anchor="w", tags=("text",))
        (x0, y0, x1, y1) = self.bbox("text")
        width = (x1 - x0) + (2*margin) + (2*borderwidth)
        height = (y1 - y0) + (2*margin) + (2*borderwidth)
        self.configure(width=width, height=height)

        # start the animation
        self.animate()

    def animate(self):
        """Animate method to perform the scrolling effect."""
        # pylint complains about y1 not being used, only needed to unpack bbox
        (x0, y0, x1, y1) = self.bbox("text")
        if x1 < 0 or y0 < 0:
            # everything is off the screen; reset the X
            # to be just past the right margin
            x0 = self.winfo_width()
            y0 = int(self.winfo_height()/2)
            self.coords("text", x0, y0)
        else:
            self.move("text", -1, 0)

        # do again in a few milliseconds
        self.after_id = self.after(int(1000/self.fps), self.animate)
