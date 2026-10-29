(() => {
  "use strict";

  const menu = document.getElementById("mobile-menu");
  const openButton = document.querySelector("[data-menu-open]");
  const closeButtons = document.querySelectorAll("[data-menu-close]");
  const focusableSelector = 'a[href], button:not([disabled]), summary, [tabindex]:not([tabindex="-1"])';
  const pageRegions = [
    document.querySelector(".site-header"),
    document.querySelector("main"),
    document.querySelector(".site-footer"),
    document.querySelector(".mobile-bar"),
  ].filter(Boolean);
  let lastFocused = null;

  const setPageInert = (state) => {
    pageRegions.forEach((element) => {
      if (state) {
        element.setAttribute("inert", "");
      } else {
        element.removeAttribute("inert");
      }
    });
  };

  const openMenu = () => {
    if (!menu || !openButton) return;
    lastFocused = document.activeElement;
    menu.hidden = false;
    openButton.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    setPageInert(true);
    const first = menu.querySelector(focusableSelector);
    if (first) first.focus();
  };

  const closeMenu = () => {
    if (!menu || !openButton) return;
    menu.hidden = true;
    openButton.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    setPageInert(false);
    if (lastFocused && typeof lastFocused.focus === "function") {
      lastFocused.focus();
    }
  };

  if (openButton && menu) {
    openButton.addEventListener("click", openMenu);

    closeButtons.forEach((button) => {
      button.addEventListener("click", closeMenu);
    });

    menu.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
      if (menu.hidden) return;

      if (event.key === "Escape") {
        event.preventDefault();
        closeMenu();
        return;
      }

      if (event.key !== "Tab") return;

      const focusable = Array.from(menu.querySelectorAll(focusableSelector)).filter(
        (el) => el.offsetParent !== null
      );
      if (!focusable.length) return;

      const first = focusable[0];
      const last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }

  const printButton = document.querySelector("[data-print]");
  if (printButton) {
    printButton.addEventListener("click", () => window.print());
  }

  const scheduleNode = document.getElementById("schedule-data");
  if (!scheduleNode) return;

  let schedule = [];
  try {
    schedule = JSON.parse(scheduleNode.textContent || "[]");
  } catch (error) {
    return;
  }

  if (!Array.isArray(schedule) || !schedule.length) return;

  const todayIso = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Europe/Moscow",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(new Date());

  const nowTime = new Intl.DateTimeFormat("en-GB", {
    timeZone: "Europe/Moscow",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(new Date());

  const rows = Array.from(document.querySelectorAll(".schedule-table tr[data-date]"));
  const todayRows = schedule.filter((item) => item.date === todayIso);

  if (todayRows.length) {
    rows.forEach((row) => {
      if (row.dataset.date === todayIso) {
        row.classList.add("is-today");
        row.setAttribute("aria-current", "date");
      }
    });

    const first = todayRows.find((item) => item.time >= nowTime) || todayRows[todayRows.length - 1];
    const value = document.querySelector("[data-today-value]");
    const note = document.querySelector("[data-today-note]");
    if (value) {
      value.textContent = `${first.date_label}, ${first.weekday} — ${first.service}, ${first.time}`;
    }
    if (note) {
      note.textContent = first.feast !== "—" ? first.feast : "Богослужения по расписанию";
    }
  } else {
    const value = document.querySelector("[data-today-value]");
    const note = document.querySelector("[data-today-note]");
    if (value) value.textContent = "Демонстрационное расписание на сентябрь 2026";
    if (note) note.textContent = "Актуальное расписание — в группе ВКонтакте и по телефону.";
  }

  const upcoming = schedule.find(
    (item) => item.date > todayIso || (item.date === todayIso && item.time >= nowTime)
  );
  if (upcoming) {
    const dateNode = document.querySelector("[data-next-date]");
    const serviceNode = document.querySelector("[data-next-service]");
    const timeNode = document.querySelector("[data-next-time]");
    const noteNode = document.querySelector("[data-next-note]");
    if (dateNode) dateNode.textContent = `${upcoming.date_label}, ${upcoming.weekday}`;
    if (serviceNode) serviceNode.textContent = upcoming.service;
    if (timeNode) timeNode.textContent = upcoming.time;
    if (noteNode) {
      noteNode.textContent = upcoming.feast !== "—" ? upcoming.feast : "Богослужения по расписанию";
    }
  }
})();
