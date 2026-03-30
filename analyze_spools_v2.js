const fs = require('fs');
const path = 'd:\\Github\\Andina\\Contexto\\PRY_413\\LIST\\LIST_Piping_MS(LIST_Spools_MS).csv';
const content = fs.readFileSync(path, 'utf8');
const lines = content.split('\n');
const header = lines[0].split(';');
const idxFab = header.indexOf('ESTADO_FABRICACION');
const idxCiclo = header.indexOf('ESTADO_CICLO_VIDA');
const idxUbic = header.indexOf('UBICACION_ACTUAL');

const valuesFab = new Set();
const valuesCiclo = new Set();
const valuesUbic = new Set();

for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(';');
    if (cols.length < 10) continue;
    if (cols[idxFab]) valuesFab.add(cols[idxFab].trim());
    if (cols[idxCiclo]) valuesCiclo.add(cols[idxCiclo].trim());
    if (cols[idxUbic]) valuesUbic.add(cols[idxUbic].trim());
}

console.log('ESTADO_FABRICACION:', Array.from(valuesFab));
console.log('ESTADO_CICLO_VIDA:', Array.from(valuesCiclo));
console.log('UBICACION_ACTUAL:', Array.from(valuesUbic));
