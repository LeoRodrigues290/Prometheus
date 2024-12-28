/**
 * Arquivo: TheFront/tailwind.config.js
 * Descrição:
 *   - Configuração base do Tailwind CSS, definindo onde buscar classes
 *     e adicionando customizações para o tema dark misterioso.
 */

module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        // Paleta sombria e misteriosa, inspirada em tons marítimos e antigos
        'dark-bg': '#0D0D0D',
        'dark-surface': '#1A1A1A',
        'dark-panel': '#252525',
        'dark-highlight': '#444444',
        'dark-accent': '#6e6b6b',
      },
      fontFamily: {
        // Exemplo: poderíamos usar uma fonte mais clássica ou gótica
        'prometheus': ['"PT Sans"', 'sans-serif']
      }
    },
  },
  plugins: [],
}
