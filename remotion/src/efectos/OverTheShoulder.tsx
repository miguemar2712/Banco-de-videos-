import React from 'react';
import { AbsoluteFill, Easing, interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { CameraMotionBlur } from '@remotion/motion-blur';
import { BehindMe } from '../componentes/BehindMe';
import { VidrioOscuro } from '../componentes/Glass';
import { CUERPO } from '../constantes';
import { fuente } from '../fuentes';

export type OverTheShoulderProps = {
  inicio: number;
  antesLabel: string; antesNumero: string; antesUnidad: string;
  despuesLabel: string; despuesNumero: string; despuesUnidad: string;
  silencio?: boolean;
};

export const overTheShoulderDefaults: OverTheShoulderProps = {
  inicio: 18.6,
  antesLabel: 'ANTES', antesNumero: '1,204', antesUnidad: 'vistas',
  despuesLabel: 'DESPUÉS', despuesNumero: '412K', despuesUnidad: 'vistas',
};

const suave = Easing.inOut(Easing.cubic);
// Movimiento de cámara: [cuadro, escala, x, y]. x/y en px del cuadro (positivo = el plano se mueve a la derecha/abajo).
// El límite para no mostrar bordes negros es (escala - 1) * 540 en x y (escala - 1) * 960 en y.
const CAMARA: [number, number, number, number][] = [
  [0, 1, 0, 0],
  [5, 1, 0, 0],
  [20, 1.3, 155, 120],   // empuje a 1.3x sobre el hombro izquierdo (lado izquierdo de la pantalla)
  [27, 1.3, 147, 114],   // pausa con un desliz mínimo
  [36, 1.12, 0, 60],     // se aleja a 1.12x cruzando
  [46, 1.3, -155, 120],  // empuje a 1.3x sobre el hombro derecho
  [55, 1.3, -149, 116],  // pausa
  [70, 1, 0, 0],         // vuelve al centro
  [84, 1, 0, 0],
];

function camara(f: number) {
  const i = Math.max(0, CAMARA.findIndex((k, j) => j < CAMARA.length - 1 && f >= k[0] && f <= CAMARA[j + 1][0]));
  const [f0, s0, x0, y0] = CAMARA[i];
  const [f1, s1, x1, y1] = CAMARA[Math.min(i + 1, CAMARA.length - 1)];
  const p = f1 === f0 ? 1 : suave(Math.min(1, Math.max(0, (f - f0) / (f1 - f0))));
  const s = s0 + (s1 - s0) * p;
  const lx = (s - 1) * 540, ly = (s - 1) * 960;   // siempre llena el cuadro
  return { s, x: Math.max(-lx, Math.min(lx, x0 + (x1 - x0) * p)), y: Math.max(-ly, Math.min(ly, y0 + (y1 - y0) * p)) };
}

const Tarjeta: React.FC<{ label: string; numero: string; unidad: string; desde: number; x: number }> = ({ label, numero, unidad, desde, x }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pop = spring({ frame: f - desde, fps, config: { damping: 11, stiffness: 220, mass: 0.6 } });
  const op = interpolate(f, [desde, desde + 5], [0, 1], { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' });
  return (
    <VidrioOscuro style={{ position: 'absolute', left: x - 150, top: CUERPO.hombroIzq.y - 330, width: 300, padding: '26px 28px 30px',
      opacity: op, transform: `scale(${0.8 + 0.2 * pop})` }}>
      <div style={{ fontFamily: fuente.cuerpo, fontWeight: 600, fontSize: 24, letterSpacing: 4, color: 'rgba(255,255,255,0.6)' }}>{label}</div>
      <div style={{ fontFamily: fuente.titulo, fontWeight: 800, fontSize: 78, lineHeight: 1.05, color: '#fff', letterSpacing: -2 }}>{numero}</div>
      <div style={{ fontFamily: fuente.cuerpo, fontWeight: 500, fontSize: 26, color: 'rgba(255,255,255,0.7)' }}>{unidad}</div>
    </VidrioOscuro>
  );
};

export const OverTheShoulder: React.FC<OverTheShoulderProps> = (p) => {
  const f = useCurrentFrame();
  const c = camara(f);
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      <CameraMotionBlur shutterAngle={200} samples={8}>
        <AbsoluteFill style={{ transform: `translate(${c.x}px, ${c.y}px) scale(${c.s})`, transformOrigin: '50% 50%' }}>
          <BehindMe inicio={p.inicio} silencio={p.silencio}>
            <Tarjeta label={p.antesLabel} numero={p.antesNumero} unidad={p.antesUnidad} desde={10} x={270} />  {/* 120–420 */}
            <Tarjeta label={p.despuesLabel} numero={p.despuesNumero} unidad={p.despuesUnidad} desde={40} x={810} />  {/* 660–960 */}
          </BehindMe>
        </AbsoluteFill>
      </CameraMotionBlur>
    </AbsoluteFill>
  );
};
