import json, os
d = r'E:\02_proyectos\eduplatform\ejercicios_completos-lengua-castellana'
files = [f for f in os.listdir(d) if f.endswith('.json')]

sin_ejercicios = []
con_ejercicios = []

for f in files:
    try:
        data = json.load(open(os.path.join(d, f), encoding='utf-8'))
        if not isinstance(data, dict):
            continue

        # Buscar lista de items
        items = None
        for key in ['tecnicas', 'historias', 'ejemplos', 'ejercicios']:
            if key in data and isinstance(data[key], list) and data[key]:
                items = data[key]
                item_key = key
                break

        if not items:
            sin_ejercicios.append((f, 'sin lista de items'))
            continue

        primer_item = items[0]
        if not isinstance(primer_item, dict):
            sin_ejercicios.append((f, 'items no son dict'))
            continue

        tiene_ejercicio = 'ejercicio' in primer_item
        tiene_respuesta = 'respuesta' in primer_item

        if tiene_ejercicio and tiene_respuesta:
            con_ejercicios.append((f, item_key, len(items)))
        else:
            sin_ejercicios.append((f, f'lista={item_key}, keys={list(primer_item.keys())[:6]}'))

    except Exception as e:
        sin_ejercicios.append((f, str(e)[:50]))

print('=== CON EJERCICIOS:', len(con_ejercicios), '===')
for f, key, n in con_ejercicios:
    print(f'  {f[:50]} | {key} | {n} items')

print()
print('=== SIN EJERCICIOS:', len(sin_ejercicios), '===')
for f, motivo in sin_ejercicios:
    print(f'  {f[:50]} | {motivo}')

