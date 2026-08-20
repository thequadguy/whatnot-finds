/**
 * Whatnot Pinterest Landing Page - Interactive Scripts
 * Lightweight, zero-dependency, ultra-fast performance.
 */

document.addEventListener('DOMContentLoaded', () => {
  initFAQAccordion();
  initScrollAnimations();
  initLiveMockupSim();
  initSmoothScroll();
});

/**
 * FAQ Accordion with accessible ARIA management
 */
function initFAQAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');
  if (!faqItems.length) return;

  faqItems.forEach((item, index) => {
    const questionBtn = item.querySelector('.faq-question');
    const answer = item.querySelector('.faq-answer');

    if (!questionBtn || !answer) return;

    // Set unique ARIA attributes for accessibility
    const qId = `faq-q-${index}`;
    const aId = `faq-a-${index}`;
    questionBtn.setAttribute('id', qId);
    questionBtn.setAttribute('aria-controls', aId);
    questionBtn.setAttribute('aria-expanded', 'false');
    answer.setAttribute('id', aId);
    answer.setAttribute('aria-labelledby', qId);
    answer.setAttribute('role', 'region');

    questionBtn.addEventListener('click', () => {
      const isActive = item.classList.contains('active');

      // Optional: Close other FAQs for clean single-open behavior
      faqItems.forEach((otherItem) => {
        if (otherItem !== item && otherItem.classList.contains('active')) {
          otherItem.classList.remove('active');
          const otherBtn = otherItem.querySelector('.faq-question');
          const otherAns = otherItem.querySelector('.faq-answer');
          if (otherBtn) otherBtn.setAttribute('aria-expanded', 'false');
          if (otherAns) otherAns.style.maxHeight = null;
        }
      });

      // Toggle current item
      if (isActive) {
        item.classList.remove('active');
        questionBtn.setAttribute('aria-expanded', 'false');
        answer.style.maxHeight = null;
      } else {
        item.classList.add('active');
        questionBtn.setAttribute('aria-expanded', 'true');
        answer.style.maxHeight = answer.scrollHeight + 24 + 'px';
      }
    });
  });
}

/**
 * Intersection Observer for subtle scroll reveal
 */
function initScrollAnimations() {
  const animatedElements = document.querySelectorAll('.fade-up');
  if (!animatedElements.length) return;

  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries, obs) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible');
            obs.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1,
        rootMargin: '0px 0px -40px 0px',
      }
    );

    animatedElements.forEach((el) => observer.observe(el));
  } else {
    // Fallback for older browsers
    animatedElements.forEach((el) => el.classList.add('visible'));
  }
}

/**
 * Interactive Live Simulation Mockup Timer & Dynamic Bid Fluctuations
 */
function initLiveMockupSim() {
  const timerElement = document.getElementById('live-sim-timer');
  const bidElement = document.getElementById('live-sim-bid');
  const viewerElement = document.getElementById('live-sim-viewers');

  if (!timerElement && !bidElement) return;

  let secondsLeft = 14;
  let currentBid = 42;
  let viewers = 384;

  setInterval(() => {
    secondsLeft--;
    if (secondsLeft <= 0) {
      secondsLeft = 15;
      // Simulate new drop auction
      currentBid = Math.floor(Math.random() * 30) + 25;
      if (bidElement) {
        bidElement.textContent = `$${currentBid}`;
        bidElement.style.transform = 'scale(1.15)';
        setTimeout(() => {
          bidElement.style.transform = 'scale(1)';
        }, 300);
      }
    }

    if (timerElement) {
      timerElement.textContent = `0:${secondsLeft < 10 ? '0' : ''}${secondsLeft}`;
    }
  }, 1000);

  // Subtle viewer count fluctuation
  if (viewerElement) {
    setInterval(() => {
      const delta = Math.floor(Math.random() * 7) - 3;
      viewers = Math.max(340, viewers + delta);
      viewerElement.textContent = `${viewers} watching`;
    }, 4000);
  }
}

/**
 * Smooth anchor scrolling for header links
 */
function initSmoothScroll() {
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  anchorLinks.forEach((link) => {
    link.addEventListener('click', (e) => {
      const targetId = link.getAttribute('href');
      if (targetId === '#') return;

      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        const headerOffset = 80;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: 'smooth',
        });
      }
    });
  });
}
