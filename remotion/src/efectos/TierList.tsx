import React from 'react';
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, getStaticFiles } from 'remotion';
import { Clip } from '../componentes/Clip';
import { fuente } from '../fuentes';

export type TierListProps = { inicio: number; tema: string; filas: Record<'S' | 'A' | 'B' | 'C' | 'D', string[]>; silencio?: boolean };
export const tierListDefaults: TierListProps = {
  inicio: 71.5,
  tema: 'herramientas de IA',
  filas: { S: ['Claude'], A: ['ChatGPT', 'Gemini', 'Perplexity'], B: ['Midjourney', 'CapCut'], C: ['Notion AI', 'Canva'], D: ['Copilot'] },
};

const COLOR: Record<string, string> = { S: '#E5484D', A: '#F2883B', B: '#F2C94C', C: '#46A758', D: '#3E8DE0' };
const ORDEN = ['S', 'A', 'B', 'C', 'D'] as const;

const logoDe = (nombre: string) => {
  const base = nombre.toLowerCase().replace(/\s+/g, '-');
  return getStaticFiles().find((f) => f.name.startsWith('logos/') && f.name.replace(/^logos\//, '').replace(/\.(png|jpe?g|svg|webp)$/i, '').toLowerCase() === base);
};

export const TierList: React.FC<TierListProps> = (p) => {
  const f = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const entrada = interpolate(f, [0, 8], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const salida = interpolate(f, [durationInFrames - 10, durationInFrames], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  // orden de caída: fila por fila, un ítem cada 4 cuadros desde el cuadro 10
  const items: { fila: string; nombre: string; idx: number }[] = [];
  ORDEN.forEach((fila) => (p.filas[fila] || []).forEach((nombre) => items.push({ fila, nombre, idx: items.length })));
  const ultimo = 10 + (items.length - 1) * 4 + 6;
  const listo = interpolate(f, [ultimo, ultimo + 5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  const giro = f * 14;
  return (
    <AbsoluteFill>
      <Clip inicio={p.inicio} silencio={p.silencio} />
      <div style={{ position: 'absolute', left: 120, width: 840, top: 990, borderRadius: 36, background: 'rgba(14,14,18,0.86)', padding: 26,
        boxShadow: '0 30px 70px rgba(0,0,0,.5)', opacity: entrada * (1 - salida), transform: `translateY(${(1 - entrada) * 60}px)` }}>
        {/* píldora de estado: "Clasificando…" ⇄ "Clasificado ✓" con fundido cruzado */}
        <div style={{ position: 'relative', height: 56, marginBottom: 18 }}>
          {[0, 1].map((cual) => (
            <div key={cual} style={{ position: 'absolute', left: 0, top: 0, display: 'inline-flex', alignItems: 'center', gap: 14, height: 56, padding: '0 24px', borderRadius: 999,
              background: cual ? 'rgba(70,167,88,.18)' : 'rgba(255,255,255,.08)', border: `1.5px solid ${cual ? 'rgba(70,167,88,.6)' : 'rgba(255,255,255,.15)'}`,
              opacity: cual ? listo : 1 - listo, fontFamily: fuente.cuerpo, fontWeight: 600, fontSize: 26, color: '#fff' }}>
              {cual ? <span style={{ color: '#46A758', fontWeight: 800 }}>✓</span>
                : <span style={{ width: 22, height: 22, borderRadius: '50%', border: '3px solid rgba(255,255,255,.25)', borderTopColor: '#fff', transform: `rotate(${giro}deg)`, display: 'inline-block' }} />}
              {cual ? 'Clasificado' : `Clasificando ${p.tema}…`}
            </div>
          ))}
        </div>
        {ORDEN.map((fila) => (
          <div key={fila} style={{ display: 'flex', gap: 14, marginBottom: 12, background: '#26262C', borderRadius: 18, padding: 10, minHeight: 92, alignItems: 'center' }}>
            <div style={{ width: 72, height: 72, borderRadius: 14, background: COLOR[fila], flex: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontFamily: fuente.titulo, fontWeight: 900, fontSize: 40, color: '#111' }}>{fila}</div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 10 }}>
              {items.filter((it) => it.fila === fila).map((it) => {
                const t = 10 + it.idx * 4;
                const s = spring({ frame: f - t, fps, config: { damping: 9, stiffness: 260, mass: 0.6 } });
                const logo = logoDe(it.nombre);
                return (
                  <div key={it.nombre} style={{ opacity: f >= t ? 1 : 0, transform: `translateY(${(1 - s) * -70}px) scale(${0.85 + 0.15 * s})` }}>
                    {logo ? <Img src={staticFile(logo.name)} style={{ width: 72, height: 72, borderRadius: 16, objectFit: 'cover', background: '#fff' }} />
                      : <div style={{ height: 72, padding: '0 22px', borderRadius: 16, background: '#3A3A42', color: '#fff', display: 'flex', alignItems: 'center',
                          fontFamily: fuente.cuerpo, fontWeight: 700, fontSize: 28, whiteSpace: 'nowrap' }}>{it.nombre}</div>}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
