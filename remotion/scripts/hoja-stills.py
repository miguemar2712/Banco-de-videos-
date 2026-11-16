# Junta stills en una hoja con las líneas de zona segura (x=120 y x=960) para revisarlos rápido.
import cv2, numpy as np, sys
salida, archivos = sys.argv[1], sys.argv[2:]
fr = []
for a in archivos:
    im = cv2.imread(a)
    if im is None: continue
    for x in (120, 960): cv2.line(im, (x, 0), (x, 1920), (60, 60, 255), 3)
    im = cv2.resize(im, (270, 480)); cv2.putText(im, a.split('/')[-1].replace('.png',''), (6, 18), 0, .45, (0,255,255), 1)
    fr.append(im)
cv2.imwrite(salida, np.hstack(fr), [cv2.IMWRITE_JPEG_QUALITY, 88])
