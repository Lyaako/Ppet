from models import *
from manager import PetManager
from datetime import datetime, date

if __name__ == "__main__":
    system = PetSystem()

    try:
        # Попытка создать животное с некорректным возрастом
        bad_pet = Pet(10, "", "Кот", "Сиамский", -1, Owner(1, "Иванов И.И.", "+79991234567"))
    except ValueError as e:
        print(f"Ошибка при создании животного: {e}")

    # Создаём владельца
    owner = Owner(1, "Иванов И.И.", "+79991234567")
    system.owners.append(owner)

    # Создаём животных
    dog = Dog(1, "Барсик", "Лабрадор", 3, owner, trained=True)
    cat = Cat(2, "Мурка", "Сиамская", 2, owner, is_indoor=True)
    bird = Bird(3, "Кеша", "Попугай", 1, owner, can_fly=False)

    system.pets.extend([dog, cat, bird])

    # Привязываем животных к владельцу
    owner.pets.extend([dog, cat, bird])

    # Добавляем медицинские записи
    record1 = HealthRecord(1, date(2024, 1, 10), "Плановый осмотр", "Ветеринар Петров")
    dog.add_health_record(record1)

    # Добавляем прививки
    vac1 = Vaccination(1, "Бешенство", date(2024, 1, 15), date(2025, 1, 15))
    dog.add_vaccination(vac1)

    # Создаём ветеринара
    vet = Vet(1, "Петров П.П.", "Терапевт")
    vet.assign_pet(dog)
    system.vets.append(vet)

    # Создаём приют
    shelter = PetShelter(1, "Собаки и кошки", "ул. Приютная, 1")
    shelter.admit_pet(cat)  # Передаём кошку в приют
    system.shelters.append(shelter)

    # Создаём магазин
    shop = PetShop(1, "Зоомагазин ЗооМир", "ул. Зоологическая, 10")
    shop.add_pet_to_sale(bird)  # Птица в продаже
    system.shops.append(shop)

    # Демонстрация работы системы
    print("ДЕМОНСТРАЦИЯ РАБОТЫ СИСТЕМЫ")
    dog.train()
    print(dog.get_info())
    print(cat.get_info())
    cat.set_indoor(False)
    bird.fly()

    print("\nСОХРАНЕНИЕ ДАННЫХ")
    # Сохраняем в JSON
    PetManager.save_to_json(system, "pets.json")

    # Сохраняем в XML
    PetManager.save_to_xml(system, "pets.xml")

    print("\n=== ЗАГРУЗКА ДАННЫХ ===")
    # Загружаем из JSON
    new_system = PetSystem()
    PetManager.load_from_json("pets.json", new_system)

    print(f"Загружено владельцев: {len(new_system.owners)}")
    print(f"Загружено животных: {len(new_system.pets)}")
    print(f"Загружено ветеринаров: {len(new_system.vets)}")
    print(f"Загружено приютов: {len(new_system.shelters)}")
    print(f"Загружено магазинов: {len(new_system.shops)}")

    if new_system.pets:
        print(f"\nПервое животное: {new_system.pets[0].get_info()}")