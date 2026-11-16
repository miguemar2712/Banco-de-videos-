import React from 'react';
import { AbsoluteFill, Freeze, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { Clip, Persona } from '../componentes/Clip';
import { CUERPO } from '../constantes';
import { fuente } from '../fuentes';

export type FreezeFrameProps = { inicio: number; nombre: string; rol: string; silencio?: boolean };
export const freezeFrameDefaults: FreezeFrameProps = { inicio: 47.9, nombre: '@tu_usuario', rol: 'CREADOR' };

const CONGELA = 15, SUELTA = 60, FIN_SUELTA = 70;
// borde blanco tipo sticker (~12 px): sombras duras en 8 direcciones + sombra suave
const BORDE = [[0, 1], [0.7, 0.7], [1, 0], [0.7, -0.7], [0, -1], [-0.7, -0.7], [-1, 0], [-0.7, 0.7]]
  .map(([x, y]) => `drop-shadow(${(x * 6).toFixed(1)}px ${(y * 6).toFixed(1)}px 0 #fff)`).join(' ');

export const FreezeFrame: React.FC<FreezeFrameProps> = (p) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  // cuadro del video: avanza, se congela en 15 y sigue desde ahí al soltar
  const cuadroVideo = f < CONGELA ? f : f < SUELTA ? CONGELA : f - (SUELTA - CONGELA);
  const congelado = f >= CONGELA && f < FIN_SUELTA;
  const k = f < CONGELA ? 0 : f < SUELTA ? 1 : interpolate(f, [SUELTA, FIN_SUELTA], [1, 0], { extrapolateRight: 'clamp' });
  const escala = 1 + 0.04 * (f < SUELTA ? spring({ frame: f - CONGELA, fps, config: { damping: 12, stiffness: 260 } }) : k);
  const flash = interpolate(f, [CONGELA, CONGELA + 6], [0.8, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' }) * (f >= CONGELA ? 1 : 0);
  const tag = f < SUELTA ? spring({ frame: f - CONGELA - 6, fps, config: { damping: 11, stiffness: 240 } }) : k;
  const origen = `${CUERPO.cabezaCentro.x}px ${CUERPO.pecho.y}px`;
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <Freeze frame={cuadroVideo}>
        {/* fondo: gris y 40% más oscuro mientras está congelado */}
        <Clip inicio={p.inicio} silencio={p.silencio || congelado}
          style={{ filter: `grayscale(${k}) brightness(${1 - 0.4 * k})` }} />
        {/* borde blanco detrás de ti (máscara agrandada) + sombra */}
        {k > 0 && (
          <Persona inicio={p.inicio} style={{ opacity: k, transform: `scale(${escala})`, transformOrigin: origen,
            filter: `${BORDE} drop-shadow(0 18px 30px rgba(0,0,0,.45))` }} />
        )}
        {/* tú, con tus colores reales */}
        <Persona inicio={p.inicio} style={{ transform: `scale(${escala})`, transformOrigin: origen }} />
      </Freeze>
      {/* etiqueta con tu nombre, debajo del pecho, dentro de x 120–960 */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 1300, display: 'flex', justifyContent: 'center', opacity: Math.min(1, tag), transform: `scale(${0.7 + 0.3 * tag})` }}>
        <div style={{ background: 'rgba(16,16,20,0.88)', borderRadius: 999, padding: '20px 48px 22px', textAlign: 'center', boxShadow: '0 16px 40px rgba(0,0,0,.4)', maxWidth: 840 }}>
          <div style={{ fontFamily: fuente.titulo, fontWeight: 800, fontSize: 56, color: '#fff', letterSpacing: -1 }}>{p.nombre}</div>
          <div style={{ fontFamily: fuente.cuerpo, fontWeight: 600, fontSize: 22, letterSpacing: 8, color: 'rgba(255,255,255,.65)', marginTop: 4 }}>{p.rol}</div>
        </div>
      </div>
      <AbsoluteFill style={{ backgroundColor: '#fff', opacity: flash }} />
    </AbsoluteFill>
  );
};
