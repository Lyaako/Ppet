import json
import xml.etree.ElementTree as ET
from datetime import datetime, date
from typing import Dict, Any
from models import *


class PetManager:
    @staticmethod
    def to_dict(system: 'PetSystem') -> Dict[str, Any]:
        """Конвертирует всю систему животных в словарь для JSON"""
        return {
            "owners": [PetManager._owner_to_dict(o) for o in system.owners],
            "vets": [PetManager._vet_to_dict(v) for v in system.vets],
            "shelters": [PetManager._shelter_to_dict(s) for s in system.shelters],
            "shops": [PetManager._shop_to_dict(s) for s in system.shops],
            "pets": [PetManager._pet_to_dict(p) for p in system.pets]
        }

    @staticmethod
    def _owner_to_dict(owner: 'Owner') -> Dict[str, Any]:
        return {
            "id": owner.id,
            "name": owner.name,
            "phone": owner.phone,
            "pets": [p.id for p in owner.pets]
        }

    @staticmethod
    def _pet_to_dict(pet: 'Pet') -> Dict[str, Any]:
        base = {
            "id": pet.id,
            "name": pet.name,
            "species": pet.species,
            "breed": pet.breed,
            "age": pet.age,
            "created_at": pet.created_at.isoformat(),
            "health_records": [PetManager._health_record_to_dict(hr) for hr in pet.health_records],
            "vaccinations": [PetManager._vaccination_to_dict(v) for v in pet.vaccinations],
            "owner_id": pet.owner.id
        }
        if isinstance(pet, Dog):
            base.update({"type": "dog", "trained": pet.trained})
        elif isinstance(pet, Cat):
            base.update({"type": "cat", "is_indoor": pet.is_indoor})
        elif isinstance(pet, Bird):
            base.update({"type": "bird", "can_fly": pet.can_fly})
        return base

    @staticmethod
    def _health_record_to_dict(hr: 'HealthRecord') -> Dict[str, Any]:
        return {
            "id": hr.id,
            "date": hr.date.isoformat(),
            "description": hr.description,
            "vet_name": hr.vet_name
        }

    @staticmethod
    def _vaccination_to_dict(vac: 'Vaccination') -> Dict[str, Any]:
        return {
            "id": vac.id,
            "name": vac.name,
            "date": vac.date.isoformat(),
            "next_due": vac.next_due.isoformat()
        }

    @staticmethod
    def _vet_to_dict(vet: 'Vet') -> Dict[str, Any]:
        return {
            "id": vet.id,
            "name": vet.name,
            "specialization": vet.specialization,
            "assigned_pets": [p.id for p in vet.assigned_pets]
        }

    @staticmethod
    def _shelter_to_dict(shelter: 'PetShelter') -> Dict[str, Any]:
        return {
            "id": shelter.id,
            "name": shelter.name,
            "address": shelter.address,
            "pets": [p.id for p in shelter.pets]
        }

    @staticmethod
    def _shop_to_dict(shop: 'PetShop') -> Dict[str, Any]:
        return {
            "id": shop.id,
            "name": shop.name,
            "address": shop.address,
            "pets": [p.id for p in shop.pets]
        }

    @staticmethod
    def save_to_json(system: 'PetSystem', filename: str):
        """Сохраняет систему животных в JSON файл"""
        data = PetManager.to_dict(system)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        print(f"Данные сохранены в {filename}")

    @staticmethod
    def load_from_json(filename: str, system: 'PetSystem'):
        """Загружает систему животных из JSON файла"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        PetManager._load_from_dict(data, system)
        print(f"Данные загружены из {filename}")

    @staticmethod
    def save_to_xml(system: 'PetSystem', filename: str):
        """Сохраняет систему животных в XML файл"""
        root = ET.Element("pet_system")

        # Owners
        owners_elem = ET.SubElement(root, "owners")
        for owner in system.owners:
            owner_elem = ET.SubElement(owners_elem, "owner")
            owner_elem.set("id", str(owner.id))
            owner_elem.set("name", owner.name)
            owner_elem.set("phone", owner.phone)

            pets_elem = ET.SubElement(owner_elem, "pets")
            for pet in owner.pets:
                ET.SubElement(pets_elem, "pet_id").text = str(pet.id)

        # Pets
        pets_elem = ET.SubElement(root, "pets")
        for pet in system.pets:
            pet_elem = ET.SubElement(pets_elem, "pet")
            pet_elem.set("id", str(pet.id))
            pet_elem.set("name", pet.name)
            pet_elem.set("species", pet.species)
            pet_elem.set("breed", pet.breed)
            pet_elem.set("age", str(pet.age))
            pet_elem.set("created_at", pet.created_at.isoformat())
            pet_elem.set("owner_id", str(pet.owner.id))

            if isinstance(pet, Dog):
                pet_elem.set("type", "dog")
                pet_elem.set("trained", str(pet.trained))
            elif isinstance(pet, Cat):
                pet_elem.set("type", "cat")
                pet_elem.set("is_indoor", str(pet.is_indoor))
            elif isinstance(pet, Bird):
                pet_elem.set("type", "bird")
                pet_elem.set("can_fly", str(pet.can_fly))

            # Health records
            health_elem = ET.SubElement(pet_elem, "health_records")
            for hr in pet.health_records:
                hr_elem = ET.SubElement(health_elem, "record")
                hr_elem.set("id", str(hr.id))
                hr_elem.set("date", hr.date.isoformat())
                hr_elem.set("description", hr.description)
                hr_elem.set("vet_name", hr.vet_name)

            # Vaccinations
            vac_elem = ET.SubElement(pet_elem, "vaccinations")
            for vac in pet.vaccinations:
                vac_elem_sub = ET.SubElement(vac_elem, "vaccination")
                vac_elem_sub.set("id", str(vac.id))
                vac_elem_sub.set("name", vac.name)
                vac_elem_sub.set("date", vac.date.isoformat())
                vac_elem_sub.set("next_due", vac.next_due.isoformat())

        # Vets
        vets_elem = ET.SubElement(root, "vets")
        for vet in system.vets:
            vet_elem = ET.SubElement(vets_elem, "vet")
            vet_elem.set("id", str(vet.id))
            vet_elem.set("name", vet.name)
            vet_elem.set("specialization", vet.specialization)

            assigned_elem = ET.SubElement(vet_elem, "assigned_pets")
            for pet in vet.assigned_pets:
                ET.SubElement(assigned_elem, "pet_id").text = str(pet.id)

        # Shelters
        shelters_elem = ET.SubElement(root, "shelters")
        for shelter in system.shelters:
            shelter_elem = ET.SubElement(shelters_elem, "shelter")
            shelter_elem.set("id", str(shelter.id))
            shelter_elem.set("name", shelter.name)
            shelter_elem.set("address", shelter.address)

            pets_elem = ET.SubElement(shelter_elem, "pets")
            for pet in shelter.pets:
                ET.SubElement(pets_elem, "pet_id").text = str(pet.id)

        # Shops
        shops_elem = ET.SubElement(root, "shops")
        for shop in system.shops:
            shop_elem = ET.SubElement(shops_elem, "shop")
            shop_elem.set("id", str(shop.id))
            shop_elem.set("name", shop.name)
            shop_elem.set("address", shop.address)

            pets_elem = ET.SubElement(shop_elem, "pets")
            for pet in shop.pets:
                ET.SubElement(pets_elem, "pet_id").text = str(pet.id)

        tree = ET.ElementTree(root)
        tree.write(filename, encoding='utf-8', xml_declaration=True)
        print(f"Данные сохранены в {filename}")

    @staticmethod
    def load_from_xml(filename: str, system: 'PetSystem'):
        """Загружает систему животных из XML файла"""
        tree = ET.parse(filename)
        root = tree.getroot()

        # Clear existing data
        system.owners.clear()
        system.vets.clear()
        system.shelters.clear()
        system.shops.clear()
        system.pets.clear()

        # Temporary mapping for linking objects
        temp_owners = {}
        temp_pets = {}

        # Load owners
        for owner_elem in root.find("owners"):
            owner_id = int(owner_elem.get("id"))
            name = owner_elem.get("name")
            phone = owner_elem.get("phone")

            owner = Owner(owner_id, name, phone)
            system.owners.append(owner)
            temp_owners[owner_id] = owner

        # Load pets
        for pet_elem in root.find("pets"):
            pet_id = int(pet_elem.get("id"))
            name = pet_elem.get("name")
            species = pet_elem.get("species")
            breed = pet_elem.get("breed")
            age = int(pet_elem.get("age"))
            owner_id = int(pet_elem.get("owner_id"))
            created_at = datetime.fromisoformat(pet_elem.get("created_at"))

            owner = temp_owners[owner_id]

            pet_type = pet_elem.get("type")
            if pet_type == "dog":
                trained = pet_elem.get("trained") == "True"
                pet = Dog(pet_id, name, breed, age, owner, trained)
            elif pet_type == "cat":
                is_indoor = pet_elem.get("is_indoor") == "True"
                pet = Cat(pet_id, name, breed, age, owner, is_indoor)
            elif pet_type == "bird":
                can_fly = pet_elem.get("can_fly") == "True"
                pet = Bird(pet_id, name, breed, age, owner, can_fly)
            else:
                pet = Pet(pet_id, name, species, breed, age, owner)

            pet.created_at = created_at

            # Load health records
            for hr_elem in pet_elem.find("health_records"):
                hr_id = int(hr_elem.get("id"))
                hr_date = date.fromisoformat(hr_elem.get("date"))
                description = hr_elem.get("description")
                vet_name = hr_elem.get("vet_name")

                hr = HealthRecord(hr_id, hr_date, description, vet_name)
                pet.health_records.append(hr)

            # Load vaccinations
            for vac_elem in pet_elem.find("vaccinations"):
                vac_id = int(vac_elem.get("id"))
                vac_name = vac_elem.get("name")
                vac_date = date.fromisoformat(vac_elem.get("date"))
                next_due = date.fromisoformat(vac_elem.get("next_due"))

                vac = Vaccination(vac_id, vac_name, vac_date, next_due)
                pet.vaccinations.append(vac)

            system.pets.append(pet)
            temp_pets[pet_id] = pet

            # Link pet to owner
            owner.pets.append(pet)

        # Load vets
        for vet_elem in root.find("vets"):
            vet_id = int(vet_elem.get("id"))
            name = vet_elem.get("name")
            specialization = vet_elem.get("specialization")

            vet = Vet(vet_id, name, specialization)

            for pet_id_elem in vet_elem.find("assigned_pets"):
                pet_id = int(pet_id_elem.text)
                if pet_id in temp_pets:
                    vet.assigned_pets.append(temp_pets[pet_id])

            system.vets.append(vet)

        # Load shelters
        for shelter_elem in root.find("shelters"):
            shelter_id = int(shelter_elem.get("id"))
            name = shelter_elem.get("name")
            address = shelter_elem.get("address")

            shelter = PetShelter(shelter_id, name, address)

            for pet_id_elem in shelter_elem.find("pets"):
                pet_id = int(pet_id_elem.text)
                if pet_id in temp_pets:
                    shelter.pets.append(temp_pets[pet_id])

            system.shelters.append(shelter)

        # Load shops
        for shop_elem in root.find("shops"):
            shop_id = int(shop_elem.get("id"))
            name = shop_elem.get("name")
            address = shop_elem.get("address")

            shop = PetShop(shop_id, name, address)

            for pet_id_elem in shop_elem.find("pets"):
                pet_id = int(pet_id_elem.text)
                if pet_id in temp_pets:
                    shop.pets.append(temp_pets[pet_id])

            system.shops.append(shop)

        print(f"Данные загружены из {filename}")

    @staticmethod
    def _load_from_dict(data: Dict[str, Any], system: 'PetSystem'):
        """Загружает данные из словаря в систему"""
        # Clear existing data
        system.owners.clear()
        system.vets.clear()
        system.shelters.clear()
        system.shops.clear()
        system.pets.clear()

        # Temporary mapping
        temp_owners = {}
        temp_pets = {}

        # Load owners
        for owner_data in data["owners"]:
            owner = Owner(
                owner_data["id"],
                owner_data["name"],
                owner_data["phone"]
            )
            system.owners.append(owner)
            temp_owners[owner.id] = owner

        # Load pets
        for pet_data in data["pets"]:
            owner_id = pet_data["owner_id"]
            owner = temp_owners[owner_id]

            pet_type = pet_data.get("type")
            if pet_type == "dog":
                pet = Dog(
                    pet_data["id"],
                    pet_data["name"],
                    pet_data["breed"],
                    pet_data["age"],
                    owner,
                    pet_data.get("trained", False)
                )
            elif pet_type == "cat":
                pet = Cat(
                    pet_data["id"],
                    pet_data["name"],
                    pet_data["breed"],
                    pet_data["age"],
                    owner,
                    pet_data.get("is_indoor", True)
                )
            elif pet_type == "bird":
                pet = Bird(
                    pet_data["id"],
                    pet_data["name"],
                    pet_data["breed"],
                    pet_data["age"],
                    owner,
                    pet_data.get("can_fly", True)
                )
            else:
                pet = Pet(
                    pet_data["id"],
                    pet_data["name"],
                    pet_data["species"],
                    pet_data["breed"],
                    pet_data["age"],
                    owner
                )

            pet.created_at = datetime.fromisoformat(pet_data["created_at"])

            # Load health records
            for hr_data in pet_data["health_records"]:
                hr = HealthRecord(
                    hr_data["id"],
                    date.fromisoformat(hr_data["date"]),
                    hr_data["description"],
                    hr_data["vet_name"]
                )
                pet.health_records.append(hr)

            # Load vaccinations
            for vac_data in pet_data["vaccinations"]:
                vac = Vaccination(
                    vac_data["id"],
                    vac_data["name"],
                    date.fromisoformat(vac_data["date"]),
                    date.fromisoformat(vac_data["next_due"])
                )
                pet.vaccinations.append(vac)

            system.pets.append(pet)
            temp_pets[pet.id] = pet
            owner.pets.append(pet)

        # Load vets
        for vet_data in data["vets"]:
            vet = Vet(
                vet_data["id"],
                vet_data["name"],
                vet_data["specialization"]
            )

            for pet_id in vet_data["assigned_pets"]:
                if pet_id in temp_pets:
                    vet.assigned_pets.append(temp_pets[pet_id])

            system.vets.append(vet)

        # Load shelters
        for shelter_data in data["shelters"]:
            shelter = PetShelter(
                shelter_data["id"],
                shelter_data["name"],
                shelter_data["address"]
            )

            for pet_id in shelter_data["pets"]:
                if pet_id in temp_pets:
                    shelter.pets.append(temp_pets[pet_id])

            system.shelters.append(shelter)

        # Load shops
        for shop_data in data["shops"]:
            shop = PetShop(
                shop_data["id"],
                shop_data["name"],
                shop_data["address"]
            )

            for pet_id in shop_data["pets"]:
                if pet_id in temp_pets:
                    shop.pets.append(temp_pets[pet_id])

            system.shops.append(shop)