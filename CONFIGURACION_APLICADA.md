# Configuración Ollama Aplicada ✓

## Hardware Detectado
- **CPU**: Intel i5-9500T (6 cores @ 2.2GHz)
- **GPU**: Intel UHD 630 (integrada, NO acelera LLMs)
- **RAM**: 31GB disponible
- **Modo**: CPU-only (correcto para este hardware)

## Optimizaciones Aplicadas

### 1. Variables Ollama ✓
```
OLLAMA_NUM_THREADS=6      # Usa los 6 cores
OLLAMA_NUM_PARALLEL=2     # Máx 2 requests simultáneos
OLLAMA_MAX_LOADED_MODELS=1 # Solo 1 modelo en RAM
```

Archivo: `/etc/systemd/system/ollama.service.d/override.conf`

### 2. CPU Governor ✓
```
Antes: powersave
Ahora: performance
```

**Nota**: Cambio temporal (se resetea al reiniciar). Para hacer permanente:

```bash
sudo apt install cpufrequtils
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl enable cpufrequtils
```

### 3. Modelo Optimizado ✓
```
qwen2.5:3b
- 3B parámetros
- ~2GB RAM
- Excelente español
- Rápido en CPU
```

## Rendimiento Actual

**Test**: "Hola, responde en una frase corta."
- **Tiempo**: 10.9 segundos
- **Velocidad**: ~1-2 tokens/segundo (normal para CPU)

**Esperado para extracción de PDFs**:
- Página simple: 15-30 segundos
- Página compleja: 30-60 segundos

## Comandos Útiles

```bash
# Ver configuración Ollama
sudo systemctl show ollama | grep Environment

# Ver logs en tiempo real
sudo journalctl -u ollama -f

# Monitorear uso CPU/RAM
htop

# Test velocidad
time ollama run qwen2.5:3b "Test rápido"
```

## Limitaciones

**NO puedes usar Intel UHD 630** porque:
1. Ollama no soporta aceleración Intel GPU en Linux
2. GPU integrada no tiene suficiente VRAM
3. oneAPI/OpenVINO son complejos y dan poco beneficio

**Única forma de acelerar**: Comprar GPU dedicada (NVIDIA RTX 3060+ o AMD RX 6700+)

## Próximos Pasos

1. ✓ Ollama optimizado
2. ✓ Modelo qwen2.5:3b instalado
3. → Instalar dependencias Python: `uv sync`
4. → Probar pipeline: `uv run python -m pipeline.run`
5. → Lanzar dashboard: `uv run shiny run --port 8086 app/app.py`
