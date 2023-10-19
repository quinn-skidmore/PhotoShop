from kivy.app import App
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
    pass


class MouseTouch(Screen, Widget):
    txtinput = ObjectProperty(None)
    button = ObjectProperty(None)
    image = ObjectProperty(None)
    def on_touch_down(self, touch):
        #print("Mouse Button Pressed")
        x, y = touch.x, touch.y
        print("X coordinate: " + str(int(x)) + " y coordinate: " + str(int(y)))
        #self.button.color = "black"
        #self.button.text = "Pressed"
        super().on_touch_down(touch)
    '''
    def on_touch_move(self, touch):
        print("Mouse Moved")
        coords = touch.pos
        print("X coordinate: " + str(int(coords[0])) + " y coordinate: " + str(int(coords[1])))
    '''
    def on_touch_up(self, touch):
        super()
        #print("Mouse Button Up")
        #coords = touch.pos
        #print("X coordinate: " + str(int(coords[0])) + " y coordinate: " + str(int(coords[1])))
        #self.button.background_color = "black"
        #self.button.color = "white"
        #self.button.text = "Press Me"


class Editor(Screen):
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

    def pixelate(self, image, name, x_coor, y_coor, width, height):
        average_red = []
        average_green = []
        average_blue = []
        img = Image.open(image)
        pixels = img.load()
        # get y spacing for each box
        for c in range(y_coor, y_coor + height, 100):
            # get x spacing for each box
            for v in range(x_coor, x_coor + width, 100):
                for y in range(img.size[1]):
                    # get average if x within box
                    for x in range(img.size[0]):
                        if (x >= v and x <= v + 100 and y >= c and y <= c + 100):
                            average_red.append(pixels[x, y][0])
                            average_green.append(pixels[x, y][1])
                            average_blue.append(pixels[x, y][2])
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