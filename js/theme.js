/* Keep the legacy Academic theme controls aligned with system preferences. */
(function () {
  'use strict';

  var storageKey = 'theme_preference';
  var mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

  function storedPreference() {
    var value = window.localStorage.getItem(storageKey);
    return value === '0' || value === '1' ? value === '1' : null;
  }

  function setTheme(isDark) {
    document.body.classList.toggle('dark', isDark);
    document.documentElement.classList.toggle('theme-light', !isDark);
    document.documentElement.style.colorScheme = isDark ? 'dark' : 'light';
    document.querySelectorAll('.js-dark-toggle i').forEach(function (icon) {
      icon.classList.toggle('fa-sun', isDark);
      icon.classList.toggle('fa-moon', !isDark);
    });

    var lightHighlight = document.querySelector('link[title="hl-light"]');
    var darkHighlight = document.querySelector('link[title="hl-dark"]');
    if (lightHighlight && darkHighlight) {
      lightHighlight.disabled = isDark;
      darkHighlight.disabled = !isDark;
    }
  }

  function currentTheme() {
    return document.body.classList.contains('dark');
  }

  function initializeAbstractToggles() {
    document.querySelectorAll('.pub-abstract-toggle').forEach(function (toggle) {
      var panelId = toggle.getAttribute('aria-controls');
      var panel = panelId ? document.getElementById(panelId) : null;
      var label = toggle.querySelector('.pub-abstract-label');
      if (!panel) {
        return;
      }

      toggle.addEventListener('click', function () {
        var isExpanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
        panel.hidden = isExpanded;
        if (label) {
          label.textContent = isExpanded ? 'Abstract' : 'Hide abstract';
        }
      });
    });
  }

  function initialize() {
    var preference = storedPreference();
    setTheme(preference === null ? mediaQuery.matches : preference);

    initializeAbstractToggles();

    document.querySelectorAll('.js-dark-toggle').forEach(function (toggle) {
      toggle.setAttribute('aria-label', 'Toggle dark mode');
      toggle.addEventListener('click', function () {
        window.localStorage.setItem(storageKey, currentTheme() ? '1' : '0');
        setTheme(currentTheme());
      });
    });

    var handleSystemChange = function (event) {
      if (storedPreference() === null) {
        setTheme(event.matches);
      }
    };
    if (mediaQuery.addEventListener) {
      mediaQuery.addEventListener('change', handleSystemChange);
    } else {
      mediaQuery.addListener(handleSystemChange);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize);
  } else {
    initialize();
  }
}());
