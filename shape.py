# Shape class for displaying and controlling current shape and next shape based on location, rotation and colour

class Shape:
    def __init__(self, shape, rotation, current_location, colour):
        self.shape = shape
        self.rotation = rotation

        self.current_location = current_location
        self.colour = colour

# Shape is created. This is done by going through a 2D list and finding what rows and columns there needs to be a block
    def create_shape(self):
        self.shape_blocks = []
        for x, row in enumerate (self.shape[self.rotation]):
            for y, column in enumerate (row):
                if column == "0":
                    self.shape_blocks.append ([x, y])

# A generated shape is created and moved to its set location
    def generate_shape(self):
        self.create_shape()
        self.move_shape (self.current_location[0], self.current_location[1])

# Based on requested rotation direction, the shapes rotation variable will either be iterated one way or the other, and then the shape will be
# generated again, moving it to its last location
    def rotate_shape(self, rotate_dir):
        if rotate_dir == "CW":
            if self.rotation < (len(self.shape) - 1):
                self.rotation += 1
                self.create_shape()
            else:
                self.rotation = 0
                self.create_shape()
        elif rotate_dir == "CCW":
            if self.rotation > 0:
                self.rotation -= 1
                self.create_shape ()
            else:
                self.rotation = (len (self.shape) - 1)
                self.create_shape ()

        for block in self.shape_blocks:
            block[0] += self.current_location[0]
            block[1] += self.current_location[1]

# Making a copy of the shape, and then rotating it is used to check for collisions in the main file by showing where the rotated blocks would be
    def check_rotate(self, rotate_dir):
        rotation_copy = self.rotation

        if rotate_dir == "CW":
            if rotation_copy < (len(self.shape) - 1):
                rotation_copy += 1
            else:
                rotation_copy = 0
        if rotate_dir == "CCW":
            if rotation_copy > 0:
                rotation_copy -= 1
            else:
                rotation_copy = (len(self.shape) - 1)


        shape_copy = []
        for x, row in enumerate (self.shape[rotation_copy]):
            for y, column in enumerate (row):
                if column == "0":
                    shape_copy.append ([x, y])

        for block in shape_copy:
            block[0] += self.current_location[0]
            block[1] += self.current_location[1]

        return shape_copy

# THe shape is moved a given amount in the x and y direction
    def move_shape(self, x_move, y_move):

        self.current_location[0] += x_move
        self.current_location[1] += y_move

        for block in self.shape_blocks:
            block[0] += (x_move)
            block[1] += (y_move)
