import json
from collections import defaultdict

def cargar_anotaciones(ruta_archivo):
    """
    Carga el JSON y agrupa las etiquetas ('Task') por cada intervalo de tiempo exacto.
    """
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        
    anotaciones_por_frase = defaultdict(set)
    
    for item in datos:
        start = round(float(item["Start"]), 3)
        end = round(float(item["end"]), 3)
        etiqueta = item["Task"].strip()
        
        anotaciones_por_frase[(start, end)].add(etiqueta)
        
    return anotaciones_por_frase

def calcular_acuerdo_jaccard(json_revisor1, json_revisor2):
    # 1. Cargar y agrupar los datos iniciales
    anot_r1 = cargar_anotaciones(json_revisor1)
    anot_r2 = cargar_anotaciones(json_revisor2)
    
    # 2. Obtener todos los intervalos y ordenarlos cronológicamente por 'Start'
    todas_las_frases = set(anot_r1.keys()).union(set(anot_r2.keys()))
    intervalos_ordenados = sorted(list(todas_las_frases))
    
    intervalos_fusionados = []
    
    # 3. Algoritmo para fusionar intervalos solapados
    if intervalos_ordenados:
        start_actual, end_actual = intervalos_ordenados[0]
        r1_labels_actuales = set(anot_r1.get((start_actual, end_actual), set()))
        r2_labels_actuales = set(anot_r2.get((start_actual, end_actual), set()))
        
        for next_start, next_end in intervalos_ordenados[1:]:
            # Si el siguiente intervalo empieza antes o justo cuando termina el actual -> Hay solapamiento
            if next_start <= end_actual:
                # Extendemos el final del bloque al máximo de los dos intervalos
                end_actual = max(end_actual, next_end)
                # Unimos las etiquetas de ese nuevo tramo de tiempo solapado
                r1_labels_actuales.update(anot_r1.get((next_start, next_end), set()))
                r2_labels_actuales.update(anot_r2.get((next_start, next_end), set()))
            else:
                # No hay solapamiento: guardamos el bloque construido y empezamos uno nuevo
                intervalos_fusionados.append(((start_actual, end_actual), r1_labels_actuales, r2_labels_actuales))
                start_actual, end_actual = next_start, next_end
                r1_labels_actuales = set(anot_r1.get((start_actual, end_actual), set()))
                r2_labels_actuales = set(anot_r2.get((start_actual, end_actual), set()))
        
        # Añadimos el último bloque evaluado
        intervalos_fusionados.append(((start_actual, end_actual), r1_labels_actuales, r2_labels_actuales))

    # 4. Calcular el Jaccard sobre los bloques ya fusionados
    resultados_jaccard = []
    total_intersecciones = 0
    total_uniones = 0
    
    print(f"{'Intervalo (Start - End)':<25} | {'Jaccard':<7} | {'Etiquetas R1':<40} | {'Etiquetas R2'}")
    print("-" * 115)
    
    for (start, end), etiquetas_r1, etiquetas_r2 in intervalos_fusionados:
        interseccion = len(etiquetas_r1.intersection(etiquetas_r2))
        union = len(etiquetas_r1.union(etiquetas_r2))

        total_intersecciones += interseccion
        total_uniones += union

        if union == 0:
            jaccard = 1.0
        else:
            jaccard = interseccion / union
            
        resultados_jaccard.append(jaccard)
        
        print(f"{start:>7} - {end:<13} | {jaccard:.4f}  | {str(etiquetas_r1):<40} | {str(etiquetas_r2)}")
        
    jaccard_medio = sum(resultados_jaccard) / len(resultados_jaccard) if resultados_jaccard else 0
    jaccard_global = total_intersecciones / total_uniones if total_uniones > 0 else 1.0
    
    print("-" * 115)
    print(f"Total de bloques conversacionales tras fusión: {len(intervalos_fusionados)}")
    print(f"JACCARD MEDIO (Instance-averaged): {jaccard_medio:.4f}")
    print(f"JACCARD GLOBAL (Micro-averaged): {jaccard_global:.4f}")

    return jaccard_medio

if __name__ == "__main__":
    archivo_revisor_1 = "G:/Mi unidad/doctorado/Pablo Castillo - DOCTORADO/2_soa/8 Prepare scenario/Audio analysis/LocalPython/Prototipo Whisperx_/structured outputs/manual_total_pablo.json" 
    archivo_revisor_2 = "G:/Mi unidad/doctorado/Pablo Castillo - DOCTORADO/2_soa/8 Prepare scenario/Audio analysis/LocalPython/Prototipo Whisperx_/structured outputs/manual_total_mcp.json"
    
    calcular_acuerdo_jaccard(archivo_revisor_1, archivo_revisor_2)