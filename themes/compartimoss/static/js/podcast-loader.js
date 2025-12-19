const FEED_URL = 'https://feeds.ivoox.com/feed_fg_f11376815_filtro_1.xml';

async function loadPodcastFeed(containerId, errorId, limit = 3, renderTemplate = 'card') {
  const container = document.getElementById(containerId);
  const errorDiv = document.getElementById(errorId);

  if (!container || !errorDiv) {
    console.error('Elements not found:', { containerId, errorId });
    return;
  }

  try {
    const proxies = [
      (url) => url,
      (url) => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
      (url) => `https://corsproxy.io/?${encodeURIComponent(url)}`,
    ];

    let xml = null;
    let lastError = null;

    for (const proxy of proxies) {
      try {
        const proxyUrl = proxy(FEED_URL);
        const response = await fetch(proxyUrl, {
          headers: {
            'Accept': 'application/xml, application/rss+xml'
          }
        });
        
        if (response.ok) {
          xml = await response.text();
          break;
        }
      } catch (e) {
        lastError = e;
        continue;
      }
    }

    if (!xml) {
      throw lastError || new Error('Failed to fetch feed from all proxies');
    }

    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(xml, 'application/xml');

    if (xmlDoc.getElementsByTagName('parsererror').length > 0) {
      console.error('XML Parse Error:', xmlDoc.documentElement.textContent);
      throw new Error('Invalid XML response');
    }

    const items = xmlDoc.querySelectorAll('item');
    if (items.length === 0) {
      throw new Error('No items found in feed');
    }

    const episodes = Array.from(items).slice(0, limit);

    container.innerHTML = episodes.map((item, index) => {
      const title = item.querySelector('title')?.textContent || 'Sin título';
      const link = item.querySelector('link')?.textContent || '#';
      const description = item.querySelector('description')?.textContent || '';
      const pubDate = item.querySelector('pubDate')?.textContent || '';
      const duration = item.querySelector('itunes\\:duration')?.textContent || 
                      item.querySelector('[name*="duration"]')?.textContent || '';

      let date = 'Fecha desconocida';
      if (pubDate) {
        try {
          date = new Date(pubDate).toLocaleDateString('es-ES', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
          });
        } catch (e) {
          console.warn('Date parse error:', pubDate);
        }
      }

      if (renderTemplate === 'article') {
        return renderArticleTemplate(title, link, description, date, duration, index);
      } else {
        return renderCardTemplate(title, link, description, date, duration);
      }
    }).join('');

    if (renderTemplate === 'article') {
      attachEpisodeListeners();
    }

    errorDiv.classList.add('hidden');
  } catch (error) {
    console.error('Error loading podcast feed:', error);
    container.innerHTML = '';
    errorDiv.classList.remove('hidden');
  }
}

function renderCardTemplate(title, link, description, date, duration) {
  return `
    <a href="${link}" target="_blank" rel="noopener" class="article-card podcast-card" style="display: flex; gap: 1rem; align-items: flex-start; text-decoration: none; color: inherit;">
      <div class="play-button" style="flex-shrink: 0; width: 3rem; height: 3rem; margin-left: 6px; margin-top: 6px; margin-bottom: 6px;">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 1.5rem; height: 1.5rem;"><polygon points="5 3 19 12 5 21 5 3"/></svg>
      </div>
      <div class="article-card-content" style="flex: 1; padding: 0;">
        <h3 class="article-card-title">${title}</h3>
        <p class="article-card-excerpt line-clamp-2">${description.replace(/<[^>]*>/g, '').substring(0, 200)}</p>
        <div class="article-card-meta">
          <div class="article-card-meta-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
            <span>${date}</span>
          </div>
          ${duration ? `<div class="article-card-meta-item">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <span>${duration}</span>
          </div>` : ''}
        </div>
      </div>
    </a>
  `;
}

function renderArticleTemplate(title, link, description, date, duration, index) {
  return `
    <article class="podcast-episode" data-episode-index="${index}" data-episode-url="${link}">
      <div class="podcast-episode-content">
        <a class="play-button" aria-label="Ir al episodio" href="${link}" target="_blank" rel="noopener">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
        </a>

        <div class="podcast-episode-info">
          <h3 class="podcast-episode-title">${title}</h3>
          <p class="podcast-episode-description line-clamp-3">${description.replace(/<[^>]*>/g, '').substring(0, 200)}</p>

          <div class="podcast-episode-meta">
            <div class="podcast-episode-meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
              <span>${date}</span>
            </div>
            ${duration ? `<div class="podcast-episode-meta-item">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
              <span>${duration}</span>
            </div>` : ''}
          </div>
        </div>
      </div>
    </article>
  `;
}

function attachEpisodeListeners() {
  const episodes = document.querySelectorAll('.podcast-episode');

  episodes.forEach((episode) => {
    const url = episode.dataset.episodeUrl;
    if (!url) return;

    episode.style.cursor = 'pointer';
    episode.addEventListener('click', () => {
      window.open(url, '_blank');
    });

    const playButton = episode.querySelector('.play-button');
    if (playButton) {
      playButton.addEventListener('click', (event) => {
        event.stopPropagation();
      });
    }
  });
}
