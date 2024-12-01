# SistemaDistribuido2

Este projeto implementa uma simulação de uma linha de produção usando threads para produtores e consumidores, com controle de acesso ao buffer compartilhado usando semáforos. Ele também gera gráficos para visualizar a produção, consumo e ocupação do buffer ao longo do tempo.

------------------------------------------------------------------------------------

Pré-requisitos
Antes de executar o código, certifique-se de que os seguintes itens estão instalados em sua máquina:

Python 3.8 ou superior

Bibliotecas Python necessárias: matplotlib

------------------------------------------------------------------------------------

Como executar

Faça o download ou clone o repositório com este código:
git clone <link-do-repositorio>
cd <pasta-do-repositorio>

Execute o script Python diretamente:
python <nome_do_arquivo>.py
-------------------------------------------------------------------------------------

Personalização
Capacidade do Buffer: Altere o valor de capacidade_buffer no código para modificar o tamanho do buffer compartilhado.
Número de Produtores/Consumidores: Configure num_produtores e num_consumidores conforme necessário.
Timesteps: Ajuste o número de ciclos da simulação alterando o valor de timesteps.

Saída
Logs no Console: Mensagens informando a produção, consumo e status do buffer em cada timestep.
Gráfico: Um gráfico exibindo:
Produção acumulada.
Consumo acumulado.
Ocupação do buffer ao longo do tempo.
Linha representando a capacidade máxima do buffer.
