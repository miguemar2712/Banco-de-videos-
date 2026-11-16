import React from 'react';
import { Composition } from 'remotion';
import { ANCHO, ALTO, FPS } from './constantes';
import { EFECTOS, NombreEfecto } from './efectos/registro';
import { ChatRender, chatRenderDefaults, CHAT_DUR } from './efectos/ChatRender';
import { FullReel, fullReelDefaults, duracionReel } from './efectos/FullReel';

// Cada efecto es su propia composición, con el nombre del efecto. Todas: 1080x1920, 30 fps.
export const Root: React.FC = () => (
  <>
    {(Object.keys(EFECTOS) as NombreEfecto[]).map((n) => (
      <Composition key={n} id={n} component={EFECTOS[n].componente as React.FC<any>} defaultProps={EFECTOS[n].defaults}
        durationInFrames={EFECTOS[n].duracion} fps={FPS} width={ANCHO} height={ALTO} />
    ))}
    <Composition id="ChatRender" component={ChatRender} defaultProps={chatRenderDefaults} durationInFrames={CHAT_DUR} fps={FPS} width={ANCHO} height={ALTO} />
    <Composition id="FullReel" component={FullReel} defaultProps={fullReelDefaults} durationInFrames={duracionReel()} fps={FPS} width={ANCHO} height={ALTO} />
  </>
);
