import json
from .models import Brand, Model, Color, Storage, MarketProduct

def process_json_data(file_path):
    with open('parsed_data_2024.02.07_23-26-33.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for product in data['products']:
        product_name = product['product_name']
        brand_name = product_name.split()[0]  # Первое слово в названии продукта
        model_name = product_name.split()[1]  # Второе слово в названии продукта
        color_name = product_name.split()[-1]  # Последнее слово в названии продукта

        # Проверяем существование бренда в таблице брендов
        brand, _ = Brand.objects.get_or_create(name=brand_name)

        # Проверяем существование модели в таблице моделей, связанной с брендом
        model, _ = Model.objects.get_or_create(name=model_name, brand=brand)

        # Проверяем существование цвета в таблице цветов
        color, _ = Color.objects.get_or_create(name=color_name)

        # Проверяем существование размера в таблице хранилищ
        storage_size = product_name.split()[-2]  # Предпоследнее слово в названии продукта
        storage, _ = Storage.objects.get_or_create(size=storage_size)

        # Сохраняем данные в таблицу MarketProduct
        market_product = MarketProduct.objects.create(
            product_name=product_name,
            brand=brand,
            model=model,
            color=color,
            storage=storage,
            price=product['current_price']
        )
