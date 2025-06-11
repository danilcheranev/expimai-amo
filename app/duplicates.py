import os
import requests
from collections import defaultdict
import phonenumbers

from fastapi import APIRouter, HTTPException
from app.config import AMO_CLIENT_ID, AMO_CLIENT_SECRET, AMO_REDIRECT_URI, AMO_SUBDOMAIN

router = APIRouter()

# Получение токена (refresh flow)
def get_token():
    refresh = os.getenv("AMO_REFRESH_TOKEN")
    url = "https://www.amocrm.ru/oauth2/access_token"
    payload = {
        "client_id": AMO_CLIENT_ID,
        "client_secret": AMO_CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh,
        "redirect_uri": AMO_REDIRECT_URI
    }
    r = requests.post(url, json=payload)
    r.raise_for_status()
    data = r.json()
    # Нужно сохранять data["refresh_token"] обратно
    return data["access_token"]

BASE = f"https://{AMO_SUBDOMAIN}.amocrm.ru/api/v4"

# Получить все контакты
def get_contacts(token):
    headers = {"Authorization": f"Bearer {token}"}
    contacts, page = [], 1
    while True:
        r = requests.get(f"{BASE}/contacts", headers=headers, params={"page": page, "limit": 250})
        r.raise_for_status()
        batch = r.json()['_embedded']['contacts']
        if not batch:
            break
        contacts.extend(batch)
        page += 1
    return contacts

# Нормализация номера
def normalize(p):
    try:
        x = phonenumbers.parse(p, None)
        return phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
    except:
        return p.strip()

# Поиск дублей
def find_dups(contacts):
    dmap = defaultdict(list)
    for c in contacts:
        for f in c.get('custom_fields_values', []):
            if f.get('field_code') == 'PHONE':
                for v in f['values']:
                    num = normalize(v['value'])
                    dmap[num].append(c['id'])
    return {num: ids for num, ids in dmap.items() if len(set(ids)) > 1}

# Создать задачу
def create_task(token, text, resp_id):
    url = f"{BASE}/tasks"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"task_type": "common", "text": text, "responsible_user_id": resp_id}
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

# Добавить заметку к контакту
def add_note(token, cid, note):
    url = f"{BASE}/contacts/{cid}/notes"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {"note_type": "common", "params": {"text": note}}
    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    return r.json()

@router.post("/api/duplicates")
async def duplicates(mode: str = 'manual', responsible_id: int = None):
    token = get_token()
    contacts = get_contacts(token)
    dups = find_dups(contacts)
    if mode == 'manual':
        return {"duplicates": dups}
    if mode == 'auto':
        if not responsible_id:
            raise HTTPException(400, "Нужен responsible_id для auto")
        for num, ids in dups.items():
            create_task(token, f"Дубли по {num}", responsible_id)
            add_note(token, ids[0], f"Дубли {ids}")
        return {"status": "processed", "duplicates": dups}
    raise HTTPException(400, "mode manual или auto")
