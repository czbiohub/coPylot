from typing import List, Tuple 
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPolygon

class Shape(QPolygon):
    def __init__(self, border_points: List[Tuple[float, float]]) -> None:
        """initializes a Shape object.

        Args:
            border_points (List[Tuple[float, float]]): a list of tuples representing the border of the shape. each tuple is an (x, y)
        """
        super().__init__(border_points)
        self.border_points = border_points
        self.pattern_style = None
        self.pattern_points = set()

    def _pattern_bidirectional(self, vertical_spacing: int, horizontal_spacing: int):
        """ adds a bidirectional (snaking) pattern to the shape.

        Args:
            vertical_spacing (int): determines how many pixels of space will be between each point in the shape vertically.
            horizontal_spacing (int): determines how many pixels of space will be between each point in the shape horizontally. 
        """
        self.border_style = "Bidirectional"
        min_x = self.boundingRect().left()
        max_x = self.boundingRect().right()
        min_y = self.boundingRect().top()
        max_y = self.boundingRect().bottom()

        curr_x = min_x
        curr_y = min_y
        direction = True # true if moving right, false if moving left

        while curr_y <= max_y:
            if direction:
                while curr_x <= max_x:
                    if self.containsPoint(QPoint(curr_x, curr_y), Qt.OddEvenFill):
                        self.pattern_points.add((curr_x, curr_y))
                    curr_x += horizontal_spacing
            else:
                while curr_x >= min_x:
                    if self.containsPoint(QPoint(curr_x, curr_y), Qt.OddEvenFill):
                        self.pattern_points.add((curr_x, curr_y))
                    curr_x -= horizontal_spacing

            curr_y += vertical_spacing
            direction = not direction

            if direction:
                curr_x = min_x
            else:
                curr_x = max_x


