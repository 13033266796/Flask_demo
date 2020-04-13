import base64

from monarch.exc.consts import CACHE_CAPTCHA_IMAGE_KEY, CACHE_FIVE_MINUTE
from monarch.utils.tools import random_text, gen_id, CustomImageCaptcha

from monarch.corelibs.mcredis import mc
from monarch.utils.api import Bizs


def get_captcha():
    text = random_text()
    image_uuid = gen_id()
    image_data = CustomImageCaptcha().generate(text)
    image_data_b64 = base64.b64encode(image_data.getvalue()).decode('utf-8')
    data = {
        'b64s': 'data:image/png;base64,{}'.format(image_data_b64),
        'id': image_uuid
    }

    # 缓存图片验证码
    cache_captcha_image_key = CACHE_CAPTCHA_IMAGE_KEY.format(image_uuid)
    mc.set(cache_captcha_image_key, text, CACHE_FIVE_MINUTE)
    return Bizs.success(data)
