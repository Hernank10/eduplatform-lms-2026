import json, os
d = r'E:\02_proyectos\eduplatform\ejercicios_completos-lengua-castellana'
files = [f for f in os.listdir(d) if f.endswith('.json')]

print('=== ANALISIS DE SALTADOS ===')
print()

for f in files:
    full = os.path.join(d, f)
    try:
        data = json.load(open(full, encoding='utf-8'))
    except Exception as e:
        print(f[:55], '| ERROR:', str(e)[:50])
        continue

    if not isinstance(data, dict):
        print(f[:55], '| no es dict')
        continue

    # Buscar lista
    tiene_tecnicas = 'tecnicas' in data and isinstance(data['tecnicas'], list) and data['tecnicas']
    tiene_historias = 'historias' in data and isinstance(data['historias'], list) and data['historias']

    if tiene_tecnicas:
        primer = data['tecnicas'][0]
        keys = list(primer.keys()) if isinstance(primer, dict) else 'N/A'
        if isinstance(primer, dict):
            if 'ejercicio' in primer and 'respuesta' in primer:
                tipo = 'ESTR-1 (ejercicio+respuesta)'
            elif 'ejercicio_correcto' in primer:
                tipo = 'ESTR-3 (ejercicio_correcto)'
            elif 'titulo_es' in primer:
                tipo = 'ESTR-2 (titulo_es)'
            else:
                tipo = 'DESCONOCIDO'
            print(f[:55], '|', tipo, '|', len(data['tecnicas']), 'items')
    elif tiene_historias:
        print(f[:55], '| ESTR-4 (historias) |', len(data['historias']), 'items')
    else:
        # Ver otras claves de lista
        claves_lista = [k for k, v in data.items() if isinstance(v, list)]
        print(f[:55], '| SIN LISTA | claves:', claves_lista[:5])

