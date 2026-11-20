Voz PROVISIONAL de IA (ella no mandó audio): Piper TTS, voz es_AR-daniela-high.
Dataset: OpenSLR 61 (https://www.openslr.org/61/), licencia CC BY-SA 4.0 → si se publica, dar crédito
(p. ej. en la descripción: "Voz: Piper es_AR-daniela, datos OpenSLR 61, CC BY-SA 4.0").
Regenerar: .venv/bin/pip install piper-tts; bajar es_AR-daniela-high.onnx(+.json) de huggingface.co/rhasspy/piper-voices
(es/es_AR/daniela/high) a voz/piper/; echo "<guion>" | .venv/bin/piper -m voz/piper/es_AR-daniela-high.onnx --length_scale 0.92 --sentence_silence 0.25 -f voz/x.wav
Números escritos en letras para que los lea bien. Si ella manda su voz o la de CapCut, reemplazar voz y palabras y re-sincronizar.
