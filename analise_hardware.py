import psutil
import subprocess
import gradio as gr
from datetime import datetime
import os
import webbrowser

def get_temperatura():
    try:
        output = subprocess.check_output(["sensors"]).decode()
        return output.strip()
    except Exception as e:
        return f"Erro ao ler sensores: {e}"

def gerar_recomendacoes(cpu, ram, disco):
    rec = []
    if cpu > 85:
        rec.append("🔺 Alto uso de CPU.")
    else:
        rec.append("✅ CPU OK.")
    if ram > 85:
        rec.append("🔺 RAM alta. Feche apps pesados.")
    else:
        rec.append("✅ RAM OK.")
    if disco > 85:
        rec.append("🔺 Disco quase cheio.")
    else:
        rec.append("✅ Disco OK.")
    return rec

def salvar_html(cpu, ram, disco, temp, recomendacoes):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html_path = os.path.expanduser("~/relatorio_hw.html")
    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Relatório de Hardware</title>
  <style>
    body {{
      background-color: #1e1e1e;
      color: #00ffcc;
      font-family: monospace;
      padding: 20px;
    }}
    h1 {{ color: #00ffff; }}
    canvas {{ margin: 20px 0; }}
    pre {{
      background: #2e2e2e;
      padding: 10px;
      border-radius: 5px;
    }}
  </style>
</head>
<body>
  <h1>🧠 Relatório de Hardware - {now}</h1>
  <canvas id="cpuChart"></canvas>
  <canvas id="ramChart"></canvas>
  <canvas id="diskChart"></canvas>
  <h2>🌡️ Temperaturas</h2>
  <pre>{temp}</pre>
  <h2>📌 Recomendações</h2>
  <ul>
    {''.join(f'<li>{r}</li>' for r in recomendacoes)}
  </ul>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    const createChart = (id, label, value) => {{
      new Chart(document.getElementById(id), {{
        type: 'doughnut',
        data: {{
          labels: [label, 'Livre'],
          datasets: [{{
            data: [value, 100 - value],
            backgroundColor: ['#00ffcc', '#444'],
            borderWidth: 1
          }}]
        }},
        options: {{
          plugins: {{
            legend: {{
              labels: {{ color: '#fff' }}
            }}
          }}
        }}
      }});
    }};
    createChart('cpuChart', 'CPU {cpu}%', {cpu});
    createChart('ramChart', 'RAM {ram}%', {ram});
    createChart('diskChart', 'Disco {disco}%', {disco});
  </script>
</body>
</html>"""
    with open(html_path, "w") as f:
        f.write(html)
    webbrowser.open(f"file://{html_path}")

def analisar():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent
    temp = get_temperatura()
    recomendacoes = gerar_recomendacoes(cpu, ram, disco)

    salvar_html(cpu, ram, disco, temp, recomendacoes)

    resumo = f"""
CPU: {cpu}%
RAM: {ram}%
Disco: {disco}%

Temperaturas:
{temp}

Recomendações:
{chr(10).join(recomendacoes)}
"""
    return resumo

iface = gr.Interface(fn=analisar, inputs=[], outputs="text",
    title="Análise de Hardware Épica 🧠🔥",
    description="Coleta dados do sistema, gera relatório com gráficos e abre em HTML.")

if __name__ == "__main__":
    iface.launch(share=False)

