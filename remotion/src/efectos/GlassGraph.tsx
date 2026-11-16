import React, { useMemo } from 'react';
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from 'remotion';
import { getLength, getPointAtLength } from '@remotion/paths';
import { Clip } from '../componentes/Clip';
import { VidrioClaro } from '../componentes/Glass';
import { NARANJA, fmtNumero } from '../constantes';
import { fuente } from '../fuentes';

export type GlassGraphProps = { inicio: number; titulo: string; desde: number; hasta: number; silencio?: boolean };
export const glassGraphDefaults: GlassGraphProps = { inicio: 39.8, titulo: 'Vistas este mes', desde: 1204, hasta: 412000 };

const W = 760, H = 520, GX = 40, GY = 250, GW = 680, GH = 220;
// Datos inventados de forma "creíble": sube en general con un par de bajadas
const PUNTOS = [0.02, 0.06, 0.05, 0.12, 0.18, 0.15, 0.27, 0.35, 0.31, 0.46, 0.58, 0.54, 0.7, 0.83, 1];

export const GlassGraph: React.FC<GlassGraphProps> = (p) => {
  const f = useCurrentFrame();
  const entrada = interpolate(f, [0, 8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const salida = interpolate(f, [80, 90], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.in(Easing.cubic) });
  const prog = interpolate(f, [8, 60], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.out(Easing.cubic) });
  const numero = p.desde + (p.hasta - p.desde) * prog;

  const { linea, area, largo } = useMemo(() => {
    const pts = PUNTOS.map((v, i) => [GX + (i / (PUNTOS.length - 1)) * GW, GY + GH - v * GH]);
    let d = `M ${pts[0][0]} ${pts[0][1]}`;
    for (let i = 1; i < pts.length; i++) {
      const [x0, y0] = pts[i - 1], [x1, y1] = pts[i], cx = (x0 + x1) / 2;
      d += ` C ${cx} ${y0}, ${cx} ${y1}, ${x1} ${y1}`;
    }
    return { linea: d, area: `${d} L ${GX + GW} ${GY + GH} L ${GX} ${GY + GH} Z`, largo: getLength(d) };
  }, []);
  const punta = getPointAtLength(linea, Math.max(0.01, largo * prog)) ?? { x: GX, y: GY + GH };
  const pulso = interpolate(f, [60, 66, 74], [1, 1.9, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const halo = interpolate(f, [60, 74], [0.9, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill>
      <Clip inicio={p.inicio} silencio={p.silencio} />
      {/* a la altura del pecho, debajo de la cara (barbilla ≈ y 720) */}
      <VidrioClaro style={{ position: 'absolute', left: 160, top: 1010, width: W, height: H,
        opacity: entrada * (1 - salida), transform: `translateY(${(1 - entrada) * 60 + salida * 30}px)` }}>
        <div style={{ position: 'absolute', left: 40, top: 36, fontFamily: fuente.cuerpo, fontWeight: 600, fontSize: 30, color: 'rgba(255,255,255,0.65)' }}>{p.titulo}</div>
        <div style={{ position: 'absolute', left: 38, top: 78, fontFamily: fuente.titulo, fontWeight: 800, fontSize: 120, letterSpacing: -4, color: '#fff', fontVariantNumeric: 'tabular-nums' }}>{fmtNumero(numero)}</div>
        <svg width={W} height={H} style={{ position: 'absolute', left: 0, top: 0, overflow: 'visible' }}>
          <defs>
            <linearGradient id="gg-relleno" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0" stopColor={NARANJA} stopOpacity={0.45} />
              <stop offset="1" stopColor={NARANJA} stopOpacity={0} />
            </linearGradient>
            <clipPath id="gg-corte"><rect x={GX - 10} y={0} width={(GW + 10) * prog + 10} height={H} /></clipPath>
            <filter id="gg-brillo" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" /></filter>
          </defs>
          <g clipPath="url(#gg-corte)">
            <path d={area} fill="url(#gg-relleno)" />
            <path d={linea} fill="none" stroke={NARANJA} strokeWidth={10} opacity={0.55} filter="url(#gg-brillo)" />
            <path d={linea} fill="none" stroke={NARANJA} strokeWidth={6} strokeLinecap="round" />
          </g>
          <circle cx={punta.x} cy={punta.y} r={22 * pulso} fill={NARANJA} opacity={halo * 0.5} />
          <circle cx={punta.x} cy={punta.y} r={11} fill="#fff" stroke={NARANJA} strokeWidth={5} style={{ filter: `drop-shadow(0 0 10px ${NARANJA})` }} />
        </svg>
      </VidrioClaro>
    </AbsoluteFill>
  );
};
