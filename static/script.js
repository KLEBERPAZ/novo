<script>
    function verificarNumeros(tipo) {
        const inputNumeros = new Set();
        const totalNumeros = tipo === 'mega_sena' ? 6 : (tipo === 'loto_facil' ? 15 : 5);
        const minimoPremiado = tipo === 'mega_sena' ? 4 : (tipo === 'loto_facil' ? 11 : 3);
        const minimoVermelhos = 2;

        for (let i = 1; i <= totalNumeros; i++) {
            const numero = document.getElementById(`${tipo}_numero${i}`).value;
            if (numero) {
                if (inputNumeros.has(numero)) {
                    alert('Número já escolhido, por favor escolha um número diferente.');
                    document.getElementById(`${tipo}_numero${i}`).value = '';
                    return;
                }
                inputNumeros.add(numero);
            }
        }

        document.querySelectorAll('.bet-numbers').forEach(aposta => {
            const tipoAposta = aposta.getAttribute('data-tipo');
            const numeros = aposta.querySelectorAll('.number');
            let acertos = 0;
            let vermelhos = 0;

            if (tipoAposta === tipo) {
                numeros.forEach(numero => {
                    if (inputNumeros.has(numero.textContent)) {
                        numero.classList.add('highlight');
                        acertos++;
                    } else {
                        numero.classList.remove('highlight');
                    }
                });
                aposta.closest('tr').classList.toggle('premiado', acertos >= minimoPremiado);
            } else {
                numeros.forEach(numero => {
                    numero.classList.remove('highlight');
                    if (tipoAposta === 'quina' && numero.classList.contains('highlight')) {
                        vermelhos++;
                    }
                });
                aposta.closest('tr').classList.toggle('premiado', vermelhos >= minimoVermelhos);
            }
        });
    }

    function moveUp(row) {
        const currentRow = row.closest('tr');
        const previousRow = currentRow.previousElementSibling;
        if (previousRow) currentRow.parentNode.insertBefore(currentRow, previousRow);
    }

    function moveDown(row) {
        const currentRow = row.closest('tr');
        const nextRow = currentRow.nextElementSibling;
        if (nextRow) currentRow.parentNode.insertBefore(currentRow, currentRow);
    }

    function calcularTotal() {
        let total = 0;
        document.querySelectorAll('.bet-value').forEach(valor => {
            total += parseFloat(valor.textContent.replace(',', '.'));
        });
        document.getElementById('totalValor').textContent = total.toFixed(2).replace('.', ',');
    }

    document.addEventListener('DOMContentLoaded', calcularTotal);
</script>
