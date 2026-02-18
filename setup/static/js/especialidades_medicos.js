 async function atualizarEspecialidades() {
    const medicoSelect = document.getElementById("id_medico");
    const especialidadeSelect = document.getElementById("id_especialidade");
    const medicoId = medicoSelect.value;

    especialidadeSelect.innerHTML = "";
    especialidadeSelect.disabled = true;

    const placeholder = document.createElement("option");
    placeholder.value = "";
    placeholder.textContent = "Selecione a especialidade";
    especialidadeSelect.appendChild(placeholder);

    if (!medicoId) return;

    const resp = await fetch(`/api/especialidades-por-medico/?medico_id=${medicoId}`);
    const data = await resp.json();
    const especialidades = data.especialidades || [];

    for (const esp of especialidades) {
      const opt = document.createElement("option");
      opt.value = esp.id;
      opt.textContent = esp.nome;
      especialidadeSelect.appendChild(opt);
    }

    especialidadeSelect.disabled = false;

    // auto seleciona se só tiver 1
    if (especialidades.length === 1) {
      especialidadeSelect.value = String(especialidades[0].id);
    } else {
      // auto seleciona a principal se existir
      const principal = especialidades.find(e => e.principal);
      if (principal) especialidadeSelect.value = String(principal.id);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    const medicoSelect = document.getElementById("id_medico");
    medicoSelect.addEventListener("change", atualizarEspecialidades);

    // se já tiver médico selecionado ao recarregar (erros de validação), preenche também
    atualizarEspecialidades();
  });