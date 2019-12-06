import drawille
from PIL import Image
import requests
def draw_img_on_canvas(image_descriptor=None,color_threshold=0,invert_threshold=False,canvas=None,pixel_limits=None):
    """
    Draws an image onto a Canvas

    Args:
        image_descriptor: open in binary mode e.g. open(MAP_IMAGE_FILEPATH,'rb') requests.get('...',stream=True)
        color_threshold: int (0-255) to paint (or not) a pixel in drawille
        invert_threshold: if set to True, the threshold test will be: paint when pixel color > threshold 
        canvas: The canvas to draw
        pixel_limits: a dict of X,Y Coordinates that limit the size of the image, used by canvas.frame(...)
            If the image size is greater than the limits, the image is resized maintaining the ratio and
            the pixel limits are updated 
            pixel_limits = {"min_x":0,"min_y":0,"max_x":128,"max_y":128}

    Returns: None. 
    """

    #Determine if the size of the image is greater than the size to print, if so, scale it down
    i = Image.open(image_descriptor).convert(mode='L')
    image_width, image_height = i.size   

    w_ratio = 1    
    if  pixel_limits["max_x"] < image_width:
        w_ratio =  pixel_limits["max_x"] / float(image_width)

    h_ratio = 1
    if pixel_limits["max_y"] < image_width:
        h_ratio = pixel_limits["max_y"] / float(image_height)
    
    ratio = 0.8*min([w_ratio,h_ratio])
    image_width = int(image_width * ratio)
    image_height = int(image_height * ratio)
    i = i.resize((image_width, image_height), Image.ANTIALIAS)
    #Update limits
    pixel_limits["max_y"] = image_height
    pixel_limits["max_x"] = image_width
            
    try:
        i_converted = i.tobytes()
    except AttributeError:
        raise
    
    if invert_threshold:
        threshold_test = lambda pix_color,color_threshold: pix_color > color_threshold
    else:
        threshold_test = lambda pix_color,color_threshold: pix_color < color_threshold

    x = y = 0
    for pix in i_converted:
        if threshold_test(pix,color_threshold):
            canvas.set(x, y)
        x += 1
        if x >= image_width:
            y += 1
            x = 0

if __name__ == "__main__":
    img = requests.get("https://spacelaunchnow-prod-east.nyc3.cdn.digitaloceanspaces.com/media/logo/national2520aeronautics2520and2520space2520administration_logo_20190207032448.png",stream=True)
    
    #img = requests.get("https://spacelaunchnow-prod-east.nyc3.cdn.digitaloceanspaces.com/media/default/cache/21/f1/21f1222a77ab913fea2ef8b2f5ffd953.jpg",stream=True)
    pixel_limits = {"min_x":0,"min_y":0,"max_x":128,"max_y":128}
    canvas = drawille.Canvas()
    #draw_img_on_canvas(img.raw,145,True,canvas,pixel_limits)
    draw_img_on_canvas(img.raw,70,True,canvas,pixel_limits)

