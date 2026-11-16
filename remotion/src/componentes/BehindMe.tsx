import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Clip, Persona } from './Clip';

/**
 * BehindMe — dibuja cualquier gráfico DETRÁS de ti y DELANTE del fondo.
 * Capas: 1) tu clip completo (fondo)  2) el gráfico  3) tú recortado con la máscara (persona.webm).
 *
 * <BehindMe inicio={18.6}><MiGrafico /></BehindMe>
 */
export const BehindMe: React.FC<{
  inicio?: number;
  silencio?: boolean;
  children: React.ReactNode;
  fondoStyle?: React.CSSProperties; // p. ej. un filtro solo para el fondo
  personaStyle?: React.CSSProperties;
}> = ({ inicio = 0, silencio, children, fondoStyle, personaStyle }) => (
  <AbsoluteFill>
    <Clip inicio={inicio} silencio={silencio} style={fondoStyle} />
    <AbsoluteFill>{children}</AbsoluteFill>
    <Persona inicio={inicio} style={personaStyle} />
  </AbsoluteFill>
);
