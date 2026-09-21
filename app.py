import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Juego Interactivo - Atlántico", page_icon="🎡", layout="centered")

# Código HTML, CSS y JavaScript todo en uno
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
      background: url('fondo.png?v=2') no-repeat center center fixed;
      background-size: cover;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 20px;
      color: #f8fafc;
    }
    .card {
      background: rgba(15, 23, 42, 0.88);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 24px;
      padding: 30px;
      max-width: 550px;
      width: 100%;
      text-align: center;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    }
    h1 { color: #38bdf8; font-size: 24px; margin-bottom: 20px; text-shadow: 0 2px 10px rgba(56, 189, 248, 0.3); }
    .ruleta-container { margin: 20px 0; }
    .ruleta {
      width: 110px; height: 110px; background: #1e293b;
      border: 4px solid #f59e0b; border-radius: 50%;
      display: flex; justify-content: center; align-items: center;
      font-size: 42px; font-weight: bold; color: #f59e0b;
      margin: 0 auto 15px; box-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
      transition: transform 0.1s linear;
    }
    button {
      background-color: #0284c7; color: #ffffff; border: none;
      padding: 12px 24px; font-size: 16px; font-weight: 600;
      border-radius: 12px; cursor: pointer; transition: all 0.2s ease;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3);
    }
    button:hover { background-color: #0369a1; transform: translateY(-2px); }
    .btn-ayuda { background-color: #d97706; margin-bottom: 12px; }
    .btn-tabla { background-color: #059669; margin-top: 15px; }
    h2 { color: #f1f5f9; font-size: 19px; margin: 15px 0; line-height: 1.4; }
    .pista {
      background: rgba(245, 158, 11, 0.15); border: 1px solid #f59e0b;
      color: #fef08a; padding: 12px; border-radius: 10px;
      font-size: 14px; margin-bottom: 15px; text-align: left;
    }
    .opciones { display: flex; flex-direction: column; gap: 10px; margin: 15px 0; }
    .opciones button {
      background-color: #1e293b; color: #e2e8f0; text-align: left;
      border: 1px solid rgba(255, 255, 255, 0.1); box-shadow: none;
    }
    .opciones button:hover { background-color: #334155; color: #ffffff; border-color: #38bdf8; }
    .resultado { font-size: 22px; font-weight: bold; margin: 15px 0; }
    .resultado.correcto { color: #4ade80; }
    .resultado.incorrecto { color: #f87171; }
    .modal {
      display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
      background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(5px);
      justify-content: center; align-items: center; z-index: 1000; padding: 20px;
    }
    .modal-content {
      background: #0f172a; border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 20px; padding: 25px; max-width: 500px; width: 100%;
      color: #f8fafc; position: relative;
    }
    .close-btn { position: absolute; top: 15px; right: 20px; font-size: 24px; color: #94a3b8; cursor: pointer; }
    table { width: 100%; border-collapse: collapse; margin: 15px 0; }
    th, td { border: 1px solid #334155; padding: 10px; text-align: center; font-size: 14px; }
    th { background-color: #1e293b; color: #38bdf8; }
    td { background-color: rgba(30, 41, 59, 0.5); }
    .oculto { display: none !important; }
  </style>
</head>
<body>

  <div class="card">
    <h1>🎡 Área Metropolitana del Atlántico</h1>
    
    <div class="ruleta-container">
      <div id="ruleta" class="ruleta">❓</div>
      <button id="btnGirar" onclick="girarRuleta()">¡Girar Ruleta!</button>
    </div>

    <div id="juego" class="oculto">
      <h2 id="pregunta">Pregunta...</h2>
      <button class="btn-ayuda" onclick="mostrarPista()">💡 Ver Pista</button>
      <div id="pista" class="pista oculto"></div>
      <div class="opciones">
        <button onclick="verificarRespuesta('A')" id="opcionA">A) ...</button>
        <button onclick="verificarRespuesta('B')" id="opcionB">B) ...</button>
        <button onclick="verificarRespuesta('C')" id="opcionC">C) ...</button>
        <button onclick="verificarRespuesta('D')" id="opcionD">D) ...</button>
      </div>
      <div id="resultado" class="resultado"></div>
      <button id="btnSiguiente" class="btn-siguiente oculto" onclick="siguientePregunta()">Siguiente Pregunta ➡️</button>
    </div>

    <button class="btn-tabla" onclick="abrirModal()">📊 Ver Tabla de Frecuencias</button>
  </div>

  <div id="modalEstadisticas" class="modal">
    <div class="modal-content">
      <span class="close-btn" onclick="cerrarModal()">&times;</span>
      <h2 style="color: #38bdf8; text-align: center;">Tabla de Frecuencia Poblacional</h2>
      <table>
        <thead>
          <tr><th>Municipio</th><th>Población (f<sub>i</sub>)</th><th>Porcentaje (%)</th></tr>
        </thead>
        <tbody>
          <tr><td>Barranquilla</td><td>1.275.854</td><td>81.5%</td></tr>
          <tr><td>Malambo</td><td>153.223</td><td>9.8%</td></tr>
          <tr><td>Galapa</td><td>70.042</td><td>4.5%</td></tr>
          <tr><td>Puerto Colombia</td><td>65.686</td><td>4.2%</td></tr>
        </tbody>
        <tfoot>
          <tr style="font-weight: bold; background-color: #1e293b;"><td>Total (N)</td><td>1.564.805</td><td>100.0%</td></tr>
        </tfoot>
      </table>
    </div>
  </div>

  <script>
    const preguntas = [
      { num: 1, pregunta: "¿Cuál es el segundo municipio con mayor población de esta muestra?", A: "Galapa", B: "Malambo", C: "Puerto Colombia", D: "Barranquilla", correcta: "B", pista: "Observa la altura de las barras: busca la que le sigue en altura a la más grande." },
      { num: 2, pregunta: "¿Qué municipio concentra la Moda (mayor población)?", A: "Malambo", B: "Galapa", C: "Barranquilla", D: "Puerto Colombia", correcta: "C", pista: "Es el núcleo principal de la zona metropolitana." },
      { num: 3, pregunta: "¿Cuál es el orden de mayor a menor población?", A: "Barranquilla > Galapa > Malambo > Puerto Colombia", B: "Barranquilla > Malambo > Galapa > Puerto Colombia", C: "Malambo > Barranquilla > Puerto Colombia > Galapa", D: "Puerto Colombia > Galapa > Malambo > Barranquilla", correcta: "B", pista: "1.275.854 > 153.223 > 70.042 > 65.686." },
      { num: 4, pregunta: "¿Cuál es la población total (N) sumando estos 4 municipios?", A: "2.100.000 hab", B: "1.275.854 hab", C: "1.564.805 hab", D: "980.500 hab", correcta: "C", pista: "Suma las 4 cifras." },
      { num: 5, pregunta: "¿Qué porcentaje del total representa aproximadamente Barranquilla?", A: "50,0%", B: "65,2%", C: "81,5%", D: "44,2%", correcta: "C", pista: "Divide 1.275.854 entre 1.564.805 y multiplícalo por 100." }
    ];

    let preguntaActual = {};

    function girarRuleta() {
      const ruleta = document.getElementById('ruleta');
      const indiceAleatorio = Math.floor(Math.random() * preguntas.length);
      preguntaActual = preguntas[indiceAleatorio];
      let giros = 0;
      const intervalo = setInterval(() => {
        ruleta.style.transform = `rotate(${giros * 90}deg)`;
        ruleta.textContent = Math.floor(Math.random() * 5) + 1;
        giros++;
        if (giros > 12) {
          clearInterval(intervalo);
          ruleta.style.transform = 'rotate(0deg)';
          ruleta.textContent = preguntaActual.num;
          cargarPregunta();
        }
      }, 80);
    }

    function cargarPregunta() {
      document.getElementById('juego').classList.remove('oculto');
      document.getElementById('pregunta').textContent = preguntaActual.pregunta;
      document.getElementById('opcionA').textContent = `A) ${preguntaActual.A}`;
      document.getElementById('opcionB').textContent = `B) ${preguntaActual.B}`;
      document.getElementById('opcionC').textContent = `C) ${preguntaActual.C}`;
      document.getElementById('opcionD').textContent = `D) ${preguntaActual.D}`;
      document.getElementById('pista').classList.add('oculto');
      document.getElementById('resultado').textContent = '';
      document.getElementById('btnSiguiente').classList.add('oculto');
    }

    function mostrarPista() {
      const pistaElem = document.getElementById('pista');
      pistaElem.textContent = preguntaActual.pista;
      pistaElem.classList.remove('oculto');
    }

    function verificarRespuesta(opcion) {
      const resultadoElem = document.getElementById('resultado');
      if (opcion === preguntaActual.correcta) {
        resultadoElem.textContent = "😊 ¡Correcto!";
        resultadoElem.className = "resultado correcto";
      } else {
        resultadoElem.textContent = "😢 ¡Incorrecto!";
        resultadoElem.className = "resultado incorrecto";
      }
      document.getElementById('btnSiguiente').classList.remove('oculto');
    }

    function siguientePregunta() {
      document.getElementById('juego').classList.add('oculto');
      document.getElementById('ruleta').textContent = "❓";
    }

    function abrirModal() { document.getElementById('modalEstadisticas').style.display = 'flex'; }
    function cerrarModal() { document.getElementById('modalEstadisticas').style.display = 'none'; }
  </script>
</body>
</html>
"""

# Renderiza la aplicación web dentro de Streamlit
st.components.v1.html(html_code, height=750, scrolling=True)
