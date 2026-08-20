/**
 * Pin Template Studio Logic
 * Real-time text swapping, template switching, and preset loading.
 */

const PRESETS = {
  pokemon: {
    template: 'a',
    badge: 'POKÉMON DISCOVERY',
    title: 'Pokémon Collectors, You Need to See This.',
    subtitle: 'Live vintage booster breaks, PSA slabs, and raw singles streaming daily.',
    cta: 'EXPLORE POKÉMON'
  },
  sneakers: {
    template: 'b',
    badge: 'SNEAKER DROPS',
    title: 'Where Sneakerheads Shop Live in 2026',
    subtitle: 'Deadstock retros, size checks on 4K camera, and sudden $1 start auctions.',
    cta: 'SEE LIVE KICKS'
  },
  fashion: {
    template: 'a',
    badge: 'EDITORIAL FASHION',
    title: 'The New Way Fashion People Are Shopping',
    subtitle: 'Stylists try on luxury handbags, vintage tees, and archive denim in real time.',
    cta: 'EXPLORE FASHION'
  },
  collectibles: {
    template: 'f',
    badge: 'RARE COLLECTIBLES',
    title: 'What If Your Next Grail Was Live?',
    subtitle: 'KAWS figures, Labubu blind box unboxings, and convention Funko grails.',
    cta: 'EXPLORE GRAILS'
  },
  beauty: {
    template: 'd',
    badge: 'K-BEAUTY & GLOW',
    title: 'Live Swatches & Viral Skincare Finds',
    subtitle: 'Watch real skin barrier routines and authentic luxury fragrances streamed live.',
    cta: 'EXPLORE BEAUTY'
  },
  listicle: {
    template: 'e',
    badge: 'SHOPPING FINDS',
    title: '5 Reasons People Are Hooked on Live Shopping',
    subtitle: 'Live auctions, curated streamers, and sudden unexpected drops.',
    cta: 'START EXPLORING'
  }
};

let currentTemplate = 'a';

document.addEventListener('DOMContentLoaded', () => {
  const badgeInput = document.getElementById('input-badge');
  const titleInput = document.getElementById('input-title');
  const subInput = document.getElementById('input-sub');
  const ctaInput = document.getElementById('input-cta');
  const tmplButtons = document.querySelectorAll('.tmpl-btn');
  const presetButtons = document.querySelectorAll('.preset-btn');

  // Input listeners
  badgeInput.addEventListener('input', updateCanvas);
  titleInput.addEventListener('input', updateCanvas);
  subInput.addEventListener('input', updateCanvas);
  ctaInput.addEventListener('input', updateCanvas);

  // Template switchers
  tmplButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      tmplButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentTemplate = btn.dataset.tmpl;
      applyTemplateClass();
      updateCanvas();
    });
  });

  // Presets
  presetButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const presetKey = btn.dataset.preset;
      const preset = PRESETS[presetKey];
      if (preset) {
        badgeInput.value = preset.badge;
        titleInput.value = preset.title;
        subInput.value = preset.subtitle;
        ctaInput.value = preset.cta;
        currentTemplate = preset.template;
        
        tmplButtons.forEach(b => {
          b.classList.toggle('active', b.dataset.tmpl === preset.template);
        });

        applyTemplateClass();
        updateCanvas();
      }
    });
  });

  applyTemplateClass();
  updateCanvas();
});

function applyTemplateClass() {
  const canvas = document.getElementById('pin-canvas');
  if (!canvas) return;
  canvas.className = `pin-canvas tmpl-${currentTemplate}`;
}

function updateCanvas() {
  const badgeInput = document.getElementById('input-badge').value;
  const titleInput = document.getElementById('input-title').value;
  const subInput = document.getElementById('input-sub').value;
  const ctaInput = document.getElementById('input-cta').value;

  const canvasBadge = document.getElementById('canvas-badge');
  const canvasTitle = document.getElementById('canvas-title');
  const canvasSub = document.getElementById('canvas-sub');
  const canvasCta = document.getElementById('canvas-cta');

  if (canvasBadge) canvasBadge.textContent = badgeInput;
  if (canvasTitle) canvasTitle.textContent = titleInput;
  if (canvasSub) canvasSub.textContent = subInput;
  if (canvasCta) canvasCta.textContent = ctaInput;
}
