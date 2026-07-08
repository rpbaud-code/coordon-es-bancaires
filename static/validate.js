function ibanValide(valeur) {
  const iban = valeur.replace(/\s/g, "").toUpperCase();
  if (!/^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$/.test(iban)) return false;
  const rearrange = iban.slice(4) + iban.slice(0, 4);
  const numerique = rearrange.replace(/[A-Z]/g, (c) => (c.charCodeAt(0) - 55).toString());
  let reste = 0;
  for (const chiffre of numerique) {
    reste = (reste * 10 + Number(chiffre)) % 97;
  }
  return reste === 1;
}

function swiftValide(valeur) {
  const swift = valeur.replace(/\s/g, "").toUpperCase();
  return /^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$/.test(swift);
}

function brancherValidation(id, validateur) {
  const champ = document.getElementById(id);
  if (!champ) return;
  champ.addEventListener("input", () => {
    if (!champ.value) {
      champ.classList.remove("valide", "invalide");
      return;
    }
    const ok = validateur(champ.value);
    champ.classList.toggle("valide", ok);
    champ.classList.toggle("invalide", !ok);
  });
}

brancherValidation("iban", ibanValide);
brancherValidation("swift", swiftValide);
