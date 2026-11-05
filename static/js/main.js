// small extras for the home page, the form works without this file too

const form = document.getElementById('summary-form');
const textarea = document.getElementById('text-input');
const counter = document.getElementById('word-counter');
const submitBtn = document.getElementById('submit-btn');
const sampleBtn = document.getElementById('sample-btn');
const copyBtn = document.getElementById('copy-btn');

const SAMPLE_TEXT =
  'Highways are lines of communication that touch life on many levels. ' +
  'They connect cities, towns and villages across the country. ' +
  'In 2020, over 5 million people used the National Highway network every day. ' +
  'Good roads also help trade grow because goods can move quickly and cheaply. ' +
  'Without them, farmers would struggle to get their crops to the market. ' +
  'The government plans to build 200 new roads by 2030. ' +
  'Experts say this will boost the economy and create thousands of jobs.';

function countWords(text) {
  const words = text.trim().split(/\s+/);
  return text.trim() === '' ? 0 : words.length;
}

function updateCounter() {
  counter.textContent = countWords(textarea.value) + ' words';
}

textarea.addEventListener('input', updateCounter);
updateCounter();

sampleBtn.addEventListener('click', function () {
  textarea.value = SAMPLE_TEXT;
  updateCounter();
});

form.addEventListener('submit', function () {
  submitBtn.disabled = true;
  submitBtn.textContent = 'Summarising...';
});

if (copyBtn) {
  copyBtn.addEventListener('click', function () {
    const summary = document.getElementById('summary-text').textContent;
    navigator.clipboard.writeText(summary).then(function () {
      copyBtn.textContent = 'Copied!';
      setTimeout(function () {
        copyBtn.textContent = 'Copy';
      }, 1500);
    });
  });
}
