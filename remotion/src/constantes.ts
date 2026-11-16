// Ajustes de TODOS los videos de este proyecto
export const ANCHO = 1080;
export const ALTO = 1920;
export const FPS = 30;

// Zona segura: todo texto y gráfico importante vive entre x=120 y x=960
// (a la derecha están los botones de Instagram/TikTok y abajo el texto del post)
export const SEGURO = { x0: 120, x1: 960 };
export const SEGURO_ANCHO = SEGURO.x1 - SEGURO.x0; // 840

// Archivos en public/
export const CLIP = 'talking.mp4'; // tu clip original (nunca se modifica)
export const PERSONA = 'persona.webm'; // tú recortado con transparencia, hecho desde public/mask/mask.mp4

// Dónde está tu cuerpo en el clip (medido sobre la máscara), en píxeles del cuadro 1080x1920
// (medido en public/mask/mask.mp4: cabeza x 418–673, y 460–700; hombros desde y≈780; la mesa tapa desde y≈1240)
export const CUERPO = {
  cabezaCentro: { x: 545, y: 580 },
  cabezaArriba: 455,
  barbilla: 720,
  hombroIzq: { x: 330, y: 840 },
  hombroDer: { x: 860, y: 840 },
  pecho: { y: 1000 },
};

// Colores
export const NARANJA = '#D97757'; // naranja Claude
export const fmtNumero = (n: number) =>
  n >= 10000 ? `${Math.round(n / 1000).toLocaleString('en-US')}K` : Math.round(n).toLocaleString('en-US');
