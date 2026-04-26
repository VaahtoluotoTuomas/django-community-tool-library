/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./tyokalut/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          // SININEN: Pääväri (Linkit, perusnapit, korostukset)
          primary: {
            DEFAULT: '#1d4ed8', // blue-700 (parempi kontrasti valkoista tekstiä vasten)
            hover: '#2563eb',   // blue-600
            light: '#60a5fa',   // blue-400 (esim. aktiivisen tekstin väri)
            ultralight: '#93c5fd', // blue-300
            dark: '#1e40af',    // blue-800 (himmeät tausta)
          },
          // VIHREÄ: Onnistumiset ja lainaus (Lainaa-nappi, aktiivinen status)
          success: {
            DEFAULT: '#16a34a', // green-600
            hover: '#22c55e',   // green-500
            light: '#86efac',   // green-300 (kirkkaampi, ylittää helposti 4.5:1 tummalla taustalla)
            dark: '#166534',    // green-800
          },
          // PUNAINEN: Vaara ja peruutukset (uloskirjautuminen, myöhässä, virheet)
          danger: {
            DEFAULT: '#dc2626', // red-600
            hover: '#ef4444',   // red-500
            light: '#fca5a5',   // red-300 (kirkkaampi, ylittää helposti 4.5:1 tummalla taustalla)
            dark: '#991b1b',    // red-800
          },
          // KELTAINEN: Varoitukset (lähestyvä eräpäivä)
          warning: {
            DEFAULT: '#eab308', // yellow-500
          },
          // RAKENNE JA TAUSTAT (harmaan sävyt)
          bg: '#111827',        // gray-900 (sivuston pohjaväri)
          surface: {
            DEFAULT: '#1f2937', // gray-800 (korttien ja navigaation tausta)
            hover: '#374151',   // gray-700 (lomakekenttien tausta ja harmaat napit)
          },
          border: {
            DEFAULT: '#4b5563', // gray-600 (aktiiviset reunukset)
            muted: '#374151',   // gray-700 (himmeät reunukset)
          },
          text: {
            main: '#ffffff',    // text-white (pääotsikot)
            muted: '#d1d5db',   // gray-300 (ohjetekstit, päivämäärät, parempi kontrasti)
          }
        }
      }
    },
  },
  plugins: [],
}

