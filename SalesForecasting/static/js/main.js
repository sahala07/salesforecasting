document.addEventListener('DOMContentLoaded', () => {
  AOS.init({ duration: 800, once: true, easing: 'ease-out-cubic' });

  const themeToggle = document.getElementById('themeToggle');
  const body = document.body;
  const savedTheme = localStorage.getItem('sales-theme');

  if (savedTheme === 'dark') {
    body.classList.add('dark-mode');
    themeToggle.innerHTML = '<i class="fa-solid fa-sun"></i>';
  }

  themeToggle?.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    const dark = body.classList.contains('dark-mode');
    localStorage.setItem('sales-theme', dark ? 'dark' : 'light');
    themeToggle.innerHTML = dark ? '<i class="fa-solid fa-sun"></i>' : '<i class="fa-solid fa-moon"></i>';
  });

  const navbar = document.querySelector('.navbar');
  const backToTop = document.getElementById('backToTop');

  const handleScroll = () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 20);
    backToTop?.classList.toggle('show', window.scrollY > 500);
  };

  handleScroll();
  window.addEventListener('scroll', handleScroll);

  backToTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });

  const counters = document.querySelectorAll('.counter');
  counters.forEach((counter) => {
    const target = Number(counter.dataset.target || 0);
    const duration = 1200;
    const startTime = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - startTime) / duration, 1);
      const value = Math.floor(progress * target);
      counter.textContent = `${value}${target === 100 ? '%' : ''}`;
      if (progress < 1) requestAnimationFrame(tick);
    };

    requestAnimationFrame(tick);
  });

  document.querySelectorAll('.faq-item').forEach((item) => {
    item.querySelector('.faq-question')?.addEventListener('click', () => {
      document.querySelectorAll('.faq-item').forEach((entry) => entry.classList.remove('active'));
      item.classList.add('active');
    });
  });

  const form = document.getElementById('predictionForm');
  const submitButton = form?.querySelector('.btn-submit');
  const spinner = form?.querySelector('.spinner-border');
  const label = form?.querySelector('.btn-label');

  form?.addEventListener('submit', (event) => {
    const requiredFields = form.querySelectorAll('input[required]');
    let valid = true;

    requiredFields.forEach((field) => {
      if (!field.value.trim()) {
        valid = false;
        field.classList.add('is-invalid');
      } else {
        field.classList.remove('is-invalid');
      }
    });

    if (!valid) {
      event.preventDefault();
      return;
    }

    submitButton?.classList.add('disabled');
    spinner?.classList.remove('d-none');
    label && (label.textContent = 'Processing...');
  });
});
