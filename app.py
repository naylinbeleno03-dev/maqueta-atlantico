import streamlit as st

st.set_page_config(page_title="Ruleta Estadística AMB", page_icon="🎡", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      min-height: 100vh;
      background: #0f172a;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 15px;
      color: #f8fafc;
      overflow-x: hidden;
    }

    .card {
      background: rgba(30, 41, 59, 0.95);
      border: 2px solid rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      padding: 25px;
      max-width: 520px;
      width: 100%;
      text-align: center;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.7);
      position: relative;
    }

    h1 {
      color: #38bdf8;
      font-size: 22px;
      margin-bottom: 15px;
      text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3);
    }

    /* Contenedor Ruleta Giratoria */
    .ruleta-box {
      position: relative;
      width: 260px;
      height: 260px;
      margin: 10px auto 20px;
    }

    /* Flecha Indicadora */
    .flecha {
      position: absolute;
      top: -12px;
      left: 50%;
      transform: translateX(-50%);
      width: 0;
      height: 0;
      border-left: 15px solid transparent;
      border-right: 15px solid transparent;
      border-top: 25px solid #e11d48;
      z-index: 10;
      filter: drop-shadow(0 3px 5px rgba(0,0,0,0.5));
    }

    /* Rueda Multicolor */
    .ruleta-wheel {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      border: 8px solid #f59e0b;
      background: conic-gradient(
        #ef4444 0deg 51.4deg,
        #3b82f6 51.4deg 102.8deg,
        #10b981 102.8deg 154.2deg,
        #f59e0b 154.2deg 205.6deg,
        #8b5cf6 205.6deg 257deg,
        #ec4899 257deg 308.4deg,
        #06b6d4 308.4deg 360deg
      );
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.4);
      transition: transform 3.5s cubic-bezier(0.15, 0.9, 0.15, 1);
    }

    .ruleta-centro {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      width: 50px;
      height: 50px;
      background: #f59e0b;
      border: 4px solid #ffffff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-weight: bold;
      font-size: 20px;
      color: #0f172a;
      box-shadow: 0 0 10px rgba(0,0,0,0.5);
    }

    /* Botones principales */
    button {
      background-color: #0284c7;
      color: #ffffff;
      border: none;
      padding: 12px 20px;
      font-size: 15px;
      font-weight: 700;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }

    button:hover {
      background-color: #0369a1;
      transform: translateY(-2px);
    }

    .btn-girar {
      background-color: #f59e0b;
      color: #0f172a;
      font-size: 17px;
      box-shadow: 0 4px 15px rgba(245, 158, 11, 0.5);
    }

    .btn-girar:hover {
      background-color: #d97706;
      color: #ffffff;
    }

    /* Preguntas y Opciones */
    .pregunta-titulo {
      color: #f1f5f9;
      font-size: 17px;
      margin: 15px 0;
      line-height: 1.4;
    }

    .opciones {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin: 15px 0;
    }

    .opciones button {
      background-color: #1e293b;
      color: #e2e8f0;
      text-align: left;
      border: 1px solid rgba(255, 255, 255, 0.15);
      padding: 12px 15px;
      font-size: 14px;
    }

    .opciones button:hover {
      background-color: #334155;
      border-color: #38bdf8;
      color: #ffffff;
    }

    /* Pantallas Overlay de Respuesta (Acierto / Error) */
    .overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      animation: fadeIn 0.3s ease-in-out;
    }

    .overlay.acierto {
      background: rgba(16, 185, 129, 0.95);
    }

    .overlay.error {
      background: rgba(225, 29, 72, 0.95);
    }

    .overlay-emoji {
      font-size: 100px;
      margin-bottom: 10px;
      animation: pop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .overlay-texto {
      font-size: 32px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 25px;
      text-align: center;
      text-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }

    .oculto { display: none !important; }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes pop { from { transform: scale(0.3); } to { transform: scale(1); } }
  </style>
</head>
<body>

  <div class="card">
    <h1>🎡 Área Metropolitana del Atlántico</h1>
    
    <div class="ruleta-box">
      <div class="flecha"></div>
      <div id="wheel" class="ruleta-wheel"></div>
      <div class="ruleta-centro">⭐</div>
    </div>

    <button id="btnGirar" class="btn-girar" onclick="girarRuleta()">¡GIRAR RULETA!</button>

    <div id="juego" class="oculto">
      <h2 id="pregunta" class="pregunta-titulo">Cargando pregunta...</h2>

      <div class="opciones">
        <button onclick="verificarRespuesta('A')" id="opcionA">A) ...</button>
        <button onclick="verificarRespuesta('B')" id="opcionB">B) ...</button>
        <button onclick="verificarRespuesta('C')" id="opcionC">C) ...</button>
        <button onclick="verificarRespuesta('D')" id="opcionD">D) ...</button>
      </div>
    </div>
  </div>

  <!-- Pantalla Acierto -->
  <div id="overlayAcierto" class="overlay acierto">
    <div class="overlay-emoji">🎉👏🥳</div>
    <div class="overlay-texto">¡EXCELENTE!<br>¡RESPUESTA CORRECTA!</div>
    <button onclick="cerrarOverlay('overlayAcierto')">Continuar ➡️</button>
  </div>

  <!-- Pantalla Error -->
  <div id="overlayError" class="overlay error">
    <div class="overlay-emoji">😢💔❌</div>
    <div class="overlay-texto">¡INCORRECTO!<br>¡INTÉNTALO DE NUEVO!</div>
    <button onclick="cerrarOverlay('overlayError')">Reintentar 🔄</button>
  </div>

  <script>
    // Configuración de Preguntas A, B, C, D
    const preguntas = [
      {
        pregunta: "1. ¿Cuál es la Población Total (N) representada en la maqueta?",
        A: "1.564.805 habitantes", B: "1.273.184 habitantes", C: "2.000.000 habitantes", D: "980.500 habitantes",
        correcta: "A"
      },
      {
        pregunta: "2. ¿Qué municipio representa la MODA (Mayor población)?",
        A: "Malambo", B: "Puerto Colombia", C: "Barranquilla", D: "Galapa",
        correcta: "C"
      },
      {
        pregunta: "3. ¿Cuál es el segundo municipio con mayor número de habitantes?",
        A: "Puerto Colombia", B: "Malambo", C: "Galapa", D: "Soledad",
        correcta: "B"
      },
      {
        pregunta: "4. ¿Cuál es la escala utilizada en el gráfico de la maqueta?",
        A: "1 cm = 1.000 habitantes", B: "1 cm = 100.000 habitantes", C: "1 cm = 10.000 habitantes", D: "1 cm = 50.000 habitantes",
        correcta: "C"
      },
      {
        pregunta: "5. ¿Qué municipio posee la menor población representada?",
        A: "Puerto Colombia (53.091 hab)", B: "Galapa (95.127 hab)", C: "Malambo (159.386 hab)", D: "Barranquilla",
        correcta: "A"
      },
      {
        pregunta: "6. ¿Cuál es la diferencia de población entre Barranquilla y Puerto Colombia?",
        A: "1.220.093 habitantes", B: "500.000 habitantes", C: "100.000 habitantes", D: "850.000 habitantes",
        correcta: "A"
      },
      {
        pregunta: "7. ¿Cuántos municipios conforman formalmente la Zona Metropolitana?",
        A: "3 municipios", B: "4 municipios", C: "5 municipios", D: "6 municipios",
        correcta: "C"
      }
    ];

    let preguntaActual = {};
    let anguloActual = 0;

    // Generador de sonidos integrados por código (Sintetizador Web Audio API)
    function reproducirSonido(tipo) {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      
      if (tipo === 'acierto') {
        // Sonido de Aplausos y Fanfarria
        const notas = [523.25, 659.25, 783.99, 1046.50];
        notas.forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.frequency.value = freq;
          gain.gain.setValueAtTime(0.3, ctx.currentTime + idx * 0.1);
          gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + idx * 0.1 + 0.3);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(ctx.currentTime + idx * 0.1);
          osc.stop(ctx.currentTime + idx * 0.1 + 0.3);
        });
      } else if (tipo === 'error') {
        // Sonido grave de error
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(60, ctx.currentTime + 0.4);
        gain.gain.setValueAtTime(0.4, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.4);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.4);
      }
    }

    function girarRuleta() {
      document.getElementById('juego').classList.add('oculto');
      const wheel = document.getElementById('wheel');
      
      // Giro aleatorio múltiple
      const girosExtra = Math.floor(Math.random() * 5) + 5;
      const anguloRandom = Math.floor(Math.random() * 360);
      anguloActual += (girosExtra * 360) + anguloRandom;
      
      wheel.style.transform = `rotate(${anguloActual}deg)`;

      // Seleccionar pregunta aleatoria tras el giro
      setTimeout(() => {
        preguntaActual = preguntas[Math.floor(Math.random() * preguntas.length)];
        mostrarPregunta();
      }, 3500);
    }

    function mostrarPregunta() {
      document.getElementById('juego').classList.remove('oculto');
      document.getElementById('pregunta').textContent = preguntaActual.pregunta;
      document.getElementById('opcionA').textContent = `A) ${preguntaActual.A}`;
      document.getElementById('opcionB').textContent = `B) ${preguntaActual.B}`;
      document.getElementById('opcionC').textContent = `C) ${preguntaActual.C}`;
      document.getElementById('opcionD').textContent = `D) ${preguntaActual.D}`;
    }

    function verificarRespuesta(opcion) {
      if (opcion === preguntaActual.correcta) {
        reproducirSonido('acierto');
        document.getElementById('overlayAcierto').style.display = 'flex';
      } else {
        reproducirSonido('error');
        document.getElementById('overlayError').style.display = 'flex';
      }
    }

    function cerrarOverlay(id) {
      document.getElementById(id).style.display = 'none';
      if (id === 'overlayAcierto') {
        document.getElementById('juego').classList.add('oculto');
      }
    }
  </script>
</body>
</html>
"""

st.components.v1.html(html_code, height=720, scrolling=True)
