#!/usr/bin/env python3
"""Genera assets/textura-gastada.png (1080x1920, gris): manchitas blancas sobre negro = desgaste tipo tinta vieja."""
import os, numpy as np
from PIL import Image, ImageFilter
rng = np.random.default_rng(7)
W, H = 1080, 1920
ruido = Image.fromarray((rng.random((H // 2, W // 2)) * 255).astype("uint8")).resize((W, H), Image.BICUBIC)
ruido = ruido.filter(ImageFilter.GaussianBlur(1.3))
a = np.asarray(ruido).astype(float)
fino = rng.random((H, W))
m = ((a > 164) | (fino > .993)).astype('uint8') * 255            # manchas medianas + puntitos sueltos
img = Image.fromarray(m).filter(ImageFilter.GaussianBlur(.6))
img.save(os.path.join(os.path.dirname(__file__), '..', 'assets', 'textura-gastada.png'))
print('✓ assets/textura-gastada.png', round(m.mean() / 255 * 100, 1), '% cubierto')
