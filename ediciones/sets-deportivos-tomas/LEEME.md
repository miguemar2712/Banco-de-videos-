# Sets deportivos · solo tomas (sin subtítulos)

Entradas (en este orden): videos/clip-b-limpio.mp4, videos/clip-a-1080.mp4, videos/broll/mk-18304.mp4 (billetes),
mk-39461.mp4 (puerto), mk-23327.mp4 (perchero), mk-31267.mp4 (carretilla con caja), mk-31346.mp4 (apilando cajas),
videos/voz-sets.m4a (voz). B-roll: Mixkit (licencia gratuita, uso comercial).

    ffmpeg -i ... (8 entradas) -filter_complex_script ediciones/sets-deportivos-tomas/montaje.fg \
      -map "[v]" -map "[a]" -t 19.09 -c:v libx264 -crf 16 -c:a aac -b:a 256k out/sets-deportivos-tomas.mp4

Único texto: "$15" (Archivo Black 300) + "dólares" (Playfair Display Italic 170) de 4,95 a 5,95 s, entrando de lados opuestos.
