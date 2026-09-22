import streamlit as st
import base64

st.set_page_config(
    page_title="Ruleta Área Metropolitana del Atlántico", 
    page_icon="🎡", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Convertir la imagen local a base64 para cargarla directamente en el CSS
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

try:
    img_base64 = get_base64_image("fondo.png")
    bg_style = f"background-image: url('data:image/png;base64,{img_base64}');"
except Exception:
    bg_style = "background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);"

st.markdown(f"""
    <style>
    #MainMenu {{visibility: hidden;}}
    header {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    .stApp {{
        {bg_style}
        background-size: 100% 100% !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    .block-container {{
        padding: 0rem !important;
        max-width: 100% !important;
    }}
    
    iframe {{
        border: none !important;
        width: 100% !important;
    }}
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
      justify-content: center;
      align-items: center;
      padding: 10px;
      color: #1e293b;
      overflow: hidden;
    }

    /* Tarjeta Principal Más Ancha */
    .card {
      background: rgba(255, 255, 255, 0.95);
      border: 2px solid rgba(255, 255, 255, 0.9);
      border-radius: 28px;
      padding: 20px 22px;
      max-width: 480px;
      width: 100%;
      text-align: center;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }

    h1 {
      font-size: 22px;
      font-weight: 800;
      color: #0f172a;
      background: linear-gradient(135deg, #0284c7 0%, #e11d48 50%, #d97706 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }

    /* Ruleta Ampliada a 340px */
    .ruleta-container {
      position: relative;
      width: 340px;
      height: 340px;
      margin: 5px auto 15px;
      display: flex;
      justify-content: center;
      align-items: center;
    }

    .ruleta-outer-ring {
      position: absolute;
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: linear-gradient(145deg, #fbbf24, #d97706, #fbbf24);
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.8), inset 0 2px 6px rgba(255,255,255,0.8);
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
      border-top: 32px solid #ff0033;
      z-index: 30;
      filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4));
    }

    #canvasRuleta {
      border-radius: 50%;
      border: 5px solid #ffffff;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
      transition: transform 4s cubic-bezier(0.15, 0.85, 0.15, 1);
    }

    .ruleta-centro {
      position: absolute;
      width: 60px;
      height: 60px;
      background: radial-gradient(circle, #fef08a 0%, #f59e0b 100%);
      border: 4px solid #ffffff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 26px;
      z-index: 20;
      box-shadow: 0 3px 12px rgba(0,0,0,0.25);
    }

    /* Botón de Girar Ruleta */
    .btn-girar {
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: #ffffff;
      border: 2px solid transparent;
      padding: 12px 32px;
      font-size: 16px;
      font-weight: 800;
      border-radius: 50px;
      cursor: pointer;
      box-shadow: 0 8px 18px -3px rgba(2, 132, 199, 0.5);
      transition: all 0.3s ease;
    }

    .btn-girar:hover, .btn-girar:active {
      background: linear-gradient(135deg, #ffe066 0%, #f59e0b 50%, #d97706 100%);
      color: #0f172a;
      border-color: #fef08a;
      transform: translateY(-2px) scale(1.05);
      box-shadow: 0 0 25px rgba(245, 158, 11, 0.9), 0 10px 20px -3px rgba(217, 119, 6, 0.6);
    }

    #juego {
      margin-top: 15px;
      animation: fadeInUp 0.4s ease-out;
    }

    .pregunta-box {
      background: rgba(241, 245, 249, 0.95);
      border: 1px solid rgba(203, 213, 225, 0.8);
      border-radius: 16px;
      padding: 14px;
      margin-bottom: 12px;
    }

    .pregunta-titulo {
      font-size: 14px;
      font-weight: 700;
      color: #0f172a;
      line-height: 1.4;
    }

    .opciones {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .opciones button {
      background: #ffffff;
      color: #1e293b;
      border: 1.5px solid #cbd5e1;
      padding: 10px 14px;
      font-size: 13px;
      font-weight: 600;
      font-family: inherit;
      border-radius: 12px;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
    }

    .opciones button:hover {
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
      transform: translateX(3px);
    }

    /* Pantallas completas opacas */
    .overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .overlay.acierto { 
      background: #00c853 !important; 
    }

    .overlay.error { 
      background: #d50000 !important; 
    }

    .overlay-card {
      background: #ffffff !important;
      border-radius: 24px;
      padding: 28px;
      text-align: center;
      max-width: 320px;
      width: 90%;
      box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .overlay-emoji { font-size: 60px; margin-bottom: 8px; }

    .overlay-titulo {
      font-size: 20px;
      font-weight: 800;
      color: #0f172a;
      margin-bottom: 15px;
    }

    .btn-continuar {
      background: #0f172a;
      color: #ffffff;
      border: none;
      padding: 12px 28px;
      font-size: 14px;
      font-weight: 800;
      border-radius: 50px;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .oculto { display: none !important; }

    @keyframes fadeInUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
  </style>
</head>
<body>

  <div class="card">
    <h1>🎡 Área Metropolitana del Atlántico</h1>
    
    <div class="ruleta-container">
      <div class="ruleta-outer-ring">
        <div class="flecha"></div>
        <canvas id="canvasRuleta" width="310" height="310"></canvas>
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
        color: "#ff0033",
        pregunta: "1. ¿Cuál es el segundo municipio más poblado (153.223 hab)?",
        A: "Malambo", B: "Galapa", C: "Puerto Colombia", D: "Barranquilla",
        correcta: "A"
      },
      {
        titulo: "MAYOR POBLACIÓN",
        color: "#0066ff",
        pregunta: "2. ¿Qué municipio concentra la mayor población (1.275.854 hab)?",
        A: "Galapa", B: "Barranquilla", C: "Malambo", D: "Puerto Colombia",
        correcta: "B"
      },
      {
        titulo: "ORDENAR POBLACIÓN",
        color: "#00cc44",
        pregunta: "3. Ordena los municipios de mayor a menor población:",
        A: "Barranquilla > Malambo > Galapa > Puerto Colombia",
        B: "Barranquilla > Malambo > Puerto Colombia > Galapa",
        C: "Malambo > Barranquilla > Galapa > Puerto Colombia",
        D: "Puerto Colombia > Galapa > Malambo > Barranquilla",
        correcta: "B"
      },
      {
        titulo: "POBLACIÓN TOTAL",
        color: "#ff8800",
        pregunta: "4. ¿Cuál es la población total de los 4 municipios combinados?",
        A: "1.275.854 habitantes", B: "1.564.805 habitantes", C: "1.850.000 habitantes", D: "2.000.000 habitantes",
        correcta: "B"
      },
      {
        titulo: "% BARRANQUILLA",
        color: "#8800ff",
        pregunta: "5. ¿Qué porcentaje de la población total del Atlántico representa Barranquilla?",
        A: "50,0%", B: "44,2%", C: "35,8%", D: "60,1%",
        correcta: "B"
      },
      {
        titulo: "RANGO POBLACIÓN",
        color: "#ff0077",
        pregunta: "6. ¿Cuál es el rango poblacional (Barranquilla - Puerto Colombia)?",
        A: "1.210.168 habitantes", B: "1.100.000 habitantes", C: "950.000 habitantes", D: "1.275.854 habitantes",
        correcta: "A"
      },
      {
        titulo: "ESCALA MAQUETA",
        color: "#00bbdd",
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
        ctx.lineWidth = 3;
        ctx.strokeStyle = "#ffffff";
        ctx.stroke();

        ctx.save();
        ctx.translate(centroX, centroY);
        ctx.rotate(anguloInicio + anguloArc / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = "#ffffff";
        /* Al ser más grande la ruleta, la letra se ajusta a 9.5px para ser muy legible */
        ctx.font = "800 9.5px Poppins, sans-serif";
        ctx.fillText(sectores[i].titulo, radio - 14, 3.5);
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

st.components.v1.html(html_code, height=820, scrolling=True)
