#!/usr/bin/env python3
"""Borra letras blancas pegadas (y stickers en rectángulos fijos) de un video, rellenando con el fondo (inpaint de OpenCV).
uso: .venv/bin/python scripts/borrar-letras.py entrada salida.mp4 --zona x0,y0,x1,y1 [--caja x0,y0,x1,y1 ...] [--hasta 4.1]
  --zona: dónde están las letras (se borra solo lo blanco + su borde oscuro)   --caja: rectángulos a borrar completos (stickers)"""
import argparse, subprocess, cv2, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument('entrada'); ap.add_argument('salida')
ap.add_argument('--zona', required=True); ap.add_argument('--caja', action='append', default=[]); ap.add_argument('--hasta', type=float)
a = ap.parse_args()
cap = cv2.VideoCapture(a.entrada); fps = cap.get(cv2.CAP_PROP_FPS) or 30
W, H = int(cap.get(3)), int(cap.get(4))
zx0, zy0, zx1, zy1 = map(int, a.zona.split(','))
cajas = [tuple(map(int, c.split(','))) for c in a.caja]
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(fps), '-i', '-',
                      '-c:v', 'libx264', '-crf', '14', '-pix_fmt', 'yuv420p', a.salida], stdin=subprocess.PIPE)
k = 0
while True:
    ok, f = cap.read()
    if not ok or (a.hasta and k / fps >= a.hasta): break
    m = np.zeros((H, W), np.uint8)
    hsv = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)
    blanco = ((hsv[..., 2] > 200) & (hsv[..., 1] < 45)).astype(np.uint8) * 255
    m[zy0:zy1, zx0:zx1] = blanco[zy0:zy1, zx0:zx1]
    m = cv2.dilate(m, np.ones((15, 15), np.uint8))          # incluye el borde negro de las letras
    for x0, y0, x1, y1 in cajas: m[y0:y1, x0:x1] = 255
    out = cv2.inpaint(f, m, 9, cv2.INPAINT_TELEA)
    out = cv2.GaussianBlur(out, (0, 0), 1.2) * (m[..., None] / 255.) + out * (1 - m[..., None] / 255.)
    p.stdin.write(out.astype(np.uint8).tobytes()); k += 1
p.stdin.close(); p.wait(); print('✓', a.salida, k, 'cuadros')
