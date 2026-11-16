#!/usr/bin/env python3
"""Transcribe tu video con Whisper con tiempos POR PALABRA.

Uso:
  python3 scripts/transcribir.py public/media/mi-video.mp4 proyectos/mi-reel/palabras.json [modelo]

Modelo por defecto: "small" (buen equilibrio). Usa "medium" para más precisión.
Funciona con faster-whisper (más rápido) o con openai-whisper, el que esté instalado.
"""
import json
import os
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]
    model_name = sys.argv[3] if len(sys.argv) > 3 else "small"
    words = []
    try:
        from faster_whisper import WhisperModel  # type: ignore
        model = WhisperModel(model_name, device="auto", compute_type="int8")
        segments, _ = model.transcribe(src, language="es", word_timestamps=True, vad_filter=True)
        for seg in segments:
            for w in seg.words or []:
                words.append({"text": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
    except ImportError:
        import whisper  # type: ignore
        model = whisper.load_model(model_name)
        res = model.transcribe(src, language="es", word_timestamps=True)
        for seg in res["segments"]:
            for w in seg.get("words", []):
                words.append({"text": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3)})

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"words": words, "text": " ".join(w["text"] for w in words)}, f, ensure_ascii=False, indent=1)
    print(f"✓ {len(words)} palabras → {out}")
    print(" ".join(w["text"] for w in words))


if __name__ == "__main__":
    main()
