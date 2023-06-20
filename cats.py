import requests
from PIL import Image
from transformers import ViTImageProcessor, ViTForImageClassification
from transformers.utils import logging
# remove warnings about CPU
logging.set_verbosity(40)
# logging.get_logger("transformers.tokenization_utils_base").setLevel(logging.ERROR)

url = './cats/cat1.jpg'

# url from web
# image = Image.open(requests.get(url, stream=True).raw)

# image locally
image = Image.open("./cats/cat3.jpg")

processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

inputs = processor(images=image, return_tensors="pt")
outputs = model(**inputs)
logits = outputs.logits
# model predicts one of the 1000 ImageNet classes
predicted_class_idx = logits.argmax(-1).item()
print("Predicted class:", model.config.id2label[predicted_class_idx])