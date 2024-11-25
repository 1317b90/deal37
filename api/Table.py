from tortoise import fields
from tortoise.models import Model

class Information(Model):
    id = fields.IntField(pk=True, generated=True)
    title = fields.CharField(max_length=255)
    src_url = fields.CharField(max_length=255)
    img_url = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(auto_now_add=True)