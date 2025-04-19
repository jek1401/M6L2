import json
import time
import requests
import base64
from PIL import Image
from io import BytesIO


class FusionBrainAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_pipeline(self):
        response = requests.get(self.URL + 'key/api/v1/pipelines', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, pipeline, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'pipeline_id': (None, pipeline),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/pipeline/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/pipeline/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['result']['files']
            attempts -= 1
            time.sleep(delay)
        return None

    def generate_image(self, prompt, save_path='generated_image.jpg'):
        pipeline_id = self.get_pipeline()
        uuid = self.generate(prompt, pipeline_id)
        files = self.check_generation(uuid)
        
        if files:
            base64_string = files[0]  # Получаем первую сгенерированную картинку
            decoded_data = base64.b64decode(base64_string)
            image = Image.open(BytesIO(decoded_data))
            image.save(save_path)
            image.show()
            print(f"Изображение сохранено как {save_path}")
        else:
            print("Не удалось сгенерировать изображение.")


if __name__ == '__main__':
    # Замени строки ниже на свои ключи API
    API_KEY = 'YOUR_API_KEY'
    SECRET_KEY = 'YOUR_SECRET_KEY'

    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    api.generate_image("Пушистый кот в очках")
