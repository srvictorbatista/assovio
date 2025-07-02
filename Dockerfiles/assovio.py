import os
import uuid
import threading
import time
import base64
import requests
import tempfile
from flask import Flask, request, jsonify
from vosk import Model, KaldiRecognizer
import wave
import subprocess
import json
from werkzeug.exceptions import RequestEntityTooLarge
from concurrent.futures import ThreadPoolExecutor
from symspellpy.symspellpy import SymSpell, Verbosity

app = Flask(__name__)

# Limite de tamanho configurável
try:
    LIMIT_MB = int(os.getenv("INTERNAL_LIMIT", "5"))
except ValueError as e:
    raise ValueError("A variável INTERNAL_LIMIT deve ser um número inteiro.") from e

app.config['MAX_CONTENT_LENGTH'] = LIMIT_MB * 1024 * 1024

# Modelo Vosk
MODEL_NAME = os.getenv("MODEL_NAME", "vosk-model-small-pt-0.3")
MODEL_PATH = f"modelos/{MODEL_NAME}"
INTERNAL_PORT = os.getenv("INTERNAL_PORT", "5000")

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("Modelo Vosk não encontrado em " + MODEL_PATH)

model = Model(MODEL_PATH)
API_KEY = os.getenv("AUTHENTICATION_API_KEY")
MAX_WORKERS = int(os.getenv("WORKERS", "4"))
executor = ThreadPoolExecutor(max_workers=MAX_WORKERS)

# Dicionário de correção
DICIONARIO_DE_FREQUENCIA = os.getenv("DICIONARIO_DE_FREQUENCIA", "true").strip().lower()
USAR_DICIONARIO = DICIONARIO_DE_FREQUENCIA not in ["false", "0", "não", "nao", "nÃO", "naO", "n"]
sym_spell = None

def carregar_dicionario():
    global sym_spell
    if sym_spell is None:
        sym_spell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
        DICIONARIO_PATH = "dicionarios/pt-br.txt"
        if not os.path.exists(DICIONARIO_PATH):
            raise FileNotFoundError(f"Dicionário não encontrado em {DICIONARIO_PATH}")
        sym_spell.load_dictionary(DICIONARIO_PATH, term_index=0, count_index=1)

def corrigir_texto(texto):
    if not USAR_DICIONARIO:
        return texto
    carregar_dicionario()
    resultado = sym_spell.lookup_compound(texto, max_edit_distance=2)
    return resultado[0].term if resultado else texto

def convert_to_wav(file_path):
    if file_path.lower().endswith(".wav"):
        try:
            with wave.open(file_path, "rb") as wf:
                if wf.getframerate() == 16000 and wf.getnchannels() == 1:
                    return file_path
        except:
            pass
    wav_path = f"/tmp/{uuid.uuid4()}.wav"
    command = [
        "ffmpeg", "-y", "-i", file_path,
        "-ar", "16000", "-ac", "1", "-f", "wav", wav_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return wav_path

def transcribe(wav_path):
    with wave.open(wav_path, "rb") as wf:
        rec = KaldiRecognizer(model, wf.getframerate())
        results = []
        while True:
            data = wf.readframes(4000)
            if not data:
                break
            if rec.AcceptWaveform(data):
                results.append(json.loads(rec.Result()).get("text", ""))
        results.append(json.loads(rec.FinalResult()).get("text", ""))
    texto_bruto = " ".join(results)
    return corrigir_texto(texto_bruto).strip()

def salvar_temp_file(suffix, data, binary=False):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='wb' if binary else 'w') as tmp:
        tmp.write(data if binary else data.encode())
        return tmp.name

def process_audio_file(filepath):
    wav_path = None
    try:
        wav_path = convert_to_wav(filepath)
        texto = transcribe(wav_path)
        return jsonify({"text": texto}), 200
    except subprocess.CalledProcessError:
        return jsonify({"error": "Erro ao converter áudio."}), 400
    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({"error": "Erro interno no servidor."}), 500
    finally:
        for path in [filepath, wav_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

@app.route('/escutar', methods=['POST'])
def escutar():
    if API_KEY and request.headers.get("apikey") != API_KEY:
        return jsonify({"error": "Não autorizado"}), 401

    try:
        if 'audio' in request.files:
            file = request.files['audio']
            temp = salvar_temp_file("_upload", file.read(), binary=True)
            return process_audio_file(temp)

        elif request.is_json and 'audioUrl' in request.json:
            url = request.json['audioUrl']
            r = requests.get(url, timeout=10)
            if r.status_code != 200:
                return jsonify({"error": "Erro ao baixar áudio da URL"}), 400
            temp = salvar_temp_file("_url", r.content, binary=True)
            return process_audio_file(temp)

        elif request.is_json and 'audioBase64' in request.json:
            base64_data = request.json['audioBase64']
            if base64_data.startswith("data:"):
                try:
                    base64_data = base64_data.split(",", 1)[1]
                except IndexError:
                    return jsonify({"error": "Base64 mal formatado"}), 400
            try:
                decoded = base64.b64decode(base64_data)
            except Exception:
                return jsonify({"error": "Base64 inválido"}), 400
            temp = salvar_temp_file("_b64", decoded, binary=True)
            return process_audio_file(temp)

        else:
            return jsonify({"error": "Nenhum áudio fornecido"}), 400

    except Exception as e:
        print(f"[ERRO] {e}")
        return jsonify({"error": "Erro no processamento da requisição"}), 500

@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(e):
    return jsonify({"error": f"Limite máximo excedido: {LIMIT_MB}MB"}), 413

# Handlers globais para garantir JSON em qualquer erro
@app.errorhandler(400)
def handle_400(e):
    return jsonify({"error": "Requisição inválida"}), 400

@app.errorhandler(401)
def handle_401(e):
    return jsonify({"error": "Não autorizado"}), 401

@app.errorhandler(403)
def handle_403(e):
    return jsonify({"error": "Proibido"}), 403

@app.errorhandler(404)
def handle_404(e):
    return jsonify({"error": "Rota não encontrada"}), 404

@app.errorhandler(405)
def handle_405(e):
    return jsonify({"error": "Método não permitido"}), 405

@app.errorhandler(500)
def handle_500(e):
    return jsonify({"error": "Erro interno no servidor"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print(f"[ERRO GENÉRICO] {e}")
    return jsonify({"error": "Erro inesperado no servidor"}), 500






# Mensagem de inicialização
def delayed_print():
    time.sleep(1)
    print("\033c", end="", flush=True)  # Limpa a tela
    print("\n" * 15, flush=True)

    print("   \033[1;37;5;24m\033[48;5;208m" + " " * 90 + "\033[0m", flush=True)
    print("   \033[1;37;5;24m\033[48;5;208m" + " " * 37 + "SETUP COMPLETO!" + " " * 38 + "\033[0m", flush=True)
    print("   \033[1;37;5;24m\033[48;5;208m" + " " * 90 + "\033[0m", flush=True)
    print("", flush=True)

    print(f"    DIC. de frequancia: {DICIONARIO_DE_FREQUENCIA}*\n", flush=True)
    print(f"   Você pode testar o serviço com o comando CURL (substitua 'seuarquivo.wav' pelo caminho do seu áudio)", flush=True)

    if API_KEY:
        print("   Como está protegida por uma API Key, envie a autenticação no header 'apikey' desta forma: \n", flush=True)
        print(f"   \033[44;37m curl -X POST -H \"apikey: {API_KEY}\" -F \"audio=@seuarquivo.wav\" http://localhost:{INTERNAL_PORT}/escutar \033[0m\n", flush=True)
    else:
        print("   Realize uma requisição simples da seguinte forma: \n", flush=True)
        print(f"   \033[44;37m curl -X POST -F \"audio=@seuarquivo.wav\" http://localhost:{INTERNAL_PORT}/escutar \033[0m\n", flush=True)

    # Insomnia / Postman
    print("   [Insomnia / Postman]", flush=True)
    print("   - Método: POST", flush=True)
    print(f"   - URL: http://localhost:{INTERNAL_PORT}/escutar", flush=True)
    print("   - Body: form-data", flush=True)
    print("     - Chave: `audio`", flush=True)
    print("     - Tipo: Arquivo", flush=True)
    print("     - Valor: seuarquivo.wav", flush=True)
    if API_KEY:
        print(f"   - Header: `apikey: {API_KEY}`", flush=True)
    print("\n", flush=True)

    print("   Exemplos de requisições em algumas linguagens:\n", flush=True)

    if API_KEY:
        apikey_line = f'"apikey": "{API_KEY}"'
        header_line = f'headers={{"apikey": "{API_KEY}"}}'
    else:
        apikey_line = ""
        header_line = "headers={}"

    # PHP
    print("   [PHP - CURL]", flush=True)
    print("   <?php", flush=True)
    print("   $ch = curl_init();", flush=True)
    print(f"   curl_setopt($ch, CURLOPT_URL, 'http://localhost:{INTERNAL_PORT}/escutar');", flush=True)
    if API_KEY:
        print(f"   curl_setopt($ch, CURLOPT_HTTPHEADER, ['apikey: {API_KEY}']);", flush=True)
    print("   curl_setopt($ch, CURLOPT_POST, 1);", flush=True)
    print("   curl_setopt($ch, CURLOPT_POSTFIELDS, [\"audio\" => new CURLFile('seuarquivo.wav')]);", flush=True)
    print("   curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);", flush=True)
    print("   $response = curl_exec($ch);", flush=True)
    print("   curl_close($ch);", flush=True)
    print("   echo $response;", flush=True)
    print("   // ... ?>\n", flush=True)

    # JavaScript (fetch com FormData)
    print("   [JavaScript - fetch (Node/Browser)]", flush=True)
    print("   <SCRIPT>", flush=True)
    print("   const formData = new FormData();", flush=True)
    print("   formData.append('audio', fs.createReadStream('seuarquivo.wav'));", flush=True)
    print(f"   fetch('http://localhost:{INTERNAL_PORT}/escutar', {{", flush=True)
    if API_KEY:
        print(f"     headers: {{ 'apikey': '{API_KEY}' }},", flush=True)
    print("     method: 'POST',", flush=True)
    print("     body: formData", flush=True)
    print("   }}).then(res => res.text()).then(console.log);", flush=True)
    print("   // ... </SCRIPT>\n", flush=True)

    # Python
    print("   [Python - requests]", flush=True)
    print("   # python.py", flush=True)
    print("   import requests", flush=True)
    print(f"   files = {{'audio': open('seuarquivo.wav', 'rb')}}", flush=True)
    print(f"   {header_line}", flush=True)
    print(f"   r = requests.post('http://localhost:{INTERNAL_PORT}/escutar', files=files, {header_line})", flush=True)
    print("   print(r.text)", flush=True)
    print("   # ...\n", flush=True)

    # Node.js com Axios
    print("   [Node.js - Axios]", flush=True)
    print("   Axios.js", flush=True)
    print("   const axios = require('axios');", flush=True)
    print("   const fs = require('fs');", flush=True)
    print("   const FormData = require('form-data');", flush=True)
    print("   const form = new FormData();", flush=True)
    print("   form.append('audio', fs.createReadStream('seuarquivo.wav'));", flush=True)
    print("   axios.post(`http://localhost:{INTERNAL_PORT}/escutar`, form, {", flush=True)
    if API_KEY:
        print(f"     headers: {{ ...form.getHeaders(), apikey: '{API_KEY}' }}", flush=True)
    else:
        print("     headers: form.getHeaders()", flush=True)
    print("   }).then(res => console.log(res.data));", flush=True)
    print("   // ...\n", flush=True)

    NOTA = "A primeira requisição irá despertar o modelo LLM, o que pode levar até 30 segundos (apenas na primeira requisição)."
    print(f"\n\n   \033[1;97m\033[48;5;166m NOTA: {NOTA} \033[0m", flush=True)
    print(f"  \033[1;97m Lembre-se que o limite máximo para envios é de {LIMIT_MB}MB. \033[0m", flush=True)
    print("\n" * 5, flush=True)


if os.getenv("RUN_MAIN") != "true":
    threading.Thread(target=delayed_print, daemon=True).start()
