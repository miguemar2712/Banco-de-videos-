import React from 'react';
import { AbsoluteFill, Audio, interpolate, Series, staticFile, getStaticFiles, useCurrentFrame, useVideoConfig } from 'remotion';
import { ChatRender, CHAT_DUR } from './ChatRender';
import { EFECTOS, ORDEN_REEL } from './registro';
import { fuente } from '../fuentes';

export type FullReelProps = { cta: string };
export const fullReelDefaults: FullReelProps = { cta: 'Comenta CLAUDE' };
export const GRID_DUR = 120; // 4 s
export const duracionReel = () => ORDEN_REEL.reduce((t, n) => t + CHAT_DUR + EFECTOS[n].duracion, 0) + GRID_DUR;

const Cierre: React.FC<{ cta: string }> = ({ cta }) => {
  const f = useCurrentFrame();
  const entra = interpolate(f, [6, 16], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* rejilla 2 x 3 con los seis efectos sonando a la vez (mudos) */}
      <div style={{ position: 'absolute', inset: 0, display: 'grid', gridTemplateColumns: '1fr 1fr', gridTemplateRows: 'repeat(3, 1fr)' }}>
        {ORDEN_REEL.map((n) => {
          const E = EFECTOS[n];
          return (
            <div key={n} style={{ position: 'relative', overflow: 'hidden', border: '3px solid #000' }}>
              <div style={{ width: 1080, height: 1920, transform: 'translateY(-160px) scale(0.5)', transformOrigin: '0 0' }}>
                <E.componente {...(E.defaults as Record<string, unknown>)} silencio />
              </div>
            </div>
          );
        })}
      </div>
      <AbsoluteFill style={{ background: 'rgba(0,0,0,0.45)' }} />
      <div style={{ position: 'absolute', left: 120, width: 840, top: 820, textAlign: 'center', opacity: entra, transform: `scale(${0.8 + 0.2 * entra})`,
        fontFamily: fuente.titulo, fontWeight: 900, fontSize: 130, lineHeight: 1, letterSpacing: -4, color: '#fff', textShadow: '0 10px 40px rgba(0,0,0,.6)' }}>{cta}</div>
    </AbsoluteFill>
  );
};

export const FullReel: React.FC<FullReelProps> = ({ cta }) => {
  const { durationInFrames } = useVideoConfig();
  const hayMusica = getStaticFiles().some((f) => f.name === 'music.mp3');
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* cortes secos entre secciones (sin fundidos) */}
      <Series>
        {ORDEN_REEL.flatMap((n) => {
          const E = EFECTOS[n];
          return [
            <Series.Sequence key={n + '-intro'} durationInFrames={CHAT_DUR}><ChatRender comando={E.comando} descripcion={E.descripcion} efecto={n} /></Series.Sequence>,
            <Series.Sequence key={n} durationInFrames={E.duracion}><E.componente {...(E.defaults as Record<string, unknown>)} silencio /></Series.Sequence>,
          ];
        })}
        <Series.Sequence durationInFrames={GRID_DUR}><Cierre cta={cta} /></Series.Sequence>
      </Series>
      {/* música a velocidad normal, el clip va muteado; se desvanece en el último medio segundo */}
      {hayMusica && <Audio src={staticFile('music.mp3')} volume={(f) => interpolate(f, [durationInFrames - 15, durationInFrames], [1, 0], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' })} />}
    </AbsoluteFill>
  );
};
