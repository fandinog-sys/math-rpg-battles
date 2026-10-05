import random

def formatear_set(s):
    """Devuelve la representación en string de un conjunto o ∅ si es vacío."""
    if not s:
        return "∅"
    return "{" + ", ".join(str(x) for x in sorted(s)) + "}"

def generar_conjuntos_solapados():
    """Genera conjuntos A y B con elementos del 1 al 9 con intersección garantizada."""
    todos = list(range(1, 10))
    tam_inter = random.randint(1, 2)
    inter = set(random.sample(todos, tam_inter))
    
    disponibles = [x for x in todos if x not in inter]
    tam_exclusivo_a = random.randint(2, 3)
    exclusivo_a = set(random.sample(disponibles, tam_exclusivo_a))
    
    disponibles_b = [x for x in disponibles if x not in exclusivo_a]
    tam_exclusivo_b = random.randint(2, 3)
    exclusivo_b = set(random.sample(disponibles_b, tam_exclusivo_b))
    
    A = inter | exclusivo_a
    B = inter | exclusivo_b
    return A, B

def generar_svg_venn(tipo_region):
    """
    Genera un diagrama de Venn SVG vectorizado retro con la región sombreada.
    tipo_region: 'interseccion', 'union', 'diferencia_a_b', 'diferencia_b_a', 'dif_simetrica', 'complemento_union'
    """
    color_sombra = "#66bb6a" # Verde esmeralda de resaltado
    color_borde = "#333333"
    
    shading_elements = ""
    mask_defs = ""
    
    if tipo_region == 'interseccion':
        mask_defs = '''
            <mask id="maskB">
                <rect width="240" height="130" fill="black"/>
                <circle cx="142" cy="68" r="40" fill="white"/>
            </mask>
        '''
        shading_elements = f'<circle cx="88" cy="68" r="40" fill="{color_sombra}" mask="url(#maskB)"/>'
        
    elif tipo_region == 'union':
        shading_elements = f'''
            <circle cx="88" cy="68" r="40" fill="{color_sombra}"/>
            <circle cx="142" cy="68" r="40" fill="{color_sombra}"/>
        '''
        
    elif tipo_region == 'diferencia_a_b':
        mask_defs = '''
            <mask id="maskNotB">
                <rect width="240" height="130" fill="white"/>
                <circle cx="142" cy="68" r="40" fill="black"/>
            </mask>
        '''
        shading_elements = f'<circle cx="88" cy="68" r="40" fill="{color_sombra}" mask="url(#maskNotB)"/>'
        
    elif tipo_region == 'diferencia_b_a':
        mask_defs = '''
            <mask id="maskNotA">
                <rect width="240" height="130" fill="white"/>
                <circle cx="88" cy="68" r="40" fill="black"/>
            </mask>
        '''
        shading_elements = f'<circle cx="142" cy="68" r="40" fill="{color_sombra}" mask="url(#maskNotA)"/>'
        
    elif tipo_region == 'dif_simetrica':
        mask_defs = '''
            <mask id="maskNotB">
                <rect width="240" height="130" fill="white"/>
                <circle cx="142" cy="68" r="40" fill="black"/>
            </mask>
            <mask id="maskNotA">
                <rect width="240" height="130" fill="white"/>
                <circle cx="88" cy="68" r="40" fill="black"/>
            </mask>
        '''
        shading_elements = f'''
            <circle cx="88" cy="68" r="40" fill="{color_sombra}" mask="url(#maskNotB)"/>
            <circle cx="142" cy="68" r="40" fill="{color_sombra}" mask="url(#maskNotA)"/>
        '''
        
    elif tipo_region == 'complemento_union':
        mask_defs = '''
            <mask id="maskOutside">
                <rect width="240" height="130" fill="white"/>
                <circle cx="88" cy="68" r="40" fill="black"/>
                <circle cx="142" cy="68" r="40" fill="black"/>
            </mask>
        '''
        shading_elements = f'<rect x="5" y="5" width="230" height="120" rx="6" fill="{color_sombra}" mask="url(#maskOutside)"/>'

    svg = f'''<svg viewBox="0 0 240 130" class="venn-diagram-svg" xmlns="http://www.w3.org/2000/svg">
        <defs>{mask_defs}</defs>
        <rect x="5" y="5" width="230" height="120" rx="6" fill="#fdfdf7" stroke="{color_borde}" stroke-width="2.5"/>
        <text x="18" y="24" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="{color_borde}">U</text>
        {shading_elements}
        <circle cx="88" cy="68" r="40" fill="none" stroke="{color_borde}" stroke-width="2.5"/>
        <circle cx="142" cy="68" r="40" fill="none" stroke="{color_borde}" stroke-width="2.5"/>
        <text x="68" y="44" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="{color_borde}">A</text>
        <text x="156" y="44" font-family="Courier New, monospace" font-size="14" font-weight="bold" fill="{color_borde}">B</text>
    </svg>'''
    return svg

def generar_pregunta(categoria):
    """
    Categorías soportadas:
    1. 'operaciones': Unión, intersección, diferencia, complemento y dif. simétrica.
    2. 'definiciones_potencia': Extensión, comprensión, vacío, universo, subconjuntos y conjunto potencia.
    3. 'diagramas_venn': Interpretación gráfica de regiones sombreadas con SVG.
    4. 'leyes_algebra': Leyes de De Morgan, absorción, asociatividad, conmutatividad, distributividad, etc.
    5. 'cardinalidad': Inclusión-exclusión para 2 y 3 conjuntos, cardinalidad de potencia.
    """
    svg = None

    if categoria == 'operaciones':
        A, B = generar_conjuntos_solapados()
        opcion_subtipo = random.choice(['union', 'interseccion', 'diferencia_ab', 'diferencia_ba', 'dif_simetrica', 'complemento'])
        
        if opcion_subtipo == 'union':
            correcta_set = A | B
            texto = f"Dado A = {formatear_set(A)} y B = {formatear_set(B)}, calcula A ∪ B:"
            distractores_set = [A & B, A - B, B - A, A ^ B]
        elif opcion_subtipo == 'interseccion':
            correcta_set = A & B
            texto = f"Dado A = {formatear_set(A)} y B = {formatear_set(B)}, calcula A ∩ B:"
            distractores_set = [A | B, A ^ B, A - B, B - A]
        elif opcion_subtipo == 'diferencia_ab':
            correcta_set = A - B
            texto = f"Dado A = {formatear_set(A)} y B = {formatear_set(B)}, calcula A - B:"
            distractores_set = [B - A, A & B, A ^ B, A | B]
        elif opcion_subtipo == 'diferencia_ba':
            correcta_set = B - A
            texto = f"Dado A = {formatear_set(A)} y B = {formatear_set(B)}, calcula B - A:"
            distractores_set = [A - B, A & B, A ^ B, A | B]
        elif opcion_subtipo == 'dif_simetrica':
            correcta_set = A ^ B
            texto = f"Dado A = {formatear_set(A)} y B = {formatear_set(B)}, calcula A △ B:"
            distractores_set = [A | B, A & B, A - B, B - A]
        else: # complemento relativo a U = {1..8}
            U = set(range(1, 9))
            tam_sub = random.randint(3, 5)
            SubA = set(random.sample(list(U), tam_sub))
            correcta_set = U - SubA
            texto = f"Dado el universo U = {formatear_set(U)} y A = {formatear_set(SubA)}, calcula su complemento Aᶜ:"
            distractores_set = [SubA, U, SubA | {random.choice(list(correcta_set))}, set(random.sample(list(U), len(correcta_set)))]
            
        correcta = formatear_set(correcta_set)
        distractores = [formatear_set(d) for d in distractores_set if formatear_set(d) != correcta]

    elif categoria == 'definiciones_potencia':
        banco_def = [
            (
                "Dado el conjunto por comprensión A = {x ∈ ℕ | 2 ≤ x ≤ 6}, ¿cuál es su forma por extensión?",
                "{2, 3, 4, 5, 6}",
                ["{3, 4, 5}", "{2, 3, 4, 5}", "{1, 2, 3, 4, 5, 6}"]
            ),
            (
                "Dado por extensión A = {-3, 3}, ¿cuál es su representación correcta por comprensión?",
                "{x ∈ ℤ | x² = 9}",
                ["{x ∈ ℕ | x² = 9}", "{x ∈ ℝ | x + 3 = 0}", "{x ∈ ℤ | x³ = 27}"]
            ),
            (
                "¿Cuál de los siguientes conjuntos es un conjunto VACÍO (∅)?",
                "{x ∈ ℝ | x² + 1 = 0}",
                ["{0}", "{∅}", "{x ∈ ℕ | x ≤ 1}"]
            ),
            (
                "¿Cuál es la cardinalidad del conjunto de conjuntos A = {∅, {1}, {1, 2}}?",
                "3",
                ["0", "4", "2"]
            ),
            (
                "Si un conjunto A tiene 3 elementos (ej. A = {a, b, c}), ¿cuántos elementos tiene su conjunto potencia 𝒫(A)?",
                "8",
                ["6", "9", "3"]
            ),
            (
                "Si un conjunto A tiene 4 elementos, ¿cuántos subconjuntos PROPIOS (subconjuntos distintos de A) posee?",
                "15",
                ["16", "14", "8"]
            ),
            (
                "¿A qué equivale el conjunto potencia del conjunto vacío: 𝒫(∅)?",
                "{∅}",
                ["∅", "0", "{{∅}}"]
            ),
            (
                "Si la cardinalidad de la potencia es |𝒫(A)| = 32, ¿cuántos elementos tiene A?",
                "5",
                ["4", "6", "16"]
            ),
            (
                "Si A ⊆ B, ¿cuál de las siguientes igualdades es SIEMPRE verdadera?",
                "A ∩ B = A",
                ["A ∪ B = A", "A - B = B", "A ∩ B = B"]
            ),
            (
                "¿Qué afirmación respecto a la relación de pertenencia (∈) e inclusión (⊆) es correcta para cualquier conjunto A?",
                "∅ ⊆ A",
                ["∅ ∈ A", "A ∈ A", "A ⊂ A"]
            )
        ]
        item = random.choice(banco_def)
        texto = item[0]
        correcta = item[1]
        distractores = list(item[2])

    elif categoria == 'diagramas_venn':
        regiones = [
            (
                "interseccion",
                "En el diagrama de Venn, ¿qué operación representa la región verde sombreada?",
                "A ∩ B",
                ["A ∪ B", "A - B", "A △ B"]
            ),
            (
                "union",
                "En el diagrama de Venn, ¿qué operación representa la región verde sombreada?",
                "A ∪ B",
                ["A ∩ B", "A △ B", "(A ∪ B)ᶜ"]
            ),
            (
                "diferencia_a_b",
                "En el diagrama de Venn, ¿qué operación representa la región verde sombreada?",
                "A - B",
                ["B - A", "A ∩ B", "A △ B"]
            ),
            (
                "diferencia_b_a",
                "En el diagrama de Venn, ¿qué operación representa la región verde sombreada?",
                "B - A",
                ["A - B", "A ∩ B", "(A ∪ B)ᶜ"]
            ),
            (
                "dif_simetrica",
                "En el diagrama de Venn, ¿qué operación representa la región verde sombreada?",
                "A △ B",
                ["A ∪ B", "A ∩ B", "A - B"]
            ),
            (
                "complemento_union",
                "En el diagrama de Venn, ¿qué operación representa la región sombreada fuera de los conjuntos?",
                "(A ∪ B)ᶜ",
                ["A ∪ B", "A ∩ B", "(A ∩ B)ᶜ"]
            )
        ]
        tipo_r, txt, corr, dists = random.choice(regiones)
        svg = generar_svg_venn(tipo_r)
        texto = txt
        correcta = corr
        distractores = list(dists)

    elif categoria == 'leyes_algebra':
        banco_leyes = [
            (
                "Por las Leyes de De Morgan, ¿a qué equivale (A ∪ B)ᶜ?",
                "Aᶜ ∩ Bᶜ",
                ["Aᶜ ∪ Bᶜ", "(A ∩ B)ᶜ", "A ∩ Bᶜ"]
            ),
            (
                "Por las Leyes de De Morgan, ¿a qué equivale (A ∩ B)ᶜ?",
                "Aᶜ ∪ Bᶜ",
                ["Aᶜ ∩ Bᶜ", "(A ∪ B)ᶜ", "Aᶜ ∩ B"]
            ),
            (
                "Por la Ley de Absorción, ¿a qué equivale la expresión A ∪ (A ∩ B)?",
                "A",
                ["B", "A ∪ B", "A ∩ B"]
            ),
            (
                "Por la Ley de Absorción, ¿a qué equivale la expresión A ∩ (A ∪ B)?",
                "A",
                ["B", "∅", "A ∪ B"]
            ),
            (
                "Por la Ley Distributiva, ¿a qué equivale A ∩ (B ∪ C)?",
                "(A ∩ B) ∪ (A ∩ C)",
                ["(A ∪ B) ∩ (A ∪ C)", "(A ∩ B) ∩ (A ∩ C)", "A ∩ B ∩ C"]
            ),
            (
                "Por la Ley Distributiva, ¿a qué equivale A ∪ (B ∩ C)?",
                "(A ∪ B) ∩ (A ∪ C)",
                ["(A ∩ B) ∪ (A ∩ C)", "(A ∪ B) ∪ (A ∪ C)", "A ∪ B ∪ C"]
            ),
            (
                "Por la Ley de Dominación / Aniquilación, ¿a qué equivale A ∩ ∅?",
                "∅",
                ["A", "U", "Aᶜ"]
            ),
            (
                "Por la Ley de Dominación / Aniquilación, ¿a qué equivale A ∪ U (con U universo)?",
                "U",
                ["A", "∅", "Aᶜ"]
            ),
            (
                "Por la Ley de Identidad, ¿a qué equivale A ∪ ∅?",
                "A",
                ["∅", "U", "Aᶜ"]
            ),
            (
                "Por la Ley de Identidad, ¿a qué equivale A ∩ U?",
                "A",
                ["U", "∅", "Aᶜ"]
            ),
            (
                "Por la Ley del Doble Complemento, ¿a qué equivale (Aᶜ)ᶜ?",
                "A",
                ["Aᶜ", "U", "∅"]
            ),
            (
                "Por la Ley de Idempotencia, ¿a qué equivale A ∪ A?",
                "A",
                ["2A", "∅", "U"]
            ),
            (
                "Por la Ley del Complemento, ¿a qué equivale A ∩ Aᶜ?",
                "∅",
                ["U", "A", "Aᶜ"]
            ),
            (
                "Por la Ley del Complemento, ¿a qué equivale A ∪ Aᶜ?",
                "U",
                ["∅", "A", "Aᶜ"]
            ),
            (
                "¿A qué equivale la diferencia de conjuntos A - B usando complemento?",
                "A ∩ Bᶜ",
                ["A ∪ Bᶜ", "Aᶜ ∩ B", "(A ∪ B)ᶜ"]
            )
        ]
        item = random.choice(banco_leyes)
        texto = item[0]
        correcta = item[1]
        distractores = list(item[2])

    else: # categoria == 'cardinalidad'
        tipo_card = random.choice(['dos_conjuntos', 'tres_conjuntos', 'potencia_card', 'problema_aplicacion'])
        
        if tipo_card == 'dos_conjuntos':
            card_a = random.randint(12, 28)
            card_b = random.randint(10, 25)
            inter = random.randint(3, min(card_a, card_b) - 2)
            union_card = card_a + card_b - inter
            
            subtipo = random.choice(['hallar_union', 'hallar_inter'])
            if subtipo == 'hallar_union':
                texto = f"Por el principio de inclusión-exclusión: si |A| = {card_a}, |B| = {card_b} y |A ∩ B| = {inter}, ¿cuál es |A ∪ B|?"
                correcta = str(union_card)
                distractores = [str(card_a + card_b), str(abs(card_a - card_b)), str(union_card + 3), str(union_card - 2)]
            else:
                texto = f"Si |A| = {card_a}, |B| = {card_b} y |A ∪ B| = {union_card}, ¿cuántos elementos tiene la intersección |A ∩ B|?"
                correcta = str(inter)
                distractores = [str(inter + 4), str(max(1, inter - 2)), str(card_a + card_b - union_card + 5), str(card_a - inter)]

        elif tipo_card == 'tres_conjuntos':
            # Inclusión-exclusión para 3 conjuntos
            # |A ∪ B ∪ C| = |A| + |B| + |C| - |A∩B| - |A∩C| - |B∩C| + |A∩B∩C|
            ca, cb, cc = random.randint(20, 30), random.randint(18, 28), random.randint(15, 25)
            i_ab = random.randint(6, 10)
            i_ac = random.randint(5, 9)
            i_bc = random.randint(4, 8)
            i_abc = random.randint(2, min(i_ab, i_ac, i_bc) - 1)
            
            total_union = ca + cb + cc - i_ab - i_ac - i_bc + i_abc
            texto = f"Dados 3 conjuntos: |A|={ca}, |B|={cb}, |C|={cc}, |A∩B|={i_ab}, |A∩C|={i_ac}, |B∩C|={i_bc} y |A∩B∩C|={i_abc}. Por inclusión-exclusión, ¿cuál es |A ∪ B ∪ C|?"
            correcta = str(total_union)
            distractores = [
                str(ca + cb + cc - i_ab - i_ac - i_bc), # Olvidó sumar la triple intersección
                str(ca + cb + cc),                     # Suma ingenua
                str(total_union + 4),
                str(total_union - 3)
            ]

        elif tipo_card == 'potencia_card':
            n = random.randint(3, 6)
            potencia = 2 ** n
            texto = f"Si la cardinalidad de la potencia de un conjunto es |𝒫(A)| = {potencia}, ¿cuántos elementos (|A|) tiene el conjunto A?"
            correcta = str(n)
            distractores = [str(n + 1), str(n - 1), str(potencia // 2), str(n * 2)]

        else: # problema_aplicacion
            total = random.randint(40, 60)
            futbol = random.randint(22, 32)
            basquet = random.randint(18, 28)
            ambos = random.randint(8, 14)
            al_menos_uno = futbol + basquet - ambos
            ninguno = total - al_menos_uno
            
            texto = f"En un grupo de {total} estudiantes: {futbol} juegan fútbol, {basquet} juegan básquet y {ambos} practican ambos. ¿Cuántos NO practican ninguno?"
            correcta = str(ninguno)
            distractores = [
                str(total - (futbol + basquet)),
                str(ninguno + ambos),
                str(max(1, ninguno + 4)),
                str(max(0, ninguno - 3))
            ]

    # Filtrar distractores únicos
    distractores_unicos = []
    for d in distractores:
        if d != correcta and d not in distractores_unicos:
            distractores_unicos.append(d)

    if len(distractores_unicos) >= 3:
        opciones = [correcta] + random.sample(distractores_unicos, 3)
    else:
        opciones = [correcta] + distractores_unicos
        fallbacks = ["∅", "{1, 2}", "U", "{3, 4}", "0", "1", "A ∩ B"]
        for f in fallbacks:
            if len(opciones) == 4:
                break
            if f not in opciones:
                opciones.append(f)

    random.shuffle(opciones)

    res = {
        "pregunta": texto,
        "opciones": opciones,
        "correcta": correcta
    }
    if svg:
        res["svg"] = svg
    return res
