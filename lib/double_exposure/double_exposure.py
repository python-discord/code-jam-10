from PIL import Image

def double_exposure(img1, img2, alpha=0.5):
    # Ensure img1 is the smaller image, or swap if necessary
    if img1.size[0] > img2.size[0] or img1.size[1] > img2.size[1]:
        img1, img2 = img2, img1

    # Convert both images to RGB
    img1 = img1.convert("RGB")
    img2 = img2.convert("RGB")

    # Resize img2 to match img1's size
    img2 = img2.resize(img1.size)

    # Blend the images
    blended = Image.blend(img1, img2, alpha)

    # Resize the resulting image to 450x450
    blended = blended.resize((450, 450))

    return blended
