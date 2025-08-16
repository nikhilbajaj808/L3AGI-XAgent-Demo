// backend/static/script.js
const $ = (id) => document.getElementById(id);

document.addEventListener("DOMContentLoaded", () => {
  $("exAdd").onclick = () => { $("prompt").value = "please add 5 and 7"; };
  $("exEcho").onclick = () => { $("prompt").value = "please echo Hello from frontend"; };
  $("runBtn").onclick = runAgent;
  $("toggleMode").onclick = toggleDarkMode;

  // Load saved theme
  if (localStorage.getItem("theme") === "light") {
    setLightMode();
  } else {
    setDarkMode();
  }
});

async function runAgent(){
  const prompt = $("prompt").value.trim();
  if(!prompt){ alert("Enter a prompt"); return; }
  $("output").textContent = "⚡ Running...";
  try{
    const r = await fetch("/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    const data = await r.json();
    $("output").textContent = JSON.stringify(data, null, 2);
  }catch(e){
    $("output").textContent = "❌ Request failed: " + e;
  }
}

function toggleDarkMode() {
  if (document.documentElement.classList.contains("dark")) {
    setLightMode();
    localStorage.setItem("theme", "light");
  } else {
    setDarkMode();
    localStorage.setItem("theme", "dark");
  }
}

function setLightMode() {
  document.documentElement.classList.remove("dark");
  document.body.classList.remove("bg-slate-950","text-slate-100");
  document.body.classList.add("bg-white","text-slate-900");
}

function setDarkMode() {
  document.documentElement.classList.add("dark");
  document.body.classList.add("bg-slate-950","text-slate-100");
  document.body.classList.remove("bg-white","text-slate-900");
}
