import cv2 as cv
import requests
import pytesseract
from PIL import Image


def recognize_text(image):
    # 识别
    test_message = Image.fromarray(image)
    text = pytesseract.image_to_string(test_message)
    print(f'识别结果：{text}')

if __name__ == '__main__':

    img_src = 'https://wsygq.com/index.php/verify/index.html'
    response = requests.get(img_src)
    with open('tmp.jpg','wb') as file_obj:
        file_obj.write(response.content)
    src = cv.imread(r'./tmp.jpg')
    cv.imshow('input image', src)
    recognize_text(src)
    cv.waitKey(0)
    cv.destroyAllWindows()
