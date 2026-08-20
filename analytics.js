/**
 * FREE CLIENT-SIDE UTM TRACKING & A/B TESTING ENGINE
 * 100% Free, Zero External Dependencies, Zero Backend, Privacy-Friendly.
 */

(function() {
  'use strict';

  // Base Whatnot referral destination
  const BASE_REFERRAL_URL = 'https://whatnot.com/invite/gittles';

  // 5 High-Converting Headline Variations for A/B Testing
  const HEADLINE_VARIATIONS = [
    "You Just Found Your New Favorite Way to Shop.",
    "The Marketplace Collectors Can't Stop Talking About.",
    "Live Auctions. Rare Finds. Endless Discoveries.",
    "There's a Whole World of Shopping You Haven't Seen Yet.",
    "What If Your Next Favorite Find Was Live?"
  ];

  // 5 High-Converting CTA Variations for A/B Testing
  const CTA_VARIATIONS = [
    "Explore Whatnot",
    "Start Exploring",
    "See What's Live",
    "Discover Whatnot",
    "Explore the Marketplace"
  ];

  // Extract query parameters
  const urlParams = new URLSearchParams(window.location.search);
  const utmSource = urlParams.get('utm_source') || 'direct';
  const utmMedium = urlParams.get('utm_medium') || 'web';
  const utmCampaign = urlParams.get('utm_campaign') || 'landing';
  const utmContent = urlParams.get('utm_content') || 'organic';

  // Handle A/B testing headline variation
  let variantIndex = parseInt(urlParams.get('ab') || urlParams.get('v'), 10);
  if (isNaN(variantIndex) || variantIndex < 0 || variantIndex >= HEADLINE_VARIATIONS.length) {
    // Check localStorage for consistent user experience, else default to 0
    const savedVariant = localStorage.getItem('wt_ab_variant');
    variantIndex = savedVariant !== null ? parseInt(savedVariant, 10) : 0;
  } else {
    localStorage.setItem('wt_ab_variant', variantIndex);
  }

  document.addEventListener('DOMContentLoaded', () => {
    applyABTesting();
    enrichOutboundLinks();
    initMobileStickyCTA();
    trackReferralClicks();
  });

  /**
   * Apply A/B test variations to hero headline and primary CTAs if configured
   */
  function applyABTesting() {
    const heroTitle = document.getElementById('ab-hero-title');
    if (heroTitle && HEADLINE_VARIATIONS[variantIndex]) {
      heroTitle.innerHTML = formatHeadlineHTML(HEADLINE_VARIATIONS[variantIndex]);
    }

    // Optional A/B test indicator pill for tester review
    const abBadge = document.getElementById('ab-variant-indicator');
    if (abBadge) {
      abBadge.textContent = `Variant ${variantIndex + 1}`;
    }
  }

  /**
   * Helper to format headline with gradient highlight
   */
  function formatHeadlineHTML(text) {
    if (text.includes("Way to Shop")) {
      return text.replace("Way to Shop", '<span class="hero-title-highlight">Way to Shop</span>');
    }
    if (text.includes("Collectors")) {
      return text.replace("Collectors", '<span class="hero-title-highlight">Collectors</span>');
    }
    if (text.includes("Live Auctions")) {
      return text.replace("Live Auctions", '<span class="hero-title-highlight">Live Auctions</span>');
    }
    if (text.includes("Live?")) {
      return text.replace("Live?", '<span class="hero-title-highlight">Live?</span>');
    }
    return text;
  }

  /**
   * Enrich all Whatnot referral links with tracking context (stored in client-side log)
   */
  function enrichOutboundLinks() {
    const referralLinks = document.querySelectorAll('a[href*="whatnot.com/invite/gittles"]');
    referralLinks.forEach((link) => {
      // Ensure target="_blank" and secure rel
      link.setAttribute('target', '_blank');
      link.setAttribute('rel', 'noopener noreferrer');

      link.addEventListener('click', () => {
        logConversion(link.getAttribute('id') || 'unlabeled_cta', link.textContent.trim());
      });
    });
  }

  /**
   * Log click conversions to LocalStorage for 100% free visitor analytics
   */
  function logConversion(ctaId, ctaText) {
    const timestamp = new Date().toISOString();
    const eventData = {
      timestamp,
      ctaId,
      ctaText,
      source: utmSource,
      medium: utmMedium,
      campaign: utmCampaign,
      content: utmContent,
      page: window.location.pathname,
      variant: variantIndex + 1
    };

    try {
      const existingLogs = JSON.parse(localStorage.getItem('wt_clicks') || '[]');
      existingLogs.push(eventData);
      // Keep last 100 events
      if (existingLogs.length > 100) existingLogs.shift();
      localStorage.setItem('wt_clicks', JSON.stringify(existingLogs));
    } catch (e) {
      // Ignore storage errors in private browsing
    }
  }

  /**
   * Mobile sticky bottom CTA controller
   */
  function initMobileStickyCTA() {
    const mobileStickyBar = document.getElementById('mobile-sticky-cta');
    if (!mobileStickyBar) return;

    window.addEventListener('scroll', () => {
      // Show sticky bar after scrolling past the first hero section (300px)
      if (window.scrollY > 320) {
        mobileStickyBar.classList.add('active');
      } else {
        mobileStickyBar.classList.remove('active');
      }
    }, { passive: true });
  }

  /**
   * Optional custom click tracker hook (Google Analytics 4 / Cloudflare / GoatCounter compatible)
   */
  function trackReferralClicks() {
    // If user later adds Google Analytics (window.gtag) or Cloudflare Web Analytics,
    // this hook will automatically forward the conversion event without code changes.
    if (typeof window.gtag === 'function') {
      document.querySelectorAll('a[href*="whatnot.com/invite/gittles"]').forEach((btn) => {
        btn.addEventListener('click', () => {
          window.gtag('event', 'referral_click', {
            event_category: 'outbound',
            event_label: btn.id || 'cta_click',
            campaign: utmCampaign
          });
        });
      });
    }
  }

})();
