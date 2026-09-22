import streamlit as st
import base64

st.set_page_config(
    page_title="Ruleta Zona Metropolitana del Atlántico", 
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
        background-size: cover !important;
        background-position: center center !important;
        background-repeat: no-repeat !important;
        background-attachment: fixed !important;
    }}

    /* Ajustes para eliminar espacios en blanco en móviles */
    .block-container {{
        padding: 0rem !important;
        max-width: 100% !important;
    }}
    
    /* Forzar al iframe a ocupar el alto útil completo */
    iframe {{
        border: none !important;
        width: 100% !important;
        height: 100vh !important;
    }}
    </style>
""", unsafe_allow_html=True)

html_code = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
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
      overflow-x: hidden;
      overflow-y: auto;
    }

    .card {
      background: rgba(255, 255, 255, 0.95);
      border: 2px solid rgba(255, 255, 255, 0.9);
      border-radius: 28px;
      padding: 20px 18px;
      max-width: 480px;
      width: 100%;
      text-align: center;
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
      margin: auto;
    }

    h1 {
      font-size: clamp(18px, 5vw, 22px);
      font-weight: 800;
      color: #0f172a;
      background: linear-gradient(135deg, #0284c7 0%, #e11d48 50%, #d97706 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }

    .ruleta-container {
      position: relative;
      width: min(320px, 80vw);
      height: min(320px, 80vw);
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
      transition: transform 0.05s ease-out;
    }

    #canvasRuleta {
      border-radius: 50%;
      border: 5px solid #ffffff;
      box-shadow: inset 0 0 10px rgba(0,0,0,0.3);
      width: 90% !important;
      height: 90% !important;
    }

    .ruleta-centro {
      position: absolute;
      width: 20%;
      height: 20%;
      background: radial-gradient(circle, #fef08a 0%, #f59e0b 100%);
      border: 3px solid #ffffff;
      border-radius: 50%;
      display: flex;
      justify-content: center;
      align-items: center;
      font-size: 20px;
      z-index: 20;
      box-shadow: 0 3px 12px rgba(0,0,0,0.25);
    }

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
      width: 100%;
      max-width: 280px;
    }

    .btn-girar:hover, .btn-girar:active {
      background: linear-gradient(135deg, #ffe066 0%, #f59e0b 50%, #d97706 100%);
      color: #0f172a;
      border-color: #fef08a;
      transform: translateY(-2px) scale(1.02);
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
      padding: 12px 14px;
      font-size: 13px;
      font-weight: 600;
      font-family: inherit;
      border-radius: 12px;
      cursor: pointer;
      text-align: left;
      transition: all 0.2s ease;
      min-height: 44px;
    }

    .opciones button:hover, .opciones button:active {
      background: #0284c7;
      color: #ffffff;
      border-color: #0284c7;
    }

    .overlay {
      position: fixed;
      top: 0; left: 0; width: 100vw; height: 100vh;
      display: none;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      z-index: 9999;
    }

    .overlay.acierto { background: rgba(0, 200, 83, 0.95) !important; }
    .overlay.error { background: rgba(213, 0, 0, 0.95) !important; }

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
    <h1>🎡 Zona Metropolitana del Atlántico</h1>
    
    <div class="ruleta-container">
      <div class="ruleta-outer-ring">
        <div class="flecha" id="flechaIndicador"></div>
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
      <button class="btn-continuar" onclick="cerrarOverlay('overlayAcierto')">Continuar</button>
    </div>
  </div>

  <div id="overlayError" class="overlay error">
    <div class="overlay-card">
      <div class="overlay-emoji">😓❌</div>
      <div class="overlay-titulo">¡INCORRECTO!<br>Inténtalo de Nuevo</div>
      <button class="btn-continuar" onclick="cerrarOverlay('overlayError')">Reintentar</button>
    </div>
  </div>

  <script>
    const sectores = [
      {
        titulo: "2do MÁS POBLADO",
        color: "#ff0033",
        pregunta: "1. ¿Cuál es el segundo municipio más poblado?",
        A: "Malambo", B: "Galapa", C: "Puerto Colombia", D: "Barranquilla",
        correcta: "A"
      },
      {
        titulo: "MAYOR POBLACIÓN",
        color: "#0066ff",
        pregunta: "2. ¿Qué municipio concentra la mayor población?",
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
        pregunta: "5. ¿Qué porcentaje de la población total representa Barranquilla?",
        A: "72,2%", B: "81,5%", C: "35,8%", D: "90,1%",
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
        ctx.font = "800 9.5px Poppins, sans-serif";
        ctx.fillText(sectores[i].titulo, radio - 14, 3.5);
        ctx.restore();
      }
    }

    dibujarRuleta();

    let sectorSeleccionado = {};
    let anguloActualRad = 0;
    let girando = false;

    // Motor de audio
    let audioCtx = null;

    function initAudio() {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      }
      if (audioCtx.state === 'suspended') {
        audioCtx.resume();
      }
    }

    function tocarClic() {
      if (!audioCtx) return;

      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'triangle';
      osc.frequency.setValueAtTime(600, audioCtx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(40, audioCtx.currentTime + 0.03);

      gain.gain.setValueAtTime(0.8, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.03);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start();
      osc.stop(audioCtx.currentTime + 0.03);

      const flecha = document.getElementById('flechaIndicador');
      flecha.style.transform = 'translateX(-50%) scale(1.25)';
      setTimeout(() => {
        flecha.style.transform = 'translateX(-50%) scale(1)';
      }, 40);
    }

    function tocarCampanaFinal() {
      if (!audioCtx) return;
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(880, audioCtx.currentTime);
      gain.gain.setValueAtTime(0.5, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.5);

      osc.connect(gain);
      gain.connect(audioCtx.destination);

      osc.start();
      osc.stop(audioCtx.currentTime + 0.5);
    }

    function reproducirSonidoResultados(tipo) {
      initAudio();
      
      if (tipo === 'acierto') {
        const notas = [523.25, 659.25, 783.99, 1046.50];
        notas.forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.value = freq;
          gain.gain.setValueAtTime(0.3, audioCtx.currentTime + idx * 0.09);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + idx * 0.09 + 0.35);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + idx * 0.09);
          osc.stop(audioCtx.currentTime + idx * 0.09 + 0.35);
        });
      } else {
        const notasError = [220, 155];
        notasError.forEach((freq, idx) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.value = freq;
          
          gain.gain.setValueAtTime(0.55, audioCtx.currentTime + idx * 0.28);
          gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + idx * 0.28 + 0.38);
          
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(audioCtx.currentTime + idx * 0.28);
          osc.stop(audioCtx.currentTime + idx * 0.28 + 0.38);
        });
      }
    }

    function girarRuleta() {
      if (girando) return;
      initAudio();
      
      girando = true;
      document.getElementById('juego').classList.add('oculto');
      document.getElementById('btnGirar').disabled = true;

      const indiceAleatorio = Math.floor(Math.random() * numSectores);
      sectorSeleccionado = sectores[indiceAleatorio];

      const anguloSectorDeg = 360 / numSectores;
      const anguloMetaDeg = 270 - (indiceAleatorio * anguloSectorDeg) - (anguloSectorDeg / 2);
      const girosCompletos = (Math.floor(Math.random() * 4) + 5) * 360;
      
      const anguloFinalDeg = girosCompletos + anguloMetaDeg;
      const anguloFinalRad = (anguloFinalDeg * Math.PI) / 180;

      const duracionMs = 4200;
      const inicioTiempo = performance.now();
      const anguloInicialRad = anguloActualRad;
      const deltaAnguloRad = anguloFinalRad - (anguloInicialRad % (2 * Math.PI));

      let ultimoSectorIndex = -1;

      function animar(tiempoActual) {
        const transcurrido = tiempoActual - inicioTiempo;
        let progreso = transcurrido / duracionMs;
        if (progreso > 1) progreso = 1;

        const factorCurva = 1 - Math.pow(1 - progreso, 3);
        anguloActualRad = anguloInicialRad + deltaAnguloRad * factorCurva;

        canvas.style.transform = `rotate(${anguloActualRad}rad)`;

        const anguloNormalizado = (3 * Math.PI / 2 - anguloActualRad) % (2 * Math.PI);
        const anguloPositivo = anguloNormalizado < 0 ? anguloNormalizado + 2 * Math.PI : anguloNormalizado;
        const sectorActualIndex = Math.floor(anguloPositivo / anguloArc);

        if (sectorActualIndex !== ultimoSectorIndex) {
          tocarClic();
          ultimoSectorIndex = sectorActualIndex;
        }

        if (progreso < 1) {
          requestAnimationFrame(animar);
        } else {
          girando = false;
          document.getElementById('btnGirar').disabled = false;
          tocarCampanaFinal();
          mostrarPregunta();
        }
      }

      requestAnimationFrame(animar);
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
        reproducirSonidoResultados('acierto');
        confetti({ particleCount: 130, spread: 80, origin: { y: 0.6 } });
        document.getElementById('overlayAcierto').style.display = 'flex';
      } else {
        reproducirSonidoResultados('error');
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

# Se cambia scrolling a False y se le da alto dinámico de pantalla completa
st.components.v1.html(html_code, height=750, scrolling=False)
