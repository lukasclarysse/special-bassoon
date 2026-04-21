const Snake = (() => {
  const GRID = 20;
  const TICK_MS = 130;

  const COLORS = {
    bg:         '#0d0d0d',
    grid:       '#141414',
    snake:      '#c8f135',
    snakeDark:  '#8aab1e',
    food:       '#ff4d4d',
    text:       '#e8e8e8',
    muted:      '#666',
  };

  let canvas, ctx, scoreEl, bestEl;
  let state, intervalId;

  function init(mountId) {
    const mount = document.getElementById(mountId);
    mount.innerHTML = '';

    const wrapper = document.createElement('div');
    wrapper.style.cssText = 'display:flex;flex-direction:column;align-items:center;gap:.75rem;';

    const meta = document.createElement('div');
    meta.style.cssText = `
      display:flex;justify-content:space-between;width:100%;
      font-family:'Space Mono',monospace;font-size:.75rem;color:${COLORS.muted};
      text-transform:uppercase;letter-spacing:.06em;
    `;
    meta.innerHTML = `
      <span>score: <strong id="snake-score" style="color:${COLORS.text}">0</strong></span>
      <span>wasd / arrows</span>
      <span>best: <strong id="snake-best" style="color:${COLORS.text}">0</strong></span>
    `;

    canvas = document.createElement('canvas');
    canvas.width  = 400;
    canvas.height = 400;
    canvas.style.cssText = `border:1px solid #2a2a2a;border-radius:4px;display:block;`;
    canvas.setAttribute('tabindex', '0');

    const hint = document.createElement('div');
    hint.style.cssText = `font-family:'Space Mono',monospace;font-size:.7rem;color:${COLORS.muted};`;
    hint.textContent = 'click the board to focus, then use arrow keys or wasd';

    wrapper.appendChild(meta);
    wrapper.appendChild(canvas);
    wrapper.appendChild(hint);
    mount.appendChild(wrapper);

    ctx      = canvas.getContext('2d');
    scoreEl  = document.getElementById('snake-score');
    bestEl   = document.getElementById('snake-best');

    canvas.addEventListener('keydown', onKey);
    canvas.addEventListener('click', () => canvas.focus());

    bestEl.textContent = localStorage.getItem('snake-best') || 0;

    reset();
    draw();
  }

  function reset() {
    clearInterval(intervalId);

    const mid = Math.floor(GRID / 2);
    state = {
      snake:    [{ x: mid, y: mid }, { x: mid - 1, y: mid }],
      dir:      { x: 1, y: 0 },
      nextDir:  { x: 1, y: 0 },
      food:     spawnFood([{ x: mid, y: mid }, { x: mid - 1, y: mid }]),
      score:    0,
      running:  false,
      dead:     false,
    };

    scoreEl.textContent = 0;
    draw();
  }

  function start() {
    if (intervalId) clearInterval(intervalId);
    state.running = true;
    state.dead    = false;
    intervalId = setInterval(tick, TICK_MS);
  }

  function tick() {
    const head = {
      x: state.snake[0].x + state.nextDir.x,
      y: state.snake[0].y + state.nextDir.y,
    };
    state.dir = { ...state.nextDir };

    if (
      head.x < 0 || head.x >= GRID ||
      head.y < 0 || head.y >= GRID ||
      state.snake.some(s => s.x === head.x && s.y === head.y)
    ) {
      die();
      return;
    }

    state.snake.unshift(head);

    if (head.x === state.food.x && head.y === state.food.y) {
      state.score++;
      scoreEl.textContent = state.score;
      const best = parseInt(localStorage.getItem('snake-best') || 0);
      if (state.score > best) {
        localStorage.setItem('snake-best', state.score);
        bestEl.textContent = state.score;
      }
      state.food = spawnFood(state.snake);
    } else {
      state.snake.pop();
    }

    draw();
  }

  function die() {
    clearInterval(intervalId);
    state.running = false;
    state.dead    = true;
    draw();
  }

  function onKey(e) {
    const map = {
      ArrowUp:    { x: 0,  y: -1 },
      ArrowDown:  { x: 0,  y:  1 },
      ArrowLeft:  { x: -1, y:  0 },
      ArrowRight: { x: 1,  y:  0 },
      w:          { x: 0,  y: -1 },
      s:          { x: 0,  y:  1 },
      a:          { x: -1, y:  0 },
      d:          { x: 1,  y:  0 },
    };

    if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      if (state.dead) { reset(); start(); }
      else if (!state.running) start();
      return;
    }

    const next = map[e.key];
    if (!next) return;
    e.preventDefault();

    if (next.x === -state.dir.x && next.y === -state.dir.y) return;
    state.nextDir = next;

    if (!state.running && !state.dead) start();
  }

  function spawnFood(snake) {
    let pos;
    do {
      pos = {
        x: Math.floor(Math.random() * GRID),
        y: Math.floor(Math.random() * GRID),
      };
    } while (snake.some(s => s.x === pos.x && s.y === pos.y));
    return pos;
  }

  function cell(x, y) {
    const size = canvas.width / GRID;
    return { px: x * size, py: y * size, size };
  }

  function draw() {
    const w = canvas.width;
    const h = canvas.height;
    const cellSize = w / GRID;

    ctx.fillStyle = COLORS.bg;
    ctx.fillRect(0, 0, w, h);

    ctx.strokeStyle = COLORS.grid;
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= GRID; i++) {
      ctx.beginPath(); ctx.moveTo(i * cellSize, 0); ctx.lineTo(i * cellSize, h); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, i * cellSize); ctx.lineTo(w, i * cellSize); ctx.stroke();
    }

    state.snake.forEach((seg, i) => {
      const { px, py, size } = cell(seg.x, seg.y);
      ctx.fillStyle = i === 0 ? COLORS.snake : COLORS.snakeDark;
      ctx.fillRect(px + 1, py + 1, size - 2, size - 2);
    });

    const { px: fx, py: fy, size: fs } = cell(state.food.x, state.food.y);
    ctx.fillStyle = COLORS.food;
    ctx.beginPath();
    ctx.arc(fx + fs / 2, fy + fs / 2, fs / 2 - 2, 0, Math.PI * 2);
    ctx.fill();

    if (!state.running) {
      ctx.fillStyle = 'rgba(13,13,13,0.75)';
      ctx.fillRect(0, 0, w, h);

      ctx.font = `700 14px 'Space Mono', monospace`;
      ctx.textAlign = 'center';

      if (state.dead) {
        ctx.fillStyle = COLORS.text;
        ctx.fillText('game over', w / 2, h / 2 - 20);
        ctx.fillStyle = COLORS.muted;
        ctx.font = `400 11px 'Space Mono', monospace`;
        ctx.fillText(`score: ${state.score}`, w / 2, h / 2);
        ctx.fillText('space / enter to restart', w / 2, h / 2 + 20);
      } else {
        ctx.fillStyle = COLORS.accent;
        ctx.fillStyle = COLORS.text;
        ctx.fillText('snake', w / 2, h / 2 - 20);
        ctx.fillStyle = COLORS.muted;
        ctx.font = `400 11px 'Space Mono', monospace`;
        ctx.fillText('space / enter or any direction to start', w / 2, h / 2 + 4);
      }
    }
  }

  return { init };
})();
