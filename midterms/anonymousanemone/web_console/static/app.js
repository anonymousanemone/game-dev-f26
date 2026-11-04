const $ = id => document.getElementById(id);
let config, runId, events;
function append(id, text) {
  const element = $(id);
  const follow = element.scrollHeight - element.scrollTop - element.clientHeight < 60;
  element.textContent += text;
  if (follow) element.scrollTop = element.scrollHeight;
}
fetch('/api/config').then(r => r.json()).then(data => {
  config = data;
  $('model-settings').textContent = `Vertex model: ${data.model || 'not configured'} · cap per run: $${data.max_cost_usd || 'not configured'} · prices dated: ${data.price_date || 'not configured'}`;
  if (!data.web_ready) $('status').textContent = 'Build browser replay first: python -m web_console.build';
}).catch(() => { $('status').textContent = 'Cannot connect to the local Python server.'; });
$('controls').onsubmit = async event => {
  event.preventDefault();
  if (!config) return;
  const live = $('policy').value === 'model';
  const details = `Spell 31 then Spell 32, development seed 30. ${live ? `Vertex model: ${config.model || 'NOT CONFIGURED'}. Shared maximum: $${config.max_cost_usd} TOTAL for both spells, including failed-call reservations. Prices: $${config.input_price || 'NOT CONFIGURED'}/M input, $${config.output_price || 'NOT CONFIGURED'}/M output, dated ${config.price_date || 'NOT CONFIGURED'}.` : 'Baseline player: no model calls or API spending.'} History: ${$('history').value}. Replay makes no new model calls. Each new confirmed run gets a new $${config.max_cost_usd} cap.`;
  $('confirmation-details').textContent = details + (live ? '\n\nHistorical Gemini 3.5 Flash-Lite history=2 pairs used $0.35–$0.43 and reserved $2.19–$2.66 at $0.30/M input and $2.50/M output. $5 gives more room for longer winning attempts; completion is still not guaranteed.' : '');
  const dialog = $('confirm-run');
  dialog.returnValue = 'cancel';
  dialog.showModal();
  const accepted = await new Promise(resolve => dialog.addEventListener('close', () => resolve(dialog.returnValue === 'confirm'), {once:true}));
  if (!accepted) return;
  $('run').disabled = true;
  $('replay').disabled = true;
  $('viewer').hidden = true;
  $('viewer').removeAttribute('src');
  $('download').hidden = true;
  $('terminal').textContent = $('json').textContent = '';
  $('status').textContent = 'Starting…';
  try {
    const response = await fetch('/api/runs', {method:'POST', headers:{'Content-Type':'application/json','X-Console-Token':config.token}, body:JSON.stringify({case:$('case').value,policy:$('policy').value,history:Number($('history').value),authorize_live:live})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    runId = data.id;
    if (events) events.close();
    events = new EventSource(`/api/runs/${runId}/events`);
    $('status').textContent = 'Running · decisions stream below';
    events.onmessage = message => {
      const data = JSON.parse(message.data);
      if (data.kind === 'log') append('terminal', data.text);
      if (data.kind === 'row') append('json', JSON.stringify(data.row) + '\n');
      if (data.kind === 'complete' || data.kind === 'error') {
        events.close();
        $('run').disabled = false;
        if (data.kind === 'complete') {
          const limited = data.budget.episodes.some(episode => episode.outcome.status === 'limit');
          $('status').textContent = limited ? 'Attempt stopped at a limit · saved replays verified' : 'Both attempts finished · native replays verified · choose an episode';
          $('replay').disabled = false;
          $('replay-episode').replaceChildren(...data.episodes.map(name => new Option(name, name)));
          $('replay-episode').disabled = false;
          updateDownload();
          append('terminal', `Shared reservations: $${data.budget.reserved_usd.toFixed(4)} / $${data.budget.cap_usd}\n`);
          $('download').hidden = false;
        } else {
          $('status').textContent = data.text;
          append('terminal', '\n' + data.text + '\n');
        }
      }
    };
    events.onerror = () => { $('status').textContent = 'Connection interrupted · reconnecting to this run…'; };
  } catch (error) {
    $('status').textContent = error.message;
    $('run').disabled = false;
  }
};
function traceURL() { return `/api/runs/${runId}/trace?episode=${encodeURIComponent($('replay-episode').value)}`; }
function updateDownload() { $('download').href = traceURL(); }
$('replay-episode').onchange = updateDownload;
$('replay').onclick = () => {
  $('viewer').src = `/replay/replay.html?trace=${encodeURIComponent(traceURL())}`;
  $('viewer').hidden = false;
  $('viewer').scrollIntoView({behavior:'smooth',block:'start'});
};
