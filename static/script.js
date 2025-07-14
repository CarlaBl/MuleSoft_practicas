const logDiv = document.getElementById("log");
    const form = document.getElementById("subForm");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      logDiv.innerHTML = "";

      const username = document.getElementById("username").value;
      const monthlyFee = parseFloat(document.getElementById("monthlyFee").value);
      const startDate = new Date(document.getElementById("startDate").value).toISOString();

      const payload = { username, monthly_fee: monthlyFee, start_date: startDate };

      try {
        const res = await fetch("https://mulesoft-practicas.onrender.com/new-subscription", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(payload)
        });

        if (res.ok) {
          for (let i = 1; i <= 5; i++) {
            const timestamp = new Date().toLocaleTimeString();
            const entry = document.createElement("div");
            entry.classList.add("entry");
            entry.innerHTML = `<strong>Envío #${i}</strong> | Usuario: ${username} | Hora: ${timestamp}`;
            logDiv.appendChild(entry);
            await new Promise(resolve => setTimeout(resolve, 5000));
          }
        } else {
          logDiv.innerHTML = "<p>Error al iniciar los envíos</p>";
        }
      } catch (err) {
        console.error(err);
        logDiv.innerHTML = "<p>Error al conectar con el servidor</p>";
      }
    });