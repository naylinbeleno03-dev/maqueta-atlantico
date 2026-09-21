import streamlit as st

st.set_page_config(
    page_title="Ruleta Área Metropolitana del Atlántico", 
    page_icon="🎡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilos CSS con siluetas ilustradas alusivas a los 4 municipios
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background: 
            /* Siluetas/Efectos festivos en marca de agua */
            radial-gradient(circle at 10% 20%, rgba(56, 189, 248, 0.25) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(244, 63, 94, 0.25) 0%, transparent 40%),
            linear-gradient(135deg, #0b132b 0%, #1c2541 40%, #3a506b 100%) !important;
        background-attachment: fixed !important;
    }

    /* Fondo con ilustración vectorial de los municipios */
    .stApp::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        opacity: 0.12;
        pointer-events: none;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600"><path fill="%23FFFFFF" d="M0,500 L200,500 L200,450 L220,400 L240,450 L240,500 L500,500 L500,480 L520,420 L540,480 L540,500 L1000,500 L1000,600 L0,600 Z"/><circle cx="150" cy="350" r="40" fill="%23FFFFFF"/><path fill="%23FFFFFF" d="M750,400 C780,380 820,380 850,400 L850,500 L750,500 Z"/></svg>');
        background-size: cover;
    }

    .block-container {
        padding: 0rem !important;
        max-width: 100% !important;
    }
    
    iframe {
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

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
      background: transparent;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 15px;
      color: #f8fafc;
      overflow-x: hidden;
    }

    /* Banners alusivos a los 4 municipios en las esquinas/fondo */
    .etiquetas-municipios {
      display: flex;
      gap: 12px;
      margin-bottom: 15px;
      flex-wrap: wrap;
      justify-content: center;
    }

    .badge-mun {
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.3);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 700;
      color: #fef08a;
      letter-spacing: 0.5px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    /* Tarjeta Principal */
    .card {
      background: rgba(15, 23, 42, 0.75);
      backdrop-filter: blur(25px);
      -webkit-backdrop-filter: blur(25px);
      border: 2px solid rgba(255, 255, 255, 0.3);
      border-radius: 32px;
      padding: 25px 22px;
      max-width: 530px;
      width: 100%;
      text-align: center;
      box-shadow: 0 30px 60px rgba(0, 0, 0, 0.6), inset 0 1px 2px rgba(255, 255, 255, 0.4);
    }

    h1 {
      font-size: 22px;
      font-weight: 800;
      background: linear-gradient(135deg, #38bdf8 0%, #f43f5e 50%, #fbbf24 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 18px;
    }

    .ruleta-container {
      position: relative;
      width: 300px;
      height: 300px;
      margin: 10px auto 20px;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .ruleta-outer-ring {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: linear-gradient(145deg, #f59e0b, #b45309, #f59e0b);
      box-shadow: 0 0 35px rgba(245, 158, 11, 0.7), inset 0 2px 6px rgba(255,255,255,0.8);
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .flecha {
      position: absolute;
      top: -16px;
      left: 50%;
      transform: translateX(-50%);
      width: 0;
      height: 0;
      border-left: 18px solid transparent;
      border-right: 18px solid transparent;
      border-top: 32px solid #f43f5e;
      z-index: 30;
      filter: drop-shadow(0 6px 10px rgba(0,0,0,0.8));
    }

    #canvasRuleta {
      border-radius: 50%;
      border: 5px solid #ffffff;
      box-shadow: inset 0 0 15px rgba(0,0,0,0.6);
      transition: transform 4s cubic-bezier(0.15, 0.85, 0.15, 1);
    }

    .ruleta-centro {
      position: absolute;
      width: 58px;
      height: 58px;
      background: radial-gradient(circle, #fef08a 0%, #f59e0b 100%);
      border: 4px solid #ffffff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 24px;
      z-index: 20;
      box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }

    .btn-girar {
      background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
      color: #0f172a;
      border: none;
      padding: 15px 36px;
      font-size: 16px;
      font-weight: 800;
      border-radius: 50px;
      cursor: pointer;
      box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.7);
      transition: all 0.25s ease;
    }

    .btn-girar:hover {
      transform: translateY(-3px) scale(1.04);
      box-shadow: 0 15px 35px -5px rgba(245, 158, 11, 0.9);
    }

    #juego {
      margin-top: 20px;
      animation: fadeInUp 0.4s ease-out;
    }

    .pregunta-box {
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 20px;
      padding: 18px;
      margin-bottom: 18px;
    }

    .pregunta-titulo {
      font-size: 15px;
      font-weight: 600;
      color: #f8fafc;
      line-height: 1.5;
    }

    .opciones {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .opciones button {
      background: rgba(30, 41, 59, 0.9);
      color: #e2e8f0;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 14px 18px;
      font-size: 14px;
      font-weight: 600;
      font-family: inherit;
      border-radius: 16px;
      cursor: pointer;
      text-align: left;
      transition: all 0.25s ease;
    }

    .opciones button:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #38bdf8;
      transform: translateX(5px);
    }

    .overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
    }

    .overlay.acierto { background: rgba(6, 78, 59, 0.92); }
    .overlay.error { background: rgba(136, 19, 55, 0.92); }

    .overlay-card {
      background: rgba(15, 23, 42, 0.9);
      border: 1px solid rgba(255,255,255,0.25);
      border-radius: 28px;
      padding: 35px;
      text-align: center;
      max-width: 380px;
      width: 90%;
      box-shadow: 0 30px 60px rgba(0,0,0,0.7);
    }

    .overlay-emoji { font-size: 70px; margin-bottom: 10px; }

    .overlay-titulo {
      font-size: 24px;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 18px;
    }

    .btn-continuar {
      background: #ffffff;
      color: #0f172a;
      border: none;
      padding: 13px 30px;
      font-size: 15px;
      font-weight: 800;
      border-radius: 50px;
      cursor: pointer;
    }

    .oculto { display: none !important; }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
  </style>
</head>
<body>

  <div class="etiquetas-municipios">
    <span class="badge-mun">🌆 Barranquilla</span>
    <span class="badge-mun">🌊 Puerto Colombia</span>
    <span class="badge-mun">🎭 Galapa</span>
    <span class="badge-mun">🏗️ Malambo</span>
  </div>

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

  <div id="overlayAcierto" class="overlay acierto">
    <div class="overlay-card">
      <div class="overlay-emoji">🥳</div>
      <div class="overlay-titulo">¡EXCELENTE!<br>Respuesta Correcta</div>
      <button class="btn-continuar" onclick="cerrarOverlay('overlayAcierto')">Continuar ➡️</button>
    </div>
  </div>

  <div id="overlayError" class="overlay error">
    <div class="overlay-card">
      <div class="overlay-emoji">😢</div>
      <div class="overlay-titulo">¡INCORRECTO!<br>Inténtalo de Nuevo</div>
      <button class="btn-continuar" onclick="cerrarOverlay('overlayError')">Reintentar 🔄</button>
    </div>
  </div>

  <script>
    const sectores = [
      {
        titulo: "2do MÁS POBLADO",
        color: "#dc2626",
        pregunta: "1. ¿Cuál es el segundo municipio más poblado (153.223 hab)?",
        A: "Malambo", B: "Galapa", C: "Puerto Colombia", D: "Barranquilla",
        correcta: "A"
      },
      {
        titulo: "MAYOR POBLACIÓN",
        color: "#2563eb",
        pregunta: "2. ¿Qué municipio concentra la mayor población (1.275.854 hab)?",
        A: "Galapa", B: "Barranquilla", C: "Malambo", D: "Puerto Colombia",
        correcta: "B"
      },
      {
        titulo: "ORDENAR POBLACIÓN",
        color: "#059669",
        pregunta: "3. Ordena los municipios de mayor a menor población:",
        A: "Barranquilla > Malambo > Galapa > Puerto Colombia",
        B: "Barranquilla > Malambo > Puerto Colombia > Galapa",
        C: "Malambo > Barranquilla > Galapa > Puerto Colombia",
        D: "Puerto Colombia > Galapa > Malambo > Barranquilla",
        correcta: "B"
      },
      {
        titulo: "POBLACIÓN TOTAL",
        color: "#d97706",
        pregunta: "4. ¿Cuál es la población total de los 4 municipios combinados?",
        A: "1.275.854 habitantes", B: "1.564.805 habitantes", C: "1.850.000 habitantes", D: "2.000.000 habitantes",
        correcta: "B"
      },
      {
        titulo: "% BARRANQUILLA",
        color: "#7c3aed",
        pregunta: "5. ¿Qué porcentaje de la población total del Atlántico representa Barranquilla?",
        A: "50,0%", B: "44,2%", C: "35,8%", D: "60,1%",
        correcta: "B"
      },
      {
        titulo: "RANGO POBLACIÓN",
        color: "#db2777",
        pregunta: "6. ¿Cuál es el rango poblacional (Barranquilla - Puerto Colombia)?",
        A: "1.210.168 habitantes", B: "1.100.000 habitantes", C: "950.000 habitantes", D: "1.275.854 habitantes",
        correcta: "A"
      },
      {
        titulo: "ESCALA MAQUETA",
        color: "#0891b2",
        pregunta: "7. ¿Qué representa la escala 1 cm = 50.000 habitantes?",
        A: "Que la maqueta mide 50 cm",
        B: "Que 1 cm de barra física equivale a 50.000 habitantes",
        C: "Que cada municipio tiene 50.000 habitantes",
        D: "Que la distancia entre municipios es de 1 cm",
        correcta: "B"
      }
    ];

    const canvas = document.getElementById('canvasRuleta');
    const ctx = canvas.getContext('2d');
    const numSectores = sectores.length;
    const anguloArc = (2 * Math.PI) / numSectores;

    function dibujarRuleta() {
      const centroX = canvas.width / 2;
      const centroY = canvas.height / 2;
      const radio = canvas.width / 2;

      for (let i = 0; i < numSectores; i++) {
        const anguloInicio = i * anguloArc;
        const anguloFin = (i + 1) * anguloArc;

        ctx.beginPath();
        ctx.fillStyle = sectores[i].color;
        ctx.moveTo(centroX, centroY);
        ctx.arc(centroX, centroY, radio, anguloInicio, anguloFin);
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();

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
        confetti({ particleCount: 130, spread: 80, origin: { y: 0.6 } });
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

st.components.v1.html(html_code, height=880, scrolling=False)
