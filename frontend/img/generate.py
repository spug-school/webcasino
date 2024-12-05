from PIL import Image, ImageFont, ImageDraw


suits = ("hearts", "diamonds", "spades", "cross")
ranks = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")
width = 744
heigth = 1039
font = ImageFont.truetype("Roboto-Bold.ttf", 512)
size = (width // 10, width // 10)



for i in suits:
    for j in ranks:
        img = Image.new('RGB', (width, heigth))
        font_img = Image.new('RGB', (512, 512))
        drawing = ImageDraw.Draw(img)
        font_drawing = ImageDraw.Draw(font_img)
        drawing.rectangle([(0, 0), (width, heigth)], fill=(255, 255, 255))
        font_drawing.rectangle([(0, 0), (512, 512)], fill=(255, 255, 255))
        font_drawing.text((0, 0), f"{j.upper()}", (0, 0, 0), font=font)
        font_resized = font_img.resize(size, resample = Image.BILINEAR)
        font_flipped = font_resized.transpose(method=Image.FLIP_TOP_BOTTOM)
        font_turned = font_flipped.transpose(method=Image.FLIP_LEFT_RIGHT)
        suits_image = Image.open(f"{i}.png")
        resized = suits_image.resize(size, resample = Image.BILINEAR)
        vertical_suits = resized.transpose(method=Image.FLIP_TOP_BOTTOM)
        suits_size = resized.size
        final_size = img.size
        img.paste(resized, (40, 40))
        img.paste(vertical_suits, (final_size[0] - suits_size[0] - 40, final_size[1] - suits_size[1] - 40))
        img.paste(font_resized, (final_size[0] - suits_size[0] - 40, 40))
        img.paste(font_turned, (40, final_size[1] - suits_size[1] - 40))
        img.save(f'{i}_{j}.png')