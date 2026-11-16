import React from 'react';

/** Tarjeta de vidrio oscuro: bordes redondeados, borde blanco fino ~20%, fondo desenfocado y sombra suave. */
export const VidrioOscuro: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{
    background: 'rgba(18,18,22,0.55)',
    border: '2px solid rgba(255,255,255,0.2)',
    borderRadius: 34,
    backdropFilter: 'blur(22px) saturate(1.2)',
    WebkitBackdropFilter: 'blur(22px) saturate(1.2)',
    boxShadow: '0 24px 60px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.12)',
    ...style,
  }}>{children}</div>
);

/** Vidrio claro/esmerilado (blanco ~10%). */
export const VidrioClaro: React.FC<{ style?: React.CSSProperties; children: React.ReactNode }> = ({ style, children }) => (
  <div style={{
    background: 'rgba(255,255,255,0.10)',
    border: '1.5px solid rgba(255,255,255,0.28)',
    borderRadius: 36,
    backdropFilter: 'blur(34px) saturate(1.3)',
    WebkitBackdropFilter: 'blur(34px) saturate(1.3)',
    boxShadow: '0 30px 70px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,255,255,0.25)',
    ...style,
  }}>{children}</div>
);
