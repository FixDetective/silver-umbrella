import re
import csv
from task2 import logger


def set_if_not_empty(entry, field, value):
    if not entry.get(field) and value.strip():
        entry[field] = value.strip()


@logger("log_1.log")
def format_phone(phone):
    cleaned = re.sub(r"[^\dдоб.]", "", phone, flags=re.IGNORECASE)

    digits = re.findall(r"\d", cleaned)
    ext_match = re.search(r"доб\.?\s*(\d+)", phone, re.IGNORECASE)

    if len(digits) < 10:
        return None  # Слишком короткий номер

    main_number = "".join(digits[-10:])

    formatted = (
        f"+7({main_number[:3]}){main_number[3:6]}-{main_number[6:8]}-{main_number[8:]}"
    )

    # Добавляем добавочный, если есть
    if ext_match:
        ext = ext_match.group(1).strip()
        formatted += f" доб.{ext}"

    return formatted


# Читаем данные
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)[1:]  # Пропускаем заголовок

contacts_dict = {}

for contact in contacts_list:
    # Объединяем ФИО и разбиваем обратно
    full_name = " ".join(contact[0:3]).split()
    lastname = full_name[0]
    firstname = full_name[1]
    key = f"{lastname} {firstname}"

    entry = contacts_dict.setdefault(
        key,
        {
            "surname": None,
            "organization": None,
            "position": None,
            "phone": None,
            "email": None,
        },
    )

    if len(full_name) > 2:
        if not entry.get("surname"):
            entry["surname"] = full_name[2]

    set_if_not_empty(entry, "organization", contact[3])
    set_if_not_empty(entry, "position", contact[4])
    set_if_not_empty(entry, "phone", contact[5])
    set_if_not_empty(entry, "email", contact[6])


for key in contacts_dict.keys():
    if contacts_dict[key]["phone"]:
        contacts_dict[key]["phone"] = format_phone(contacts_dict[key]["phone"])

corrected_contacts_list = []

corrected_contacts_list = []

for key, entry in contacts_dict.items():
    lastname, firstname = key.split()
    corrected_contacts_list.append(
        [
            lastname,
            firstname,
            entry["surname"] or "",
            entry["organization"] or "",
            entry["position"] or "",
            entry["phone"] or "",
            entry["email"] or "",
        ]
    )

with open("phonebook.csv", "w", encoding="utf-8") as f:
    datawriter = csv.writer(f, delimiter=",")
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(corrected_contacts_list)
