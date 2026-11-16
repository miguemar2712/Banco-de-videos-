# Editor Remotion · Level Up (opcional)

8 efectos hechos con Remotion sobre TU video: TextBehind (palabra detrás de ti), OverTheShoulder (la cámara va a tus
hombros y salen tarjetas), GlassGraph (gráfica de vidrio), FreezeFrame (congelado con tu nombre), TierList, ColorGrade,
ChatRender (Claude "renderiza" tu video) y FullReel (todos juntos).

## Preparar (Claude lo hace por ti)
1. `npm install`
2. Tu video vertical a 30 fps como `public/talking.mp4`:
   `ffmpeg -i tu-video.mov -vf "scale=1080:1920,fps=30" -c:v libx264 -crf 14 -c:a aac public/talking.mp4`
3. Tu silueta:
   - **Mac:** compila `swiftc scripts/mascara.swift -o scripts/mascara`. Luego corre `scripts/mascara public/talking.mp4 1080 1920 | ffmpeg -f rawvideo -pix_fmt gray -s 1080x1920 -r 30 -i - -c:v libx264 -crf 12 public/mask/mask.mp4`.
   - **Windows:** genera la máscara con MediaPipe. Sirve la de `../scripts/editar.py` (función `recorte`).
4. Tú recortado con transparencia:
   `ffmpeg -i public/talking.mp4 -i public/mask/mask.mp4 -filter_complex "[1]format=gray[m];[0][m]alphamerge" -c:v libvpx-vp9 -pix_fmt yuva420p -an public/persona.webm`
5. Pídele a Claude que mida dónde están tu cabeza y tus hombros en la máscara. Debe actualizar `src/constantes.ts` y los segundos de inicio de cada efecto (`src/efectos/*.tsx`).

## Usar
- `npm run studio` → vista previa en el navegador.
- `sh scripts/render-todo.sh` → renderiza cada efecto en `out/`.

Por **José Sibú · Level Up**.
