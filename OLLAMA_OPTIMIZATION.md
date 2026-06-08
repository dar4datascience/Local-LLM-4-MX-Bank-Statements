# Optimización Ollama para CPU (Linux Mint)

## Tu Hardware
- **CPU**: Intel i5-9500T (6 cores @ 2.2GHz)
- **GPU**: Intel UHD 630 (integrada, NO acelera LLMs)
- **RAM**: 31GB

## Estado Actual
✓ Ollama instalado correctamente
✓ Corriendo en modo CPU (esperado, no hay GPU dedicada)
✓ Modelo qwen2.5:3b descargado (~2GB)

## Optimizaciones CPU

### 1. Variables de Entorno Ollama

Crea archivo de configuración:

```bash
sudo mkdir -p /etc/systemd/system/ollama.service.d
sudo nano /etc/systemd/system/ollama.service.d/override.conf
```

Agrega:

```ini
[Service]
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_THREADS=6"
```

Reinicia servicio:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

**Explicación:**
- `OLLAMA_NUM_PARALLEL=2`: Máximo 2 requests simultáneos
- `OLLAMA_MAX_LOADED_MODELS=1`: Solo 1 modelo en RAM
- `OLLAMA_NUM_THREADS=6`: Usa los 6 cores del CPU

### 2. Modelo Correcto (Ya Configurado)

✓ **qwen2.5:3b** — Óptimo para tu CPU
- 3B parámetros
- ~2GB RAM
- Rápido en CPU
- Excelente español

**NO uses modelos más grandes** (7B+) — serán muy lentos en CPU.

### 3. Governor CPU (Performance Mode)

Verifica governor actual:

```bash
cat /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

Si dice "powersave", cambia a "performance":

```bash
# Temporal (hasta reinicio)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor

# Permanente
sudo apt install cpufrequtils
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl restart cpufrequtils
```

### 4. Monitoreo

Verifica uso durante inferencia:

```bash
# Terminal 1: corre modelo
ollama run qwen2.5:3b "Hola, ¿cómo estás?"

# Terminal 2: monitorea
htop  # presiona F5 para árbol de procesos
```

Deberías ver:
- 6 threads de ollama activos
- ~2GB RAM usada
- CPU al 100% durante generación

### 5. Alternativa: Quantización Menor

Si qwen2.5:3b es lento, prueba versión más cuantizada:

```bash
# Q4_0 = más rápido, menos preciso
ollama pull qwen2.5:3b-q4_0

# Q2_K = muy rápido, menor calidad
ollama pull qwen2.5:3b-q2_k
```

Actualiza código para usar `model="qwen2.5:3b-q4_0"`.

## Limitaciones Hardware

**Intel UHD 630 NO se puede usar** para acelerar LLMs porque:
1. No tiene suficiente VRAM dedicada
2. Ollama no soporta aceleración Intel GPU en Linux
3. oneAPI/OpenVINO requieren configuración compleja y dan poco beneficio

**Soluciones:**
- ✓ Mantener CPU mode (funciona bien con qwen2.5:3b)
- ✗ Comprar GPU dedicada (NVIDIA RTX 3060+ o AMD RX 6700+)
- ✗ Usar servicio cloud (Groq, Together.ai)

## Velocidad Esperada

Con i5-9500T + qwen2.5:3b:
- **Primera respuesta**: 2-5 segundos
- **Tokens/segundo**: 8-15 tok/s
- **Extracción PDF**: 10-30 segundos por página

Esto es **normal para CPU**. Si necesitas más velocidad, única opción es GPU dedicada.

## Verificar Configuración

```bash
# Ver variables Ollama
sudo systemctl show ollama | grep Environment

# Ver logs
sudo journalctl -u ollama -f

# Test rápido
time ollama run qwen2.5:3b "Hola"
```
