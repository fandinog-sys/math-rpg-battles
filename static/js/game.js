// ================= ESTADO GLOBAL =================
let gameMode = 'practice'; // 'practice' o 'multiplayer'
let playerHP = 100;
let enemyHP = 100;
let isMyTurn = true;
let isLoadingQuestion = false;
let myUsername = "";
let enemyUsername = "Rival Matemático";
let mySid = null;
let currentRoomCode = null;
let practiceCorrectAnswer = "";

// Conexión Socket.IO (se inicializa automáticamente si está disponible)
let socket = null;
if (typeof io !== 'undefined') {
    socket = io();
}

// Elementos del DOM - Pantallas
const lobbyScreen = document.getElementById('lobby-screen');
const battleScreen = document.getElementById('battle-screen');
const waitingBox = document.getElementById('waiting-box');
const lobbyError = document.getElementById('lobby-error');
const usernameInput = document.getElementById('username-input');
const roomCodeInput = document.getElementById('room-code-input');
const displayRoomCode = document.getElementById('display-room-code');
const battleModeBadge = document.getElementById('battle-mode-badge');
const currentRoomBadge = document.getElementById('current-room-badge');

// Botones de Lobby
const btnPractice = document.getElementById('btn-practice');
const btnCreateRoom = document.getElementById('btn-create-room');
const btnJoinRoom = document.getElementById('btn-join-room');
const btnCancelRoom = document.getElementById('btn-cancel-room');
const btnLeaveBattle = document.getElementById('btn-leave-battle');

// Elementos de Batalla
const playerNameElem = document.getElementById('player-name');
const enemyNameElem = document.getElementById('enemy-name');
const playerHpBar = document.getElementById('player-hp');
const playerHpText = document.getElementById('player-hp-text');
const enemyHpBar = document.getElementById('enemy-hp');
const enemyHpText = document.getElementById('enemy-hp-text');
const playerSprite = document.getElementById('player-sprite');
const enemySprite = document.getElementById('enemy-sprite');
const dialogueText = document.getElementById('dialogue-text');
const diagramContainer = document.getElementById('diagram-container');

// Menús y Opciones de Ataque
const actionMenu = document.getElementById('action-menu');
const questionMenu = document.getElementById('question-menu');
const restartMenu = document.getElementById('restart-menu');
const restartBtn = document.getElementById('restart-btn');
const attackButtons = document.querySelectorAll('.attack-btn');
const optionButtons = document.querySelectorAll('.option-btn');

// ================= UTILIDADES VISUALES =================

function showScreen(screen) {
    if (screen === 'lobby') {
        lobbyScreen.style.display = 'block';
        battleScreen.style.display = 'none';
        waitingBox.style.display = 'none';
        lobbyError.textContent = '';
    } else {
        lobbyScreen.style.display = 'none';
        battleScreen.style.display = 'flex';
    }
}

function showBattleMenu(menuType) {
    actionMenu.style.display = (menuType === 'action') ? 'grid' : 'none';
    questionMenu.style.display = (menuType === 'question') ? 'grid' : 'none';
    restartMenu.style.display = (menuType === 'restart') ? 'flex' : 'none';
}

function setAttackButtonsEnabled(enabled) {
    attackButtons.forEach(btn => btn.disabled = !enabled);
}

function triggerDamageAnimation(spriteElement) {
    if (!spriteElement) return;
    spriteElement.classList.remove('hit');
    void spriteElement.offsetWidth;
    spriteElement.classList.add('hit');
    setTimeout(() => spriteElement.classList.remove('hit'), 500);
}

function updateHPUI() {
    playerHP = Math.max(0, playerHP);
    enemyHP = Math.max(0, enemyHP);

    playerHpBar.style.width = playerHP + '%';
    playerHpText.textContent = playerHP;

    enemyHpBar.style.width = enemyHP + '%';
    enemyHpText.textContent = enemyHP;

    playerHpBar.style.backgroundColor = playerHP <= 20 ? '#f44336' : (playerHP <= 50 ? '#ff9800' : '#4caf50');
    enemyHpBar.style.backgroundColor = enemyHP <= 20 ? '#f44336' : (enemyHP <= 50 ? '#ff9800' : '#4caf50');
}

function renderDialogue(text, svgContent = null) {
    dialogueText.textContent = text;
    if (svgContent) {
        diagramContainer.innerHTML = svgContent;
        diagramContainer.style.display = 'flex';
    } else {
        diagramContainer.innerHTML = '';
        diagramContainer.style.display = 'none';
    }
}

// ================= MODO PRÁCTICA (SOLO vs IA) =================

function startPracticeMode() {
    gameMode = 'practice';
    myUsername = usernameInput.value.trim() || 'Mago Matemático';
    enemyUsername = 'Rival Matemático';

    playerNameElem.textContent = myUsername;
    enemyNameElem.textContent = enemyUsername;
    playerSprite.textContent = '🧙‍♂️';
    enemySprite.textContent = '👾';

    playerHP = 100;
    enemyHP = 100;
    isMyTurn = true;
    isLoadingQuestion = false;

    battleModeBadge.textContent = '🧙‍♂️ Modo Práctica (vs IA)';
    currentRoomBadge.textContent = 'SOLO';

    updateHPUI();
    showScreen('battle');
    showBattleMenu('action');
    setAttackButtonsEnabled(true);
    renderDialogue("¡Un Rival salvaje te desafía a un duelo de conjuntos! Elige tu ataque.");
}

function fetchPracticeQuestion(categoria, attackName) {
    if (!isMyTurn || isLoadingQuestion) return;

    isLoadingQuestion = true;
    setAttackButtonsEnabled(false);
    renderDialogue(`Concentrando conocimiento para ${attackName}...`);

    fetch(`/api/pregunta/${categoria}`)
        .then(res => res.json())
        .then(data => {
            practiceCorrectAnswer = data.correcta;
            renderDialogue(data.pregunta, data.svg || null);

            data.opciones.forEach((opcion, index) => {
                if (optionButtons[index]) {
                    optionButtons[index].textContent = opcion;
                    optionButtons[index].disabled = false;
                }
            });

            showBattleMenu('question');
            isLoadingQuestion = false;
        })
        .catch(err => {
            console.error(err);
            renderDialogue("Error al conectar con el grimorio matemático. ¡Reintenta!");
            isLoadingQuestion = false;
            setAttackButtonsEnabled(true);
            showBattleMenu('action');
        });
}

function handlePracticeAnswer(selectedAnswer) {
    if (!isMyTurn) return;
    isMyTurn = false;
    optionButtons.forEach(btn => btn.disabled = true);
    showBattleMenu('none');

    if (selectedAnswer === practiceCorrectAnswer) {
        const damage = 25;
        enemyHP -= damage;
        updateHPUI();
        triggerDamageAnimation(enemySprite);

        if (enemyHP <= 0) {
            renderDialogue("¡Respuesta impecable! El rival no resistió tu conocimiento. ¡Ganaste! 🎉");
            showBattleMenu('restart');
            return;
        }

        renderDialogue(`¡Correcto! Causaste ${damage} de daño. Turno del rival...`);
        setTimeout(practiceEnemyTurn, 1800);
    } else {
        renderDialogue(`¡Fallaste! La respuesta correcta era: ${practiceCorrectAnswer}. Turno del rival...`);
        setTimeout(practiceEnemyTurn, 2200);
    }
}

function practiceEnemyTurn() {
    renderDialogue("El rival contraataca con una paradoja lógica...");

    setTimeout(() => {
        const damage = 20;
        playerHP -= damage;
        updateHPUI();
        triggerDamageAnimation(playerSprite);

        if (playerHP <= 0) {
            renderDialogue("Tu mente se agotó. Has perdido el duelo. 💀");
            showBattleMenu('restart');
            return;
        }

        renderDialogue(`¡Recibiste ${damage} de daño! Es tu turno, elige un ataque.`);
        isMyTurn = true;
        setAttackButtonsEnabled(true);
        showBattleMenu('action');
    }, 1400);
}

// ================= MODO MULTIJUGADOR 1v1 (SOCKET.IO) =================

if (socket) {
    socket.on('connect', () => {
        mySid = socket.id;
    });

    socket.on('room_created', (data) => {
        currentRoomCode = data.room_code;
        displayRoomCode.textContent = data.room_code;
        waitingBox.style.display = 'block';
        lobbyError.textContent = '';
    });

    socket.on('join_error', (data) => {
        lobbyError.textContent = data.message;
    });

    socket.on('game_started', (data) => {
        gameMode = 'multiplayer';
        currentRoomCode = data.room_code;

        // Determinar qué jugador soy yo
        const isP1 = (socket.id === data.player1.sid);
        const myData = isP1 ? data.player1 : data.player2;
        const enemyData = isP1 ? data.player2 : data.player1;

        myUsername = myData.name;
        enemyUsername = enemyData.name;

        playerNameElem.textContent = myUsername;
        enemyNameElem.textContent = enemyUsername;
        playerSprite.textContent = myData.sprite;
        enemySprite.textContent = enemyData.sprite;

        playerHP = 100;
        enemyHP = 100;
        updateHPUI();

        battleModeBadge.textContent = `⚔️ Modo 1v1 | Sala: ${currentRoomCode}`;
        showScreen('battle');

        // Configurar turno
        isMyTurn = (socket.id === data.current_turn);
        if (isMyTurn) {
            renderDialogue("¡Comienza la batalla! Eres el primero en atacar. Elige tu ataque.");
            showBattleMenu('action');
            setAttackButtonsEnabled(true);
        } else {
            renderDialogue(`¡Comienza la batalla! Turno inicial de ${enemyUsername}... Esperando su jugada.`);
            showBattleMenu('action');
            setAttackButtonsEnabled(false);
        }
    });

    // El servidor envía la pregunta SOLO al atacante
    socket.on('question_for_attacker', (data) => {
        renderDialogue(data.pregunta, data.svg || null);

        data.opciones.forEach((opcion, index) => {
            if (optionButtons[index]) {
                optionButtons[index].textContent = opcion;
                optionButtons[index].disabled = false;
            }
        });

        showBattleMenu('question');
        isLoadingQuestion = false;
    });

    // Notificación al defensor mientras el rival piensa
    socket.on('opponent_thinking', (data) => {
        renderDialogue(data.message);
        showBattleMenu('none');
    });

    // Resolución del ataque por el servidor
    socket.on('turn_resolved', (data) => {
        const isAttacker = (socket.id === data.attacker_sid);
        showBattleMenu('none');

        // Actualizar vida de quien recibió el daño
        if (data.target_sid === socket.id) {
            playerHP = data.target_hp;
            if (data.damage > 0) triggerDamageAnimation(playerSprite);
        } else {
            enemyHP = data.target_hp;
            if (data.damage > 0) triggerDamageAnimation(enemySprite);
        }
        updateHPUI();

        // Diálogo informativo
        if (data.es_correcto) {
            renderDialogue(`¡Acierto! ${data.attacker_name} infligió ${data.damage} de daño a ${data.target_name}.`);
        } else {
            renderDialogue(`¡Falló! ${data.attacker_name} erró el ataque. La respuesta correcta era: ${data.correcta}.`);
        }

        if (data.game_over) {
            setTimeout(() => {
                if (data.attacker_sid === socket.id) {
                    renderDialogue(`🏆 ¡VICTORIA TOTAL! Has derrotado a ${data.target_name} en el duelo de conjuntos.`);
                } else {
                    renderDialogue(`💀 ¡DERROTA! ${data.attacker_name} ha vencido tus defensas matemáticas.`);
                }
                showBattleMenu('restart');
            }, 1800);
        }
    });

    // Cambio de turno en multijugador
    socket.on('next_turn', (data) => {
        setTimeout(() => {
            isMyTurn = (socket.id === data.current_turn);
            if (isMyTurn) {
                renderDialogue("¡Es tu turno! Elige tu ataque matemático.");
                showBattleMenu('action');
                setAttackButtonsEnabled(true);
            } else {
                renderDialogue(`Turno de ${enemyUsername}... Pensando su jugada.`);
                showBattleMenu('action');
                setAttackButtonsEnabled(false);
            }
        }, 1800);
    });

    socket.on('rematch_started', (data) => {
        playerHP = 100;
        enemyHP = 100;
        updateHPUI();

        isMyTurn = (socket.id === data.current_turn);
        if (isMyTurn) {
            renderDialogue("¡Revancha iniciada! Tu turno para atacar.");
            showBattleMenu('action');
            setAttackButtonsEnabled(true);
        } else {
            renderDialogue(`¡Revancha iniciada! Turno de ${enemyUsername}...`);
            showBattleMenu('action');
            setAttackButtonsEnabled(false);
        }
    });

    socket.on('player_left', (data) => {
        renderDialogue(`⚠️ ${data.message}`);
        showBattleMenu('restart');
    });
}

// ================= EVENT LISTENERS =================

// Botón Modo Práctica
btnPractice.addEventListener('click', () => {
    startPracticeMode();
});

// Botón Crear Sala 1v1
btnCreateRoom.addEventListener('click', () => {
    const username = usernameInput.value.trim() || 'Jugador 1';
    if (!socket) {
        lobbyError.textContent = "Error: No se pudo conectar al servidor de multijugador.";
        return;
    }
    socket.emit('create_room', { username });
});

// Botón Unirse a Sala 1v1
btnJoinRoom.addEventListener('click', () => {
    const username = usernameInput.value.trim() || 'Jugador 2';
    const roomCode = roomCodeInput.value.trim().toUpperCase();

    if (!roomCode) {
        lobbyError.textContent = "Ingresa el código de 4 caracteres de la sala.";
        return;
    }
    if (!socket) {
        lobbyError.textContent = "Error: No se pudo conectar al servidor de multijugador.";
        return;
    }
    socket.emit('join_room_game', { room_code: roomCode, username });
});

// Cancelar Sala en espera
btnCancelRoom.addEventListener('click', () => {
    waitingBox.style.display = 'none';
    lobbyError.textContent = '';
});

// Salir de la Batalla al Lobby
btnLeaveBattle.addEventListener('click', () => {
    showScreen('lobby');
    if (socket && currentRoomCode) {
        window.location.reload(); // Recarga para resetear socket limpio
    }
});

// Clicks en Botones de Ataque
attackButtons.forEach(button => {
    button.addEventListener('click', () => {
        const categoria = button.getAttribute('data-categoria');
        const attackName = button.textContent.replace(/^[0-9.]\s*/, '').trim();

        if (gameMode === 'practice') {
            fetchPracticeQuestion(categoria, attackName);
        } else {
            if (!isMyTurn || isLoadingQuestion) return;
            isLoadingQuestion = true;
            setAttackButtonsEnabled(false);
            renderDialogue(`Convocando ataque '${attackName}'...`);
            socket.emit('request_attack', {
                room_code: currentRoomCode,
                categoria: categoria,
                attack_name: attackName
            });
        }
    });
});

// Clicks en Botones de Opción / Respuesta
optionButtons.forEach(button => {
    button.addEventListener('click', () => {
        const selected = button.textContent.trim();
        if (gameMode === 'practice') {
            handlePracticeAnswer(selected);
        } else {
            socket.emit('submit_answer', {
                room_code: currentRoomCode,
                answer: selected
            });
            showBattleMenu('none');
        }
    });
});

// Botón de Reinicio / Revancha
restartBtn.addEventListener('click', () => {
    if (gameMode === 'practice') {
        startPracticeMode();
    } else {
        socket.emit('rematch_request', { room_code: currentRoomCode });
    }
});

// Inicialización: Empezar en pantalla de Lobby
showScreen('lobby');