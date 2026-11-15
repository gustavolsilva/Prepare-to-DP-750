/**
 * Databricks Formation — Prepare to DP-750
 * lens.js: Controle Global de Nível (Lentes Pedagógicas no padrão DP-700),
 * Tema Global (Light / Dark Mode Midnight Edition), Sticky Audio Player com Motor Neural de Fala e Fisher-Yates Quiz Shuffle.
 */

// Guarda global de idempotência para evitar execuções duplicadas
if (window.__DP750_LENS_INITIALIZED__) {
  // Já carregado na página, evita listeners duplicados
} else {
  window.__DP750_LENS_INITIALIZED__ = true;

  // =========================================================================
  // 0. Controle Global de Tema (Dark / Light Mode) — Inicialização Imediata
  // =========================================================================
  const GLOBAL_THEME_KEY = 'databricks_dp750_theme';

  function applyThemeToDOM(theme) {
    const targetTheme = (theme === 'dark') ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', targetTheme);
    if (document.body) {
      document.body.setAttribute('data-theme', targetTheme);
    }
    try {
      localStorage.setItem(GLOBAL_THEME_KEY, targetTheme);
    } catch (e) {}

    const themeButtons = document.querySelectorAll('.theme-toggle-btn');
    themeButtons.forEach((btn) => {
      if (targetTheme === 'dark') {
        btn.innerHTML = '☀️ Modo Light';
        btn.setAttribute('title', 'Alternar para Modo Claro');
      } else {
        btn.innerHTML = '🌙 Modo Dark';
        btn.setAttribute('title', 'Alternar para Modo Escuro');
      }
    });
  }

  window.toggleAppTheme = function () {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyThemeToDOM(next);
  };

  // Execução precoce para prevenir flash de tela branca (FOUC)
  (function initThemeEarly() {
    try {
      const savedTheme = localStorage.getItem(GLOBAL_THEME_KEY) || 'light';
      document.documentElement.setAttribute('data-theme', savedTheme);
    } catch (e) {}
  })();

  (function () {
    'use strict';

    const GLOBAL_LENS_KEY = 'databricks_dp750_global_lens';
    const FALLBACK_LENS_KEY = 'dp750_active_lens';

    const LABELS = {
      'unificado': '🌐 Visão Unificada Completa',
      'junior': '🌱 Júnior (Fundamentos do Zero)',
      'pleno': '🛠️ Pleno (Implementação Prática & Pipelines)',
      'senior': '🎯 Sênior & Exame DP-750',
      'staff': '⚙️ Staff / Internals (Sob o Capô & Escala)',
      'clevel': '🏛️ C-Level / Head (Estratégia & FinOps)'
    };

    // Normalização de chaves de lentes para interoperabilidade (DP-700 e DP-750)
    function normalizeLens(rawLens) {
      if (!rawLens) return 'unificado';
      const l = rawLens.toLowerCase();
      if (l === 'all' || l === 'completo' || l === 'unificado') return 'unificado';
      if (l === 'junior' || l === '0') return 'junior';
      if (l === 'pleno' || l === 'mid' || l === '1') return 'pleno';
      if (l === 'senior' || l === 'dp750' || l === '2') return 'senior';
      if (l === 'staff' || l === 'principal' || l === '3') return 'staff';
      if (l === 'clevel' || l === 'c-level' || l === 'finops' || l === '4') return 'clevel';
      return 'unificado';
    }

    // =========================================================================
    // 1. Gerenciador Multi-Lente Global
    // =========================================================================
    function initLensManager() {
      const savedLens = normalizeLens(
        localStorage.getItem(GLOBAL_LENS_KEY) || localStorage.getItem(FALLBACK_LENS_KEY) || 'unificado'
      );

      function setGlobalLens(targetLens) {
        const normalized = normalizeLens(targetLens);
        document.body.setAttribute('data-active-lens', normalized);
        
        try {
          localStorage.setItem(GLOBAL_LENS_KEY, normalized);
          localStorage.setItem(FALLBACK_LENS_KEY, normalized);
        } catch (e) {}

        // Atualiza botões de navegação de lentes
        const lensButtons = document.querySelectorAll('.lens-btn');
        lensButtons.forEach((btn) => {
          const btnLens = normalizeLens(btn.getAttribute('data-lens') || btn.getAttribute('data-lens-target'));
          if (btnLens === normalized) {
            btn.classList.add('active');
          } else {
            btn.classList.remove('active');
          }
        });

        // Atualiza badge de perfil ativo
        const labelBadge = document.getElementById('current-profile-label');
        if (labelBadge && LABELS[normalized]) {
          labelBadge.textContent = LABELS[normalized];
        }

        // Aplica visibilidade nos blocos de conteúdo da lição (chaveamento estrito por nível no padrão DP-700)
        const lensBlocks = document.querySelectorAll('.lens-text-content, [data-lens-block]');
        lensBlocks.forEach((block) => {
          const blockLens = normalizeLens(
            block.getAttribute('data-lens') || block.getAttribute('data-lens-alt') || block.getAttribute('data-lens-content')
          );

          if (blockLens === normalized) {
            block.style.display = 'block';
            block.style.opacity = '1';
          } else {
            block.style.display = 'none';
          }
        });
      }

      // Listeners nos botões de lente
      const lensButtons = document.querySelectorAll('.lens-btn');
      lensButtons.forEach((btn) => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const target = btn.getAttribute('data-lens') || btn.getAttribute('data-lens-target');
          setGlobalLens(target);
        });
      });

      // Aplica a lente salva
      setGlobalLens(savedLens);

      // Sincronização entre abas
      window.addEventListener('storage', (e) => {
        if (e.key === GLOBAL_LENS_KEY || e.key === FALLBACK_LENS_KEY) {
          if (e.newValue) {
            setGlobalLens(e.newValue);
          }
        }
      });

      // Atalhos de teclado [0..5] para troca rápida de lente
      document.addEventListener('keydown', (e) => {
        if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) {
          return;
        }

        const keyMap = {
          '0': 'unificado',
          '1': 'junior',
          '2': 'pleno',
          '3': 'senior',
          '4': 'staff',
          '5': 'clevel'
        };

        if (keyMap[e.key]) {
          setGlobalLens(keyMap[e.key]);
        }
      });
    }

    // =========================================================================
    // 2. Sticky Audio Player Controller
    // =========================================================================
    function initStickyAudio() {
      if (window.__DP750_AUDIO_INITIALIZED__) return;
      window.__DP750_AUDIO_INITIALIZED__ = true;

      const audio = document.getElementById('lesson-audio');
      const btnPlay = document.getElementById('btn-audio-play');
      if (!btnPlay || !audio) return;

      const progressFill = document.getElementById('audio-progress-fill');
      const progressBar = document.getElementById('audio-progress-bar');
      const timeCurrent = document.getElementById('audio-time-current');
      const timeTotal = document.getElementById('audio-time-total');
      const btnSpeed = document.getElementById('btn-audio-speed');
      const subTitle = document.querySelector('.audio-text-sub');

      const speeds = [1.0, 1.25, 1.5, 2.0];
      let currentSpeedIndex = 0;

      function formatTime(seconds) {
        if (isNaN(seconds) || seconds < 0) return '00:00';
        const m = Math.floor(seconds / 60);
        const s = Math.floor(seconds % 60);
        return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
      }

      function updateDuration() {
        if (audio.duration && !isNaN(audio.duration)) {
          if (timeTotal) timeTotal.textContent = formatTime(audio.duration);
        }
      }

      // Tenta carregar metadados do áudio imediatamente
      audio.addEventListener('loadedmetadata', updateDuration);
      audio.addEventListener('canplay', updateDuration);
      audio.addEventListener('durationchange', updateDuration);

      // Se já tiver metadados carregados
      if (audio.readyState >= 1) {
        updateDuration();
      } else {
        audio.load();
      }

      // Atualização de Progresso durante reprodução
      audio.addEventListener('timeupdate', () => {
        if (audio.duration && !isNaN(audio.duration)) {
          const percent = Math.min(100, (audio.currentTime / audio.duration) * 100);
          if (progressFill) progressFill.style.width = `${percent}%`;
          if (timeCurrent) timeCurrent.textContent = formatTime(audio.currentTime);
        }
      });

      // Sincronização de Estado com o Botão Play / Pause
      audio.addEventListener('play', () => {
        btnPlay.innerHTML = '⏸';
        btnPlay.setAttribute('title', 'Pausar Narração');
        if (subTitle) {
          subTitle.textContent = '🎧 Reproduzindo narração neural Kokoro 82M...';
          subTitle.style.color = '#00E5CF';
        }
      });

      audio.addEventListener('pause', () => {
        btnPlay.innerHTML = '▶';
        btnPlay.setAttribute('title', 'Reproduzir Narração');
        if (subTitle) {
          subTitle.textContent = '⏸ Narração pausada';
          subTitle.style.color = '#FFD875';
        }
      });

      audio.addEventListener('ended', () => {
        btnPlay.innerHTML = '▶';
        btnPlay.setAttribute('title', 'Reproduzir Narração');
        if (progressFill) progressFill.style.width = '0%';
        if (timeCurrent) timeCurrent.textContent = '00:00';
        if (subTitle) {
          subTitle.textContent = 'Áudio Neural PT-BR • Pronúncia Técnica Databricks (Kokoro 82M)';
          subTitle.style.color = '';
        }
      });

      // Clique no Botão Play / Pause
      btnPlay.addEventListener('click', (e) => {
        e.preventDefault();
        if (audio.paused) {
          const playPromise = audio.play();
          if (playPromise !== undefined) {
            playPromise.then(() => {
              btnPlay.innerHTML = '⏸';
            }).catch((err) => {
              console.warn('[DP-750 Audio] Erro ao reproduzir:', err);
              // Fallback para Web Speech API se disponível
              if ('speechSynthesis' in window) {
                const titleText = document.querySelector('#bloco-contexto h1')?.textContent || '';
                const utter = new SpeechSynthesisUtterance(titleText);
                utter.lang = 'pt-BR';
                window.speechSynthesis.speak(utter);
              }
            });
          }
        } else {
          audio.pause();
          btnPlay.innerHTML = '▶';
        }
      });

      // Seek Interativo na Barra de Progresso
      if (progressBar) {
        progressBar.addEventListener('click', (e) => {
          const rect = progressBar.getBoundingClientRect();
          const clickPos = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
          if (audio.duration && !isNaN(audio.duration)) {
            audio.currentTime = clickPos * audio.duration;
            if (audio.paused) {
              audio.play();
            }
          }
        });
      }

      // Controle de Velocidade (1x, 1.25x, 1.5x, 2x)
      if (btnSpeed) {
        btnSpeed.addEventListener('click', (e) => {
          e.preventDefault();
          currentSpeedIndex = (currentSpeedIndex + 1) % speeds.length;
          const newSpeed = speeds[currentSpeedIndex];
          audio.playbackRate = newSpeed;
          btnSpeed.textContent = `${newSpeed}x`;
        });
      }

      // =======================================================================
      // Controle de Fixação (Pin / Unpin) e Ocultação (Hide / Show)
      // =======================================================================
      const stickyBar = document.getElementById('sticky-audio-bar') || document.querySelector('.sticky-audio-bar');
      const btnPin = document.getElementById('btn-audio-pin');
      const btnHide = document.getElementById('btn-audio-hide');
      const btnReopen = document.getElementById('btn-audio-reopen');
      const pillPlayState = document.getElementById('pill-play-state');

      const STORAGE_PIN_KEY = 'databricks_dp750_audio_pinned';
      const STORAGE_HIDE_KEY = 'databricks_dp750_audio_hidden';

      function applyAudioPinState(isPinned) {
        if (!stickyBar) return;
        if (isPinned) {
          stickyBar.classList.remove('is-unpinned');
          if (btnPin) {
            btnPin.classList.add('active');
            btnPin.innerHTML = '<span class="pin-icon">📌</span> <span class="pin-label">Fixado</span>';
            btnPin.setAttribute('title', 'Clique para desafixar da base da tela (embutir na página)');
          }
          document.querySelectorAll('.inline-pin-label').forEach((el) => {
            el.textContent = '📍 Desafixar da Base';
          });
        } else {
          stickyBar.classList.add('is-unpinned');
          if (btnPin) {
            btnPin.classList.remove('active');
            btnPin.innerHTML = '<span class="pin-icon">📍</span> <span class="pin-label">Desafixado</span>';
            btnPin.setAttribute('title', 'Clique para fixar na base da tela (sticky)');
          }
          document.querySelectorAll('.inline-pin-label').forEach((el) => {
            el.textContent = '📌 Fixar na Base';
          });
        }
        try {
          localStorage.setItem(STORAGE_PIN_KEY, isPinned ? 'true' : 'false');
        } catch (e) {}
      }

      function applyAudioHideState(isHidden) {
        if (!stickyBar) return;
        if (isHidden) {
          stickyBar.classList.add('is-hidden');
          if (btnReopen) {
            btnReopen.style.display = 'flex';
          }
        } else {
          stickyBar.classList.remove('is-hidden');
          if (btnReopen) {
            btnReopen.style.display = 'none';
          }
        }
        try {
          localStorage.setItem(STORAGE_HIDE_KEY, isHidden ? 'true' : 'false');
        } catch (e) {}
      }

      window.toggleAudioPin = function () {
        if (!stickyBar) return;
        const currentlyUnpinned = stickyBar.classList.contains('is-unpinned');
        applyAudioPinState(currentlyUnpinned);
      };

      window.toggleAudioHide = function (forceState) {
        if (!stickyBar) return;
        const currentlyHidden = stickyBar.classList.contains('is-hidden');
        const nextState = typeof forceState === 'boolean' ? forceState : !currentlyHidden;
        applyAudioHideState(nextState);
      };

      window.toggleAudioPlayFromSection = function () {
        if (!audio) return;
        applyAudioHideState(false);
        btnPlay.click();
      };

      if (btnPin) {
        btnPin.addEventListener('click', (e) => {
          e.preventDefault();
          window.toggleAudioPin();
        });
      }

      if (btnHide) {
        btnHide.addEventListener('click', (e) => {
          e.preventDefault();
          window.toggleAudioHide(true);
        });
      }

      if (btnReopen) {
        btnReopen.addEventListener('click', (e) => {
          e.preventDefault();
          window.toggleAudioHide(false);
        });
      }

      // Sincroniza indicador de play no pill flutuante
      audio.addEventListener('play', () => {
        if (pillPlayState) pillPlayState.textContent = '⏸';
      });
      audio.addEventListener('pause', () => {
        if (pillPlayState) pillPlayState.textContent = '▶';
      });
      audio.addEventListener('ended', () => {
        if (pillPlayState) pillPlayState.textContent = '▶';
      });

      // Inicializa preferências salvas
      const savedPinned = localStorage.getItem(STORAGE_PIN_KEY);
      if (savedPinned === 'false') {
        applyAudioPinState(false);
      } else {
        applyAudioPinState(true);
      }

      const savedHidden = localStorage.getItem(STORAGE_HIDE_KEY);
      if (savedHidden === 'true') {
        applyAudioHideState(true);
      } else {
        applyAudioHideState(false);
      }
    }

    // =========================================================================
    // 3. Algoritmo Fisher-Yates Shuffle & Flash Quizzes das Lições
    // =========================================================================
    function shuffleArray(array) {
      const arr = [...array];
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
      return arr;
    }

    function initFlashQuizzes() {
      const quizContainers = document.querySelectorAll('.flash-quiz-box');

      quizContainers.forEach((quizBox) => {
        const optionsList = quizBox.querySelector('.flash-options-list');
        const feedbackBox = quizBox.querySelector('.flash-feedback-box');
        const shuffleBtn = quizBox.querySelector('.btn-shuffle');
        if (!optionsList) return;

        if (!quizBox._originalOptions) {
          const optionNodes = Array.from(optionsList.querySelectorAll('.flash-option-item'));
          quizBox._originalOptions = optionNodes.map((opt) => ({
            text: opt.querySelector('.flash-option-text').textContent.trim(),
            isCorrect: opt.getAttribute('data-correct') === 'true',
            explanation: opt.getAttribute('data-explanation') || ''
          }));
        }

        function renderShuffledOptions() {
          const shuffled = shuffleArray(quizBox._originalOptions);
          optionsList.innerHTML = '';
          if (feedbackBox) {
            feedbackBox.className = 'flash-feedback-box';
            feedbackBox.textContent = '';
          }

          const letters = ['A', 'B', 'C', 'D', 'E'];

          shuffled.forEach((optData, idx) => {
            const item = document.createElement('div');
            item.className = 'flash-option-item';
            item.setAttribute('data-correct', optData.isCorrect ? 'true' : 'false');
            item.setAttribute('data-explanation', optData.explanation);

            const marker = document.createElement('span');
            marker.className = 'flash-option-marker';
            marker.textContent = `${letters[idx]})`;

            const textSpan = document.createElement('span');
            textSpan.className = 'flash-option-text';
            textSpan.textContent = optData.text;

            item.appendChild(marker);
            item.appendChild(textSpan);

            item.addEventListener('click', () => {
              const allItems = optionsList.querySelectorAll('.flash-option-item');
              allItems.forEach((el) => {
                el.style.pointerEvents = 'none';
                if (el.getAttribute('data-correct') === 'true') {
                  el.classList.add('correct');
                }
              });

              if (optData.isCorrect) {
                item.classList.add('correct');
                if (feedbackBox) {
                  feedbackBox.className = 'flash-feedback-box show flash-feedback-success';
                  feedbackBox.innerHTML = `<strong>✅ Correto!</strong> ${optData.explanation || 'Excelente análise arquitetural de acordo com o exame oficial DP-750.'}`;
                }
              } else {
                item.classList.add('incorrect');
                if (feedbackBox) {
                  feedbackBox.className = 'flash-feedback-box show flash-feedback-error';
                  feedbackBox.innerHTML = `<strong>❌ Incorreto.</strong> ${optData.explanation || 'Esta alternativa não atende aos requisitos técnicos da prova DP-750.'}`;
                }
              }
            });

            optionsList.appendChild(item);
          });
        }

        renderShuffledOptions();

        if (shuffleBtn) {
          shuffleBtn.addEventListener('click', () => {
            renderShuffledOptions();
          });
        }
      });
    }

    // Inicialização geral ao carregar a página
    document.addEventListener('DOMContentLoaded', () => {
      // Sincroniza estado visual do botão de tema
      const currentTheme = localStorage.getItem(GLOBAL_THEME_KEY) || 'light';
      applyThemeToDOM(currentTheme);

      initLensManager();
      initStickyAudio();
      initFlashQuizzes();
    });
  })();
}
