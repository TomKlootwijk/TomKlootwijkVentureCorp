(() => {
  const data = window.TRACE_DATA;
  const $ = (q) => document.querySelector(q);
  const sats = (n) => new Intl.NumberFormat('en-US', {maximumFractionDigits:2}).format(Number(n || 0));
  const btc = (n) => (Number(n || 0) / 100000000).toFixed(8) + ' BTC';
  const short = (s, n=9) => s.length > n*2+3 ? s.slice(0,n)+'...'+s.slice(-n) : s;
  const summary = data.summary;
  const maxHop = Math.ceil(Math.max(...data.nodes.map(n => n.depth)));
  const cards = [
    ['Starting value', btc(summary.target.starting_sats), 'one starting UTXO'],
    ['Current target balance', sats(summary.target.live_confirmed_balance_sats ?? summary.target.source_confirmed_balance_sats) + ' sats', 'checked at the recorded tip'],
    ['Captured map', summary.captured_graph.nodes + ' nodes', summary.captured_graph.flow_edges + ' directed edges'],
    ['Latest captured spend', (summary.captured_graph.last_traced_transaction_utc || '').slice(0,10), 'the map stops by policy, not by identity'],
  ];
  $('#cards').innerHTML = cards.map(c => `<article class="card"><small>${c[0]}</small><strong>${c[1]}</strong><small>${c[2]}</small></article>`).join('');

  const bench = summary.cuda;
  $('#cuda-title').textContent = bench.cuda_used ? bench.gpu_name : 'CPU fallback used';
  $('#cuda-copy').textContent = bench.cuda_used
    ? `CUDA really ran ${bench.pagerank_iterations} PageRank passes. Median GPU path: ${bench.selected_device_median_ms.toFixed(2)} ms; CPU path: ${bench.cpu_median_ms.toFixed(2)} ms. Small graphs may be faster on CPU.`
    : `CUDA was not available, so the same deterministic tensor path ran on CPU in ${bench.cpu_median_ms.toFixed(2)} ms median.`;
  const stopCounts = summary.terminal_coverage.count_by_reason;
  $('#stops-title').textContent = Object.values(stopCounts).reduce((a,b)=>a+b,0) + ' terminal outputs';
  $('#stops-copy').textContent = Object.entries(stopCounts).map(([k,v]) => `${v} ${k.replaceAll('_',' ')}`).join(', ') + '. These are disclosed coverage boundaries.';

  const top = data.nodes.filter(n => n.kind !== 'transaction').sort((a,b) => b.incoming_attributed_sats-a.incoming_attributed_sats).slice(0,15);
  $('#top-rows').innerHTML = top.map(n => `<tr><td title="${n.id}">${short(n.id,12)}</td><td>${n.kind}</td><td>${n.depth}</td><td>${sats(n.incoming_attributed_sats)}</td><td>${sats(n.confirmed_balance_sats)}</td></tr>`).join('');

  const canvas = $('#map'), ctx = canvas.getContext('2d');
  const hop = $('#hop'), hopValue = $('#hop-value'), minimum = $('#minimum');
  hop.max = maxHop; hop.value = maxHop; hopValue.textContent = maxHop;
  let selected = null;
  const byId = new Map(data.nodes.map(n => [n.id,n]));
  let screen = [];

  function resize(){
    const dpr = window.devicePixelRatio || 1, rect = canvas.getBoundingClientRect();
    canvas.width = Math.max(1, Math.floor(rect.width*dpr)); canvas.height = Math.max(1,Math.floor(rect.height*dpr));
    ctx.setTransform(dpr,0,0,dpr,0,0); draw();
  }
  function visible(n){ return n.depth <= Number(hop.value) && (n.kind === 'target' || Math.max(n.incoming_attributed_sats,n.outgoing_attributed_sats) >= Number(minimum.value||0)); }
  function draw(){
    const w=canvas.clientWidth,h=canvas.clientHeight,pad=38,nodes=data.nodes.filter(visible), map=new Map();
    ctx.clearRect(0,0,w,h); ctx.fillStyle='#121c31'; ctx.fillRect(0,0,w,h);
    const shownMax=Math.max(1,Number(hop.value));
    for(const n of nodes){ const x=pad+(w-2*pad)*(n.depth/shownMax), y=pad+(h-2*pad)*((n.y+1)/2); map.set(n.id,{x,y,n}); }
    ctx.lineWidth=.55;
    for(const e of data.edges){ const a=map.get(e.source),b=map.get(e.target); if(!a||!b||e.attributed_sats<Number(minimum.value||0))continue; const alpha=.07+Math.min(.38,Math.log10(1+e.attributed_sats)/24); ctx.strokeStyle=`rgba(125,174,193,${alpha})`; ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.stroke(); }
    screen=[];
    for(const {x,y,n} of map.values()){
      const r=n.kind==='target'?8:n.kind==='transaction'?4.2:2.8+Math.min(4,Math.log10(1+n.incoming_attributed_sats)/3);
      ctx.fillStyle=n.kind==='target'?'#e6534e':n.kind==='transaction'?'#e1a82d':n.kind==='script'?'#8a96aa':'#21a7a2';
      ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();
      if(selected===n.id){ctx.strokeStyle='#fff';ctx.lineWidth=2;ctx.beginPath();ctx.arc(x,y,r+5,0,Math.PI*2);ctx.stroke();}
      screen.push({x,y,r:Math.max(r,7),n});
    }
  }
  function details(n){
    selected=n.id;
    $('#details').innerHTML=`<p class="eyebrow">${n.kind.toUpperCase()}</p><h2>${n.kind==='transaction'?'Transaction':'Address / script'}</h2><p class="node-id"></p><dl><dt>Hop position</dt><dd>${n.depth}</dd><dt>Modeled attribution in</dt><dd>${sats(n.incoming_attributed_sats)} sats</dd><dt>Modeled attribution out</dt><dd>${sats(n.outgoing_attributed_sats)} sats</dd><dt>Current whole-address balance</dt><dd>${sats(n.confirmed_balance_sats)} sats (${n.balance_status})</dd><dt>Terminal reason</dt><dd>${n.terminal_reason||'not terminal in captured map'}</dd><dt>Captured block time</dt><dd>${n.block_time||'not applicable'}</dd></dl>`;
    $('#details .node-id').textContent=n.id; draw();
  }
  canvas.addEventListener('click',ev=>{const r=canvas.getBoundingClientRect(),x=ev.clientX-r.left,y=ev.clientY-r.top;let best=null,d=Infinity;for(const s of screen){const q=Math.hypot(s.x-x,s.y-y);if(q<d&&q<14){best=s.n;d=q;}}if(best)details(best);});
  hop.addEventListener('input',()=>{hopValue.textContent=hop.value;draw();}); minimum.addEventListener('input',draw);
  $('#find').addEventListener('click',()=>{const q=$('#search').value.trim().toLowerCase();const n=data.nodes.find(n=>n.id.toLowerCase().includes(q));if(n){hop.value=Math.max(Number(hop.value),Math.ceil(n.depth));hopValue.textContent=hop.value;details(n);}});
  $('#reset').addEventListener('click',()=>{hop.value=maxHop;hopValue.textContent=maxHop;minimum.value=0;selected=null;draw();});
  window.addEventListener('resize',resize); resize();
})();
