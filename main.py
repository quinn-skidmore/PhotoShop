import kivy.uix.image
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from PIL import Image
from PIL import ImageDraw
import random
import math

from kivy.uix.widget import Widget


#Builder.load_file("PhotoGallery.kv")

class PhotoShopApp(App):
    def build(self):
        return


class TouchableImage(kivy.uix.image.Image):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.down_coord = ()
        self.up_coord = [0,0]
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print("Touched at", touch.pos)
            self.down_coord = touch.pos
            #return True
        lr_space = (self.width - self.norm_image_size[0]) / 2  # empty space in Image widget left and right of actual image
        tb_space = (self.height - self.norm_image_size[1]) / 2  # empty space in Image widget above and below actual image
        #print('lr_space =', lr_space, ', tb_space =', tb_space)
        #print("Touch Cords", touch.x, touch.y)
        #print('Size of image within ImageView widget:', self.norm_image_size)
        #print('ImageView widget:, pos:', self.pos, ', size:', self.size)
        #print('image extents in x:', self.x + lr_space, self.right - lr_space)
        #print('image extents in y:', self.y + tb_space, self.top - tb_space)
        pixel_x = touch.x - lr_space - self.x  # x coordinate of touch measured from lower left of actual image
        pixel_y = touch.y - tb_space - self.y  # y coordinate of touch measured from lower left of actual image
        if pixel_x < 0 or pixel_y < 0:
            print('clicked outside of image\n')
            #return True
        elif pixel_x > self.norm_image_size[0] or \
                pixel_y > self.norm_image_size[1]:
            print('clicked outside of image\n')
            #return True
        else:
            print('clicked inside image, coords:', pixel_x, pixel_y)

            # scale coordinates to actual pixels of the Image source
            print('actual pixel coords:',
                  pixel_x * self.texture_size[0] / self.norm_image_size[0],
                  pixel_y * self.texture_size[1] / self.norm_image_size[1], '\n')
            x = pixel_x * self.texture_size[0] / self.norm_image_size[0]
            y = pixel_y * self.texture_size[1] / self.norm_image_size[1]
            self.down_coord = list((x,y))
            #self.down_coord[1] = pixel_y * self.texture_size[1] / self.norm_image_size[1]
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            print("Released at", touch.pos)
            return True
        return super().on_touch_up(touch)


class MouseTouch(Screen, Widget):
    txtinput = ObjectProperty(None)
    button = ObjectProperty(None)
    image = ObjectProperty(None)
    coords = []
    # def on_touch_down(self, touch):
    #     #print("Mouse Button Pressed")
    #     x, y = touch.x, touch.y
    #     print("X coordinate: " + str(int(x)) + " y coordinate: " + str(int(y)))
    #     super().on_touch_down(touch)
    #     self.coords.append(int(x))
    #     self.coords.append(int(y))
    #     if len(self.coords) > 4:
    #         self.coords = self.coords[2:]
    '''
    def on_touch_move(self, touch):
        print("Mouse Moved")
        coords = touch.pos
        print("X coordinate: " + str(int(coords[0])) + " y coordinate: " + str(int(coords[1])))
    '''


class Editor(Screen):
    touchimg = ObjectProperty(None)
    down_coord = []
    up_coord = []
    def load_image(self):
        self.ids.image.source = self.ids.img_name.text

    def pointillism(self, image, name):
        img = Image.open(image)
        pixels = img.load()
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        for i in range(100000):
            x = random.randint(0, img.size[0] - 1)
            y = random.randint(0, img.size[1] - 1)
            size = random.randint(10, 20)
            ellipsebox = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
            del draw
        canvas.save(name + "_pointillism.png")
        self.ids.image.source = name + "_pointillism.png"

    def line_drawing(self,image, name):
        img = Image.open(image)
        pixels = img.load()
        total_difference = 0
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                for i in range(-1, 2):
                    if (x > 1 and y > 1 and x < img.size[0] - 1 and y < img.size[1] - 1):
                        total_difference += (pixels[x, y][0] - pixels[x + i, y][0])
                        total_difference += (pixels[x, y][1] - pixels[x + i, y][1])
                        total_difference += (pixels[x, y][2] - pixels[x + i, y][2])

                        total_difference += (pixels[x, y][0] - pixels[x, y + 1][0])
                        total_difference += (pixels[x, y][1] - pixels[x + i, y + 1][1])
                        total_difference += (pixels[x, y][2] - pixels[x + i, y + 1][2])
                        if (total_difference > 500):
                            pixels[x, y] = (0, 0, 0)
                        else:
                            pixels[x, y] = (255, 255, 255)
                        total_difference = 0
                    else:
                        pixels[x, y] = (255, 255, 255)
        img.save(name + "_line_drawing.png")
        self.ids.image.source = name + "_line_drawing.png"

    def pixelate(self, image, name, width, height):
        x_coor = int(self.touchimg.down_coord[0])
        y_coor = int(self.touchimg.up_coord[1])
        print(str(x_coor),str(y_coor))
        average_red = []
        average_green = []
        average_blue = []
        img = Image.open(image)
        pixels = img.load()
        # get y spacing for each box
        for c in range(y_coor, y_coor + height, 10):
            # get x spacing for each box
            for v in range(x_coor, x_coor + width, 10):
                for y in range(img.size[1]):
                    # get average if x within box
                    for x in range(img.size[0]):
                        if (x >= v and x <= v + 10 and y >= c and y <= c + 10):
                            average_red.append(pixels[x, y][0])
                            average_green.append(pixels[x, y][1])
                            average_blue.append(pixels[x, y][2])
                print(average_red)
                red = int(sum(average_red) / len(average_red))
                green = int(sum(average_green) / len(average_green))
                blue = int(sum(average_blue) / len(average_blue))
                # set pixel to the average color
                for y in range(img.size[1]):
                    for x in range(img.size[0]):
                        if (x >= v and x <= v + 100 and y >= c and y <= c + 100):
                            pixels[x, y] = (red, green, blue)
        img.save(name + "_pixelated.png")
        self.ids.image.source = name + "_pixelated.png"

    def invert(self, image, name):
        img = Image.open(image)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = 255 - pixels[x, y][0]
                green = 255 - pixels[x, y][1]
                blue = 255 - pixels[x, y][2]
                pixels[x, y] = (red, green, blue)
        img.save(name + "_inverted.png")
        self.ids.image.source = name + "_inverted.png"

    def sepia(self,image, name):
        img = Image.open(image)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = int(pixels[x, y][0] * .393 + pixels[x, y][1] * 0.769 + pixels[x, y][2] * 0.189)
                green = int(pixels[x, y][0] * .349 + pixels[x, y][1] * 0.686 + pixels[x, y][2] * 0.168)
                blue = int(pixels[x, y][0] * .272 + pixels[x, y][1] * 0.534 + pixels[x, y][2] * 0.131)
                pixels[x, y] = (red, green, blue)
        img.save(name + "_sepia.png")
        self.ids.image.source = name + "_sepia.png"

    def black_and_white(self, image, name):
        img = Image.open(image)
        pixels = img.load()
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = pixels[x, y][0]
                green = pixels[x, y][1]
                blue = pixels[x, y][2]
                pixels[x, y] = (red, red, red)
        img.save(name + "_BAW.png")
        self.ids.image.source = name + "_BAW.png"
PhotoShopApp().run()