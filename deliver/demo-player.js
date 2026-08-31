/* Film clock for deliver/demo.html. No modules. Safe on file:// and in Node. */
(function (root) {
  function create(opts) {
    opts = opts || {};
    var timeline = opts.timeline;
    if (!timeline || !timeline.beats || !timeline.beats.length) {
      throw new Error("FilmPlayer.create requires timeline.beats");
    }
    var duration = Number(timeline.duration);
    var beats = timeline.beats.slice().sort(function (a, b) { return a.t - b.t; });
    var now = 0;
    var paused = false;
    var lastTs = null;
    var rafId = null;
    var onTick = opts.onTick || function () {};
    var raf = opts.raf;
    var caf = opts.caf;
    if (!raf) {
      raf = typeof requestAnimationFrame === "function"
        ? requestAnimationFrame.bind(typeof window !== "undefined" ? window : root)
        : function (fn) { return setTimeout(function () { fn(Date.now()); }, 16); };
    }
    if (!caf) {
      caf = typeof cancelAnimationFrame === "function"
        ? cancelAnimationFrame.bind(typeof window !== "undefined" ? window : root)
        : function (id) { clearTimeout(id); };
    }

    function beatAt(t) {
      var b = beats[0];
      for (var i = 0; i < beats.length; i++) {
        if (t + 1e-9 >= beats[i].t) b = beats[i];
      }
      return b;
    }

    function emit() {
      onTick(now, beatAt(now), paused);
    }

    function frame(ts) {
      if (lastTs == null) lastTs = ts;
      var dt = (ts - lastTs) / 1000;
      lastTs = ts;
      if (!paused) {
        now += dt;
        if (now > duration) now = duration;
      }
      emit();
      if (!paused && now < duration) rafId = raf(frame);
      else rafId = null;
    }

    function play() {
      paused = false;
      lastTs = null;
      if (rafId != null) caf(rafId);
      rafId = raf(frame);
    }

    function togglePause() {
      paused = !paused;
      lastTs = null;
      if (!paused) {
        if (rafId != null) caf(rafId);
        rafId = raf(frame);
      }
      emit();
    }

    function restart() {
      now = 0;
      paused = false;
      lastTs = null;
      if (rafId != null) caf(rafId);
      rafId = raf(frame);
      emit();
    }

    function getState() {
      var b = beatAt(now);
      return {
        t: now,
        paused: paused,
        beat: b.id,
        duration: duration
      };
    }

    function handleKey(e) {
      var key = typeof e === "string" ? e : (e && (e.key || e.code)) || "";
      if (key === " " || key === "Space" || key === "Spacebar") {
        if (e && e.preventDefault) e.preventDefault();
        togglePause();
        return true;
      }
      if (key === "r" || key === "R") {
        if (e && e.preventDefault) e.preventDefault();
        restart();
        return true;
      }
      return false;
    }

    return {
      play: play,
      togglePause: togglePause,
      restart: restart,
      getState: getState,
      handleKey: handleKey
    };
  }

  root.FilmPlayer = { create: create };
})(typeof window !== "undefined" ? window : this);
