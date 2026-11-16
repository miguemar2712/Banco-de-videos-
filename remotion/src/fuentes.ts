import { loadFont as cargarInter } from '@remotion/google-fonts/Inter';
import { loadFont as cargarAnton } from '@remotion/google-fonts/Anton';

const inter = cargarInter('normal', { weights: ['400', '500', '600', '700', '800', '900'], subsets: ['latin'] });
const anton = cargarAnton('normal', { weights: ['400'], subsets: ['latin'] });

export const fuente = {
  titulo: inter.fontFamily,      // números y títulos en negrita
  cuerpo: inter.fontFamily,
  condensada: anton.fontFamily,  // palabra gigante (TextBehind)
};
