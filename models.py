from datetime import datetime, date
from typing import List, Optional

class Owner:
    def __init__(self, id: int, name: str, phone: str):
        self.id = id
        self.name = name
        self.phone = phone
        self.pets: List['Pet'] = []

    def add_pet(self, pet: 'Pet'):
        self.pets.append(pet)
        print(f"Животное {pet.name} добавлено к владельцу {self.name}")

    def remove_pet(self, pet_id: int):
        self.pets = [p for p in self.pets if p.id != pet_id]
        print(f"Животное с ID {pet_id} удалено у владельца {self.name}")


class Pet:
    def __init__(self, id: int, name: str, species: str, breed: str, age: int, owner: Owner):
        if age < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if not name or not species:
            raise ValueError("Имя и вид животного обязательны")
        self.id = id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner = owner
        self.created_at = datetime.now()
        self.health_records: List[HealthRecord] = []
        self.vaccinations: List[Vaccination] = []

    def add_health_record(self, record: 'HealthRecord'):
        self.health_records.append(record)
        print(f"Медицинская запись добавлена для {self.name}")

    def add_vaccination(self, vac: 'Vaccination'):
        self.vaccinations.append(vac)
        print(f"Прививка {vac.name} добавлена для {self.name}")

    def update_info(self, name: str = None, age: int = None):
        if name:
            self.name = name
        if age:
            if age < 0:
                raise ValueError("Возраст не может быть отрицательным")
            self.age = age
        print(f"Информация о животном {self.name} обновлена")

    def get_info(self) -> str:
        return f"Животное ID: {self.id}, Имя: {self.name}, Вид: {self.species}, Порода: {self.breed}, Возраст: {self.age}, Владелец: {self.owner.name}"


class Dog(Pet):
    def __init__(self, id: int, name: str, breed: str, age: int, owner: Owner, trained: bool = False):
        super().__init__(id, name, "Собака", breed, age, owner)
        self.trained = trained

    def train(self):
        self.trained = True
        print(f"{self.name} обучен!")


class Cat(Pet):
    def __init__(self, id: int, name: str, breed: str, age: int, owner: Owner, is_indoor: bool = True):
        super().__init__(id, name, "Кошка", breed, age, owner)
        self.is_indoor = is_indoor

    def set_indoor(self, indoor: bool):
        self.is_indoor = indoor
        print(f"Статус 'домашняя' для {self.name} изменён: {'да' if indoor else 'нет'}")


class Bird(Pet):
    def __init__(self, id: int, name: str, breed: str, age: int, owner: Owner, can_fly: bool = True):
        super().__init__(id, name, "Птица", breed, age, owner)
        self.can_fly = can_fly

    def fly(self):
        if self.can_fly:
            print(f"{self.name} летает!")
        else:
            print(f"{self.name} не может летать")


class HealthRecord:
    def __init__(self, id: int, date: date, description: str, vet_name: str):
        self.id = id
        self.date = date
        self.description = description
        self.vet_name = vet_name

    def update_description(self, new_desc: str):
        self.description = new_desc
        print(f"Описание записи обновлено: {new_desc}")


class Vaccination:
    def __init__(self, id: int, name: str, date: date, next_due: date):
        self.id = id
        self.name = name
        self.date = date
        self.next_due = next_due

    def update_due_date(self, new_date: date):
        self.next_due = new_date
        print(f"Следующая дата прививки {self.name} обновлена: {new_date}")


class Vet:
    def __init__(self, id: int, name: str, specialization: str):
        self.id = id
        self.name = name
        self.specialization = specialization
        self.assigned_pets: List[Pet] = []

    def assign_pet(self, pet: Pet):
        self.assigned_pets.append(pet)
        print(f"Животное {pet.name} назначено ветеринару {self.name}")

    def remove_pet(self, pet_id: int):
        self.assigned_pets = [p for p in self.assigned_pets if p.id != pet_id]
        print(f"Животное с ID {pet_id} снято с ветеринара {self.name}")


class PetShelter:
    def __init__(self, id: int, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address
        self.pets: List[Pet] = []

    def admit_pet(self, pet: Pet):
        self.pets.append(pet)
        print(f"Животное {pet.name} принято в приют {self.name}")

    def release_pet(self, pet_id: int):
        for pet in self.pets:
            if pet.id == pet_id:
                self.pets.remove(pet)
                print(f"Животное {pet.name} выпущено из приюта")
                return
        print(f"Животное с ID {pet_id} не найдено в приюте")


class PetShop:
    def __init__(self, id: int, name: str, address: str):
        self.id = id
        self.name = name
        self.address = address
        self.pets: List[Pet] = []

    def add_pet_to_sale(self, pet: Pet):
        self.pets.append(pet)
        print(f"Животное {pet.name} добавлено в магазин {self.name}")

    def sell_pet(self, pet_id: int):
        for pet in self.pets:
            if pet.id == pet_id:
                self.pets.remove(pet)
                print(f"Животное {pet.name} продано из магазина")
                return
        print(f"Животное с ID {pet_id} не найдено в магазине")


class PetSystem:
    """Класс для управления всей системой домашних животных"""
    def __init__(self):
        self.owners: List[Owner] = []
        self.vets: List[Vet] = []
        self.shelters: List[PetShelter] = []
        self.shops: List[PetShop] = []
        self.pets: List[Pet] = []