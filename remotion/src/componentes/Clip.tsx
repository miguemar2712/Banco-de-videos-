import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { CLIP, FPS, PERSONA } from '../constantes';

/** Tu clip a pantalla completa. `inicio` = segundo del clip donde empieza el efecto. */
export const Clip: React.FC<{ inicio?: number; silencio?: boolean; style?: React.CSSProperties }> = ({ inicio = 0, silencio, style }) => (
  <AbsoluteFill style={style}>
    <OffthreadVideo src={staticFile(CLIP)} startFrom={Math.round(inicio * FPS)} muted={silencio}
      style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
  </AbsoluteFill>
);

/** Solo tú (fondo transparente), cuadro a cuadro igual que el clip. */
export const Persona: React.FC<{ inicio?: number; style?: React.CSSProperties }> = ({ inicio = 0, style }) => (
  <AbsoluteFill style={style}>
    <OffthreadVideo src={staticFile(PERSONA)} startFrom={Math.round(inicio * FPS)} muted transparent
      style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
  </AbsoluteFill>
);
