from functools import partial
import SimpleCV as cv


def render_blob(layer, blob):
    x, y, w, h = blob.boundingBox()
    ball_marking = layer.centeredRectangle(
        (x + w//2, y + h//2),
        (w, h),
        filled=False,
        color=cv.Color.RED
    )

img = cv.Image('/home/sjosund/Programming/Pictures/IMG_4931.JPG').resize(1200)
ball_img = img.colorDistance((255,177,38)).binarize(40)
blobs = filter(lambda b:b.isCircle(0.3), ball_img.findBlobs())

ball_layer = cv.DrawingLayer((img.width, img.height))
map(partial(render_blob, ball_layer), blobs[-1:])
print("X: {}, y: {}".format(blobs[-1].x, blobs[-1].y))
img_ = img - ball_img
img_.addDrawingLayer(ball_layer)
img_.applyLayers()
img_.show()
raw_input("")
