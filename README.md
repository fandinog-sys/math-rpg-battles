# ⚔️ Math RPG Battles - Duelo de Teoría de Conjuntos

Videojuego web retro por turnos estilo RPG (*Pokémon / Game Boy*) enfocado en el aprendizaje y práctica de **Teoría de Conjuntos (Matemáticas Discretas)**. Permite jugar en solitario contra la IA o en duelos **1 vs 1 en tiempo real** con salas privadas.

---

## 📚 Temas Matemáticos Cubiertos

1. **Conjuntos: Definiciones y Notación**:
   - Representación por extensión y por comprensión.
   - Conjunto vacío ($\emptyset$) y conjunto universo ($U$).
   - Relaciones de pertenencia ($\in$) e inclusión / subconjuntos ($\subseteq, \subset$).
   - Conjunto potencia ($\mathcal{P}(A)$) y subconjuntos propios ($2^n - 1$).
2. **Operaciones con Conjuntos**:
   - Unión ($A \cup B$).
   - Intersección ($A \cap B$).
   - Diferencia ($A - B$ y $B - A$).
   - Complemento ($A^c = U - A$).
   - Diferencia simétrica ($A \triangle B$).
3. **Diagramas de Venn**:
   - Interpretación de regiones sombreadas con diagramas vectoriales interactivos generados en **SVG**.
4. **Leyes del Álgebra de Conjuntos**:
   - Conmutatividad y Asociatividad.
   - Distributividad.
   - Leyes de De Morgan.
   - Idempotencia e Identidad.
   - Dominación / Aniquilación.
   - Doble Complemento y Leyes de Absorción.
5. **Cardinalidad e Inclusión-Exclusión**:
   - Conteo de elementos y cardinalidad del conjunto potencia.
   - Principio de inclusión-exclusión para **2 conjuntos** ($|A \cup B| = |A| + |B| - |A \cap B|$).
   - Principio de inclusión-exclusión para **3 conjuntos** ($|A \cup B \cup C|$).
   - Problemas contextualizados de aplicación.

---

## 🎮 Modos de Juego

- **🧙‍♂️ Modo Práctica (Solo vs IA)**: Entrena tus habilidades combatiendo contra el *Rival Matemático* con retroalimentación inmediata.
- **⚔️ Versus 1 a 1 (Multijugador en tiempo real)**:
  - **Crear Sala**: Ingresa tu nombre y obtén un código de 4 caracteres (ej. `M4TH`).
  - **Unirse a Sala**: Tu amigo/compañero ingresa su nombre, introduce el código y entra instantáneamente al combate.
  - Combate por turnos sincronizado por WebSockets (Socket.IO).
  - Validación segura en servidor (el oponente no puede espiar las respuestas).

---

## 🚀 Ejecución Local

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Inicia el servidor:
   ```bash
   python app.py
   ```
3. Abre en tu navegador:
   👉 **`http://127.0.0.1:5000`**

---

## ☁️ Despliegue en Railway

El proyecto ya incluye `Procfile` y detección dinámica de puerto (`PORT`) para Railway.

1. Sube este repositorio a **GitHub**.
2. Ve a [Railway.app](https://railway.app/) y selecciona **"New Project" -> "Deploy from GitHub repo"**.
3. Selecciona tu repositorio `math-rpg-battles`.
4. Railway detectará automáticamente el archivo `Procfile` y las dependencias de `requirements.txt`.
5. En la pestaña de configuración del servicio en Railway, genera un dominio público (**Generate Domain**).
6. ¡Listo! Comparte el enlace con tus amigos para jugar partidas 1v1 desde cualquier dispositivo.