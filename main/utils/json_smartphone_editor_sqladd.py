import os
import django

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# Загружаем настройки Django
django.setup()


from main.models import Brand, Model, Storage, Color, Smartphones

def process_product_data(product_data):
    product_name = product_data.get("product_name", "")
    brand_id = extract_brand(product_name)
    if not brand_id:
        return

    model_id = extract_model(product_name)
    storage_id = extract_storage(product_name)
    color_id = extract_color(product_name)
    category_id = determine_category()

    smartphone = Smartphones.objects.create(
        brand_id=brand_id,
        model_id=model_id,
        storage_id=storage_id,
        color_id=color_id,
        category_id=category_id
    )

def extract_brand(product_name):
    product_name_lower = product_name.lower()
    brand = Brand.objects.filter(name__iexact=product_name_lower).first()
    return brand.id if brand else None


def extract_model(product_name):
    # Приводим название продукта к нижнему регистру для сравнения
    product_name = product_name.lower()

    # Извлекаем название бренда из строки продукта
    brands = Brand.objects.all()
    brand_id = None
    for brand in brands:
        if brand.name.lower() in product_name:
            brand_id = brand.id
            product_name = product_name.replace(brand.name.lower(), '').strip()
            break

    # Извлекаем название модели из строки продукта
    models = Model.objects.all()
    model_id = None
    for model in models:
        if model.name.lower() in product_name:
            model_id = model.id
            product_name = product_name.replace(model.name.lower(), '').strip()
            break

    return model_id


def extract_storage(product_name):
    # Извлекаем информацию о памяти из строки продукта
    storage_info = product_name.split('/')[0].strip()

    # Извлекаем только числовое значение памяти
    storage_capacity = ''.join(filter(str.isdigit, storage_info))

    # Ищем или создаем запись о памяти в базе данных
    storage, created = Storage.objects.get_or_create(capacity=storage_capacity)

    return storage.id


def extract_color(product_name):
    # Извлекаем цвет из строки продукта
    color = product_name.split('(')[-1].split(')')[0].strip()

    # Ищем или создаем запись о цвете в базе данных
    color_obj, created = Color.objects.get_or_create(name=color)

    return color_obj.id


def determine_category(product_name):
    return 1


def process_json_file(file_path):
    # Прочитать JSON-файл и обработать каждый продукт
    import json
    with open(file_path, 'r') as file:
        products = json.load(file)
        for product_data in products:
            process_product_data(product_data)

def main():
    # Путь к вашему JSON-файлу
    file_path = r'C:\Users\Kayaba1\Desktop\technodom\parsed_data_2024.02.07_23-26-33.json'
    process_json_file(file_path)

if __name__ == "__main__":
    main()
