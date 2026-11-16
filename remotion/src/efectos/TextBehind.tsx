import React from 'react';
import { Easing, interpolate, useCurrentFrame } from 'remotion';
import { fitText } from '@remotion/layout-utils';
import { BehindMe } from '../componentes/BehindMe';
import { CUERPO, SEGURO_ANCHO } from '../constantes';
import { fuente } from '../fuentes';

export type TextBehindProps = { inicio: number; palabra: string; silencio?: boolean };
export const textBehindDefaults: TextBehindProps = { inicio: 20.0, palabra: 'VIRAL' };

export const TextBehind: React.FC<TextBehindProps> = (p) => {
  const f = useCurrentFrame();
  // ~330 px de alto; si no cabe en x 120–960 se encoge
  const ajuste = fitText({ text: p.palabra, withinWidth: SEGURO_ANCHO, fontFamily: fuente.condensada, fontWeight: '400', textTransform: 'uppercase' });
  const tam = Math.min(ajuste.fontSize, 400);
  const sube = interpolate(f, [0, 10], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const baja = interpolate(f, [75, 90], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic) });
  const lift = interpolate(f, [10, 75], [0, -20], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const y = sube * 160 + baja * 140 + lift;
  return (
    <BehindMe inicio={p.inicio} silencio={p.silencio}>
      {/* centrada detrás de la cabeza: la cabeza tapa parte de la palabra */}
      <div style={{ position: 'absolute', left: 120, width: SEGURO_ANCHO, top: CUERPO.cabezaCentro.y - tam * 0.62, textAlign: 'center',
        fontFamily: fuente.condensada, fontSize: tam, lineHeight: 1, color: '#fff', textTransform: 'uppercase', whiteSpace: 'nowrap',
        transform: `translateY(${y}px)`, opacity: (1 - sube) * (1 - baja), filter: `blur(${sube * 18 + baja * 10}px)`,
        textShadow: '0 10px 40px rgba(0,0,0,.25)' }}>{p.palabra}</div>
    </BehindMe>
  );
};
