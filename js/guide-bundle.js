import bundle from '../data/guides.bundle.json' assert { type: 'json' };
import guideCatalog from '../data/guide_catalog.json' assert { type: 'json' };

const cloneBundle = (payload) => {
  if (!payload || typeof payload !== 'object') return null;
  if (typeof structuredClone === 'function') {
    try {
      return structuredClone(payload);
    } catch (err) {
      console.warn('Structured clone failed for guide bundle, using JSON fallback.', err);
    }
  }
  try {
    return JSON.parse(JSON.stringify(payload));
  } catch (err) {
    console.warn('JSON clone failed for guide bundle; returning original reference.', err);
    return payload;
  }
};

const ready = Promise.resolve(bundle)
  .then(cloneBundle)
  .then((data) => {
    if (!data) return null;
    if (!Array.isArray(data.routes)) data.routes = [];
    if (!Array.isArray(data.extras)) data.extras = [];
    if (!data.metadata) data.metadata = null;
    return data;
  })
  .catch((err) => {
    console.error('Failed to import bundled guide data.', err);
    return null;
  });

window.__GUIDE_BUNDLE_PROMISE__ = ready;
ready.then((data) => {
  if (data) {
    window.__GUIDE_BUNDLE__ = data;
  }
});

const catalogReady = Promise.resolve(guideCatalog)
  .then(cloneBundle)
  .then((data) => {
    if (data) {
      window.__GUIDE_CATALOG_FALLBACK__ = data;
    }
    return data;
  })
  .catch((err) => {
    console.error('Failed to import fallback guide catalog.', err);
    return null;
  });

window.__GUIDE_CATALOG_FALLBACK_PROMISE__ = catalogReady;
