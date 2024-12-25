import os
import shutil
import random

def create_class_folders(base_path, class_ids):
    """Создает папки для классов в заданной директории."""
    for class_id in class_ids:
        os.makedirs(os.path.join(base_path, str(class_id)), exist_ok=True)

def get_class_from_number(number):
    """Соотносит номер с классом."""
    class_mapping = {
        1: 6, 2: 8, 3: 10, 4: 14, 5: 106,
        6: 108, 7: 109, 8: 110, 9: 111,
        10: 112, 11: 114, 12: 116, 13: 118,
        14: 120, 15: 122, 16: 124, 17: 151,
        18: 153, 19: 290, 20: 152
    }
    
    return class_mapping.get(number)

def split_data(files, train_ratio=0.8):
    """Разбивает данные на тренировочные и тестовые наборы."""
    train_size = int(len(files) * train_ratio)
    return files[:train_size], files[train_size:]

def process_files(input_folder, train_folder, test_folder, class_ids):
    """Обрабатывает файлы, распределяя изображения по классам."""
    # Создаем папки для train и test классов
    create_class_folders(train_folder, class_ids)
    create_class_folders(test_folder, class_ids)

    # Получаем список файлов в папке и перемешиваем его
    files = os.listdir(input_folder)
    files = [f for f in files if f.endswith('.txt')]  # Оставляем только текстовые файлы
    random.shuffle(files)

    # Разделяем на тренировочные и тестовые наборы
    train_files, test_files = split_data(files)

    for file_set in [("train", train_files), ("test", test_files)]:
        set_name, file_list = file_set
        for filename in file_list:
            txt_file_path = os.path.join(input_folder, filename)

            # Читаем первый номер из текстового файла
            with open(txt_file_path, 'r') as file:
                first_line = file.readline().strip()
                first_number = int(first_line.split()[0])  # Парсим первое число

            class_id = get_class_from_number(first_number)

            if class_id is not None:
                # Пытаемся найти соответствующее изображение
                image_filename = filename.replace('.txt', '.jpg')  # Предполагается формат JPG
                image_file_path = os.path.join(input_folder, image_filename)

                if os.path.exists(image_file_path):
                    # Определяем папку назначения
                    destination_folder = os.path.join(train_folder if set_name == "train" else test_folder, str(class_id))
                    # Копируем изображение и текстовый файл в папку класса
                    shutil.copy(image_file_path, destination_folder)
                    shutil.copy(txt_file_path, destination_folder)
                    print(f"{set_name.capitalize()} - Изображение {image_filename} и текстовый файл скопированы в папку класса {class_id}.")
                else:
                    print(f"{set_name.capitalize()} - Изображение {image_filename} не найдено.")
            else:
                print(f"{set_name.capitalize()} - Класс для {first_number} не найден.")

def main():
    input_folder = 'YOLOv11/raw_dataset'  # Укажите путь к вашей папке с изображениями и текстами
    train_folder = 'YOLOv11/datasets/train'  # Укажите путь к целевой папке для обучающего набора
    test_folder = 'YOLOv11/datasets/test'  # Укажите путь к целевой папке для тестового набора
    class_ids = [
        6, 8, 10, 14, 106, 108, 109, 110,
        111, 112, 114, 116, 118, 120, 122,
        124, 151, 153, 290, 152
    ]

    process_files(input_folder, train_folder, test_folder, class_ids)

if __name__ == "__main__":
    main()
