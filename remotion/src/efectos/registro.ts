import React from 'react';
import { OverTheShoulder, overTheShoulderDefaults } from './OverTheShoulder';
import { GlassGraph, glassGraphDefaults } from './GlassGraph';
import { FreezeFrame, freezeFrameDefaults } from './FreezeFrame';
import { TierList, tierListDefaults } from './TierList';
import { TextBehind, textBehindDefaults } from './TextBehind';
import { ColorGrade, colorGradeDefaults } from './ColorGrade';

type Efecto = { componente: React.FC<any>; defaults: Record<string, unknown>; duracion: number; comando: string; descripcion: string };

/** Todos los efectos: nombre → componente, props por defecto, duración (cuadros) y su comando para la intro. */
export type NombreEfecto = 'OverTheShoulder' | 'GlassGraph' | 'FreezeFrame' | 'TierList' | 'TextBehind' | 'ColorGrade';
export const EFECTOS: Record<NombreEfecto, Efecto> = {
  OverTheShoulder: { componente: OverTheShoulder, defaults: overTheShoulderDefaults, duracion: 84, comando: '/over-the-shoulder', descripcion: 'Tarjetas antes/después detrás de tus hombros' },
  GlassGraph: { componente: GlassGraph, defaults: glassGraphDefaults, duracion: 90, comando: '/glass-graph', descripcion: 'Una tarjeta de vidrio con una gráfica que sube' },
  FreezeFrame: { componente: FreezeFrame, defaults: freezeFrameDefaults, duracion: 90, comando: '/freeze-frame', descripcion: 'Congela la imagen y te convierte en sticker' },
  TierList: { componente: TierList, defaults: tierListDefaults, duracion: 90, comando: '/tier-list', descripcion: 'Un ranking S-A-B-C-D que se llena solo' },
  TextBehind: { componente: TextBehind, defaults: textBehindDefaults, duracion: 90, comando: '/text-behind', descripcion: 'Una palabra gigante detrás de tu cabeza' },
  ColorGrade: { componente: ColorGrade, defaults: colorGradeDefaults, duracion: 90, comando: '/color-grade', descripcion: 'De video plano a color de cine' },
};
export const ORDEN_REEL: NombreEfecto[] = ['OverTheShoulder', 'GlassGraph', 'FreezeFrame', 'TierList', 'TextBehind', 'ColorGrade'];
