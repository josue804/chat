from pilkit.lib import Image, ImageDraw
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize

class UserAccountAvatar(ImageSpec):
    processors = [ResizeToFill(264, 264),]

register.generator('user-account-avatar', UserAccountAvatar)
