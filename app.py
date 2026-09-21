import streamlit as st

st.set_page_config(page_title="Ruleta Interactiva AMB", page_icon="🎡", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Poppins', sans-serif;
      min-height: 100vh;
      background: radial-gradient(circle at center, #1e293b 0%, #0f172a 100%);
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 15px;
      color: #f8fafc;
      overflow-x: hidden;
    }

    /* Tarjeta Principal */
    .card {
      background: rgba(30, 41, 59, 0.75);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 28px;
      padding: 30px 20px;
      max-width: 540px;
      width: 100%;
      text-align: center;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      position: relative;
    }

    h1 {
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 20px;
      letter-spacing: -0.5px;
    }

    /* Contenedor de la Ruleta */
    .ruleta-container {
      position: relative;
      width: 310px;
      height: 310px;
      margin: 10px auto 25px;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    /* Marco Exterior Dorado */
    .ruleta-outer-ring {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: linear-gradient(145deg, #fbbf24, #b45309);
      box-shadow: 0 0 30px rgba(245, 158, 11, 0.4), inset 0 2px 5px rgba(255,255,255,0.5);
      display: flex;
      justify-content: center;
      align-items: center;
    }

    /* Flecha Indicadora 3D */
    .flecha {
      position: absolute;
      top: -15px;
      left: 50%;
      transform: translateX(-50%);
      width: 0;
      height: 0;
      border-left: 18px solid transparent;
      border-right: 18px solid transparent;
      border-top: 30px solid #f43f5e;
      z-index: 30;
      filter: drop-shadow(0 6px 8px rgba(0,0,0,0.6));
    }

    /* Ruleta Canvas con Nombres */
    #canvasRuleta {
      border-radius: 50%;
      border: 5px solid #ffffff;
      box-shadow: inset 0 0 15px rgba(0,0,0,0.5);
      transition: transform 4s cubic-bezier(0.15, 0.85, 0.15, 1);
    }

    /* Centro Estrella 3D */
    .ruleta-centro {
      position: absolute;
      width: 55px;
      height: 55px;
      background: radial-gradient(circle, #fef08a 0%, #f59e0b 100%);
      border: 4px solid #ffffff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 22px;
      z-index: 20;
      box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }

    /* Botón Principal */
    .btn-girar {
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      color: #0f172a;
      border: none;
      padding: 14px 32px;
      font-size: 16px;
      font-weight: 800;
      border-radius: 50px;
      cursor: pointer;
      box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.5);
      transition: all 0.2s ease;
      letter-spacing: 0.5px;
    }

    .btn-girar:hover {
      transform: translateY(-3px) scale(1.02);
      box-shadow: 0 15px 30px -5px rgba(245, 158, 11, 0.7);
    }

    /* Panel de Preguntas */
    #juego {
      margin-top: 25px;
      animation: fadeInUp 0.4s ease-out;
    }

    .pregunta-box {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 18px;
      padding: 18px;
      margin-bottom: 20px;
    }

    .pregunta-titulo {
      font-size: 16px;
      font-weight: 600;
      color: #f1f5f9;
      line-height: 1.5;
    }

    /* Opciones A, B, C, D */
    .opciones {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .opciones button {
      background: rgba(30, 41, 59, 0.8);
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.12);
      padding: 14px 18px;
      font-size: 14px;
      font-weight: 600;
      font-family: inherit;
      border-radius: 14px;
      cursor: pointer;
      text-align: left;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .opciones button:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      transform: translateX(5px);
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.4);
    }

    /* Overlays Pantalla Completa */
    .overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      animation: fadeIn 0.3s ease;
    }

    .overlay.acierto { background: rgba(6, 78, 59, 0.92); }
    .overlay.error { background: rgba(136, 19, 55, 0.92); }

    .overlay-card {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255,255,255,0.2);
      border-radius: 24px;
      padding: 40px;
      text-align: center;
      max-width: 400px;
      width: 90%;
      box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    .overlay-emoji { font-size: 75px; margin-bottom: 15px; }

    .overlay-titulo {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 20px;
    }

    .btn-continuar {
      background: #ffffff;
      color: #0f172a;
      border: none;
      padding: 12px 28px;
      font-size: 15px;
      font-weight: 700;
      border-radius: 50px;
      cursor: pointer;
      transition: all 0.2s;
    }

    .btn-continuar:hover { transform: scale(1.05); }

    .oculto { display: none !important; }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(15px); } to { opacity: 1; transform: translateY(0); } }
  </style>
</head>
<body>

  <div class="card">
    <h1>🎡 Área Metropolitana del Atlántico</h1>
    
    <div class="ruleta-container">
      <div class="ruleta-outer-ring">
        <div class="flecha"></div>
        <canvas id="canvasRuleta" width="280" height="280"></canvas>
        <div class="ruleta-centro">⭐</div>
      </div>
    </div>

    <button id="btnGirar" class="btn-girar" onclick="girarRuleta()">¡GIRAR RULETA!</button>

    <div id="juego" class="oculto">
      <div class="pregunta-box">
        <div id="pregunta" class="pregunta-titulo">Cargando pregunta...</div>
      </div>

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
    <div class="overlay-card">
      <div class="overlay-emoji">🥳</div>
      <div class="overlay-titulo">¡EXCELENTE!<br>Respuesta Correcta</div>
      <button class="btn-continuar" onclick="cerrarOverlay('overlayAcierto')">Continuar ➡️</button>
    </div>
  </div>

  <!-- Pantalla Error -->
  <div id="overlayError" class="overlay error">
    <div class="overlay-card">
      <div class="overlay-emoji">😢</div>
      <div class="overlay-titulo">¡INCORRECTO!<br>Inténtalo de Nuevo</div>
      <button class="btn-continuar" onclick="cerrarOverlay('overlayError')">Reintentar 🔄</button>
    </div>
  </div>

  <script>
    // Las 7 preguntas exactas ajustadas sin Soledad
    const sectores = [
      {
        titulo: "2do MÁS POBLADO",
        color: "#dc2626",
        pregunta: "1. ¿Cuál es el segundo municipio con más población?",
        A: "Malambo", B: "Galapa", C: "Puerto Colombia", D: "Barranquilla",
        correcta: "A"
      },
      {
        titulo: "MAYOR POBLACIÓN",
        color: "#2563eb",
        pregunta: "2. ¿Qué municipio concentra la mayor población?",
        A: "Galapa", B: "Barranquilla", C: "Malambo", D: "Puerto Colombia",
        correcta: "B"
      },
      {
        titulo: "ORDENAR POBLACIÓN",
        color: "#059669",
        pregunta: "3. Ordena los municipios de mayor a menor población:",
        A: "Barranquilla > Malambo > Galapa > Puerto Colombia",
        B: "Barranquilla > Galapa > Malambo > Puerto Colombia",
        C: "Malambo > Barranquilla > Galapa > Puerto Colombia",
        D: "Puerto Colombia > Galapa > Malambo > Barranquilla",
        correcta: "A"
      },
      {
        titulo: "POBLACIÓN TOTAL",
        color: "#d97706",
        pregunta: "4. ¿Cuál es la población total de la zona metropolitana representada?",
        A: "1.273.184 habitantes", B: "1.580.788 habitantes", C: "1.850.000 habitantes", D: "950.000 habitantes",
        correcta: "B"
      },
      {
        titulo: "% BARRANQUILLA",
        color: "#7c3aed",
        pregunta: "5. ¿Aproximadamente qué porcentaje de la población total representa Barranquilla?",
        A: "50%", B: "80%", C: "65%", D: "95%",
        correcta: "B"
      },
      {
        titulo: "RANGO POBLACIÓN",
        color: "#db2777",
        pregunta: "6. ¿Cuál es el rango de la población (Diferencia entre el mayor y menor)?",
        A: "1.220.093 habitantes", B: "1.100.000 habitantes", C: "950.000 habitantes", D: "1.273.184 habitantes",
        correcta: "A"
      },
      {
        titulo: "ESCALA MAQUETA",
        color: "#0891b2",
        pregunta: "7. ¿Qué significa la escala 1 cm = 50.000 habitantes?",
        A: "Que la maqueta mide 50 cm de largo",
        B: "Que 1 cm de barra representa 50.000 personas reales",
        C: "Que hay 50.000 habitantes en todo el Atlántico",
        D: "Que cada municipio mide 1 cm",
        correcta: "B"
      }
    ];

    const canvas = document.getElementById('canvasRuleta');
    const ctx = canvas.getContext('2d');
    const numSectores = sectores.length;
    const anguloArc = (2 * Math.PI) / numSectores;

    // Dibujar la Ruleta con Textos
    function dibujarRuleta() {
      const centroX = canvas.width / 2;
      const centroY = canvas.height / 2;
      const radio = canvas.width / 2;

      for (let i = 0; i < numSectores; i++) {
        const anguloInicio = i * anguloArc;
        const anguloFin = (i + 1) * anguloArc;

        // Sector de color
        ctx.beginPath();
        ctx.fillStyle = sectores[i].color;
        ctx.moveTo(centroX, centroY);
        ctx.arc(centroX, centroY, radio, anguloInicio, anguloFin);
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();

        // Texto curvado/rotado en cada sector
        ctx.save();
        ctx.translate(centroX, centroY);
        ctx.rotate(anguloInicio + anguloArc / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = "#ffffff";
        ctx.font = "bold 10px Poppins, sans-serif";
        ctx.fillText(sectores[i].titulo, radio - 12, 4);
        ctx.restore();
      }
    }

    dibujarRuleta();

    let sectorSeleccionado = {};
    let anguloActual = 0;

    // Sintetizador Web Audio para Sonidos HD
    function reproducirSonido(tipo) {
      const ctxAudio = new (window.AudioContext || window.webkitAudioContext)();
      if (tipo === 'acierto') {
        const notas = [523.25, 659.25, 783.99, 1046.50];
        notas.forEach((freq, idx) => {
          const osc = ctxAudio.createOscillator();
          const gain = ctxAudio.createGain();
          osc.frequency.value = freq;
          gain.gain.setValueAtTime(0.2, ctxAudio.currentTime + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.001, ctxAudio.currentTime + idx * 0.08 + 0.3);
          osc.connect(gain);
          gain.connect(ctxAudio.destination);
          osc.start(ctxAudio.currentTime + idx * 0.08);
          osc.stop(ctxAudio.currentTime + idx * 0.08 + 0.3);
        });
      } else {
        const osc = ctxAudio.createOscillator();
        const gain = ctxAudio.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(140, ctxAudio.currentTime);
        osc.frequency.exponentialRampToValueAtTime(40, ctxAudio.currentTime + 0.35);
        gain.gain.setValueAtTime(0.3, ctxAudio.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctxAudio.currentTime + 0.35);
        osc.connect(gain);
        gain.connect(ctxAudio.destination);
        osc.start();
        osc.stop(ctxAudio.currentTime + 0.35);
      }
    }

    function girarRuleta() {
      document.getElementById('juego').classList.add('oculto');
      const girosExtra = Math.floor(Math.random() * 5) + 6;
      const indiceAleatorio = Math.floor(Math.random() * numSectores);
      
      sectorSeleccionado = sectores[indiceAleatorio];

      // Cálculo del ángulo exacto para detenerse bajo la flecha superior (270 deg)
      const anguloSectorDeg = 360 / numSectores;
      const anguloMeta = 270 - (indiceAleatorio * anguloSectorDeg) - (anguloSectorDeg / 2);
      
      anguloActual += (girosExtra * 360) + (anguloMeta - (anguloActual % 360));
      canvas.style.transform = `rotate(${anguloActual}deg)`;

      setTimeout(() => {
        mostrarPregunta();
      }, 4000);
    }

    function mostrarPregunta() {
      document.getElementById('juego').classList.remove('oculto');
      document.getElementById('pregunta').textContent = sectorSeleccionado.pregunta;
      document.getElementById('opcionA').textContent = `A) ${sectorSeleccionado.A}`;
      document.getElementById('opcionB').textContent = `B) ${sectorSeleccionado.B}`;
      document.getElementById('opcionC').textContent = `C) ${sectorSeleccionado.C}`;
      document.getElementById('opcionD').textContent = `D) ${sectorSeleccionado.D}`;
    }

    function verificarRespuesta(opcion) {
      if (opcion === sectorSeleccionado.correcta) {
        reproducirSonido('acierto');
        confetti({ particleCount: 120, spread: 70, origin: { y: 0.6 } });
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

st.components.v1.html(html_code, height=780, scrolling=True)
