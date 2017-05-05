import os
from pilkit.lib import Image, ImageDraw
from imagekit import ImageSpec, register
from imagekit.processors import ResizeToFill, ResizeToFit, SmartResize
from storages.backends.s3boto3 import S3Boto3Storage
from tempfile import SpooledTemporaryFile


class UserAccountAvatar(ImageSpec):
    processors = [ResizeToFill(208, 208),]

register.generator('user-account-avatar', UserAccountAvatar)
