
import re

def format_phone_number(phone_number: str) -> str:
    # Remover quaisquer caracteres não numéricos
    phone_number = re.sub(r'\D', '', phone_number)
    
    # Verificar se o número tem exatamente 11 dígitos
    if len(phone_number) == 11:
        formatted_number = f"({phone_number[:2]}) {phone_number[2:7]}-{phone_number[7:]}"
        return formatted_number
    else:
        return phone_number

def valida_email(email: str) -> bool:
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regex, email):
        return True
    return False

def valida_telefone(telefone: str) -> bool:
    regex = r'^\+?[1-9]\d{1,14}$'
    if re.match(regex, telefone):
        return True
    return False