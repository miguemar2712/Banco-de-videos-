import React from 'react';
import { AbsoluteFill, Easing, Freeze, interpolate, random, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { Clip } from '../componentes/Clip';
import { NARANJA } from '../constantes';
import { fuente } from '../fuentes';
import { EFECTOS, NombreEfecto } from './registro';

export type ChatRenderProps = { comando: string; descripcion: string; efecto: NombreEfecto };
export const chatRenderDefaults: ChatRenderProps = { comando: '/glass-graph', descripcion: 'Una tarjeta de vidrio con una gráfica que sube', efecto: 'GlassGraph' };
export const CHAT_DUR = 75; // 2.5 s

const FILAS = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm'];
const FONDO = '#141414', BURBUJA = '#232323', GRIS = '#8E8E8E';
const ease = Easing.inOut(Easing.cubic);
const cl = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };

const Icono: React.FC<{ d: string; x: number; y: number; s?: number; color?: string }> = ({ d, x, y, s = 44, color = '#EDEDED' }) => (
  <svg width={s} height={s} viewBox="0 0 24 24" style={{ position: 'absolute', left: x, top: y }}><path d={d} fill="none" stroke={color} strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" /></svg>
);
const Estrella: React.FC<{ giro: number }> = ({ giro }) => (
  <svg width={30} height={30} viewBox="0 0 24 24" style={{ transform: `rotate(${giro}deg)` }}>
    {[0, 45, 90, 135].map((a) => <rect key={a} x={11} y={2} width={2} height={20} rx={1} fill={NARANJA} transform={`rotate(${a} 12 12)`} />)}
  </svg>
);

export const ChatRender: React.FC<ChatRenderProps> = ({ comando, descripcion, efecto }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const Efecto = EFECTOS[efecto].componente;
  const props = EFECTOS[efecto].defaults;
  const inicioClip = (props as { inicio?: number }).inicio ?? 0;

  // tiempos
  const T_BARRA = 8, T_ESCRIBE = 12, T_FIN_ESCRIBE = 32, T_ENVIA = 35, T_TILE = 43, T_REVELA = 58, T_CRECE = 60;
  const resto = comando.slice(1);
  const nTeclas = f < T_BARRA ? 0 : f < T_ESCRIBE ? 1 : 1 + Math.min(resto.length, Math.floor(((f - T_ESCRIBE) / (T_FIN_ESCRIBE - T_ESCRIBE)) * resto.length + 1));
  const escrito = f >= T_ENVIA ? '' : comando.slice(0, nTeclas);   // al enviar, la caja queda vacía
  const teclaActual = nTeclas > 1 && f < T_FIN_ESCRIBE + 2 ? comando[nTeclas - 1]?.toLowerCase() : '';
  const tarjeta = spring({ frame: f - T_BARRA, fps, config: { damping: 13, stiffness: 240 } }) * (f < T_ENVIA ? 1 : interpolate(f, [T_ENVIA, T_ENVIA + 4], [1, 0], cl));
  const enviado = interpolate(f, [T_ENVIA, T_ENVIA + 8], [0, 1], { ...cl, easing: ease });
  const textoEditando = interpolate(f, [T_ENVIA + 5, T_ENVIA + 9], [0, 1], cl);
  const tile = spring({ frame: f - T_TILE, fps, config: { damping: 14, stiffness: 200 } });
  const revela = interpolate(f, [T_TILE + 2, T_REVELA], [0, 1], cl);
  const crece = interpolate(f, [T_CRECE, CHAT_DUR - 3], [0, 1], { ...cl, easing: Easing.in(Easing.cubic) });

  // miniatura: en la caja de texto → sube como mensaje enviado arriba a la derecha
  const mini0 = { x: 150, y: 1132, w: 96, h: 170 }, mini1 = { x: 640, y: 330, w: 300, h: 534 };
  const mini = { x: mini0.x + (mini1.x - mini0.x) * enviado, y: mini0.y + (mini1.y - mini0.y) * enviado, w: mini0.w + (mini1.w - mini0.w) * enviado, h: mini0.h + (mini1.h - mini0.h) * enviado };

  // tile de puntos que se vuelve el primer cuadro del efecto
  const t0 = { x: 240, y: 520, w: 600, h: 1066 };
  const tw = t0.w + (1080 - t0.w) * crece, th = t0.h + (1920 - t0.h) * crece, tx = t0.x * (1 - crece), ty = t0.y * (1 - crece);
  const COLS = 18, ROWS = 32;

  return (
    <AbsoluteFill style={{ backgroundColor: FONDO, fontFamily: fuente.cuerpo }}>
      {/* barra superior */}
      <Icono d="M4 7h16M4 12h16M4 17h16" x={120} y={150} />
      <Icono d="M12 20h9M16.5 3.5a2.1 2.1 0 1 1 3 3L7 19l-4 1 1-4Z" x={916} y={150} />
      <div style={{ position: 'absolute', left: 0, right: 0, top: 156, textAlign: 'center', color: '#EDEDED', fontWeight: 600, fontSize: 34 }}>Editor</div>

      {/* mensaje enviado: miniatura + píldora naranja + "Editando con…" */}
      <div style={{ position: 'absolute', left: 640, top: 330 + 534 + 18, width: 300, display: 'flex', justifyContent: 'flex-end', opacity: textoEditando }}>
        <span style={{ background: NARANJA, color: '#fff', fontWeight: 700, fontSize: 28, padding: '10px 22px', borderRadius: 999 }}>{comando}</span>
      </div>
      <div style={{ position: 'absolute', left: 120, top: 960, display: 'flex', alignItems: 'center', gap: 14, opacity: textoEditando * (1 - tile * 0.0), color: GRIS, fontSize: 30 }}>
        <Estrella giro={f * 12} /> Editando con {comando}…
      </div>

      {/* tarjeta del comando sobre la caja */}
      <div style={{ position: 'absolute', left: 120, width: 840, top: 990, opacity: tarjeta, transform: `translateY(${(1 - tarjeta) * 30}px) scale(${0.95 + 0.05 * tarjeta})`,
        background: BURBUJA, borderRadius: 24, padding: '22px 28px', border: '1.5px solid #333' }}>
        <div style={{ color: '#fff', fontWeight: 700, fontSize: 32 }}>{comando}</div>
        <div style={{ color: GRIS, fontSize: 26, marginTop: 4 }}>{descripcion}</div>
      </div>

      {/* caja de mensaje */}
      <div style={{ position: 'absolute', left: 120, width: 840, top: 1110, height: 214, borderRadius: 40, background: BURBUJA, border: '1.5px solid #2E2E2E' }}>
        <div style={{ position: 'absolute', left: 150, top: 34, fontSize: 34, color: escrito ? '#fff' : GRIS }}>{escrito || 'Responder…'}<span style={{ opacity: f % 16 < 8 && f < T_ENVIA ? 1 : 0, color: NARANJA }}>|</span></div>
        <Icono d="M12 5v14M5 12h14" x={26} y={140} s={42} color={GRIS} />
        <Icono d="M12 3a3 3 0 0 0-3 3v6a3 3 0 0 0 6 0V6a3 3 0 0 0-3-3ZM5 11a7 7 0 0 0 14 0M12 18v3" x={690} y={140} s={42} color={GRIS} />
        <div style={{ position: 'absolute', right: 22, top: 130, width: 64, height: 64, borderRadius: '50%', background: NARANJA, display: 'flex', alignItems: 'center', justifyContent: 'center',
          transform: `scale(${f >= T_ENVIA - 1 && f < T_ENVIA + 3 ? 0.85 : 1})` }}>
          <svg width={30} height={30} viewBox="0 0 24 24"><path d="M12 19V5M5 12l7-7 7 7" fill="none" stroke="#fff" strokeWidth={2.8} strokeLinecap="round" strokeLinejoin="round" /></svg>
        </div>
      </div>

      {/* miniatura del clip (con x mientras está adjunta) */}
      <div style={{ position: 'absolute', left: mini.x, top: mini.y, width: mini.w, height: mini.h, borderRadius: 18 + 10 * enviado, overflow: 'hidden', boxShadow: '0 10px 30px rgba(0,0,0,.5)' }}>
        <Freeze frame={0}><div style={{ width: 1080, height: 1920, transform: `scale(${mini.w / 1080})`, transformOrigin: '0 0' }}><Clip inicio={inicioClip} silencio /></div></Freeze>
        {enviado < 0.2 && <div style={{ position: 'absolute', right: 6, top: 6, width: 26, height: 26, borderRadius: '50%', background: 'rgba(0,0,0,.7)', color: '#fff', fontSize: 18, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>×</div>}
      </div>

      {/* teclado */}
      <div style={{ position: 'absolute', left: 0, right: 0, top: 1360, bottom: 0, background: '#1E1E1E', paddingTop: 22 }}>
        {[...FILAS, '/  ', ' '].map((fila, i) => (
          <div key={i} style={{ display: 'flex', justifyContent: 'center', gap: 10, marginBottom: 14 }}>
            {(i === 4 ? ['espacio'] : i === 3 ? ['123', '/', '-', '⏎'] : fila.split('')).map((k) => {
              const on = (k === teclaActual) || (k === '/' && f >= T_BARRA && f < T_BARRA + 3) || (k === '-' && teclaActual === '-');
              return (
                <div key={k} style={{ minWidth: k.length > 1 ? (k === 'espacio' ? 520 : 130) : 88, height: 104, borderRadius: 14, background: on ? '#5A5A5A' : '#2F2F2F',
                  color: '#EDEDED', fontSize: 38, display: 'flex', alignItems: 'center', justifyContent: 'center', transform: on ? 'translateY(-6px) scale(1.12)' : 'none',
                  boxShadow: on ? `0 0 0 2px ${NARANJA}` : '0 2px 0 #111' }}>{k}</div>
              );
            })}
          </div>
        ))}
      </div>

      {/* tile de puntos → primer cuadro del efecto → pantalla completa */}
      {f >= T_TILE && (
        <div style={{ position: 'absolute', left: tx, top: ty, width: tw, height: th, borderRadius: 30 * (1 - crece), overflow: 'hidden', background: '#0C0C0C',
          transform: `scale(${0.6 + 0.4 * tile})`, opacity: Math.min(1, tile * 1.5), boxShadow: '0 30px 80px rgba(0,0,0,.6)' }}>
          <div style={{ width: 1080, height: 1920, transform: `scale(${tw / 1080}, ${th / 1920})`, transformOrigin: '0 0', opacity: revela }}>
            <Freeze frame={0}><Efecto {...(props as Record<string, unknown>)} silencio /></Freeze>
          </div>
          <div style={{ position: 'absolute', inset: 0, display: 'grid', gridTemplateColumns: `repeat(${COLS}, 1fr)`, gridTemplateRows: `repeat(${ROWS}, 1fr)` }}>
            {Array.from({ length: COLS * ROWS }, (_, i) => {
              const umbral = random(`punto-${i}`);
              const luz = interpolate(revela, [umbral * 0.8, umbral * 0.8 + 0.2], [0, 1], cl);
              return <div key={i} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', background: `rgba(12,12,12,${1 - luz})` }}>
                <div style={{ width: 6, height: 6, borderRadius: '50%', background: luz > 0.05 && luz < 0.95 ? NARANJA : '#3A3A3A', opacity: 1 - luz }} />
              </div>;
            })}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
