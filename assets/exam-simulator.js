/**
 * Databricks Formation — Prepare to DP-750
 * exam-simulator.js: Motor de Simulado Pearson VUE com Split-Screen e Fisher-Yates Shuffle
 */

(function () {
  'use strict';

  // Variáveis de Estado da Sessão de Exame
  let currentExamMode = 'official';
  let activeQuestions = [];
  let currentIndex = 0;
  let userAnswers = {}; // { questionId: ['A', 'B'] }
  let reviewMarks = new Set();
  let timerInterval = null;
  let remainingSeconds = 100 * 60; // 100 min padrão
  let examFinished = false;

  // Utilitário: Algoritmo Fisher-Yates
  function shuffle(array) {
    const arr = [...array];
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  // Prepara as questões com embaralhamento das opções e recálculo das letras
  function prepareQuestion(rawQ) {
    const shuffledOptions = shuffle(rawQ.options);
    const letters = ['A', 'B', 'C', 'D', 'E', 'F'];
    
    const mappedOptions = shuffledOptions.map((opt, idx) => ({
      id: letters[idx],
      originalId: opt.id,
      text: opt.text,
      correct: opt.correct,
      explanation: opt.explanation
    }));

    const correctLetters = mappedOptions.filter(o => o.correct).map(o => o.id);

    return {
      ...rawQ,
      options: mappedOptions,
      correctAnswers: correctLetters
    };
  }

  function startExam(mode, domainFilter = null) {
    currentExamMode = mode;
    examFinished = false;
    currentIndex = 0;
    userAnswers = {};
    reviewMarks.clear();

    let pool = [...EXAM_QUESTIONS];

    if (mode === 'official') {
      pool = shuffle(pool).slice(0, 55);
      remainingSeconds = 100 * 60;
    } else if (mode === 'marathon') {
      pool = shuffle(pool).slice(0, 90);
      remainingSeconds = 160 * 60;
    } else if (mode === 'full') {
      pool = shuffle(pool);
      remainingSeconds = pool.length * 2 * 60;
    } else if (mode === 'domain') {
      if (domainFilter) {
        pool = pool.filter(q => q.domain === parseInt(domainFilter, 10));
      }
      pool = shuffle(pool);
      remainingSeconds = pool.length * 2 * 60;
    } else if (mode === 'case-studies') {
      pool = pool.filter(q => q.caseStudyId !== null);
      pool = shuffle(pool);
      remainingSeconds = pool.length * 2 * 60;
    } else if (mode === 'quick-review') {
      pool = shuffle(pool).slice(0, 25);
      remainingSeconds = 40 * 60;
    }

    activeQuestions = pool.map(prepareQuestion);

    // Troca de Telas
    document.getElementById('exam-mode-selection').style.display = 'none';
    document.getElementById('exam-results-screen').style.display = 'none';
    document.getElementById('exam-active-screen').style.display = 'block';

    initTimer();
    renderQuestion(currentIndex);
    renderQuestionPalette();
  }

  function initTimer() {
    if (timerInterval) clearInterval(timerInterval);
    const timerDisplay = document.getElementById('exam-timer-display');

    timerInterval = setInterval(() => {
      if (remainingSeconds <= 0) {
        clearInterval(timerInterval);
        finishExam();
        return;
      }
      remainingSeconds--;
      const hours = Math.floor(remainingSeconds / 3600);
      const minutes = Math.floor((remainingSeconds % 3600) / 60);
      const seconds = remainingSeconds % 60;
      
      const formatted = hours > 0 
        ? `${hours}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
        : `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      
      if (timerDisplay) timerDisplay.textContent = formatted;
    }, 1000);
  }

  function renderQuestion(index) {
    if (index < 0 || index >= activeQuestions.length) return;
    currentIndex = index;

    const q = activeQuestions[index];
    const caseStudy = q.caseStudyId ? CASE_STUDIES.find(cs => cs.id === q.caseStudyId) : null;

    const splitLayout = document.getElementById('exam-split-layout');
    const casePanel = document.getElementById('exam-case-study-panel');
    const questionPanel = document.getElementById('exam-question-panel');

    // Split-Screen se houver Estudo de Caso
    if (caseStudy) {
      splitLayout.style.gridTemplateColumns = '1.1fr 1fr';
      casePanel.style.display = 'flex';
      renderCaseStudy(caseStudy);
    } else {
      splitLayout.style.gridTemplateColumns = '1fr';
      casePanel.style.display = 'none';
    }

    // Renderiza a Questão no Painel Direito
    const qBadge = document.getElementById('exam-q-domain-badge');
    if (qBadge) qBadge.textContent = q.domainName;

    const qNumber = document.getElementById('exam-q-number');
    if (qNumber) qNumber.textContent = `Questão ${index + 1} de ${activeQuestions.length}`;

    const markBtn = document.getElementById('btn-mark-review');
    if (markBtn) {
      if (reviewMarks.has(q.id)) {
        markBtn.classList.add('marked');
        markBtn.innerHTML = '🚩 Marcada para Revisão';
      } else {
        markBtn.classList.remove('marked');
        markBtn.innerHTML = '🏳️ Marcar para Revisão';
      }
    }

    const qText = document.getElementById('exam-q-text');
    if (qText) qText.textContent = q.question;

    const optionsContainer = document.getElementById('exam-options-container');
    optionsContainer.innerHTML = '';

    const isMultiple = q.type === 'multiple';
    const limit = q.correctAnswers.length;

    q.options.forEach(opt => {
      const label = document.createElement('label');
      label.className = 'exam-option-card';

      const currentSelected = userAnswers[q.id] || [];
      const isChecked = currentSelected.includes(opt.id);
      if (isChecked) label.classList.add('selected');

      const input = document.createElement('input');
      input.type = isMultiple ? 'checkbox' : 'radio';
      input.name = `exam-q-${q.id}`;
      input.value = opt.id;
      input.checked = isChecked;

      input.addEventListener('change', () => {
        if (!isMultiple) {
          userAnswers[q.id] = [opt.id];
        } else {
          let selected = userAnswers[q.id] || [];
          if (input.checked) {
            if (selected.length < limit) {
              selected.push(opt.id);
            } else {
              input.checked = false; // trava no limite exato de escolhas
              alert(`Você pode selecionar no máximo ${limit} alternativas para esta questão.`);
              return;
            }
          } else {
            selected = selected.filter(id => id !== opt.id);
          }
          userAnswers[q.id] = selected;
        }
        renderQuestion(currentIndex);
        renderQuestionPalette();

        // Se modo Quick Review, exibe feedback imediato
        if (currentExamMode === 'quick-review') {
          showImmediateFeedback(q);
        }
      });

      const letterBadge = document.createElement('span');
      letterBadge.className = 'exam-option-letter';
      letterBadge.textContent = `${opt.id})`;

      const textSpan = document.createElement('span');
      textSpan.className = 'exam-option-text';
      textSpan.textContent = opt.text;

      label.appendChild(input);
      label.appendChild(letterBadge);
      label.appendChild(textSpan);
      optionsContainer.appendChild(label);
    });

    // Feedback imediato no modo quick-review
    const feedbackBox = document.getElementById('exam-immediate-feedback');
    if (feedbackBox) {
      if (currentExamMode === 'quick-review' && userAnswers[q.id]) {
        showImmediateFeedback(q);
      } else {
        feedbackBox.style.display = 'none';
      }
    }

    // Botões Anterior / Próximo
    const btnPrev = document.getElementById('btn-exam-prev');
    const btnNext = document.getElementById('btn-exam-next');
    if (btnPrev) btnPrev.disabled = index === 0;
    if (btnNext) btnNext.textContent = index === activeQuestions.length - 1 ? 'Finalizar Exame 🏁' : 'Próxima Questão →';
  }

  function showImmediateFeedback(q) {
    const feedbackBox = document.getElementById('exam-immediate-feedback');
    if (!feedbackBox) return;

    const selected = userAnswers[q.id] || [];
    const isCorrect = selected.length === q.correctAnswers.length && selected.every(val => q.correctAnswers.includes(val));

    feedbackBox.style.display = 'block';
    if (isCorrect) {
      feedbackBox.className = 'flash-feedback-box show flash-feedback-success';
      feedbackBox.innerHTML = `<strong>✅ Resposta Correta!</strong> ${q.overallExplanation}`;
    } else {
      feedbackBox.className = 'flash-feedback-box show flash-feedback-error';
      feedbackBox.innerHTML = `<strong>❌ Resposta Incorreta.</strong> Gabarito correto: ${q.correctAnswers.join(', ')}.<br>${q.overallExplanation}`;
    }
  }

  function renderCaseStudy(caseStudy) {
    const titleEl = document.getElementById('case-study-title');
    if (titleEl) titleEl.textContent = caseStudy.title;

    const tabsContainer = document.getElementById('case-study-tabs-bar');
    tabsContainer.innerHTML = '';

    const tabKeys = [
      { key: 'overview', label: 'Visão Geral' },
      { key: 'architecture', label: 'Arquitetura Atual' },
      { key: 'requirements', label: 'Requisitos de Dados' },
      { key: 'security', label: 'Segurança / Unity Catalog' },
      { key: 'issues', label: 'Problemas de Pipeline' }
    ];

    const contentBox = document.getElementById('case-study-tab-content');

    tabKeys.forEach((tab, idx) => {
      const btn = document.createElement('button');
      btn.className = `case-tab-btn ${idx === 0 ? 'active' : ''}`;
      btn.textContent = tab.label;
      btn.addEventListener('click', () => {
        tabsContainer.querySelectorAll('.case-tab-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        contentBox.textContent = caseStudy.tabs[tab.key] || 'Conteúdo não especificado.';
      });
      tabsContainer.appendChild(btn);
    });

    contentBox.textContent = caseStudy.tabs['overview'];
  }

  function renderQuestionPalette() {
    const palette = document.getElementById('exam-palette-grid');
    if (!palette) return;

    palette.innerHTML = '';

    activeQuestions.forEach((q, idx) => {
      const btn = document.createElement('button');
      btn.className = 'palette-btn';
      if (idx === currentIndex) btn.classList.add('current');

      const isAnswered = userAnswers[q.id] && userAnswers[q.id].length > 0;
      if (isAnswered) btn.classList.add('answered');

      const isMarked = reviewMarks.has(q.id);
      if (isMarked) btn.classList.add('marked');

      btn.textContent = idx + 1;
      btn.addEventListener('click', () => {
        renderQuestion(idx);
        renderQuestionPalette();
      });

      palette.appendChild(btn);
    });
  }

  function finishExam() {
    if (timerInterval) clearInterval(timerInterval);
    examFinished = true;

    // Calcula Pontuação Oficial
    let correctCount = 0;
    const domainBreakdown = {
      1: { total: 0, correct: 0, name: 'Domínio 1: Configurar o Ambiente' },
      2: { total: 0, correct: 0, name: 'Domínio 2: Segurança & Unity Catalog' },
      3: { total: 0, correct: 0, name: 'Domínio 3: Ingestão & Processamento' },
      4: { total: 0, correct: 0, name: 'Domínio 4: Pipelines & Orquestração' }
    };

    activeQuestions.forEach(q => {
      const selected = userAnswers[q.id] || [];
      const isCorrect = selected.length === q.correctAnswers.length && selected.every(v => q.correctAnswers.includes(v));

      if (domainBreakdown[q.domain]) {
        domainBreakdown[q.domain].total++;
        if (isCorrect) domainBreakdown[q.domain].correct++;
      }

      if (isCorrect) correctCount++;
    });

    const percent = Math.round((correctCount / activeQuestions.length) * 100);
    const scaledScore = Math.round((percent / 100) * 1000);
    const passed = scaledScore >= 700;

    // Telas
    document.getElementById('exam-active-screen').style.display = 'none';
    document.getElementById('exam-results-screen').style.display = 'block';

    const resultBanner = document.getElementById('exam-result-banner');
    if (resultBanner) {
      resultBanner.className = `exam-result-banner ${passed ? 'passed' : 'failed'}`;
      resultBanner.innerHTML = `
        <div style="font-size: 2.2rem; font-weight: 800; margin-bottom: 0.5rem;">
          ${passed ? '🎉 APROVADO NO EXAME DP-750!' : '⚠️ NÃO APROVADO DESTA VEZ'}
        </div>
        <div style="font-size: 1.2rem;">Sua pontuação: <strong>${scaledScore} / 1000</strong> (${percent}%) — Nota de corte: 700 / 1000</div>
        <p style="margin-top: 0.8rem; font-size: 0.95rem;">
          ${passed 
            ? 'Parabéns! Seu domínio técnico em Azure Databricks, Unity Catalog, Delta Lake e Workflows está no padrão oficial Microsoft Certified: Azure Databricks Data Engineer Associate!' 
            : 'Revise os domínios com pontuação inferior a 70% nas Folhas de Referência Rápida e repita o simulado focado.'}
        </p>
      `;
    }

    // Breakdown por Domínio
    const breakdownContainer = document.getElementById('exam-domain-breakdown');
    if (breakdownContainer) {
      breakdownContainer.innerHTML = '';
      Object.keys(domainBreakdown).forEach(k => {
        const d = domainBreakdown[k];
        if (d.total === 0) return;
        const dPercent = Math.round((d.correct / d.total) * 100);

        const card = document.createElement('div');
        card.className = 'domain-score-card';
        card.innerHTML = `
          <div style="display: flex; justify-content: space-between; font-weight: 600; margin-bottom: 0.4rem;">
            <span>${d.name}</span>
            <span>${d.correct} / ${d.total} (${dPercent}%)</span>
          </div>
          <div class="score-progress-bar">
            <div class="score-progress-fill" style="width: ${dPercent}%; background: ${dPercent >= 70 ? '#00A972' : '#FF3621'};"></div>
          </div>
        `;
        breakdownContainer.appendChild(card);
      });
    }

    // Gabarito Comentado Completo de todas as questões
    renderFullReviewList();
  }

  function renderFullReviewList() {
    const listContainer = document.getElementById('exam-full-review-list');
    if (!listContainer) return;
    listContainer.innerHTML = '';

    activeQuestions.forEach((q, idx) => {
      const selected = userAnswers[q.id] || [];
      const isCorrect = selected.length === q.correctAnswers.length && selected.every(v => q.correctAnswers.includes(v));

      const item = document.createElement('div');
      item.className = `review-question-card ${isCorrect ? 'correct' : 'incorrect'}`;

      let optionsHtml = '';
      q.options.forEach(opt => {
        const wasSelected = selected.includes(opt.id);
        const isRight = opt.correct;
        let badge = '';
        let rowClass = '';
        if (wasSelected && isRight) {
          badge = '<span class="review-badge-correct" style="font-weight: 700;">(Sua resposta - Correta)</span>';
          rowClass = 'review-opt-correct';
        } else if (wasSelected && !isRight) {
          badge = '<span class="review-badge-incorrect" style="font-weight: 700;">(Sua resposta - Incorreta)</span>';
          rowClass = 'review-opt-incorrect';
        } else if (!wasSelected && isRight) {
          badge = '<span class="review-badge-official" style="font-weight: 700;">(Gabarito Oficial)</span>';
          rowClass = 'review-opt-correct';
        }

        optionsHtml += `
          <div class="review-opt-row ${rowClass}" style="margin: 0.4rem 0; padding: 0.5rem 0.8rem; border-radius: 4px;">
            <strong>${opt.id})</strong> ${opt.text} ${badge}
            ${opt.explanation ? `<div class="review-opt-explanation" style="font-size: 0.8rem; margin-top: 0.2rem; margin-left: 1.2rem;">↳ ${opt.explanation}</div>` : ''}
          </div>
        `;
      });

      item.innerHTML = `
        <div style="font-weight: 700; margin-bottom: 0.5rem;">
          ${isCorrect ? '✅' : '❌'} Questão ${idx + 1}: ${q.domainName}
        </div>
        <p style="margin: 0.5rem 0;">${q.question}</p>
        <div style="margin: 0.8rem 0;">${optionsHtml}</div>
        <div class="review-explanation-box" style="font-size: 0.85rem; padding: 0.75rem 1rem; border-radius: 0 4px 4px 0;">
          <strong>Explicação da Arquitetura:</strong> ${q.overallExplanation}
        </div>
      `;

      listContainer.appendChild(item);
    });
  }

  // Event Listeners globais
  document.addEventListener('DOMContentLoaded', () => {
    // Botões de Início de Modo
    document.querySelectorAll('.btn-start-mode').forEach(btn => {
      btn.addEventListener('click', () => {
        const mode = btn.getAttribute('data-mode');
        const domain = btn.getAttribute('data-domain');
        startExam(mode, domain);
      });
    });

    // Navegação Anterior e Próximo
    const btnPrev = document.getElementById('btn-exam-prev');
    if (btnPrev) {
      btnPrev.addEventListener('click', () => {
        if (currentIndex > 0) {
          renderQuestion(currentIndex - 1);
          renderQuestionPalette();
        }
      });
    }

    const btnNext = document.getElementById('btn-exam-next');
    if (btnNext) {
      btnNext.addEventListener('click', () => {
        if (currentIndex < activeQuestions.length - 1) {
          renderQuestion(currentIndex + 1);
          renderQuestionPalette();
        } else {
          if (confirm('Deseja realmente finalizar o exame agora?')) {
            finishExam();
          }
        }
      });
    }

    // Botão de Marcação para Revisão
    const markBtn = document.getElementById('btn-mark-review');
    if (markBtn) {
      markBtn.addEventListener('click', () => {
        const q = activeQuestions[currentIndex];
        if (reviewMarks.has(q.id)) {
          reviewMarks.delete(q.id);
        } else {
          reviewMarks.add(q.id);
        }
        renderQuestion(currentIndex);
        renderQuestionPalette();
      });
    }

    // Botão Finalizar Exame no Topo
    const btnFinish = document.getElementById('btn-finish-exam-top');
    if (btnFinish) {
      btnFinish.addEventListener('click', () => {
        if (confirm('Tem certeza de que deseja entregar a prova e calcular sua pontuação oficial?')) {
          finishExam();
        }
      });
    }

    // Botão Reiniciar Simulado
    const btnRestart = document.getElementById('btn-restart-exam');
    if (btnRestart) {
      btnRestart.addEventListener('click', () => {
        document.getElementById('exam-results-screen').style.display = 'none';
        document.getElementById('exam-active-screen').style.display = 'none';
        document.getElementById('exam-mode-selection').style.display = 'block';
      });
    }
  });

})();

