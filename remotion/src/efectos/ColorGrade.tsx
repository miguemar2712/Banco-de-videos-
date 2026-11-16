import React from 'react';
import { AbsoluteFill, Easing, interpolate, useCurrentFrame } from 'remotion';
import { Clip } from '../componentes/Clip';
import { fuente } from '../fuentes';

export type ColorGradeProps = { inicio: number; antes: string; despues: string; silencio?: boolean };
export const colorGradeDefaults: ColorGradeProps = { inicio: 102.6, antes: 'ANTES', despues: 'DESPUÉS' };

// Plano (tipo LOG): poco contraste, poca saturación, negros levantados
const PLANO: React.CSSProperties = { filter: 'contrast(0.74) saturate(0.6) brightness(1.06)' };
// Gradado: más contraste, altas cálidas, sombras un poco teal, viñeta. Piel natural (nada naranja).
const Gradado: React.FC<{ inicio: number; silencio?: boolean }> = ({ inicio, silencio }) => (
  <AbsoluteFill>
    <Clip inicio={inicio} silencio={silencio} style={{ filter: 'contrast(1.12) saturate(1.08) brightness(0.98)' }} />
    {/* sombras teal: tinte que solo pesa en lo oscuro */}
    <AbsoluteFill style={{ background: 'rgba(0,92,104,0.16)', mixBlendMode: 'soft-light' }} />
    {/* altas cálidas suaves */}
    <AbsoluteFill style={{ background: 'radial-gradient(80% 55% at 55% 30%, rgba(255,196,140,0.22), transparent 70%)', mixBlendMode: 'soft-light' }} />
    {/* viñeta */}
    <AbsoluteFill style={{ background: 'radial-gradient(120% 85% at 50% 45%, transparent 55%, rgba(0,0,0,0.45) 100%)' }} />
  </AbsoluteFill>
);

const Pill: React.FC<{ texto: string; x: number; op: number }> = ({ texto, x, op }) => (
  <div style={{ position: 'absolute', top: 340, left: x, transform: 'translateX(-50%)', opacity: op, background: 'rgba(10,10,12,0.72)', borderRadius: 999,
    padding: '12px 26px', fontFamily: fuente.cuerpo, fontWeight: 700, fontSize: 26, letterSpacing: 6, color: '#fff', whiteSpace: 'nowrap' }}>{texto}</div>
);

export const ColorGrade: React.FC<ColorGradeProps> = (p) => {
  const f = useCurrentFrame();
  const w = interpolate(f, [25, 45], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: Easing.inOut(Easing.cubic) });
  const x = w * 1080;
  const limita = (v: number) => Math.max(200, Math.min(880, v)); // píldoras dentro de x 120–960
  const derecha = limita((x + 1080) / 2), izquierda = limita(x / 2);
  return (
    <AbsoluteFill>
      <Clip inicio={p.inicio} silencio={p.silencio} style={PLANO} />
      <AbsoluteFill style={{ clipPath: `inset(0 ${(1 - w) * 100}% 0 0)` }}><Gradado inicio={p.inicio} silencio /></AbsoluteFill>
      {w > 0 && w < 1 && (
        <div style={{ position: 'absolute', top: 0, bottom: 0, left: x - 2, width: 4, background: '#fff',
          boxShadow: '0 0 18px 6px rgba(255,255,255,.75), 0 0 60px 20px rgba(255,236,210,.35)' }} />
      )}
      <Pill texto={p.antes} x={f < 25 ? 540 : derecha} op={1 - w} />
      <Pill texto={p.despues} x={w >= 1 ? 540 : izquierda} op={interpolate(w, [0, 0.15], [0, 1], { extrapolateRight: 'clamp' })} />
    </AbsoluteFill>
  );
};
