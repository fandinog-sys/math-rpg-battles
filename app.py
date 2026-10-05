from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
import string
import os
from math_engine import generar_pregunta

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'math-rpg-secret-key-1234')
app.config['JSON_AS_ASCII'] = False

# Socket.IO con soporte CORS para despliegue en Railway
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Almacenamiento de salas activas para el 1v1
# { room_code: { ... } }
rooms = {}

def generar_codigo_sala():
    caracteres = string.ascii_uppercase + string.digits
    while True:
        codigo = ''.join(random.choices(caracteres, k=4))
        if codigo not in rooms:
            return codigo

@app.route('/')
def index():
    return render_template('index.html')

# Endpoint REST para el modo práctica (Solo vs IA)
@app.route('/api/pregunta/<categoria>', methods=['GET'])
def obtener_pregunta(categoria):
    pregunta_data = generar_pregunta(categoria)
    return jsonify(pregunta_data)

# ==================== SOCKET.IO: MULTIJUGADOR 1v1 ====================

@socketio.on('create_room')
def on_create_room(data):
    username = (data.get('username') or 'Jugador 1').strip()[:15]
    room_code = generar_codigo_sala()
    
    rooms[room_code] = {
        "code": room_code,
        "players": {
            request.sid: {
                "name": username,
                "hp": 100,
                "sprite": "🧙‍♂️"
            }
        },
        "order": [request.sid],
        "current_turn": None,
        "active_question": None,
        "game_over": False
    }
    
    join_room(room_code)
    emit('room_created', {
        "room_code": room_code,
        "username": username,
        "sid": request.sid
    })

@socketio.on('join_room_game')
def on_join_room_game(data):
    room_code = (data.get('room_code') or '').strip().upper()
    username = (data.get('username') or 'Jugador 2').strip()[:15]
    
    if room_code not in rooms:
        emit('join_error', {"message": "La sala indicada no existe."})
        return
        
    sala = rooms[room_code]
    if len(sala["players"]) >= 2:
        emit('join_error', {"message": "La sala ya está llena (máximo 2 jugadores)."})
        return
        
    # Asignar Jugador 2
    sala["players"][request.sid] = {
        "name": username,
        "hp": 100,
        "sprite": "🧝‍♀️"
    }
    sala["order"].append(request.sid)
    join_room(room_code)
    
    # Elegir aleatoriamente quién empieza el combate
    primer_turno = random.choice(sala["order"])
    sala["current_turn"] = primer_turno
    
    p1_sid, p2_sid = sala["order"][0], sala["order"][1]
    p1 = sala["players"][p1_sid]
    p2 = sala["players"][p2_sid]
    
    # Avisar a ambos que la batalla comenzó
    emit('game_started', {
        "room_code": room_code,
        "player1": {"sid": p1_sid, "name": p1["name"], "hp": p1["hp"], "sprite": p1["sprite"]},
        "player2": {"sid": p2_sid, "name": p2["name"], "hp": p2["hp"], "sprite": p2["sprite"]},
        "current_turn": primer_turno,
        "turn_name": sala["players"][primer_turno]["name"]
    }, to=room_code)

@socketio.on('request_attack')
def on_request_attack(data):
    room_code = data.get('room_code')
    categoria = data.get('categoria')
    attack_name = data.get('attack_name')
    
    if room_code not in rooms:
        return
    sala = rooms[room_code]
    if sala["current_turn"] != request.sid:
        return # No es su turno
        
    pregunta_obj = generar_pregunta(categoria)
    sala["active_question"] = {
        "correcta": pregunta_obj["correcta"],
        "attacker": request.sid
    }
    
    # Enviar la pregunta con opciones (y SVG si hay) solo al atacante para evitar trampas
    emit('question_for_attacker', {
        "pregunta": pregunta_obj["pregunta"],
        "opciones": pregunta_obj["opciones"],
        "svg": pregunta_obj.get("svg"),
        "categoria": categoria,
        "attack_name": attack_name
    })
    
    # Avisar al rival que el jugador está respondiendo
    attacker_name = sala["players"][request.sid]["name"]
    emit('opponent_thinking', {
        "message": f"¡{attacker_name} está preparando el ataque '{attack_name}'! Espera su jugada..."
    }, to=room_code, include_self=False)

@socketio.on('submit_answer')
def on_submit_answer(data):
    room_code = data.get('room_code')
    chosen_answer = (data.get('answer') or '').strip()
    
    if room_code not in rooms:
        return
    sala = rooms[room_code]
    if sala["current_turn"] != request.sid or not sala["active_question"]:
        return
        
    correcta = sala["active_question"]["correcta"].strip()
    attacker_sid = request.sid
    target_sid = [s for s in sala["order"] if s != attacker_sid][0]
    
    attacker_name = sala["players"][attacker_sid]["name"]
    target_name = sala["players"][target_sid]["name"]
    
    es_correcto = (chosen_answer == correcta)
    damage = 25 if es_correcto else 0
    
    if es_correcto:
        sala["players"][target_sid]["hp"] = max(0, sala["players"][target_sid]["hp"] - damage)
        
    target_hp = sala["players"][target_sid]["hp"]
    game_over = (target_hp <= 0)
    
    # Resultado del ataque a ambos jugadores
    emit('turn_resolved', {
        "es_correcto": es_correcto,
        "damage": damage,
        "attacker_sid": attacker_sid,
        "target_sid": target_sid,
        "target_hp": target_hp,
        "attacker_name": attacker_name,
        "target_name": target_name,
        "correcta": correcta,
        "game_over": game_over
    }, to=room_code)
    
    sala["active_question"] = None
    
    if not game_over:
        # Cambiar turno al otro jugador
        sala["current_turn"] = target_sid
        emit('next_turn', {
            "current_turn": target_sid,
            "turn_name": target_name
        }, to=room_code)

@socketio.on('rematch_request')
def on_rematch_request(data):
    room_code = data.get('room_code')
    if room_code not in rooms:
        return
    sala = rooms[room_code]
    
    # Reiniciar vidas
    for sid in sala["players"]:
        sala["players"][sid]["hp"] = 100
        
    sala["game_over"] = False
    primer_turno = random.choice(sala["order"])
    sala["current_turn"] = primer_turno
    
    emit('rematch_started', {
        "current_turn": primer_turno,
        "turn_name": sala["players"][primer_turno]["name"]
    }, to=room_code)

@socketio.on('disconnect')
def on_disconnect():
    # Buscar si el socket estaba en alguna sala
    for room_code, sala in list(rooms.items()):
        if request.sid in sala["players"]:
            leaving_name = sala["players"][request.sid]["name"]
            emit('player_left', {
                "message": f"El jugador {leaving_name} se ha desconectado de la sala."
            }, to=room_code, include_self=False)
            del sala["players"][request.sid]
            if request.sid in sala["order"]:
                sala["order"].remove(request.sid)
            # Si quedó vacía la sala, eliminarla
            if not sala["players"]:
                del rooms[room_code]
            break

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"¡Servidor Math RPG Battles iniciado en http://localhost:{port}!")
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)